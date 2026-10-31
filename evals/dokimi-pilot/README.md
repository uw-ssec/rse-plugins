# dokimi skill-eval pilot (#230)

Inputs and scripts for piloting [intel/dokimi](https://github.com/intel/dokimi)
on three skills before deciding whether to use it for all 76:

| Skill | Kind | Layers |
|---|---|---|
| `design-tokens` | knowledge | trigger, quality, novelty |
| `pixi-package-manager` | procedural | trigger, quality |
| `python-testing` | artifact | trigger, quality, Harbor task |
| `security-audit` (plugin) | artifact | trigger, quality, Harbor task |

This directory is its own pixi workspace, so the eval tooling never touches
the root `pixi.lock`. dokimi is alpha with no stable release, so it is pinned
to commit `b226dba`; Harbor is pinned to 0.25.0.

## Layout

- `cases/<skill>/trigger.json`: user-phrased trigger queries. Each skill has
  8 positives, 4 near-misses that belong to a sibling skill and 3 negatives
  (`expected_skill: null`).
- `cases/<skill>/routing-queries.json`: the positives only, for `novelty routing`.
- `cases/<skill>/quality-extra.json`: extra quality cases. design-tokens has
  none in rse-plugins-testcases. pixi and python-testing get 2 each to reach 7,
  above dokimi's 6-pair minimum for significance tests.
- `testcases_to_dokimi.py`: converts rse-plugins-testcases YAML (`prompt`,
  `criteria`, `expect_skill`) into a skill-creator `evals.json` (quality) and a
  skill-reach query set (trigger). `expect_skill: false` cases join the trigger
  set as negatives.
- `harbor-tasks/python-testing-numlib`: a Harbor task. The agent writes a
  pytest suite for a small numerical package. The verifier scores it by
  mutation: the suite must pass on the reference code, and the reward is the
  fraction of 5 planted bugs it catches. Each run starts from a fresh copy of
  the submitted workspace and its own `TMPDIR`, so a suite that leaves state
  behind can't fail every mutant and fake a perfect score.
  `check_harbor_task.sh` holds the controls: oracle 1.0, no tests 0, a smoke
  suite 0.0, and stateful suites 0.0.
- `harbor-tasks/security-recon-configdrift`: a Harbor task for the
  security-audit plugin's recon phase (verifier controls need no network and
  no LLM). The agent audits a synthetic deploy repo (two environments,
  planted git history) after a written incident and writes an audit report.
  Five findings are planted: un-rotated master key (ciphertext identical
  across history), six-month version lag on a critical advisory, prod
  missing the salt key that staging has, a mutable `:latest` image tag, and
  a shared master-key secret between staging services. Partial credit for
  the rotation finding requires citing the ciphertext/env-file evidence,
  not just the claim. Its `check_harbor_task.sh` controls: oracle 1.0, no
  report 0, vague report 0, partial 0.8, claim-without-evidence 0.7.
- `cases/security-audit/`: trigger queries for the four security-audit
  skills (12 positives across the skills, 4 near-misses that belong to
  supply-chain-security skills, 3 negatives) plus quality cases covering
  the two behaviors that matter most: the live-testing scope gate and the
  ciphertext-based rotation check.

## Running

```bash
cd evals/dokimi-pilot
pixi run catalog-scan                      # free: strict load of all 76 skills
pixi run convert ../../../rse-plugins-testcases   # writes out/<skill>/
pixi run routing-bm25                      # free lexical routing floor
pixi run harbor-lint
./check_harbor_task.sh [image]                 # verifier regression controls (Docker, no LLM)
```

`convert` fails if a skill has no rse-plugins-testcases cases, so a wrong
checkout path can't silently shrink the evaluation. design-tokens has none on
purpose and passes `--no-testcases`.

Model-backed runs need gateway credentials (`LITELLM_PROXY_URL` /
`LITELLM_API_KEY`). Each command takes `--model`/`--provider`; set `--max-usd`
wherever it exists, because `arms run` and `tasks run` have no cost cap.

```bash
# Trigger: does the right skill win against the whole catalog?
pixi run routing-bm25 --model <model> --provider anthropic --repeats 3 --max-usd 2
dokimi arms run --questions out/<skill>/trigger.questions.json --arms skill-catalog:<catalog dir> --model <model>
# Quality: with vs without the skill, judged by a different model family
dokimi arms run --questions out/<skill>/questions.v2.json \
  --arms baseline,skill:../../plugins/<path> --model <model> --judge --judge-provider openai
# Novelty (design-tokens)
dokimi novelty analyze --artifact skill:../../plugins/uiux-design-team/skills/design-tokens \
  --tier triage --include-resources --model <model> --estimate-only
# Harbor task, baseline vs with-skill
dokimi tasks run --tasks-root harbor-tasks --tasks python-testing-numlib \
  --harnesses docker-claude,docker-claude-skill:../../plugins/scientific-python-development/skills/python-testing \
  --baseline-harness docker-claude --model <model>
```

## Gateway notes (llmoxie LiteLLM)

These were learned running the pilot:

- **Routing:** route through the OpenAI-compatible endpoint with
  `--provider openai`, `OPENAI_BASE_URL=<gateway>/v1` and `OPENAI_API_KEY`. Use
  the gateway's model aliases (`ssec-claude-haiku-5-5`, `ssec-claude-sonnet-5-5`,
  `ssec-gpt-6.1-sol`).
- **Pricing:** `--max-usd` stops on a model with no known price. Register the
  aliases with `litellm.register_model`, copying the underlying model's list
  prices, e.g. from a `sitecustomize.py` on `PYTHONPATH`.
- **Sampling params:** the Claude aliases reject `--temperature` and `--seed`
  in `arms run`. dokimi's pre-flight probe refuses the run before spending
  anything.
- **Catalog-arm cost:** the `skill-catalog:` arm sends all 76 skill listings
  on every turn. It costs about $0.09 per skill on Haiku 5.5 and about $2 per
  skill on Sonnet 5.5.
- **Harbor agent on macOS:** dokimi's `docker-claude` harness copies the host
  `claude` binary into the container, so it needs a Linux host. On macOS, use
  `harbor run -a claude-code --skill <dir>` with `ANTHROPIC_BASE_URL` /
  `ANTHROPIC_API_KEY` pointed at the gateway.
- **Reports:** `dokimi report model-compare --regular-runs <haiku.json>
  <sonnet.json> --run-ids haiku,sonnet` is the report for `arms run` output.
  `report generate` and `report eval` read a different schema.

## Notes

- `network_mode = "no-network"` in `task.toml` needs Harbor's kernel egress
  control. Harbor 0.24 and 0.25 both reject it on hosts without that control
  (macOS Docker); Linux runners are expected to support it.
- `harbor lint` advises `verifier.environment_mode = "separate"`. The verifier
  shares the agent's sandbox, so it restores `src/` from its own copy before
  scoring.

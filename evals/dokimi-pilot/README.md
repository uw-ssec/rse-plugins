# dokimi skill-eval pilot (#230)

Inputs and scripts for piloting [intel/dokimi](https://github.com/intel/dokimi)
on three skills before deciding whether to use it for all 76:

| Skill | Kind | Layers |
|---|---|---|
| `design-tokens` | knowledge | trigger, quality, novelty |
| `pixi-package-manager` | procedural | trigger, quality |
| `python-testing` | artifact | trigger, quality, Harbor task |

This directory is its own pixi workspace, so the eval tooling never touches
the root `pixi.lock`. dokimi is alpha with no stable release, so it is pinned
to commit `b226dba`; Harbor is pinned to 0.25.0.

## Layout

- `cases/<skill>/trigger.json`: user-phrased trigger queries. Each skill has
  8 positives, 4 near-misses that belong to a sibling skill and 3 negatives
  (`expected_skill: null`).
- `cases/<skill>/routing-queries.json`: the positives only, for `novelty routing`.
- `cases/design-tokens/quality-extra.json`: quality cases for design-tokens,
  which has none in rse-plugins-testcases.
- `testcases_to_dokimi.py`: converts rse-plugins-testcases YAML (`prompt`,
  `criteria`, `expect_skill`) into a skill-creator `evals.json` (quality) and a
  skill-reach query set (trigger). `expect_skill: false` cases join the trigger
  set as negatives.
- `harbor-tasks/python-testing-numlib`: a Harbor task. The agent writes a
  pytest suite for a small numerical package. The verifier scores it by
  mutation: the suite must pass on the reference code, and the reward is the
  fraction of 5 planted bugs it catches.

## Running

```bash
cd evals/dokimi-pilot
pixi run catalog-scan                      # free: strict load of all 76 skills
pixi run convert ../../../rse-plugins-testcases   # writes out/<skill>/
pixi run routing-bm25                      # free lexical routing floor
pixi run harbor-lint
```

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

## Notes

- `network_mode = "no-network"` in `task.toml` needs Harbor's kernel egress
  control. Harbor 0.24 and 0.25 both reject it on hosts without that control
  (macOS Docker); Linux runners are expected to support it.
- `harbor lint` advises `verifier.environment_mode = "separate"`. The verifier
  shares the agent's sandbox, so it restores `src/` from its own copy before
  scoring.

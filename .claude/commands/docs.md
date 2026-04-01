Write comprehensive documentation for recent work in this session.

Arguments: $ARGUMENTS (optional — topic, section, or "all" to regenerate broadly)

## Instructions

1. **Gather context** — Run these in parallel to understand what changed:
   - `git log --oneline -20` (recent commits)
   - `git diff main...HEAD --stat` (if on a feature branch)
   - `git log --oneline --since="8 hours ago"` (today's work)
   - Review any open plans in `docs/plans/`
   - Read `docs/index.md` and `mkdocs.yml` for existing structure

2. **Determine scope** — Based on the argument and recent changes, decide which docs need writing or updating:
   - If argument is a specific topic (e.g., "queues", "auth", "notifications"), focus there
   - If argument is a section (e.g., "architecture", "database", "guides"), update that section
   - If argument is "all" or empty, document everything from the current session
   - Always check existing docs first — update rather than duplicate

3. **Write documentation** covering these categories as relevant:

   ### Technical Details
   - What was built, changed, or fixed
   - API contracts, database schema changes, new RPC functions
   - Configuration changes, environment variables, dependencies added
   - Code patterns introduced or modified

   ### Technical Architecture
   - System design and component relationships
   - Data flow diagrams (use Mermaid syntax)
   - Integration points between services (workers, platform, database)
   - Infrastructure decisions (Cloudflare, Neon, WorkOS, Stripe, etc.)

   ### Session Learnings
   - Decisions made and their rationale (ADR-style: Decision / Why / Result)
   - Technical issues encountered and how they were resolved
   - Trade-offs considered and which path was chosen
   - Gotchas, edge cases, or surprising behavior discovered
   - Things that didn't work and why

4. **Place documentation correctly:**
   - New architecture docs → `docs/architecture/`
   - Database changes → `docs/database/`
   - Frontend changes → `docs/frontend/`
   - How-to content → `docs/guides/`
   - Implementation plans → `docs/plans/` (named `YYYY-MM-DD-topic.md`)
   - Session learnings → `docs/guides/architecture-decisions.md` (append new entries at top of relevant section)
   - Script documentation → `docs/scripts/`

5. **Update mkdocs.yml nav** — If you created a new file, add it to the `nav:` section in `mkdocs.yml` under the correct heading. Match existing indentation and naming style.

6. **Update docs/index.md** — If the new doc is significant, add a link in the Documentation section of `docs/index.md` with a one-line description.

7. **Verify** — Run `pixi run docs-build` to confirm MkDocs builds without errors.

8. **Report** — Show the user:
   - Files created or updated (with paths)
   - New nav entries added
   - Build status (pass/fail)

## Documentation Style

- Use MkDocs Material features: admonitions (`!!! note`, `!!! warning`, `!!! tip`), tabs, Mermaid diagrams, code blocks with language tags
- Start every doc with a level-1 heading and a 1-2 sentence summary
- Use tables for structured data (configs, env vars, field mappings)
- Keep headings hierarchical (h1 → h2 → h3, never skip levels)
- Use imperative voice for guides ("Run the migration", not "You should run the migration")
- Architecture decisions follow the pattern:

```markdown
### YYYY-MM-DD: Decision Title (Status)

- **Decision:** What was decided
- **Why:** The reasoning and constraints
- **Result:** What was implemented and any notable outcomes
```

## Mermaid Diagram Conventions

- Use `graph TD` for top-down architecture diagrams
- Use `sequenceDiagram` for request/response flows
- Use `erDiagram` for database relationships
- Keep diagrams focused — split complex systems into multiple diagrams
- Label edges with the protocol or mechanism (e.g., `-->|JWT|`, `-->|REST|`, `-->|Queue|`)

## Rules

- Never delete existing documentation — update or extend it
- Always read existing docs before writing to avoid duplication
- Every new doc must appear in `mkdocs.yml` nav
- Date-stamp architecture decisions and plans
- Use relative links between docs (e.g., `../guides/getting-started.md`)
- Build must pass before considering the task done
- If `pixi run docs-build` fails, fix the issue (usually a nav mismatch or broken link)

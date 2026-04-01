Create a versioned release with changelog, tag, GitHub release, and plugin zip assets.

## Arguments

$ARGUMENTS — version bump type: `patch`, `minor`, or `major` (optional, defaults to analyzing changes)

## Instructions

1. Determine the version bump:
   - If `$ARGUMENTS` specifies `patch`, `minor`, or `major`, use that
   - If not specified, analyze commits since the last tag to determine:
     - `major`: breaking changes (commits with `!` or `BREAKING CHANGE`)
     - `minor`: new features (`feat:` commits)
     - `patch`: fixes, refactors, docs, chores only

2. Get the current version:
   - Check `git tag --sort=-v:refname | head -1` for the latest tag
   - If no tags exist, start at `v0.1.0`

3. Calculate the new version following semver.

4. Verify readiness:
   - `git status` — must be on `main` with no uncommitted changes
   - `git pull origin main` — must be up to date
   - Warn and stop if not on `main` or if there are uncommitted changes

5. Read `CHANGELOG.md` and check that the `[Unreleased]` section has content.

6. Update `CHANGELOG.md`:
   - Rename `[Unreleased]` to `[X.Y.Z] -- YYYY-MM-DD` (today's date)
   - Add a new empty `[Unreleased]` section above it

7. Commit the changelog update:
   ```bash
   git add CHANGELOG.md
   git commit -m "$(cat <<'EOF'
   chore(release): prepare vX.Y.Z

   Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
   EOF
   )"
   ```

8. Create the git tag:
   ```bash
   git tag -a vX.Y.Z -m "vX.Y.Z"
   ```

9. Push the commit and tag:
   ```bash
   git push origin main --follow-tags
   ```

10. Build plugin zip assets:
    - For each directory in `plugins/`, create a zip archive
    - **Zip naming convention:**
      - Default: `plugin_name_MM_DD_YYYY.zip` (snake_case plugin name + date)
      - If a release already exists for today (check `gh release list`), append a sequence suffix: `plugin_name_MM_DD_YYYY_2.zip`, `_3.zip`, etc.
    - Example: `recipe_workshop_03_30_2026.zip`, or `recipe_workshop_03_30_2026_2.zip` for a second release that day
    - Create zips from within the `plugins/` directory so the zip root is the plugin folder itself:
      ```bash
      cd plugins && zip -r ../plugin_name_MM_DD_YYYY.zip plugin-dir-name/ -x "*.DS_Store" "*__pycache__/*" "*.pyc" && cd ..
      ```
    - Exclude unnecessary files from zip: `.DS_Store`, `__pycache__`, `*.pyc`

11. Create a GitHub release with plugin zips as assets:
    ```bash
    gh release create vX.Y.Z --title "vX.Y.Z" \
      --notes "$(cat <<'EOF'
    ## What's Changed

    <extract the relevant section from CHANGELOG.md>

    ## Plugin Assets

    <list each plugin zip with name and description>

    **Full Changelog**: https://github.com/cdcore09/recipe-workshop/compare/vPREVIOUS...vX.Y.Z
    EOF
    )" \
      plugin_name_MM_DD_YYYY.zip
    ```

12. Clean up zip files from the repo root after successful upload.

13. Confirm: "Released vX.Y.Z — <release URL>"

## Version Guidelines

| Bump | When | Example |
|------|------|---------|
| `patch` (0.1.X) | Bug fixes, docs, chores, refactors | `v0.1.1` → `v0.1.2` |
| `minor` (0.X.0) | New features, non-breaking changes | `v0.1.2` → `v0.2.0` |
| `major` (X.0.0) | Breaking changes, major rewrites | `v0.2.0` → `v1.0.0` |

## Zip Naming Rules

- Plugin directory name is converted to snake_case: `recipe-workshop` → `recipe_workshop`
- Date format is `MM_DD_YYYY`
- Sequence suffix only added when multiple releases occur on the same day
- Sequence starts at `_2` (first release of the day has no suffix)

## Rules

- Must be on `main` branch with no uncommitted changes
- Must have content in `[Unreleased]` section of CHANGELOG.md
- Never create a release from a feature branch
- Tag format is always `vX.Y.Z` (with `v` prefix)
- Ask for confirmation before pushing the tag and creating the release
- If CHANGELOG.md doesn't exist or has no `[Unreleased]` section, warn and ask how to proceed
- Never commit generated zip files — they are upload artifacts only

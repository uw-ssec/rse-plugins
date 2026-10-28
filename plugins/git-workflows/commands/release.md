---
description: Cut a version: changelog, tag, GitHub release, and assets
user-invocable: true
---

Use the `git-workflows:publishing-releases` skill to handle this request.

Arguments (optional bump: patch, minor, or major): $ARGUMENTS

If no arguments were provided, infer the bump from the commits since the last tag and state the reasoning before proceeding.

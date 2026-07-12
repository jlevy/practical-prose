## Publishing Releases

This is how to publish a Python package to [**PyPI**](https://pypi.org/) from GitHub
Actions, when using the
[**simple-modern-uv**](https://github.com/jlevy/simple-modern-uv) template.

Thanks to
[the dynamic versioning plugin](https://github.com/ninoseki/uv-dynamic-versioning/) and
the
[`publish.yml` workflow](https://github.com/jlevy/simple-modern-uv/blob/main/template/.github/workflows/publish.yml),
you can simply create tagged releases (using standard format for the tag name, e.g.
`v0.1.0`) on GitHub and the tag will trigger a release build, which then uploads it to
PyPI.

### First-Time Setup

This part is a little confusing the first time.
Here is the simplest way to do it.
For this repo the values are: PyPI project name `pprose`, GitHub repo owner `jlevy`,
GitHub repo name `practical-prose`.

**Note:** These steps assume you already have a GitHub repo with your code pushed.
If you used [`uvx uvtemplate`](https://github.com/jlevy/uvtemplate), it handles repo
creation for you. If you’re setting up manually, create an **empty** GitHub repo (no
README, no .gitignore, no license; the template already provides these) and push your
code to it. See the
[README](https://github.com/jlevy/simple-modern-uv#option-2-use-copier-and-git-yourself)
for details.

1. **Get a PyPI account** at [pypi.org](https://pypi.org/) and sign in.

2. **Pick a name for the project** that isn’t already taken.

   - Go to `https://pypi.org/project/pprose` to see if another project with that name
     already exits.

   - If needed, update your `pyproject.toml` with the correct name.

3. **Authorize** your repository to publish to PyPI:

   - Go to [the publishing settings page](https://pypi.org/manage/account/publishing/).

   - Find “Trusted Publisher Management” and register your GitHub repo as a new
     “pending” trusted publisher.

   - Enter the project name (`pprose`), repo owner (`jlevy`), repo name
     (`practical-prose`), and `publish.yml` as the workflow name.
     (You can leave the “environment name” field blank.)

4. **Create a release** on GitHub:

   - Commit code and make sure it’s running correctly.

   - Go to your GitHub project page, then click on Actions tab.

   - Confirm all tests are passing in the last CI workflow.
     (If you want, you can even publish this template when it’s empty as just a stub
     project, to try all this out.)

   - Go to your GitHub project page, click on Releases.

   - Fill in the tag and the release name.
     Select to create a new tag, and pick a version.
     A good option is `v0.1.0`. (It’s wise to have it start with a `v`.)

   - Submit to create the release.

5. **Confirm it publishes to PyPI**

   - Watch for the release workflow in the GitHub Actions tab.

   - If it succeeds, you should see it appear at `https://pypi.org/project/pprose`.

### Publishing Subsequent Releases

Follow this checklist for each new release.

#### Pre-Release Checklist

1. **Use the exact current `main` commit:**

   ```shell
   git fetch --tags --prune origin
   git switch main
   git pull --ff-only
   test -z "$(git status --porcelain)"
   RELEASE_COMMIT="$(git rev-parse HEAD)"
   test "$RELEASE_COMMIT" = "$(git rev-parse origin/main)"
   ```

   Keep `RELEASE_COMMIT` in the same shell through release creation.
   It is the reviewed commit that the tag and release notes must describe.

2. **Run the read-only release gates locally:**

   ```shell
   make install
   make lint-check
   make test
   make -C tools/pprose build
   ```

3. **Confirm CI is passing:**

   ```shell
   gh run list --workflow=ci.yml --commit "$RELEASE_COMMIT" --limit 1
   ```

   Or check the Actions tab on GitHub.

4. **Determine the new version number:**

   ```shell
   # Check current/latest version:
   gh release list --limit 1
   ```

   Use [semantic versioning](https://semver.org/):

   - **Patch** (e.g., `v0.5.8` → `v0.5.9`): Bug fixes, minor changes

   - **Minor** (e.g., `v0.5.9` → `v0.6.0`): New features, backward-compatible

   - **Major** (e.g., `v0.6.0` → `v1.0.0`): Breaking changes

5. **Update the CHANGELOG:**

   Move the accumulated entries from `## [Unreleased]` into a new
   `## [X.Y.Z] - YYYY-MM-DD` section in `CHANGELOG.md`.

6. **Bump the discovery pin to match the tag:**

   Set `DISCOVERY_VERSION` in `src/pprose/install.py` to the new version (no leading
   `v`), then re-render the committed discovery skills from the repo root:

   ```shell
   make generate
   ```

   This step is mandatory.
   `devtools/check_release_version.py` (run by `publish.yml`) fails the publish unless
   the release tag equals `DISCOVERY_VERSION`, and `tests/test_resources_sync.py` fails
   if the committed `skills/` drift from it.
   The pin backs the `uvx pprose@<version>` zero-install bootstrap, so it must point at
   the version being published.

7. **Verify the release guard locally before tagging:**

   ```shell
   env UV_NO_CONFIG=1 UV_LOCKED=1 \
     UV_BUILD_CONSTRAINT="$(pwd)/tools/pprose/build-constraints.txt" \
     uv run --project tools/pprose --no-sync python \
     tools/pprose/devtools/check_release_version.py vX.Y.Z
   # → "Release version check OK"
   ```

#### Create the Release

8. **Generate release notes content:**

   Review changes since the last release:

   ```shell
   # Get the last release tag:
   LAST_TAG=$(gh release list --limit 1 --json tagName -q '.[0].tagName')

   # View commits since the last release on the exact candidate:
   git log "${LAST_TAG}..${RELEASE_COMMIT}" --oneline

   # View full diff:
   git diff "${LAST_TAG}..${RELEASE_COMMIT}"
   ```

9. **Create the release with `gh`:**

   ```shell
   NEW_TAG="vX.Y.Z"  # Replace with actual version
   LAST_TAG=$(gh release list --limit 1 --json tagName -q '.[0].tagName')

   gh release create "${NEW_TAG}" \
     --target "${RELEASE_COMMIT}" \
     --fail-on-no-commits \
     --title "${NEW_TAG}" \
     --notes "$(cat <<'EOF'
   ## What's Changed

   [Summarize changes here--see format guide below]

   **Full commit history**:
   https://github.com/jlevy/practical-prose/compare/${LAST_TAG}...${NEW_TAG}
   EOF
   )"
   ```

   Alternatively, use `--generate-notes` for GitHub’s auto-generated notes, or
   `--notes-file FILENAME` to read from a file.

10. **Verify the release published and installs successfully:**

    ```shell
    # Wait for the release workflow and inspect its final result:
    PUBLISH_RUN=$(gh run list --workflow=publish.yml --commit "$RELEASE_COMMIT" \
      --limit 1 --json databaseId -q '.[0].databaseId')
    # The release event may take a few seconds to appear; rerun the assignment if empty.
    test -n "$PUBLISH_RUN"
    gh run watch "$PUBLISH_RUN" --exit-status

    # Verify the exact version from outside the source checkout:
    cd /tmp
    uvx "pprose@X.Y.Z" --version
    uvx "pprose@X.Y.Z" list
    ```

### Release Notes Format

Use this structure for release notes:

```markdown
## What's Changed

### Features

- **Feature name**: Describe what users can now do.

### Fixes

- **Fix name**: Describe what was corrected and why it matters.

### Guidelines and content

- **Content name**: Describe shipped guidelines, skills, shortcuts, or templates that
  changed.

### Breaking changes

- **Breaking change**: Describe what changed and how to migrate.

### Documentation

- **Documentation area**: Include only notable user-facing documentation changes.

**Full commit history**:
https://github.com/jlevy/practical-prose/compare/vPREVIOUS...vNEW
```

Guidelines:

- Use `## What's Changed` as the top-level heading.

- Group changes under the applicable headings above and omit empty sections.

- Treat shipped guidelines, skills, shortcuts, and templates as product changes under
  `### Guidelines and content`, not as internal documentation.

- Use `**bold**` for short titles of individual changes.

- Include technical details only when helpful for users.

- Always include the Full Changelog compare link at the end.

- For small releases, a simple bullet list is acceptable instead of full sections.

* * *

*This file was built with
[simple-modern-uv](https://github.com/jlevy/simple-modern-uv).*

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->

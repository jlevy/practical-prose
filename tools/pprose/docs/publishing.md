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

#### Why the Order Matters

A release here is not just a tag.
Four things must name the same version, produced by different mechanisms:

| What | Where it comes from |
| --- | --- |
| The git tag | Created by you |
| The PyPI artifact version | Derived from the tag at build time |
| `install.DISCOVERY_VERSION` | A hand-edited constant in the source |
| `uvx pprose@X` in every committed skill | Rendered from `DISCOVERY_VERSION` by `make generate` |

`DISCOVERY_VERSION` exists because a skill must tell an agent how to run `pprose` when
it is not on `PATH`, and the skill copies committed under `skills/` are rendered from a
dev checkout whose own version (`0.3.1.dev10+2955f57`) was never published.
So the rendering falls back to a hardcoded constant.

That constant is a **promise that a release with this number will exist on PyPI**.
Bumping it and merging publishes that promise to everyone who installs the skills.
**Only the tag keeps it.** Until the tag exists and the publish succeeds, every skill on
`main` instructs agents to run a command that fails:

```shell
$ uvx pprose@0.3.1 --version
x No solution found: there is no version of pprose==0.3.1
```

This is not hypothetical.
v0.3.1 was prepared and merged on 2026-07-24 and never tagged; the broken bootstrap sat
on `main` until v0.4.0. **Phases 1 and 2 below are not safe to leave unfinished.** Start
a release only when you can finish phase 3 in the same sitting.

Two guards enforce different halves of this, and neither substitutes for the other:

- `devtools/check_release_version.py` (run by `publish.yml`) fails the publish unless
  the tag equals `DISCOVERY_VERSION`. This proves a release is self-consistent.
  It cannot prove a release happened.
- `devtools/check_discovery_pin_published.py` (run daily by `discovery-pin.yml`) fails
  when `DISCOVERY_VERSION` names a version PyPI does not have.
  This is what catches a forgotten tag — within a day, not a month.
  It is deliberately not a pull-request gate, because phases 1-2 legitimately leave
  `main` ahead of PyPI for the minutes until phase 3 completes.

#### A Note on `gh` in Proxied Sessions

In a remote or cloud session with `HTTPS_PROXY` set, `gh auth status` may report
`The token in GH_TOKEN is invalid` for a perfectly valid token, because the proxy
intercepts the GraphQL query it uses.
Do not conclude the token is bad.
Test egress, and if it is open, prefix `gh` commands to bypass the proxy for GitHub
hosts only (`HTTPS_PROXY` stays set for everything else; TLS verification stays on).
Run `tbd shortcut setup-github-cli` for the full decision rule and the verified recipe.

#### Phase 1: Prepare the Release Commit

Do this on a branch, not on `main`.

1. **Determine the new version number:**

   ```shell
   gh release list --limit 1
   ```

   Use [semantic versioning](https://semver.org/):

   - **Patch** (e.g., `v0.5.8` → `v0.5.9`): Bug fixes, minor changes

   - **Minor** (e.g., `v0.5.9` → `v0.6.0`): New features, backward-compatible

   - **Major** (e.g., `v0.6.0` → `v1.0.0`): Breaking changes

2. **Bump the discovery pin to match the intended tag:**

   Set `DISCOVERY_VERSION` in `src/pprose/install.py` to the new version (no leading
   `v`), then re-render the committed discovery skills from the repo root:

   ```shell
   make generate
   ```

   This step is mandatory, and it is the step that starts the clock described above.

3. **Update the CHANGELOG:**

   Move the accumulated entries from `## [Unreleased]` into a new
   `## [X.Y.Z] - YYYY-MM-DD` section in `CHANGELOG.md`.

4. **Verify the release guard locally before merging:**

   ```shell
   env UV_NO_CONFIG=1 UV_LOCKED=1 \
     UV_BUILD_CONSTRAINT="$(pwd)/tools/pprose/build-constraints.txt" \
     uv run --project tools/pprose --no-sync python \
     tools/pprose/devtools/check_release_version.py vX.Y.Z
   # → "Release version check OK"
   ```

5. **Run the read-only release gates locally:**

   ```shell
   make install
   make lint-check
   make test
   make -C tools/pprose build
   ```

#### Phase 2: Merge to `main`

6. **Merge the release-prep branch**, then take the exact resulting commit:

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

7. **Confirm CI is passing on that exact commit:**

   ```shell
   gh run list --workflow=ci.yml --commit "$RELEASE_COMMIT" --limit 1
   ```

   `main` now advertises a version that does not exist yet.
   Continue to phase 3 without stopping.

#### Phase 3: Tag and Publish

8. **Review what is shipping:**

   ```shell
   LAST_TAG=$(gh release list --limit 1 --json tagName -q '.[0].tagName')
   git log "${LAST_TAG}..${RELEASE_COMMIT}" --oneline
   git diff "${LAST_TAG}..${RELEASE_COMMIT}"
   ```

9. **Create the release** (this creates the tag and triggers `publish.yml`):

   ```shell
   NEW_TAG="vX.Y.Z"  # Replace with actual version

   gh release create "${NEW_TAG}" \
     --target "${RELEASE_COMMIT}" \
     --fail-on-no-commits \
     --title "${NEW_TAG}" \
     --notes-file RELEASE-NOTES.md
   ```

   `--notes` with an inline heredoc and `--generate-notes` both work too; see
   [Release Notes Format](#release-notes-format).

   If a session git broker refuses `refs/tags/*` pushes (it may, while accepting branch
   pushes, and `git push --dry-run` misleadingly passes), create the tag through the API
   instead and then create the release against it:

   ```shell
   gh api repos/jlevy/practical-prose/git/refs \
     -f ref="refs/tags/${NEW_TAG}" -f sha="${RELEASE_COMMIT}"
   ```

#### Phase 4: Verify the Promise Is Kept

10. **Watch the publish workflow and confirm the artifact is installable:**

    ```shell
    PUBLISH_RUN=$(gh run list --workflow=publish.yml --commit "$RELEASE_COMMIT" \
      --limit 1 --json databaseId -q '.[0].databaseId')
    # The release event may take a few seconds to appear; rerun the assignment if empty.
    test -n "$PUBLISH_RUN"
    gh run watch "$PUBLISH_RUN" --exit-status
    ```

11. **Verify the exact version resolves from outside the source checkout.** This is the
    check that would have caught the v0.3.1 failure, so do not skip it:

    ```shell
    cd /tmp
    uvx "pprose@X.Y.Z" --version
    uvx "pprose@X.Y.Z" list
    ```

    A brief `No solution found` immediately after publishing is usually PyPI index
    propagation; retry for a minute or two before treating it as a failure.

12. **Confirm the daily pin check is satisfied:**

    ```shell
    uv run --project tools/pprose --no-sync python \
      tools/pprose/devtools/check_discovery_pin_published.py
    # → "Discovery pin check OK: pprose X.Y.Z is published on PyPI"
    ```

#### Recovery: The Pin Was Merged but Never Tagged

If `check_discovery_pin_published.py` fails — or `discovery-pin.yml` goes red — `main`
is advertising an unpublished version and every zero-install bootstrap is broken.
Two ways out:

- **Finish the release** (preferred): confirm CI is green on `main`, then run phases 3
  and 4 against the current `main` commit.
  The pin is already correct; only the tag is missing.
- **Retreat to a published version** (stopgap): set `DISCOVERY_VERSION` back to the
  newest version actually on PyPI, run `make generate`, and merge.
  This repairs the bootstrap immediately, at the cost of skills serving the older
  release’s bundled docs until a real release ships.

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

## Installing uv and Python

This project uses [**uv**](https://docs.astral.sh/uv/) to manage Python and dependencies.

Install uv (macOS/Linux):

```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```

On macOS with [Homebrew](https://brew.sh/), `brew install uv` also works. See
[uv's install docs](https://docs.astral.sh/uv/getting-started/installation/) for other
platforms.

Then install a Python toolchain:

```shell
uv python install 3.13  # or another version
```

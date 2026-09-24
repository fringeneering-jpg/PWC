#!/usr/bin/env bash
set -e
if [ ! -x "$HOME/.local/bin/uv" ]; then
  curl -LsSf https://astral.sh/uv/install.sh | sh >/dev/null 2>&1
fi
export PATH="$HOME/.local/bin:$PATH"
mkdir -p "$HOME/rbh1" && cd "$HOME/rbh1"
[ -d .venv ] || uv venv --python 3.12 .venv -q
uv pip install --python .venv/bin/python jwst astroquery 2>&1 | tail -3
.venv/bin/python -c "import jwst, sys; print('jwst', jwst.__version__, '| python', sys.version.split()[0])"

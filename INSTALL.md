# Installing Dependencies

The `requirements.txt` was generated with `pip freeze` and contains some declared metadata conflicts (e.g. `cryptography` vs `presidio-anonymizer`, `sse-starlette` vs `starlette`). These packages work together at runtime, but strict resolvers like `uv` will reject the install.

## Correct Install Command

Use `--no-deps` to bypass conflict resolution and install exactly what is listed:

```bash
source .venv/bin/activate
uv pip install --no-deps -r requirements.txt
```

This is safe because `pip freeze` already captured every transitive dependency in the file — nothing is missing.

## Updating requirements.txt

After installing or upgrading packages, regenerate the file with:

```bash
uv pip freeze > requirements.txt
```

## Why not plain `uv pip install -r requirements.txt`?

`uv` uses a strict SAT solver that validates all dependency constraints before installing. The pinned versions in this file have conflicting metadata, so `uv` refuses to proceed. The `--no-deps` flag skips that check and installs each package as listed.

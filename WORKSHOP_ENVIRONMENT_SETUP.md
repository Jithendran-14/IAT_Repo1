# One environment for all four rounds

The facilitator shares four repository links sequentially. Create one Python environment **outside** all four clones, install the complete pinned dependency set once, and reuse it. Do not merge fixes forward; the next repository includes a correct baseline.

## Prerequisites
- Trainer-tested Python 3.12 recommended; declared range is >=3.11,<3.14.
- Git and `uv`, installed through your approved process.
- Access to the Oracle internal Artifactory index in `pyproject.toml` and required authentication/network configuration. No credentials are embedded in this repo.
- A dedicated workshop Oracle database/schema supporting VECTOR, with quota and permission to create the SDK's tables and read/write its own data. Ask the facilitator to provision it.
- Ollama running at `http://localhost:11434`, with `qwen3-embedding:0.6b` available. Provision/download models **before** the timed round. The adapter requires 1024-dimensional output.

These services are supplied infrastructure, not defects participants must repair. Never use production credentials.

## Windows PowerShell
Choose a parent directory outside every cloned repository. Example:
```powershell
New-Item -ItemType Directory -Path "$env:USERPROFILE\Documents\iat-workshop" -Force
Set-Location "$env:USERPROFILE\Documents\iat-workshop"
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
git clone <round-1-repository-url> repo1-ingestion
Set-Location repo1-ingestion
uv sync --active --frozen --no-install-project
python -c "import sys; print(sys.executable)"
python scripts/preflight.py
```
The printed interpreter must be the parent's `.venv`, not a repository-local or system interpreter. If activation is blocked by policy, ask the facilitator or call the environment's Python executable directly; do not change organisation policy merely for this workshop.

For the already-created local trial folder, activate any approved shared environment and run `uv sync --active --frozen --no-install-project` from `IAT_MOCK_REPO`. Do not clone into that existing non-empty folder.

### Configure credentials in the current terminal
```powershell
$env:IAT_RAG_USER = Read-Host 'Workshop Oracle username'
$credentialPassword = Read-Host 'Workshop Oracle password' -AsSecureString
$env:IAT_RAG_PASSWORD = [System.Net.NetworkCredential]::new('', $credentialPassword).Password
$env:IAT_RAG_DSN = 'localhost:1521/FREEPDB1'
python scripts/preflight.py --services
```
Use the facilitator's DSN if different. Credentials are process environment variables; `.env.example` is documentation and is not loaded automatically. Do not save real values in tracked files or share terminals exposing secrets.

## macOS/Linux
```bash
mkdir -p ~/iat-workshop
cd ~/iat-workshop
python3.12 -m venv .venv
source .venv/bin/activate
git clone <round-1-repository-url> repo1-ingestion
cd repo1-ingestion
uv sync --active --frozen --no-install-project
python scripts/preflight.py
```
Set `IAT_RAG_USER`, `IAT_RAG_PASSWORD` and optional `IAT_RAG_DSN` securely in the current shell using your approved secret-entry method. Do not paste secrets into shell history. Run `python scripts/preflight.py --services`.

## Next round
Leave the environment active. Move to the parent, clone the next released link, enter that new repository and run its documented preflight and launch commands. No new venv is required.

All stages must retain this same dependency set and lockfile. `--no-install-project` prevents an editable package from one checkout shadowing another. Scripts explicitly select their own repository root. Use `python ...` from the active environment rather than an unconfigured `uv run`.

## IDE
Select the parent `.venv` interpreter in VS Code/PyCharm for each clone. Open a fresh terminal or reactivate if necessary. Verify with `python -c "import sys; print(sys.executable)"`.

## Dependency sources
`pyproject.toml` plus `uv.lock` copied from the reference application are the canonical full dependency specification for this trial. They pin the four SDKs (plus Evaluation) and transitive versions. Do not update the lockfile to fix challenge errors. Later repositories must use the same tested files. Only Python application dependencies are installed here; Oracle and Ollama are separate prerequisites.

## Recovery
Missing packages: verify the active interpreter and sync with the frozen lock. Artifactory errors: check access with the facilitator. To rebuild the shared environment, first deactivate and **rename** the old environment for investigation, create a new one in the same workshop parent and repeat installation. Do not delete unrelated environments.

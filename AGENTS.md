# Repository Instructions for AI Agents

## Project Purpose

This repository demonstrates a stateless GitOps rendering workflow:

- Pulumi is used as an offline configuration compiler, not as a live cluster deployment tool.
- The Python Pulumi program renders Kubernetes resources to local YAML under `compiled-manifests/` via `render_yaml_to_directory`.
- The rendered directory is intended to be packaged and transported as an OCI artifact with ORAS, then consumed by GitOps tooling such as Argo CD.
- Avoid introducing dependencies on a live Kubernetes cluster, Pulumi Cloud state, or long-lived remote state backends unless explicitly requested.

## Key Files and Directories

- `__main__.py`: Main Pulumi Python program. It defines the render-only Kubernetes provider and composes manifests from native SDK resources, inline YAML, external YAML files, and a Helm chart.
- `Pulumi.yaml`: Pulumi project metadata. Runtime is Python.
- `Pulumi.dev.yaml` and `Pulumi.prod.yaml`: Stack files. Treat stack configuration carefully; do not add secrets in plaintext.
- `requirements.txt`: Python dependencies for the Pulumi program.
- `raw-manifests/`: Source Kubernetes YAML files that are read into the Pulumi program.
- `compiled-manifests/`: Generated render output. This is ignored by git and should normally not be edited by hand.
- `venv/`: Local Python virtual environment. This is ignored by git and should not be modified as source.

## Development Workflow

Use local Pulumi state for this project:

```bash
pulumi login --local
export PULUMI_CONFIG_PASSPHRASE="my-test-secret-key"
```

Set up Python dependencies from the repository root:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Render manifests locally:

```bash
pulumi stack select dev
pulumi preview
```

If the stack does not exist locally, create/select it first:

```bash
pulumi stack init dev
```

## Coding Guidelines

- Keep the Pulumi program render-only. The provider in `__main__.py` should continue to use `render_yaml_to_directory`.
- Prefer small, explicit changes in `__main__.py`; this repository is a focused demonstration, not a framework.
- When adding Kubernetes resources, prefer native `pulumi_kubernetes` SDK objects for typed examples unless the task specifically needs raw YAML or Helm.
- Put reusable external manifests in `raw-manifests/` and reference them from the Pulumi program.
- Do not hand-edit generated YAML under `compiled-manifests/`; change the source inputs instead.
- Do not commit virtual environments, caches, generated manifests, pulled OCI artifacts, kubeconfigs, registry credentials, or Pulumi secrets.

## Dependency Notes

- `__main__.py` imports both `pulumi` and `pulumi_kubernetes`; keep `requirements.txt` aligned with imports when changing dependencies.
- The Helm chart example uses Bitnami Redis via `pulumi_kubernetes.helm.v3.Chart` with `ChartOpts` and `FetchOpts`.

## Validation

Before finishing changes that affect rendering, run at least:

```bash
python -m compileall __main__.py
```

When the required CLIs and dependencies are available, also run:

```bash
pulumi preview
```

Check generated output only to verify behavior; do not treat generated files as source of truth.

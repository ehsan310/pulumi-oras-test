# Stateless Pulumi Manifest Rendering with GitOps OCI Transport

This guide demonstrates how to use Pulumi as a pure, stateless configuration compiler. Instead of using Pulumi to deploy directly to a cluster (which introduces state tracking files), Pulumi operates completely offline. It compiles native Python SDK objects, inline YAML strings, external files, and Helm charts into a single localized directory. That directory is then bundled into an immutable, atomic OCI configuration layer using **ORAS** (OCI Registry As Storage), ready to be consumed natively by an ArgoCD application controller.

## Architecture Highlights
* **Zero Cluster State Management:** No long-lived state backends or infrastructure locking mechanisms.
* **Multi-Source Composition:** Combines Helm charts, legacy files, inline strings, and native code into one compiled folder.
* **Secure Delivery:** The pipeline needs zero cluster administrative network paths, only push access to an OCI registry.

---

## 1. Prerequisites

Ensure your development workspace has the following tools installed:
* [Pulumi CLI](https://www.pulumi.com/docs/install/)
* [ORAS CLI](https://oras.land/docs/installation)
* [Docker](https://docs.docker.com/get-docker/) (or Podman for local registry validation)
* Python 3.9+

---

## 2. Step-by-Step Workspace Initialization

Run the following from the checked-out repository root. This project already contains `Pulumi.yaml`, stack files, source manifests, and the Python entrypoint, so do **not** run `pulumi new` or scaffold an empty replacement project.

```bash
# Force the Pulumi CLI to use your local storage drive for configuration records
pulumi login --local
export PULUMI_CONFIG_PASSPHRASE=""

# Activate an isolated shell environment and install this project's dependencies
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Use the existing stack and render the manifests locally
pulumi stack select dev
pulumi preview
```

Pulumi's local backend still requires a stack secrets manager, even when this project stores no secrets and only renders YAML. These demo stacks are intentionally initialized with an empty passphrase, so setting `PULUMI_CONFIG_PASSPHRASE=""` makes rendering non-interactive without requiring developers to know or share a password. Do not add secret values to `Pulumi.*.yaml`; inject them through your GitOps secret-management workflow instead.

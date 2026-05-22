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

Run the following block in your terminal to bootstrap a clean workspace, configure Pulumi to execute locally without a cloud account SaaS login, and setup dependencies.

```bash
# Force the Pulumi CLI to use your local storage drive for configuration records
pulumi login --local
export PULUMI_CONFIG_PASSPHRASE="my-test-secret-key"

# Create target directories
mkdir -p pulumi-oras-gitops/raw-manifests
cd pulumi-oras-gitops

# Scaffold an empty Python program blueprint
pulumi new python --name local-renderer --stack dev --yes

# Activate the isolated shell environment and install the correct Kubernetes provider SDK
source venv/bin/activate
pip install pulumi-kubernetes==4.19.0

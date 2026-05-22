import os
import pulumi
import pulumi_kubernetes as k8s
# Explicitly pull the correct type wrappers from the Helm submodule
from pulumi_kubernetes.helm.v3 import Chart, ChartOpts, FetchOpts

output_dir = "compiled-manifests"
os.makedirs(output_dir, exist_ok=True)

# Core Architecture: The Stateless Render Engine
render_provider = k8s.Provider(
    "render-only-provider",
    render_yaml_to_directory=output_dir
)

# ---------------------------------------------------------------------
# METHOD 1: Pure Native Python SDK Object
# ---------------------------------------------------------------------
native_config = k8s.core.v1.ConfigMap(
    "native-config",
    metadata=k8s.meta.v1.ObjectMetaArgs(
        name="showcase-native-config",
        namespace="production"
    ),
    data={"SOURCE": "native-python-sdk"},
    opts=pulumi.ResourceOptions(provider=render_provider)
)

# ---------------------------------------------------------------------
# METHOD 2: Inline Raw YAML String Block
# ---------------------------------------------------------------------
inline_yaml_block = """
apiVersion: v1
kind: Namespace
metadata:
  name: production
"""
inline_manifest = k8s.yaml.v2.ConfigGroup(
    "inline-string-manifest",
    yaml=inline_yaml_block,
    opts=pulumi.ResourceOptions(provider=render_provider)
)

# ---------------------------------------------------------------------
# METHOD 3: Raw YAML Read From an External File
# ---------------------------------------------------------------------
file_manifest = k8s.yaml.v2.ConfigFile(
    "external-file-manifest",
    file="raw-manifests/external-service.yaml",
    opts=pulumi.ResourceOptions(provider=render_provider)
)

# ---------------------------------------------------------------------
# METHOD 4: Native Helm Chart Rendering (FIXED: Using ChartOpts & FetchOpts)
# ---------------------------------------------------------------------
redis_chart = Chart(
    "redis-cache",
    ChartOpts(
        chart="redis",
        version="18.0.0",
        fetch_opts=FetchOpts(
            repo="https://charts.bitnami.com/bitnami"
        ),
        values={
            "architecture": "standalone",
            "auth": {"enabled": False},
            "master": {"persistence": {"enabled": False}}
        },
        namespace="production"
    ),
    opts=pulumi.ResourceOptions(provider=render_provider)
)

pulumi.export("manifest_directory", output_dir)

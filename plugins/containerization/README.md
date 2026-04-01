# Containerization Plugin

Language-agnostic containerization for research software projects. This plugin
provides agents, skills, and commands for creating, auditing, and managing
containers across Docker, Podman, Singularity/Apptainer, and GPU-accelerated
environments. It is designed for research software engineers who need
reproducible, secure, and optimized container images for scientific computing
workflows, HPC clusters, and cloud-native deployments.

## Agents

| Name | Description |
|------|-------------|
| **Container Build Specialist** | Expert in multi-stage Dockerfile construction, image optimization, and build automation for any language ecosystem |
| **Container Security Analyst** | Expert in container security scanning, vulnerability remediation, supply chain integrity, and hardening for research software |

## Skills

| Name | Description |
|------|-------------|
| **dockerfile-patterns** | Multi-stage build patterns, base image selection, and language-specific Dockerfile templates for Python, Rust, Go, Node, R, Julia, C/C++, and .NET |
| **compose-orchestration** | Docker Compose and Podman Compose patterns for multi-service research applications, development environments, and local testing |
| **container-security** | Container security scanning with Trivy, Grype, and Snyk; image hardening; secrets management; and SBOM generation |
| **devcontainers** | Dev container configuration for VS Code and GitHub Codespaces with language-specific tooling and extension recommendations |
| **gpu-containers** | NVIDIA CUDA and AMD ROCm container patterns for GPU-accelerated scientific computing, ML training, and inference workloads |
| **podman** | Rootless Podman usage, Docker compatibility, systemd integration, and pod-based workflows for development and HPC |
| **singularity-apptainer** | Singularity/Apptainer definition files for HPC clusters, converting Docker images, and MPI-enabled containers |
| **container-registries** | Publishing images to GHCR, Docker Hub, and private registries with tagging strategies, retention policies, and CI/CD integration |

## Commands

| Command | Description |
|---------|-------------|
| `/containerize` | Create a Dockerfile for a project by analyzing its language, dependencies, and structure |
| `/container-audit` | Audit an existing Dockerfile or container image for best practices, security, and optimization opportunities |

## When to Use

- Creating a Dockerfile for a new or existing research software project
- Auditing an existing Dockerfile for best practices and security issues
- Setting up GPU-accelerated containers for ML or scientific computing
- Converting Docker images to Singularity/Apptainer for HPC clusters
- Configuring dev containers for VS Code or GitHub Codespaces
- Publishing container images to a registry with proper tagging
- Setting up multi-service development environments with Docker Compose
- Hardening containers for production deployment

## Out of Scope

This plugin focuses on building, auditing, and publishing container images. It
does **not** cover:

- **Container orchestration platforms** — Kubernetes, Docker Swarm, Nomad, or
  other orchestration systems are outside the scope of this plugin
- **Cloud deployment** — Deploying containers to AWS ECS/EKS, Google Cloud Run,
  Azure Container Instances, or other cloud platforms
- **CI/CD pipelines beyond image publishing** — Full CI/CD workflow design,
  GitHub Actions configuration, and pipeline orchestration belong to the GitHub
  plugin
- **Infrastructure as code** — Terraform, Pulumi, CloudFormation, or other IaC
  tools for provisioning container infrastructure
- **Service mesh and networking** — Istio, Linkerd, or advanced networking
  configuration between containerized services

## Related Plugins

| Need | Plugin |
|------|--------|
| Project scaffolding, community health files, handoff readiness | [Project Management](../project-management/) |
| Python-specific development practices, packaging, testing | [Scientific Python Development](../scientific-python-development/) |

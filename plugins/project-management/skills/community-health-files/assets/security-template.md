# Security Policy

## Supported Versions

<!-- Update this table to reflect which versions of your project currently
     receive security updates. -->

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

Only the latest minor release of each supported major version receives security
patches. We recommend always running the latest version.

## Reporting a Vulnerability

We take the security of [Project Name] seriously. If you believe you have found
a security vulnerability, please report it responsibly.

### How to Report

**Please do NOT report security vulnerabilities through public GitHub issues.**

Instead, use one of the following methods:

1. **GitHub Private Vulnerability Reporting** (preferred):
   Go to the [Security Advisories page](https://github.com/ORG/REPO/security/advisories/new)
   and create a new private security advisory.

2. **Email**: Send a detailed report to **[security@example.com]**

   If possible, encrypt your message using our PGP key:
   [Public key link or fingerprint]

### What to Include

Please include as much of the following information as possible to help us
understand and address the issue:

- **Description**: A clear description of the vulnerability
- **Impact**: The potential impact and severity of the vulnerability
- **Affected versions**: Which versions of the software are affected
- **Steps to reproduce**: Detailed steps to reproduce the vulnerability
- **Proof of concept**: Code or commands that demonstrate the issue (if applicable)
- **Suggested fix**: Any ideas you have for how to fix the issue (if applicable)
- **Environment**: Operating system, Python version, and relevant dependency versions

### What to Expect

After you submit a report:

| Step | Timeline | Action |
|------|----------|--------|
| 1 | Within 48 hours | We will acknowledge receipt of your report |
| 2 | Within 7 days | We will confirm the vulnerability and assess its impact |
| 3 | Within 30 days | We will develop and test a fix |
| 4 | Within 90 days | We will release the fix and publish a security advisory |

These timelines are targets. Complex issues may require more time. We will keep
you informed of our progress throughout the process.

## Scope

### In Scope

The following are considered security concerns for this project:

- **Code execution vulnerabilities**: Arbitrary code execution, injection attacks
- **Data integrity issues**: Incorrect computation results due to exploitable flaws
- **Dependency vulnerabilities**: Known vulnerabilities in direct dependencies
- **Information disclosure**: Unintended exposure of sensitive data
- **Authentication/authorization**: Issues in any access control mechanisms
- **Denial of service**: Resource exhaustion or crash-inducing inputs

### Scientific Software Specific Concerns

For scientific software, we also consider the following as security-relevant:

- **Data corruption**: Bugs that silently produce incorrect scientific results
- **Supply chain attacks**: Compromised dependencies that affect data integrity
- **Deserialization vulnerabilities**: Issues with loading data files (pickle, HDF5, etc.)
- **Path traversal**: Issues with file path handling in data I/O operations

### Out of Scope

The following are generally not considered security vulnerabilities:

- Bugs that cause crashes but do not expose data or allow code execution
- Performance issues (unless they enable denial-of-service attacks)
- Issues requiring physical access to the machine
- Issues in unsupported versions
- Issues in third-party dependencies (report these to the dependency maintainers)
- Social engineering attacks

## Disclosure Policy

We follow a coordinated disclosure process:

1. **Reporter submits vulnerability** through a private channel
2. **We confirm and assess** the vulnerability
3. **We develop a fix** and prepare a release
4. **We notify the reporter** of the planned fix and disclosure date
5. **We release the fix** and publish a security advisory
6. **We credit the reporter** in the advisory (with their permission)

We ask reporters to:

- Give us reasonable time to address the issue before public disclosure
- Avoid exploiting the vulnerability beyond what is necessary to demonstrate it
- Not access or modify other users' data
- Act in good faith to avoid privacy violations, destruction of data, and
  disruption of services

## Security Best Practices for Users

To keep your installation secure:

- **Keep your software up to date**: Install the latest version promptly
- **Pin dependencies**: Use lock files or pinned requirements for production
- **Verify downloads**: Check package integrity when installing from PyPI
- **Review changelogs**: Read the changelog for each release, especially security fixes
- **Report issues**: If you notice anything suspicious, report it following the
  process above

## Recognition

We appreciate the efforts of security researchers and community members who
help keep [Project Name] secure. With the reporter's permission, we will
acknowledge their contribution in:

- The security advisory
- The changelog entry for the fix
- The project's CONTRIBUTORS file (if applicable)

## Contact

For security-related questions that are not vulnerability reports, please
contact [security@example.com] or open a
[GitHub Discussion](https://github.com/ORG/REPO/discussions).

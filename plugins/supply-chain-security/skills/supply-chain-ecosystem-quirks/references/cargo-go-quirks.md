# cargo / Go Supply Chain Quirks

## Threat Relevance

Rust and Go are often perceived as safer-by-default ecosystems, but both have install-time or build-time execution surfaces that the general "pin and scan" advice from `supply-chain-dependency-security` does not address. Cargo runs `build.rs` for every crate that has one on every build, with no global disable. Go's `go generate` and module-proxy/checksum-database settings (`GOPROXY`, `GOSUMDB`) decide whether the supply-chain integrity guarantees actually hold. Misconfigure either, and the lockfile/`go.sum` is decorative.

## Cargo build.rs Arbitrary Execution

Every `cargo build` of a crate that ships a `build.rs` file executes that script at build time with the project's privileges. There is no global "disable build scripts" flag — `build.rs` is a first-class Cargo feature used for legitimate native-library linking and codegen. That makes auditing the contents of `build.rs` the only mitigation.

Find every `build.rs` pulled into the build (project plus cached crate source):

```bash
find . -name build.rs -not -path './target/*' | head -20
find ~/.cargo/registry/src -name build.rs 2>/dev/null | head -20
```

For a specific suspicious crate:

```bash
find ~/.cargo/registry/src -path "*<crate-name>*/build.rs"
```

Cargo provides no built-in attestation that a `build.rs` is the same one published to crates.io. Tools like `cargo-vet` and `cargo-crev` provide human-audited trust databases — recommend `cargo vet` for any project where the dependency graph contains unfamiliar crates.

## .cargo/config.toml Registries

`.cargo/config.toml` (project-local or `~/.cargo/`) can configure alternative registries. Any non-crates.io registry is a supply-chain decision that needs explicit review.

Audit:

```bash
grep -A 2 '\[registries\.' .cargo/config.toml ~/.cargo/config.toml 2>/dev/null
grep -A 2 '\[source\.' .cargo/config.toml ~/.cargo/config.toml 2>/dev/null
```

`[source]` blocks can redirect crates.io to a mirror — a legitimate use is an air-gapped corporate proxy, an illegitimate use is dependency-confusion via a typo-mirror. Verify the URL and document the choice.

## Cargo.lock Discipline

For binary crates, `Cargo.lock` is committed and `cargo build --locked` refuses to update it. For library crates the convention has been "do not commit," but for security-sensitive libraries commit anyway — the lock applies when downstream consumers run `cargo build --locked` against your repo (e.g., when building from a Git dependency).

Verify CI respects the lock:

```bash
grep -rE 'cargo (build|test|run)' .github/workflows/ | grep -v -- '--locked'
```

Any `cargo build` without `--locked` in CI is a finding — it permits silent dep upgrades.

## Go //go:generate Directives

`go generate ./...` walks Go files and executes any line starting with `//go:generate ` as a shell command. Less risky than Cargo's `build.rs` because `go generate` only runs on explicit invocation (not on every `go build`), but a malicious or compromised dep can ship a directive that runs the first time a developer or CI invokes generate.

Audit before running `go generate` on a fresh dep:

```bash
grep -rn '^//go:generate ' . | head -50
```

For a specific module:

```bash
grep -rn '^//go:generate ' $(go env GOMODCACHE)/<module>@<version>
```

Flag any directive that fetches from the network or writes outside the module directory.

## GOPROXY and GOSUMDB Discipline

Go's module integrity rests on two settings:

- `GOPROXY=https://proxy.golang.org,direct` — module proxy with fallback to direct VCS. The proxy provides immutability (a published version cannot be silently replaced).
- `GOSUMDB=sum.golang.org` — checksum database. Every module fetched is verified against a globally-consistent transparency log.

Disabling either weakens the chain. Check:

```bash
go env GOPROXY GOSUMDB GOFLAGS
```

If `GOSUMDB=off` or `GOFLAGS` contains `-insecure`, flag and investigate why. If `GOPROXY=direct` (or `off`), the proxy's immutability is bypassed and `go.sum` is the only check — sufficient for trusted deps but loses the transparency-log audit trail.

The corresponding controls in CI:

```bash
# Block silent go.sum changes
go build -mod=readonly ./...        # refuses to add new entries
go mod verify                        # checks downloaded modules match go.sum
```

Audit:

```bash
grep -rE 'go (build|test|run)' .github/workflows/ | grep -v 'mod=readonly\|mod=vendor'
```

## References

- Cargo build scripts: <https://doc.rust-lang.org/cargo/reference/build-scripts.html>
- cargo-vet: <https://mozilla.github.io/cargo-vet/>
- Go module proxy protocol: <https://go.dev/ref/mod#module-proxy>
- Go checksum database: <https://sum.golang.org/>
- `go generate`: <https://go.dev/blog/generate>

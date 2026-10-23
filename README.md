# RED

Systems and tooling. I work close to the metal — process internals, request
pipelines, the parts of a stack that don't show up in a diagram.

Currently building **[s0ulctl](https://github.com/rrddngtnn/s0ulctl)** — a patcher
that replaces the hardcoded system prompts inside [9router](https://www.npmjs.com/package/9router)
with a markdown file on disk, hot-reloaded per request.

---

## Focus

| Area | What that means in practice |
|---|---|
| **Systems** | Linux process model, file descriptors, mtime-based caching, service supervision under systemd |
| **Runtime patching** | Rewriting bundled JS in place, idempotent installers, backup and rollback discipline |
| **LLM plumbing** | Provider adapters, request transforms, prompt injection at the transport layer |
| **Shell** | POSIX-compatible installers, multi-install discovery, failure paths that report instead of guess |

---

## Selected work

### s0ulctl

Three provider adapters inside 9router discard the inbound `role:system` message
and substitute their own identity string before forwarding upstream. `s0ulctl`
replaces those strings with a call to a loader that reads `soul.md` from disk,
cached by mtime.

```bash
git clone https://github.com/rrddngtnn/s0ulctl
cd s0ulctl
bash src/install.sh                          # patch every discovered 9router install
sudo systemctl restart 9router.service
```

Constraints it holds to:

- **Idempotent** — safe to re-run after `npm i -g 9router` replaces the chunks
- **Multi-install aware** — nvm, Hermes-managed node, and global npm trees all get patched
- **Fails safe** — `?.()` guards the startup race; `||<original>` falls back to the vendor string when `soul.md` is missing or empty
- **Reversible** — every touched file gets a `.bak-*` sibling; `uninstall.sh` restores them

`Shell` · `Node.js` · 202 lines across three files

---

## Working notes

- Composition over inheritance. Small modules with explicit inputs.
- Errors as values at boundaries; exceptions reserved for programmer error.
- Immutability by default, mutation behind a named function.
- Profile the hot path before touching it. Guessing produces cache misses and cargo cults.
- Comments explain *why*. The code already says *what*.

---

## Contact

[GitHub](https://github.com/rrddngtnn) · [Email](mailto:you@example.com)

<sub>Updated 2026-10-22</sub>

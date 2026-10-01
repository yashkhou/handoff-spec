> [!IMPORTANT]
> **This project now lives in [agent-reliability-lab](https://github.com/yashkhou/agent-reliability-lab/tree/main/packages/handoff-spec).** Its full history was moved there and this repository is archived.
>
> `pip install "git+https://github.com/yashkhou/agent-reliability-lab#subdirectory=packages/handoff-spec"`


# handoff-spec

A strict, resumable handoff document for long-running agents: state, evidence, authority and continuation invariants in one portable contract.

## What it does

- validates objectives, completed work, evidence references and unresolved decisions
- keeps allowed and forbidden authority explicit across continuation boundaries
- requires continuation invariants and ordered next actions
- canonicalizes handoffs and emits a stable SHA-256 content digest

## Quick start

```bash
PYTHONPATH=src python -m handoff_spec examples/handoff.json
```

No model API, network service, or third-party package is required.

## Architecture

The handoff is a JSON document with a required schema enforced by a small validator. Canonical serialization makes state comparisons and checkpoint identities stable across processes.

See [`docs/architecture.md`](docs/architecture.md) for the data model and trade-offs.

## V1 boundary

V1 validates structure and local semantic invariants; it does not authenticate evidence URLs or grant authority by itself.

## Development

```bash
python -m unittest discover -s tests -v
```

MIT licensed.


## v0.1.1

**Authority-safe resume validation.** Handoffs can now be checked across resumptions so objective drift, authority expansion, relaxed forbidden actions, and dropped continuation invariants fail closed.

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

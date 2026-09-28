# Architecture

The handoff is a JSON document with a required schema enforced by a small validator. Canonical serialization makes state comparisons and checkpoint identities stable across processes.

## Design constraints

- deterministic offline behavior
- explicit machine-readable inputs and outputs
- small standard-library surface area
- failures are surfaced rather than hidden

## V1 limitation

V1 validates structure and local semantic invariants; it does not authenticate evidence URLs or grant authority by itself.

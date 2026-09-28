# Implementation note

Working V1 scope: A strict, resumable handoff document for long-running agents: state, evidence, authority and continuation invariants in one portable contract.

Verified with `python -m unittest discover -s tests -v`.

Known boundary: V1 validates structure and local semantic invariants; it does not authenticate evidence URLs or grant authority by itself.

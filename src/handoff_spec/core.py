from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json

REQUIRED = ("version", "objective", "completed", "evidence", "unresolved", "authority", "invariants", "next")


class HandoffError(ValueError):
    pass


@dataclass(frozen=True)
class TransitionCheck:
    ok: bool
    reasons: tuple[str, ...]

    def as_dict(self):
        return {"ok": self.ok, "reasons": list(self.reasons)}


def validate(data):
    missing = [key for key in REQUIRED if key not in data]
    if missing:
        raise HandoffError("missing: " + ",".join(missing))
    if data["version"] != "1":
        raise HandoffError("unsupported version")
    for key in ("completed", "evidence", "unresolved", "invariants", "next"):
        if not isinstance(data[key], list):
            raise HandoffError(f"{key} must be a list")
    if not isinstance(data["objective"], str) or not data["objective"].strip():
        raise HandoffError("objective must be non-empty")
    authority = data["authority"]
    if not isinstance(authority, dict) or not isinstance(authority.get("allowed"), list) or not isinstance(authority.get("forbidden"), list):
        raise HandoffError("authority requires allowed/forbidden lists")
    overlap = set(authority["allowed"]) & set(authority["forbidden"])
    if overlap:
        raise HandoffError("authority conflict: " + ",".join(sorted(overlap)))
    if not data["invariants"]:
        raise HandoffError("at least one continuation invariant is required")
    return data


def canonical(data):
    validate(data)
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(data):
    return hashlib.sha256(canonical(data).encode()).hexdigest()


def check_transition(previous, current) -> TransitionCheck:
    """Fail closed when a resumed handoff silently expands authority or drops invariants."""
    validate(previous)
    validate(current)
    reasons: list[str] = []
    if current["objective"] != previous["objective"]:
        reasons.append("objective changed across handoff")
    previous_allowed = set(previous["authority"]["allowed"])
    current_allowed = set(current["authority"]["allowed"])
    expanded = sorted(current_allowed - previous_allowed)
    if expanded:
        reasons.append("authority expanded: " + ",".join(expanded))
    previous_forbidden = set(previous["authority"]["forbidden"])
    current_forbidden = set(current["authority"]["forbidden"])
    relaxed = sorted(previous_forbidden - current_forbidden)
    if relaxed:
        reasons.append("forbidden authority relaxed: " + ",".join(relaxed))
    lost = [item for item in previous["invariants"] if item not in current["invariants"]]
    if lost:
        reasons.append("continuation invariants removed: " + "; ".join(map(str, lost)))
    return TransitionCheck(not reasons, tuple(reasons))


def assert_transition(previous, current):
    check = check_transition(previous, current)
    if not check.ok:
        raise HandoffError("; ".join(check.reasons))
    return current

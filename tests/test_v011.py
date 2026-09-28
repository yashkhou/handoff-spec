import unittest

from handoff_spec.core import HandoffError, assert_transition, check_transition


def handoff(**overrides):
    base = {
        "version": "1",
        "objective": "ship safely",
        "completed": [],
        "evidence": [],
        "unresolved": [],
        "authority": {"allowed": ["read"], "forbidden": ["deploy", "delete"]},
        "invariants": ["no live writes"],
        "next": [],
    }
    base.update(overrides)
    return base


class TransitionTests(unittest.TestCase):
    def test_equal_or_stricter_authority_can_resume(self):
        current = handoff(authority={"allowed": ["read"], "forbidden": ["deploy", "delete", "network"]})
        self.assertTrue(check_transition(handoff(), current).ok)

    def test_authority_expansion_is_rejected(self):
        current = handoff(authority={"allowed": ["read", "deploy"], "forbidden": ["delete"]})
        check = check_transition(handoff(), current)
        self.assertFalse(check.ok)
        self.assertIn("authority expanded", check.reasons[0])

    def test_invariant_loss_is_rejected(self):
        current = handoff(invariants=["different invariant"])
        with self.assertRaises(HandoffError):
            assert_transition(handoff(), current)


if __name__ == "__main__":
    unittest.main()

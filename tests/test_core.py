import unittest,sys; sys.path.insert(0,'src')
from handoff_spec.core import *
D={'version':'1','objective':'x','completed':[],'evidence':[],'unresolved':[],'authority':{'allowed':['edit'],'forbidden':['publish']},'invariants':['api stable'],'next':['test']}
class T(unittest.TestCase):
 def test_valid(self): self.assertIs(validate(D),D)
 def test_digest_stable(self): self.assertEqual(digest(D),digest(dict(reversed(list(D.items())))))
 def test_authority_conflict(self):
  x={**D,'authority':{'allowed':['edit'],'forbidden':['edit']}}
  with self.assertRaises(HandoffError): validate(x)

import unittest

from traiter.pylib.darwin_core import DarwinCore

from tests.setup import to_ent

LABEL = "leaf_folding"


class TestLeafFolding(unittest.TestCase):
    def test_leaf_folding_dwc_01(self):
        dwc = DarwinCore()
        ent = to_ent(LABEL, "cucullate")
        ent._.trait.to_dwc(dwc, ent)
        actual = dwc.to_dict()
        self.assertEqual(actual, {"dynamicProperties": {"leafFolding": "cucullate"}})

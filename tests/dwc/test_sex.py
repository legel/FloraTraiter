import unittest

from traiter.pylib.darwin_core import DarwinCore

from tests.setup import to_ent

LABEL = "sex"


class TestSex(unittest.TestCase):
    def test_sex_dwc_01(self):
        dwc = DarwinCore()
        ent = to_ent(LABEL, "(pistillate)")
        ent._.trait.to_dwc(dwc, ent)
        actual = dwc.to_dict()
        self.assertEqual(actual, {"sex": "pistillate"})

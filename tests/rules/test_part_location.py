import unittest

from flora.pylib.rules.part import Part
from flora.pylib.rules.part_location import PartLocation
from flora.pylib.rules.shape import Shape
from flora.pylib.rules.size import Dimension, Size
from flora.pylib.rules.surface import Surface
from tests.setup import parse


class TestPartLocation(unittest.TestCase):
    def test_part_location_01(self):
        self.assertEqual(
            parse("stipules 3-8 mm, semiamplexicaul, adnate to petiole for 1-2 mm"),
            [
                Part(part="stipule", type="leaf_part", start=0, end=8),
                Size(
                    dims=[Dimension("length", low=0.3, high=0.8)],
                    start=9,
                    end=15,
                    units="cm",
                    part="stipule",
                ),
                Shape(
                    shape="semiamplexicaul",
                    start=17,
                    end=32,
                    part="stipule",
                ),
                PartLocation(
                    part_location="adnate to petiole for 1 - 2 mm",
                    type="part_as_distance",
                    start=34,
                    end=62,
                ),
            ],
        )

    def test_part_location_02(self):
        self.assertEqual(
            parse("leaves completely embracing stem but not connate"),
            [
                Part(
                    part="leaf",
                    type="leaf_part",
                    start=0,
                    end=6,
                    part_location="embracing stem",
                ),
                PartLocation(
                    part_location="embracing stem",
                    type="part_as_location",
                    start=18,
                    end=32,
                ),
            ],
        )

    def test_part_location_03(self):
        self.maxDiff = None
        self.assertEqual(
            parse("stipules shortly ciliate at margin"),
            [
                Part(
                    part="stipule",
                    type="leaf_part",
                    part_location="at margin",
                    start=0,
                    end=8,
                ),
                Surface(
                    surface="ciliate",
                    part_location="at margin",
                    start=9,
                    end=24,
                    part="stipule",
                ),
                PartLocation(
                    part_location="at margin",
                    type="subpart_as_location",
                    start=25,
                    end=34,
                ),
            ],
        )

    def test_part_location_04(self):
        self.assertEqual(
            parse("capitula immersed in foliage."),
            [
                Part(
                    part="capitulum",
                    type="inflorescence",
                    part_location="immersed in foliage",
                    start=0,
                    end=8,
                ),
                PartLocation(
                    part_location="immersed in foliage",
                    type="part_as_location",
                    start=9,
                    end=28,
                ),
            ],
        )

    def test_part_location_05(self):
        self.maxDiff = None
        self.assertEqual(
            parse(
                "the short terminal pseudoraceme of ovoid-ellipsoid or globose "
                "capitula immersed in foliage.",
            ),
            [
                PartLocation(
                    start=10,
                    end=18,
                    part_location="terminal",
                    type="part_location",
                ),
                Part(
                    part="pseudoraceme",
                    type="inflorescence",
                    start=19,
                    end=31,
                    part_location="terminal",
                ),
                Shape(
                    shape="ovoid-ellipsoid",
                    start=35,
                    end=50,
                    part="capitulum",
                    part_location="immersed in foliage",
                ),
                Shape(
                    shape="spheric",
                    start=54,
                    end=61,
                    part="capitulum",
                    part_location="immersed in foliage",
                ),
                Part(
                    part="capitulum",
                    type="inflorescence",
                    start=62,
                    end=70,
                    part_location="immersed in foliage",
                ),
                PartLocation(
                    part_location="immersed in foliage",
                    type="part_as_location",
                    start=71,
                    end=90,
                ),
            ],
        )

    def test_part_location_06(self):
        self.assertEqual(
            parse("""setose their whole length dorsally and the flowers are smaller"""),
            [
                Surface(
                    surface="setose",
                    start=0,
                    end=6,
                    part="flower",
                    part_location="dorsal",
                ),
                PartLocation(
                    type="part_location",
                    part_location="dorsal",
                    start=26,
                    end=34,
                ),
                Part(
                    part="flower",
                    start=43,
                    end=50,
                    part_location="dorsal",
                    type="flower_part",
                ),
            ],
        )

import unittest

from traiter.pylib.traits.color import Color
from traiter.pylib.traits.elevation import Elevation
from traiter.pylib.traits.habitat import Habitat

from flora.pylib.traits.locality import Locality
from flora.pylib.traits.part import Part
from flora.pylib.traits.plant_duration import PlantDuration
from flora.pylib.traits.subpart import Subpart
from tests.setup import test


class TestLocality(unittest.TestCase):
    def test_locality_01(self):
        self.assertEqual(
            test("""5 miles North of Mason off Hwy 386."""),
            [
                Locality(
                    locality="5 miles North of Mason off Hwy 386.",
                    trait="locality",
                    start=0,
                    end=35,
                )
            ],
        )

    def test_locality_02(self):
        self.assertEqual(
            test(
                """
                Tunkhannock Twp. Pocono Pines Quadrangle. Mud Run, Stonecrest Park,.16
                miles SSW of Long Pond, PA. Headwaters wetland of Indiana Mountains
                Lake.
                """
            ),
            [
                Locality(
                    locality="Tunkhannock Twp.",
                    trait="locality",
                    start=0,
                    end=16,
                ),
                Locality(
                    locality="Pocono Pines Quadrangle.",
                    trait="locality",
                    start=17,
                    end=41,
                ),
                Locality(
                    locality="Mud Run, Stonecrest Park,"
                    ".16 miles SSW of Long Pond, PA.",
                    trait="locality",
                    start=42,
                    end=98,
                ),
                Locality(
                    locality="Headwaters wetland of Indiana Mountains Lake.",
                    trait="locality",
                    start=99,
                    end=144,
                ),
            ],
        )

    def test_locality_03(self):
        self.assertEqual(
            test("""; files. purple."""),
            [],
        )

    def test_locality_04(self):
        self.assertEqual(
            test("""(Florida's Turnpike)"""),
            [
                Locality(
                    locality="Florida's Turnpike",
                    trait="locality",
                    start=0,
                    end=19,
                )
            ],
        )

    def test_locality_05(self):
        self.assertEqual(
            test(
                """
                Wallowa-Whitman National Forest, Forest Service Road 7312.
                """
            ),
            [
                Locality(
                    locality="Wallowa-Whitman National Forest, Forest Service "
                    "Road 7312.",
                    trait="locality",
                    start=0,
                    end=58,
                ),
            ],
        )

    def test_locality_06(self):
        self.assertEqual(
            test("""Sonoran Desert scrub, disturbed trail side. Occasional annual."""),
            [
                Habitat(
                    habitat="sonoran desert scrub",
                    trait="habitat",
                    start=0,
                    end=20,
                ),
                Locality(
                    locality="disturbed trail side.",
                    trait="locality",
                    start=22,
                    end=43,
                ),
                PlantDuration(
                    plant_duration="annual",
                    trait="plant_duration",
                    start=55,
                    end=61,
                ),
            ],
        )

    def test_locality_07(self):
        self.assertEqual(
            test(
                """
                Arizona Uppland Sonoran Desert desert scrub, flats.
                Sandy soil Local erecta annual,
                """
            ),
            [
                Habitat(
                    habitat="uppland sonoran desert desert scrub flats",
                    trait="habitat",
                    start=8,
                    end=50,
                ),
                Habitat(habitat="sandy soil", trait="habitat", start=52, end=62),
                PlantDuration(
                    plant_duration="annual",
                    trait="plant_duration",
                    start=76,
                    end=82,
                ),
            ],
        )

    def test_locality_08(self):
        self.assertEqual(
            test("""Scattered on edge of forest;"""),
            [Habitat(end=27, habitat="edge of forest", start=13, trait="habitat")],
        )

    def test_locality_09(self):
        self.assertEqual(
            test("""lobes turned out or black."""),
            [
                Subpart(trait="subpart", subpart="lobe", start=0, end=5),
                Color(
                    color="black",
                    trait="color",
                    start=20,
                    end=25,
                    subpart="lobe",
                ),
            ],
        )

    def test_locality_10(self):
        self.assertEqual(
            test(
                """
                LOCATION Along Rte. 39, 9.1 mi SEof Santiago Papasquiaro.
                HABITAT Pine-juniper-oak-acacia zone.
                """
            ),
            [
                Locality(
                    locality="Along Rte. 39, 9.1 mi SEof Santiago Papasquiaro.",
                    labeled=True,
                    trait="locality",
                    start=0,
                    end=57,
                ),
                Habitat(
                    habitat="Pine-juniper-oak-acacia zone",
                    trait="habitat",
                    start=58,
                    end=94,
                ),
            ],
        )

    def test_locality_11(self):
        self.assertEqual(
            test(
                """
                Fruit is a
                grape and is dark purple in color.
                """
            ),
            [
                Part(fruit_part="fruit", trait="fruit_part", start=0, end=5),
                Color(
                    color="purple-in-color",
                    trait="color",
                    start=24,
                    end=44,
                    part="fruit",
                ),
            ],
        )

    def test_locality_12(self):
        self.assertEqual(
            test("""Monteverde. Elev. 1400- 1500 m. Lower montane rainforest"""),
            [
                Elevation(
                    trait="elevation",
                    elevation=1400.0,
                    elevation_high=1500.0,
                    units="m",
                    start=12,
                    end=31,
                ),
                Habitat(
                    end=56,
                    habitat="montane rain forest",
                    start=38,
                    trait="habitat",
                ),
            ],
        )

    def test_locality_13(self):
        self.assertEqual(
            test("""Point Sublime Road about 1 miles east of Milk Creek."""),
            [
                Locality(
                    locality="Point Sublime Road about 1 miles east of Milk Creek.",
                    trait="locality",
                    start=0,
                    end=52,
                ),
            ],
        )

    def test_locality_14(self):
        self.assertEqual(
            test("""north of the Illinois Central Railroad,"""),
            [
                Locality(
                    locality="north of the Illinois Central Railroad",
                    trait="locality",
                    start=0,
                    end=38,
                ),
            ],
        )

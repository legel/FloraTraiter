import unittest

from flora.pylib.rules.part import Part
from flora.pylib.rules.reproduction import Reproduction
from flora.pylib.rules.sex import Sex
from tests.setup import parse


class TestReproduction(unittest.TestCase):
    def test_reproduction_01(self):
        self.maxDiff = None
        self.assertEqual(
            parse(
                """
                bisexual (unisexual and plants sometimes gynodioecious,
                or plants dioecious""",
            ),
            [
                Sex(sex="bisexual", start=0, end=8),
                Sex(sex="unisexual", start=10, end=19),
                Part(
                    part="plant",
                    type="plant_part",
                    sex="unisexual",
                    start=24,
                    end=30,
                ),
                Reproduction(
                    reproduction="gynodioecious",
                    start=41,
                    end=54,
                ),
                Part(
                    type="plant_part",
                    part="plant",
                    sex="unisexual",
                    start=59,
                    end=65,
                ),
                Reproduction(
                    reproduction="dioecious",
                    start=66,
                    end=75,
                ),
            ],
        )

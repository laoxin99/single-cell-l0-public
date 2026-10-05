import unittest

from cell_env import Env
from l0_sensing import SenseOrgan
from public_l0 import PublicCell, run_fixture


class PublicL0Tests(unittest.TestCase):
    def test_sensor_exposes_local_physical_signals(self) -> None:
        env = Env()
        sense = SenseOrgan().scan(env, 68.0, 90.0, 0.0, 6.0)
        self.assertGreater(sense.here.nutrient, 0.0)
        self.assertLessEqual(sense.afferent().harm, 1.0)

    def test_harmful_field_selects_avoid_label(self) -> None:
        env = Env()
        cell = PublicCell(x=190.0, y=52.0)
        sense = SenseOrgan().scan(env, cell.x, cell.y, cell.heading, cell.radius)
        self.assertGreaterEqual(sense.afferent().harm, 0.30)
        self.assertEqual(cell._choose_behavior(sense.afferent()), "avoid")

    def test_fixed_twenty_run_fixture(self) -> None:
        results = [run_fixture(seed) for seed in range(101, 121)]
        self.assertEqual(len(results), 20)
        self.assertTrue(all(result["division_count"] == 1 for result in results))
        self.assertTrue(all(result["first_division"] == 21 for result in results))


if __name__ == "__main__":
    unittest.main()


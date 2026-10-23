import unittest

from src.power_budget import (
    calculate_total_power,
    calculate_total_energy,
)


class TestPowerBudget(unittest.TestCase):

    def setUp(self):
        self.subsystems = [
            {
                "name": "OBC",
                "power_w": 1.5,
                "operating_hours": 1.0,
            },
            {
                "name": "Communications",
                "power_w": 2.5,
                "operating_hours": 0.4,
            },
            {
                "name": "Payload",
                "power_w": 3.0,
                "operating_hours": 0.5,
            },
        ]

    def test_total_power(self):
        self.assertAlmostEqual(
            calculate_total_power(self.subsystems),
            7.0,
        )

    def test_total_energy(self):
        self.assertAlmostEqual(
            calculate_total_energy(self.subsystems),
            4.0,
        )

    def test_empty_subsystems(self):
        self.assertEqual(calculate_total_power([]), 0.0)
        self.assertEqual(calculate_total_energy([]), 0.0)

    def test_zero_power(self):
        subsystems = [
            {
                "name": "OBC",
                "power_w": 0.0,
                "operating_hours": 5.0,
            }
        ]

        self.assertEqual(calculate_total_power(subsystems), 0.0)
        self.assertEqual(calculate_total_energy(subsystems), 0.0)

    def test_zero_operating_time(self):
        subsystems = [
            {
                "name": "Communications",
                "power_w": 4.0,
                "operating_hours": 0.0,
            }
        ]

        self.assertEqual(calculate_total_energy(subsystems), 0.0)


if __name__ == "__main__":
    unittest.main()

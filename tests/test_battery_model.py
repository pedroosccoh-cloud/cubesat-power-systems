import unittest

from src.battery_model import calculate_final_soc


class TestBatteryModel(unittest.TestCase):
    def test_discharge(self):
        self.assertAlmostEqual(
            calculate_final_soc(80, 10, energy_used_wh=2),
            60,
        )

    def test_charge_with_efficiency(self):
        self.assertAlmostEqual(
            calculate_final_soc(20, 10, energy_charged_wh=4, charge_efficiency=0.9),
            56,
        )

    def test_soc_does_not_exceed_capacity(self):
        self.assertAlmostEqual(
            calculate_final_soc(90, 10, energy_charged_wh=5),
            100,
        )

    def test_soc_does_not_go_below_zero(self):
        self.assertAlmostEqual(
            calculate_final_soc(10, 10, energy_used_wh=5),
            0,
        )

    def test_invalid_capacity_raises(self):
        with self.assertRaises(ValueError):
            calculate_final_soc(50, 0)


if __name__ == "__main__":
    unittest.main()

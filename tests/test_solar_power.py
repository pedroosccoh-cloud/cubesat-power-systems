import unittest

from src.solar_power import calculate_solar_power, calculate_solar_energy


class TestSolarPower(unittest.TestCase):
    def test_nominal_power(self):
        self.assertAlmostEqual(
            calculate_solar_power(0.02, 1361, 0.30),
            8.166,
        )

    def test_degradation_reduces_power(self):
        self.assertAlmostEqual(
            calculate_solar_power(0.02, 1000, 0.25, degradation=0.10),
            4.5,
        )

    def test_energy(self):
        self.assertAlmostEqual(calculate_solar_energy(5.0, 4.0), 20.0)

    def test_negative_area_raises(self):
        with self.assertRaises(ValueError):
            calculate_solar_power(-0.1, 1000, 0.25)


if __name__ == "__main__":
    unittest.main()

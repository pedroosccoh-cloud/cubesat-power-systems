"""Simple educational solar-array power estimates for CubeSat studies.

All inputs are configurable and should be treated as illustrative assumptions,
not as specifications for any real spacecraft or mission.
"""


def calculate_solar_power(
    area_m2,
    irradiance_w_m2,
    efficiency,
    degradation=0.0,
):
    """Return estimated electrical power in watts.

    Args:
        area_m2: Total active solar-cell area in square metres (>= 0).
        irradiance_w_m2: Incident solar irradiance in W/m^2 (>= 0).
        efficiency: Conversion efficiency as a fraction in [0, 1].
        degradation: Fractional power loss in [0, 1].
    """
    if area_m2 < 0:
        raise ValueError("area_m2 cannot be negative")
    if irradiance_w_m2 < 0:
        raise ValueError("irradiance_w_m2 cannot be negative")
    if not 0 <= efficiency <= 1:
        raise ValueError("efficiency must be between 0 and 1")
    if not 0 <= degradation <= 1:
        raise ValueError("degradation must be between 0 and 1")

    return area_m2 * irradiance_w_m2 * efficiency * (1 - degradation)


def calculate_solar_energy(power_w, sunlight_hours):
    """Return generated electrical energy in watt-hours."""
    if power_w < 0:
        raise ValueError("power_w cannot be negative")
    if sunlight_hours < 0:
        raise ValueError("sunlight_hours cannot be negative")

    return power_w * sunlight_hours

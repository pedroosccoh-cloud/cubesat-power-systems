"""Basic battery state-of-charge calculations for educational studies.

This simplified model ignores voltage variation, temperature, aging,
rate-dependent capacity, and battery management system limits.
"""


def calculate_final_soc(
    initial_soc_percent,
    capacity_wh,
    energy_charged_wh=0.0,
    energy_used_wh=0.0,
    charge_efficiency=1.0,
):
    """Estimate final battery state of charge as a percentage.

    Charging efficiency is applied to incoming energy. The resulting state of
    charge is limited to [0, 100] percent for this simple bookkeeping model.
    """
    if not 0 <= initial_soc_percent <= 100:
        raise ValueError("initial_soc_percent must be between 0 and 100")
    if capacity_wh <= 0:
        raise ValueError("capacity_wh must be greater than zero")
    if energy_charged_wh < 0 or energy_used_wh < 0:
        raise ValueError("energy values cannot be negative")
    if not 0 <= charge_efficiency <= 1:
        raise ValueError("charge_efficiency must be between 0 and 1")

    initial_energy_wh = capacity_wh * initial_soc_percent / 100
    stored_charge_wh = energy_charged_wh * charge_efficiency
    final_energy_wh = initial_energy_wh + stored_charge_wh - energy_used_wh
    final_energy_wh = min(capacity_wh, max(0.0, final_energy_wh))

    return 100 * final_energy_wh / capacity_wh

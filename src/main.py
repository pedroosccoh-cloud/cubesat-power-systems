"""Interactive menu for the educational CubeSat power-system models."""

import math

from src.power_budget import calculate_total_power, calculate_total_energy
from src.solar_power import calculate_solar_power, calculate_solar_energy
from src.battery_model import calculate_final_soc


def read_number(prompt, minimum=0.0, maximum=None):
    """Read a finite number within the requested bounds."""
    while True:
        try:
            value = float(input(prompt))
            if not math.isfinite(value):
                print("Error: enter a finite number.")
                continue
            if value < minimum:
                print(f"Error: value must be at least {minimum}.")
                continue
            if maximum is not None and value > maximum:
                print(f"Error: value must be at most {maximum}.")
                continue
            return value
        except ValueError:
            print("Error: enter a valid number.")


def power_budget_menu():
    print("\n--- Power budget ---")
    count = int(read_number("Number of subsystems: ", minimum=1))
    subsystems = []
    for index in range(count):
        print(f"\nSubsystem {index + 1}")
        name = input("Name: ").strip()
        while not name:
            print("Name cannot be empty.")
            name = input("Name: ").strip()
        power = read_number("Power consumption (W): ")
        hours = read_number("Operating time in analysis period (h): ")
        subsystems.append({
            "name": name,
            "power_w": power,
            "operating_hours": hours,
        })

    print("\nResults")
    print(f"{'Subsystem':<24}{'Power (W)':>12}{'Time (h)':>12}{'Energy (Wh)':>14}")
    for item in subsystems:
        energy = item["power_w"] * item["operating_hours"]
        print(f"{item['name']:<24}{item['power_w']:>12.2f}{item['operating_hours']:>12.2f}{energy:>14.2f}")
    print(f"Total listed power: {calculate_total_power(subsystems):.2f} W")
    print(f"Total energy use:   {calculate_total_energy(subsystems):.2f} Wh")
    print("Note: total listed power assumes all listed subsystems operate simultaneously.")


def solar_menu():
    print("\n--- Solar-array estimate ---")
    area = read_number("Active solar-cell area (m^2): ")
    irradiance = read_number("Incident irradiance (W/m^2): ")
    efficiency = read_number("Cell efficiency (0-1, e.g. 0.30 for 30%): ", 0, 1)
    degradation = read_number("Assumed degradation (0-1, default 0): ", 0, 1)
    power = calculate_solar_power(area, irradiance, efficiency, degradation)
    hours = read_number("Sunlight duration (h): ")
    energy = calculate_solar_energy(power, hours)
    print(f"Estimated solar electrical power: {power:.3f} W")
    print(f"Estimated energy over sunlight interval: {energy:.3f} Wh")


def battery_menu():
    print("\n--- Battery state-of-charge estimate ---")
    initial_soc = read_number("Initial state of charge (%): ", 0, 100)
    capacity = read_number("Nominal battery capacity (Wh): ", minimum=0.000001)
    charged = read_number("Energy supplied for charging (Wh): ")
    used = read_number("Energy consumed (Wh): ")
    efficiency = read_number("Charging efficiency (0-1, e.g. 0.90 for 90%): ", 0, 1)
    final_soc = calculate_final_soc(
        initial_soc, capacity, energy_charged_wh=charged,
        energy_used_wh=used, charge_efficiency=efficiency,
    )
    print(f"Estimated final state of charge: {final_soc:.2f}%")


def main():
    """Display the interactive application menu until the user exits."""
    actions = {
        "1": power_budget_menu,
        "2": solar_menu,
        "3": battery_menu,
    }
    while True:
        print("\n" + "=" * 48)
        print("       CUBESAT POWER SYSTEMS TOOLKIT")
        print("=" * 48)
        print("1. Calculate subsystem power budget")
        print("2. Estimate solar-array power and energy")
        print("3. Estimate battery state of charge")
        print("0. Exit")
        choice = input("Select an option: ").strip()
        if choice == "0":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action is None:
            print("Invalid option. Choose 0, 1, 2, or 3.")
            continue
        try:
            action()
        except (EOFError, KeyboardInterrupt):
            print("\nInput cancelled.")
            break
        input("\nPress Enter to return to the main menu...")


if __name__ == "__main__":
    main()

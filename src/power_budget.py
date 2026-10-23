"""
CubeSat Power Budget Calculator

Interactive tool for estimating the power consumption
and energy usage of CubeSat subsystems.
"""


def read_positive_float(prompt):
    """Read a non-negative number from user input."""

    while True:
        try:
            value = float(input(prompt))

            if value < 0:
                print("Error: value cannot be negative.")
                continue

            return value

        except ValueError:
            print("Error: please enter a valid number.")


def read_positive_integer(prompt):
    """Read a positive integer from user input."""

    while True:
        try:
            value = int(input(prompt))

            if value <= 0:
                print("Error: enter an integer greater than zero.")
                continue

            return value

        except ValueError:
            print("Error: please enter a valid integer.")


def calculate_total_power(subsystems):
    """Calculate total power consumption in watts."""

    return sum(subsystem["power_w"] for subsystem in subsystems)


def calculate_total_energy(subsystems):
    """Calculate total energy consumption in watt-hours."""

    return sum(
        subsystem["power_w"] * subsystem["operating_hours"]
        for subsystem in subsystems
    )


def main():
    """Run the interactive CubeSat power budget calculator."""

    print("=" * 45)
    print("       CUBESAT POWER BUDGET CALCULATOR")
    print("=" * 45)

    number_of_subsystems = read_positive_integer(
        "\nHow many subsystems do you want to register? "
    )

    subsystems = []

    for i in range(number_of_subsystems):
        print(f"\nSubsystem {i + 1}")

        while True:
            name = input("Subsystem name: ").strip()

            if name:
                break

            print("Error: subsystem name cannot be empty.")

        power = read_positive_float("Power consumption (W): ")

        operating_hours = read_positive_float(
            "Operating time during the analysis period (h): "
        )

        subsystems.append({
            "name": name,
            "power_w": power,
            "operating_hours": operating_hours,
        })

    total_power = calculate_total_power(subsystems)
    total_energy = calculate_total_energy(subsystems)

    print("\n" + "=" * 65)
    print("                         RESULTS")
    print("=" * 65)

    print(
        f"{'Subsystem':<25}"
        f"{'Power (W)':>15}"
        f"{'Time (h)':>12}"
        f"{'Energy (Wh)':>13}"
    )

    print("-" * 65)

    for subsystem in subsystems:
        energy = (
            subsystem["power_w"] * subsystem["operating_hours"]
        )

        print(
            f"{subsystem['name']:<25}"
            f"{subsystem['power_w']:>15.2f}"
            f"{subsystem['operating_hours']:>12.2f}"
            f"{energy:>13.2f}"
        )

    print("-" * 65)
    print(f"{'TOTAL POWER':<25}{total_power:>15.2f} W")
    print(f"{'TOTAL ENERGY':<25}{total_energy:>15.2f} Wh")
    print("=" * 65)


if __name__ == "__main__":
    main()

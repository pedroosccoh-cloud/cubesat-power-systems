# CubeSat Power Systems

An educational engineering project for estimating and analyzing electrical power systems for CubeSat-class spacecraft.

The repository is being developed as a portfolio project. **All example values are illustrative and are not official specifications for any spacecraft or mission.**

## Current Features

- **Power budget:** calculate the sum of subsystem power ratings and estimate energy use from power and operating time.
- **Solar-array estimate:** estimate electrical output from active cell area, irradiance, conversion efficiency, and a configurable degradation factor.
- **Battery bookkeeping model:** estimate final state of charge from initial SOC, battery capacity, incoming energy, energy used, and charging efficiency.
- **Automated tests:** unit tests for the calculation functions, run by GitHub Actions.

## Repository Structure

```text
.
├── src/
│   ├── power_budget.py
│   ├── solar_power.py
│   └── battery_model.py
├── tests/
│   ├── test_power_budget.py
│   ├── test_solar_power.py
│   └── test_battery_model.py
└── .github/
    └── workflows/
        └── tests.yml
```

## Requirements

- Python 3.12 or a compatible recent Python 3 version.
- The current calculation modules and unit tests use only the Python standard library.

## Run the Interactive Toolkit

From the repository root, run:

```bash
python -m src.main
```

A menu lets you choose between three interactive tools:

1. **Power budget:** register subsystems, their power consumption, and operating time to calculate total listed power and energy use.
2. **Solar-array estimate:** enter active cell area, irradiance, conversion efficiency, degradation, and sunlight duration to estimate power and energy.
3. **Battery state of charge:** enter initial SOC, capacity, charging energy, energy consumed, and charging efficiency to estimate final SOC.

The original power-budget-only interface is also available with `python -m src.power_budget`. All inputs are illustrative assumptions, not real mission specifications.

## Run the Tests

From the repository root:

```bash
python -m unittest discover -s tests -v
```

## Model Equations

### Power budget

For subsystem (i), estimated energy is:

`E_i = P_i \\times t_i`

Total energy for the analysis period is:

`E_{total} = \\sum_i P_i t_i`

The current total-power function sums all entered subsystem ratings. This represents simultaneous total power only when those subsystems are assumed to operate at the same time.

### Solar-array output

`P_{solar} = A \\times G \\times \\eta \\times (1-d)`

where (A) is active cell area in m², (G) is incident irradiance in W/m², (eta) is conversion efficiency as a fraction, and (d) is the fractional degradation assumption.

Estimated energy over a sunlight interval is:

`E_{solar} = P_{solar} \\times t_{sun}`

This first-order estimate does not yet model cell temperature, incidence angle, shadowing, orbital geometry, or electrical losses outside the configured degradation factor.

### Battery state of charge

The simplified model uses:

`E_{final} = E_{initial} + \\eta_{charge} E_{charged} - E_{used}`

The stored energy is clamped to the range from zero to nominal capacity before converting it to a percentage SOC. This is a bookkeeping approximation, not a validated electrochemical or battery-management-system model.

## Scope and Limitations

- This is an educational model, not flight software or a spacecraft qualification tool.
- Results depend on input assumptions and should not be treated as mission-verified values.
- Orbital illumination, eclipse periods, pointing, temperature, cell degradation physics, battery discharge limits, and converter efficiencies are not yet modeled in detail.
- Future work can add operating modes, orbital sunlight/eclipse timelines, energy-balance plots, and more detailed battery constraints.

## Project Status

Under development. The goal is to build transparent, reusable, tested engineering models and document their assumptions as the project evolves.

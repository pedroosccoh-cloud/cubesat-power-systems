# CubeSat Power Systems

I built this project to explore a practical spacecraft engineering question: how much energy do the onboard systems use, and can the solar array and battery keep up?

The project is an educational calculator for CubeSat-style electrical power systems. It includes both a terminal menu and a small interactive dashboard, so you can change the assumptions and see how the estimates respond.

**Please note:** the numbers entered in examples are illustrative. This is a learning project, not a validated model for a real spacecraft or mission.

## What it can do right now

- **Estimate power and energy use:** enter subsystems, their power ratings, and how long they operate.
- **Estimate solar-array output:** use cell area, sunlight intensity, conversion efficiency, and an assumed degradation factor.
- **Track battery state of charge:** estimate how charging energy and energy use affect the battery's state of charge.
- **Explore the results:** the Streamlit dashboard includes energy-balance charts and a CSV download.
- **Run tests:** unit tests check the calculation functions, with GitHub Actions running the test suite.

## Project layout

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

## Getting started

You'll need Python 3.12 or a compatible recent Python 3 version. The calculation modules and unit tests use only the Python standard library.

### Open the interactive dashboard

From the repository root, install the dashboard dependencies and start the app:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

It opens in your browser. You can edit subsystem loads, change solar-array and battery inputs, inspect the energy-balance charts, and download a CSV summary. If you need help setting up Streamlit, see the [official installation guide](https://docs.streamlit.io/get-started/installation).

### Use the terminal menu

You can also run the project without the dashboard:

```bash
python -m src.main
```

The menu has three tools:

1. **Power budget:** enter subsystem power consumption and operating time to estimate power and energy use.
2. **Solar-array estimate:** enter active cell area, irradiance, efficiency, degradation, and sunlight duration.
3. **Battery state of charge:** enter initial state of charge, capacity, charging energy, energy consumed, and charging efficiency.

The original power-budget-only interface is still available with `python -m src.power_budget`.

### Run the tests

From the repository root:

```bash
python -m unittest discover -s tests -v
```

## How the estimates work

These are deliberately simple first-pass models. The goal is to make the assumptions visible and understand the basic energy balance before adding more realistic spacecraft behavior.

### Power budget

For subsystem *i*, estimated energy use is:

`E_i = P_i × t_i`

For all listed subsystems:

`E_total = Σ(P_i × t_i)`

The total-power function adds the power ratings entered. It represents simultaneous total power only if those subsystems are assumed to be on at the same time.

### Solar-array output

`P_solar = A × G × η × (1 - d)`

Here, `A` is active cell area in m², `G` is incident irradiance in W/m², `η` is conversion efficiency expressed as a fraction, and `d` is the assumed fractional degradation.

Estimated energy over a sunlight interval is:

`E_solar = P_solar × t_sun`

This estimate doesn't yet account for factors such as cell temperature, incidence angle, shadowing, orbital geometry, or electrical losses beyond the configured degradation factor.

### Battery state of charge

The simplified energy bookkeeping is:

`E_final = E_initial + η_charge × E_charged - E_used`

The stored energy is limited to the range between zero and nominal capacity before being converted to a state-of-charge percentage. This is a basic accounting model, not an electrochemical simulation or a validated battery-management model.

## Limitations and next steps

There's plenty left to improve. The current version doesn't model orbital sunlight and eclipse timelines, spacecraft pointing, temperature effects, detailed battery discharge limits, or converter efficiencies. Those would be useful next steps, along with operating modes and more detailed energy-balance analysis.

For now, the priority is to keep the calculations understandable, test the code, and be clear about what the model can—and can't—tell us.

## Status

This project is a work in progress. I'm using it to connect what I learn in aerospace engineering with programming, and to build up the model step by step as I learn more.

# CubeSat Power Systems

How do you know whether a small satellite can generate enough electricity to run its onboard systems?

That's the question I'm exploring with this project. I wanted to build something practical that connects programming with spacecraft engineering, so I put together a simple power-budget calculator for a CubeSat-style mission. You can use it from the terminal or through an interactive Streamlit dashboard.

This is an educational model, not a flight-ready tool. The example values are illustrative, and the calculations leave out several real mission effects.

## What you can try

- **Build a power budget:** add subsystems, enter their power ratings and operating times, and estimate their energy use.
- **Estimate solar power:** change the active cell area, sunlight intensity, efficiency, and assumed degradation.
- **Follow battery charge:** see how charging energy and energy consumption affect the estimated state of charge.
- **Explore the results:** use the dashboard charts and export a CSV summary.
- **Run the tests:** the calculation functions have unit tests, and GitHub Actions runs the test suite.

## Project structure

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

You'll need Python 3.12 or a compatible recent Python 3 version. The calculation modules and tests use only Python's standard library; the dashboard has additional dependencies.

### Run the dashboard

From the repository root, install the dependencies and launch Streamlit:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

The dashboard opens in your browser. From there, you can change subsystem loads, adjust the solar-array and battery inputs, look at the energy-balance charts, and download the results as a CSV file. If you need it, here's the [official Streamlit installation guide](https://docs.streamlit.io/get-started/installation).

### Run it in the terminal

If you prefer a command-line interface, start the menu with:

```bash
python -m src.main
```

It includes three options:

1. **Power budget** — estimate subsystem power and energy use from power ratings and operating times.
2. **Solar-array estimate** — estimate output from cell area, irradiance, efficiency, degradation, and sunlight duration.
3. **Battery state of charge** — estimate the effect of initial charge, capacity, charging energy, energy use, and charging efficiency.

You can also run the original power-budget tool directly:

```bash
python -m src.power_budget
```

### Run the tests

From the repository root:

```bash
python -m unittest discover -s tests -v
```

## The calculations behind it

I kept the first version deliberately simple. The idea is to make the energy balance easy to follow before trying to model the many details of an actual spacecraft.

### 1. Power budget

For a subsystem *i*, the estimated energy used is:

`E_i = P_i × t_i`

For all subsystems in the budget:

`E_total = Σ(P_i × t_i)`

The total-power function adds the power ratings you enter. That sum represents the spacecraft's simultaneous power demand only if the listed subsystems are operating at the same time.

### 2. Solar-array output

`P_solar = A × G × η × (1 - d)`

Where:
- `A` is the active solar-cell area in m².
- `G` is the incident irradiance in W/m².
- `η` is the conversion efficiency, entered as a fraction.
- `d` is the assumed fractional degradation.

For a given sunlight interval:

`E_solar = P_solar × t_sun`

This is a first estimate. The current model doesn't account for cell temperature, incidence angle, shadowing, orbital geometry, or electrical losses beyond the configured degradation factor.

### 3. Battery state of charge

The model uses a simple energy balance:

`E_final = E_initial + η_charge × E_charged - E_used`

Stored energy is kept between zero and the battery's nominal capacity, then converted into a state-of-charge percentage. This is energy bookkeeping—not an electrochemical simulation or a validated battery-management model.

## What it doesn't model yet

A real spacecraft power system has more going on than these calculations capture. For now, the model doesn't simulate orbital sunlight and eclipse periods, spacecraft pointing, temperature effects, detailed battery discharge limits, or power-converter efficiencies.

Those are possible directions for future improvements, along with operating modes and a more detailed energy-balance analysis. I want to build those features gradually and make sure I understand the assumptions behind them rather than add complexity just for the sake of it.

## Project status

This is a work in progress. I'm building it alongside my Aerospace Engineering studies at the National University of Engineering (UNI) in Peru, using it to practise Python and explore the kind of power-system questions that come up in spacecraft design.

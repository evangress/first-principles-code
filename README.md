# First Principles Code

A template Python project that **teaches engineers to solve real engineering
problems in Python** — and shows that the open-source scientific stack
(`numpy`, `scipy`, and friends) can replace expensive proprietary tools like
MATLAB and Maplesoft.

You get:

- **`main.py`** — a worked example that calculates displacement from
  acceleration and velocity three different ways (closed-form, numerical
  integration of constant acceleration, and numerical integration of a
  time-varying acceleration).
- **`library/`** — one well-documented class per engineering domain
  (dynamics, statics, thermo, fluids, materials, gears, electrical,
  mechatronics, modal/vibration, controls) plus a `Utility` class for files
  and dialogs.

Every method uses keyword-only arguments and carries a docstring, so the code
itself doubles as a reference you can read and learn from.

---

## Quick start

```bash
# 1. Install dependencies into a project virtual environment
uv sync

# 2. Run the displacement demo
uv run main.py
```

Expected output:

```
Displacement of an object after 3.0 s
================================================
  x0 = 0.0 m,  v0 = 5.0 m/s,  a = g = 9.81 m/s^2

  1. Analytical formula        :    59.1450 m
  2. scipy (constant a)        :    59.1450 m
  4. Dynamics library class    :    59.1450 m
     -> numerical vs exact err : 2.13e-14 m

  3. scipy (a = g + 2*sin(t))  :    64.8628 m
     (no simple closed form - this is why we integrate numerically)
```

---

## A short tutorial on `uv`

[`uv`](https://docs.astral.sh/uv/) is a fast, all-in-one Python package and
project manager (a modern replacement for `pip` + `venv` + `pip-tools`). It
reads `pyproject.toml`, manages a `.venv` for you, and pins exact versions in a
`uv.lock` file so your environment is reproducible.

### Install uv

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### The commands you'll actually use

| Command | What it does |
| --- | --- |
| `uv sync` | Create/update `.venv` to match `pyproject.toml` + `uv.lock` |
| `uv run main.py` | Run a script inside the project environment (auto-syncs first) |
| `uv run python` | Open a Python REPL with the project's packages available |
| `uv add scipy` | Add a dependency (updates `pyproject.toml` and the lockfile) |
| `uv add --dev pytest` | Add a *development-only* dependency (e.g. a test runner) |
| `uv remove scipy` | Remove a dependency |
| `uv lock` | Re-resolve and rewrite `uv.lock` without installing |
| `uv python install 3.14` | Install a specific Python version |

The golden rule: **prefix anything that needs your packages with `uv run`**.
You never have to manually `activate` a virtual environment.

### Typical workflow

```bash
git clone <this-repo>
cd first-principles-code
uv sync                 # one-time setup
uv run main.py          # run the demo
uv add matplotlib       # pull in a new library when you need it
uv run python           # experiment interactively
```

---

## Using the library

Import a class, create an instance, and call its methods with **named
arguments** (this is the project's house style — calls read like sentences):

```python
from library.dynamics import Dynamics
from library.thermo import Thermo

dyn = Dynamics()
distance = dyn.displacement_constant_acceleration(
    initial_position=0.0,
    initial_velocity=5.0,
    acceleration=9.81,
    time=3.0,
)  # -> 59.145 m

thermo = Thermo()
efficiency = thermo.carnot_efficiency(hot_temperature=800, cold_temperature=300)
# -> 0.625  (the best a heat engine between these temperatures could ever do)
```

You can also import everything at once:

```python
from library import Dynamics, Statics, Fluids, Controls
```

### Creating and calling objects from lists and dictionaries

A common pattern: build several objects, store them in a container, then loop
over them. This is how you scale from one calculation to a whole study.

```python
from library.dynamics import Dynamics

dyn = Dynamics()

# --- A list of scenarios (each scenario is a dict of keyword arguments) ---
launches = [
    {"speed": 20, "angle_deg": 30},
    {"speed": 20, "angle_deg": 45},
    {"speed": 20, "angle_deg": 60},
]

# The ** operator unpacks a dict straight into keyword arguments.
for case in launches:
    distance = dyn.projectile_range(**case)
    print(f"{case['angle_deg']:>3}deg -> {distance:6.2f} m")

# --- A dictionary that maps a name to a configured object/result ---
materials = {
    "steel":    200e9,   # Young's modulus [Pa]
    "aluminum":  69e9,
    "titanium": 114e9,
}
for name, modulus in materials.items():
    print(f"{name:>9}: E = {modulus/1e9:.0f} GPa")
```

### Conditional flow control and loops

```python
from library.fluids import Fluids

fluids = Fluids()
re = fluids.reynolds_number(density=1000, velocity=2, length=0.05, viscosity=1e-3)

# if / elif / else: classify the flow regime
if re < 2300:
    regime = "laminar"
elif re < 4000:
    regime = "transitional"
else:
    regime = "turbulent"
print(f"Re = {re:.0f} -> {regime}")

# while loop: increase velocity until the flow turns turbulent
velocity = 0.01
while fluids.reynolds_number(density=1000, velocity=velocity,
                             length=0.05, viscosity=1e-3) < 4000:
    velocity += 0.01
print(f"Flow becomes turbulent at about {velocity:.2f} m/s")
```

### Lambda functions

A `lambda` is a small, unnamed function written inline — handy for quick math
and for telling other functions *how* to behave (sorting, mapping, filtering).

```python
# 1. A throwaway formula you can call like any function
kinetic_energy = lambda mass, velocity: 0.5 * mass * velocity ** 2
print(kinetic_energy(2.0, 3.0))          # -> 9.0

# 2. As a sort key: order parts by stress, highest first
parts = [("bracket", 120e6), ("pin", 240e6), ("plate", 80e6)]
parts.sort(key=lambda part: part[1], reverse=True)

# 3. With map/filter: convert a list of Celsius temps to Kelvin
celsius = [0, 25, 100]
kelvin = list(map(lambda c: c + 273.15, celsius))   # [273.15, 298.15, 373.15]
```

---

## Python packages for science, engineering & data work

| Package | Use it for |
| --- | --- |
| [NumPy](https://numpy.org/) | Fast N-dimensional arrays and vectorised math — the foundation of everything below |
| [SciPy](https://scipy.org/) | Integration, optimization, linear algebra, signal processing, statistics |
| [Matplotlib](https://matplotlib.org/) | Plotting and figures (the MATLAB-style `pyplot` interface) |
| [pandas](https://pandas.pydata.org/) | Tabular data, time series, CSV/Excel I/O |
| [SymPy](https://www.sympy.org/) | Symbolic math / computer algebra (a free Maple/Mathematica) |
| [Plotly](https://plotly.com/python/) | Interactive, web-ready charts and dashboards |
| [Seaborn](https://seaborn.pydata.org/) | Statistical plotting built on Matplotlib |
| [scikit-learn](https://scikit-learn.org/) | Classic machine learning (regression, clustering, classification) |
| [Jupyter](https://jupyter.org/) | Notebooks that mix code, math, plots, and prose |
| [Pint](https://pint.readthedocs.io/) | Physical units and automatic unit conversion |
| [CoolProp](http://www.coolprop.org/) | Thermophysical fluid properties for thermo/HVAC work |
| [control](https://python-control.readthedocs.io/) | Control-systems design (a free Control System Toolbox) |
| [CadQuery](https://cadquery.readthedocs.io/) | Parametric 3D CAD modelling in Python |
| [pytest](https://docs.pytest.org/) | Testing framework to verify your calculations stay correct |

Add any of them with `uv add <package>`.

---

## Learning resources

**Python fundamentals**
- [The Official Python Tutorial](https://docs.python.org/3/tutorial/)
- [Real Python](https://realpython.com/) — practical, well-edited tutorials
- [Automate the Boring Stuff with Python](https://automatetheboringstuff.com/) (free online)

**Scientific & numerical Python**
- [SciPy Lecture Notes](https://scipy-lectures.org/) — a full course in the scientific stack
- [NumPy: the absolute basics for beginners](https://numpy.org/doc/stable/user/absolute_beginners.html)
- [Python Numerical Methods (UC Berkeley)](https://pythonnumericalmethods.berkeley.edu/) — free online textbook
- [Nature: A guide to NumPy](https://www.nature.com/articles/s41586-020-2649-2)

**Engineering & for MATLAB users**
- [NumPy for MATLAB users](https://numpy.org/doc/stable/user/numpy-for-matlab-users.html) — translation cheat sheet
- [python-control Library docs](https://python-control.readthedocs.io/)
- [Engineering with Python](https://www.engineeringwithpython.com/)

**Tooling**
- [uv documentation](https://docs.astral.sh/uv/)
- [Real Python: Python Virtual Environments](https://realpython.com/python-virtual-environments-a-primer/)

---

## Project layout

```
first-principles-code/
├── main.py              # displacement demo (start here)
├── gui.py               # MATLAB-style console GUI (uv run gui.py)
├── library/             # one class per engineering domain
│   ├── __init__.py      # re-exports every class
│   ├── utility.py       # JSON/CSV/file-picker helpers
│   ├── dynamics.py
│   ├── statics.py
│   ├── modal.py
│   ├── thermo.py
│   ├── fluids.py
│   ├── material.py
│   ├── gear.py
│   ├── electrical.py
│   ├── mechatronics.py
│   └── controls.py
├── pyproject.toml       # project metadata & dependencies
├── SPEC.md              # full project design spec
└── README.md            # you are here
```

## The console GUI

`gui.py` is a small tkinter app that mimics the MATLAB/Maplesoft command
window. Launch it with:

```bash
uv run gui.py
```

- Type a Python expression in the command box and press **Enter** (or **Run**).
  The result prints to the **Session log** and is recorded in the **Workspace**
  table — just like MATLAB's `ans`/workspace.
- The interpreter comes preloaded with `math`, `numpy as np`, and a ready
  instance of every library class (`dyn`, `statics`, `thermo`, `fluids`, …), so
  you can compute immediately:
  `dyn.projectile_range(speed=20, angle_deg=45)`.
- **Open Script** loads a `.py` file into the command box; **Run Script** runs
  the whole box at once.
- **Export CSV** / **Export JSON** save every recorded result to disk (via
  `library.Utility`).

> The GUI needs a graphical display. The evaluation engine (the `Session`
> class) is separated from the Tk widgets, so it can be imported and scripted
> without a window.

---

## Conventions for contributors

- Pass arguments **by keyword** (`acceleration=9.81`, not `9.81`). Methods use
  keyword-only signatures (`def method(self, *, ...)`) to enforce this.
- Every class and method gets a **docstring** with parameter units.
- Comment the **why** of non-obvious math, not just the what.
- Keep one engineering domain per file, one class per file.

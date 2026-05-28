# First Principles Code — Project Spec

A Github repo that provides a template Python script and class library that functionally teaches engineers to use the Python programming techniques and empowers them to solve real world engineering problems with the Python programming language.

## Concepts

### main.py
The primary script with some basic imports for math and scipy. It should demonstrate how to calculate displacement from a known acceleration and velocity as a function of time.

### ./library
A direcotry that will contain all classes.

Initial class list:
- utility.py
  - "class utility():" a class that contains utility methods, like converting json files to dictionaries, or opening a file picker to choose a file location.
- dynamics.py
  - a class for dynamics methods
- statics.py
  - a class for common statics calculations
- thermo.py
  - a class for themodynamics calculations
- fluids.py
  - a class for fluid dynamics calculations
- material.py
  - a class for material science and strength of materials calculations
- gear.py
  - a class for common gear, gear pair, and powertrain calculations
- electrical.py
  - a class for electrical engineering calculations
- mechatronics.py
  - a class for mechatronics calculations: ball screws, servo motors, etc..
- modal.py
  - a class for classical vibration and modal calculations
- controls.py
  - a class for P, PD, PID, and other control technology calculations
- "please suggest other classes"

## Convntions
- Use kwargs** to teach verbose variable passing
- Always add docstrings to classes and methods to demonstrate how to document code
- Add comments explaining each method and significant portions of the code
- Add a README.md file that explains how to leverage the power of this template
  - Add a table of python packages that would benefit science, engineering, and data science
  - Provide a list of links to reference material and learning resources
- Provide an example of how to create and call objects from lists and dictionaries
- Provide examples of conditional program flow control and loop structures
- Provide a few examples of how to create and use lambda functions
- Provide a simple tkinter GUI script that can run scripts and record and export results that provides an interface that provides similar functionality to that of MATLAB or Maplesoft

## Python concepts to teach (roadmap)

Beyond the core library, these are the Python concepts that most help an
engineer move from "a single formula" to "a real workflow they can compute,
visualize, and trust." Listed roughly in order of payoff. Items marked
**(done)** are already in the project.

1. **NumPy array thinking / vectorization** — operating on whole arrays instead
   of looping element by element; broadcasting and boolean masking
   (`stress[stress > yield_strength]`). The biggest shift coming from MATLAB.
2. **Plotting with matplotlib (done)** — turning result arrays into figures
   (`main.py` plots position/velocity/acceleration vs time and saves a PNG).
   The figure is usually the real engineering deliverable.
3. **The wider SciPy toolbox** — root finding (`optimize.brentq`, `fsolve`),
   curve fitting to test data (`optimize.curve_fit`), general ODE simulation
   (`integrate.solve_ivp`, the principled version of the Euler loop in
   `controls.py`), and interpolation (`scipy.interpolate`).
4. **Physical units with Pint** — quantities that carry units, auto-convert,
   and raise if you add metres to seconds. Guards against unit-mismatch errors
   that plain floats cannot catch.
5. **Type hints and dataclasses** — annotate units/types on signatures so the
   editor catches mistakes; model entities (e.g. `Beam(length, area, modulus)`)
   as `@dataclass` objects instead of passing loose floats.
6. **Error handling and input validation** — `raise ValueError(...)` for bad
   inputs (negative area, etc.) and `try/except` to fail loudly and clearly.
7. **Testing with pytest (done)** — pure-function methods checked against known
   textbook answers (`tests/`), so the library can be refactored fearlessly.
8. **Data handling with pandas** — reading sensor logs / material-property
   tables from CSV/Excel, filtering, grouping, and exporting results.

Smaller but useful: `@property` / `@staticmethod` for richer class design,
list/dict comprehensions, `enum` for fixed choices (e.g. material types),
context managers (`with`) for resources, and f-string formatting for reports.

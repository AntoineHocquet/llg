# 🆀 LLG Simulation App

This project is a **modular scientific simulation pipeline** for solving the **Landau–Lifshitz–Gilbert (LLG) equation** on a 2D disk using [FreeFEM++](https://freefem.org/), powered by Docker and a Python CLI.

The baseline code was adapted from the author's **PhD simulation framework** for solving the stochastic Landau-Lifshitz-Gilbert equation with Gaussian noise. The finite element formulation follows the logic of the **Crank–Nicolson scheme with projection step** as introduced in:

> F. Alouges & A. De Bouard, *A semi-discrete scheme for the stochastic LLG equation*, **Stochastic PDE: Analysis and Computations**, 2014. \[https://link.springer.com/article/10.1007/s40072-014-0033-7]

and, see Chapter 5 in my PhD thesis:

> The Landau-Lifshitz-Gilbert equation driven by Gaussian noise: \[https://pastel.hal.science/tel-01265433v2]

---

## 📆 Features

* 📜 Define all physical and numerical parameters in a single `params.json`
* 🐳 Run simulations inside a Docker container for full reproducibility
* 🧯 Visualize magnetization fields in 3D (static + animated GIF)
* ⚙️ Easily tweak parameters via command line (`--set key=value`)
* 🧪 Clean, testable Python codebase with `venv` and editable install

---

## 🚀 Installation

Clone the repo and set up a virtual environment:

```bash
git clone https://github.com/AntoineHocquet/llg.git
cd llg
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

Make sure [Docker](https://www.docker.com/) is installed and running.

---

## 🥪 Usage

### ⚙️ Run a full pipeline:

```bash
simulate --sim --viz --gif
```

### 🧮 Run only the simulation:

```bash
simulate --sim
```

### 🎨 Generate static plot:

```bash
simulate --viz
```

### 🔀 Generate animated GIF:

```bash
simulate --gif
```

### ⚙️ Override parameters at runtime:

```bash
simulate --sim --set T=2.0 damping=0.1 arrow_length=0.05
```

---

## ⚙️ Parameters (`params.json`)

You can configure everything via the JSON file **or override it using `--set`**.

| Parameter         | Type   | Description                                             |
| ----------------- | ------ | ------------------------------------------------------- |
| `T`               | float  | Final simulation time                                   |
| `dt`              | float  | Time step size                                          |
| `mesh_resolution` | int    | Mesh resolution of the disk                             |
| `damping`         | float  | Damping coefficient in the LLG equation                 |
| `noise_amplitude` | float  | Strength of stochastic perturbation (optional, if used) |
| `arrow_length`    | float  | Length of quiver arrows in visualization                |
| `arrow_width`     | float  | Line width of the quiver arrows                         |
| `elev`            | float  | 3D elevation angle of the camera (in degrees)           |
| `azim`            | float  | Azimuthal angle of the camera                           |
| `fps`             | int    | Frames per second for GIF generation                    |
| `init_u0`         | string | FreeFEM expression for u₀ initial condition             |
| `init_u1`         | string | FreeFEM expression for u₁ initial condition             |
| `init_u2`         | string | FreeFEM expression for u₂ initial condition             |

Example `params.json`:

```json
{
  "T": 1.0,
  "dt": 0.05,
  "mesh_resolution": 50,
  "damping": 0.1,
  "arrow_length": 0.04,
  "arrow_width": 0.5,
  "elev": 30,
  "azim": 135,
  "fps": 10,
  "init_u0": "sin(pi * r) * cos(theta)",
  "init_u1": "sin(pi * r) * sin(theta)",
  "init_u2": "cos(pi * r)"
}
```
Here theta, and r are the usual polar coordinates of the unit disk in R^2.
One may also use cartesian coordinates x,y, x^2+y^2<=1.
Make sure that the provided vector field lives in the unit sphere (as in the physical model), otherwise an error might occur.

---

## 🖼️ Outputs

All outputs are saved to the `data/` folder by default.

### 🔹 Static frame:

![Static Plot](data/llg_final.png)

### ♻️ Animated GIF:

![GIF](data/llg_equation_simulation.gif)

---

## 🧰 Requirements

* Python 3.8+
* Docker
* matplotlib, pandas (installed via `pip install -e .`)

---

## 🙌 Credits

This project uses:

* FreeFEM++ for FEM-based PDE solving
* Docker for isolated environments
* matplotlib for 3D visualizations

---

## 🔄 Coming Soon

* `--preset` profiles for switching between initial conditions
* MP4 rendering via `ffmpeg`
* Parameter sweep support (`--grid T=[0.5,1.0,1.5]`)

---

## 🔀 License

MIT License

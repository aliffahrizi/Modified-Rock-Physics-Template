# Modified Rock Physics Template

Calibration of a modified rock-physics template against Well_2 log data, linking measured elastic and petrophysical properties to mineral composition, porosity, and fluid saturation.

## Overview

This project builds a rock-physics workflow that:

1. Derives elastic and petrophysical attributes (AI, shear modulus, Vp/Vs, fluid/quartz fractions) from raw well-log data.
2. Calibrates matrix density and P-wave velocity end members (quartz, shale) using multi-linear regression.
3. Cross-checks those regression-derived end members against independently computed mineral-physics values (moduli-based), and resolves the divergence between them (see *Important Note* in the notebook).
4. Builds reference velocity/density trends with a modified Wyllie Time-Average equation across reservoir shale-volume scenarios.
5. Fits a modified Fawad-Mondol / Pranatikta rock-physics template via parameter search to estimate fluid saturation, and compares the fitted response against observed elastic behavior.

The end goal is a calibrated template that predicts elastic response from porosity, lithology, and fluid state — and can be checked against the observed well log as a validation step.

This workflow is the implementation behind the published paper:

> Fahrizi, M. A., & Winardhi, S. (2026). *Multilinear Regression–Based Rock Physics Template Modeling for Sandstone Reservoir Characterization.* Scientific Contribution in Oil and Gas (SCOG). [https://doi.org/10.29017/scog.v49i1.2014](https://doi.org/10.29017/scog.v49i1.2014)

**Note:** this repository demonstrates the modeling workflow using the public Well 2 dataset (see Dataset section below) for reproducibility. The published paper's results were generated using proprietary field data (the "MAF" field, Gabus formation) that cannot be shared publicly. The methodology and code here are the same, but numerical outputs will differ from the paper.

## Project Structure

```
.
├── main.ipynb          # Full workflow: data loading → calibration → saturation modeling
├── utils.py             # Rock-physics equations actually used by main.ipynb
├── plot_utils.py         # Shared plotting helpers (grid style, cross-plots, depth-track comparisons)
├── requirements.txt       # Pinned dependencies
├── Data/
│   └── qsiwell2.csv     # Well-log input (see Data section below)
└── README.md
```

## Requirements

See `requirements.txt` for pinned versions. Install with:

```bash
pip install -r requirements.txt
```

## Dataset

This repository demonstrates the workflow using the **Well 2** example dataset from *Quantitative Seismic Interpretation* by Avseth, Mukerji, and Mavko.

The processed dataset (`qsiwell2.csv`) is derived from the original Stanford University educational materials and follows the cleaned version prepared for the SEG Tutorial **Seismic Petrophysics I**.

### Data Sources

* **Stanford Rock Physics & Geofluids Project (SRGP)** — *Quantitative Seismic Interpretation*
  https://srgp.stanford.edu/publications/books/quantitative-seismic-interpretation

* **SEG Tutorial: Seismic Petrophysics I**
  https://github.com/seg/tutorials/tree/master/1504_Seismic_petrophysics_1

### Attribution

The well-log dataset used in this repository is not an original contribution of this project. Credit belongs to the original authors of the *Quantitative Seismic Interpretation* educational dataset and the contributors of the SEG Tutorial who prepared the cleaned `qsiwell2.csv` version.

This repository focuses on the implementation of the **Modified Rock Physics Template (RPT)** workflow and the associated Python code.

> This repo's MIT license (see below) covers the code in this repository (`main.ipynb`, `utils.py`, `plot_utils.py`) only. It does not extend to `Data/qsiwell2.csv`, which remains subject to the terms of its original source (Stanford SRGP / SEG Tutorial), as credited above.

## Workflow

| Stage | What it does |
|---|---|
| **Data loading & derived properties** | Loads the well table, derives AI, shear modulus, Vp/Vs, SFL, VQTZ, and filters to the target depth interval |
| **Density model calibration** | Multi-linear regression to estimate quartz/shale matrix density end members (`rho_qtz`, `rho_shale`) |
| **Velocity model calibration** | Multi-linear regression + fluid-velocity search to estimate quartz/shale Vp end members and fluid Vp |
| **Shale-volume comparison** | Cross-checks logged VSH against a velocity-derived VSH estimate (`VSH_NEW`) |
| **Wyllie template & reservoir scenarios** | Builds reference Vp/AI/Vp-Vs trends across porosity and shale-volume scenarios; defines the reservoir as VSH < 0.5, using VSH = 0.25 as the characteristic reservoir value |
| **Fluid-saturation model (Pranatikta / modified Fawad-Mondol)** | Parameter search to fit a saturation response against the well's SW log, and compares fitted AI–Vp/Vs response to observed data |
| **End-member validation** | Compares regression-derived vs. moduli-derived Vp quartz/shale end members and shows both converge near the reservoir's characteristic VSH (see *Important Note* in the notebook) |

## utils.py

`utils.py` is trimmed to the three rock-physics functions `main.ipynb` actually calls: `FluidSaturation`, `porosityKrishna`, and `wyllie_with_vsh`. It's a pared-down copy of a broader thesis codebase — the rest of that module (alternate VSH estimators, quantile matching, elastic-modulus mixing rules, etc.) isn't needed here and was left out for clarity. If a future notebook cell needs one of those, pull it back in from the thesis repo rather than re-adding the whole file.

## Usage

1. Place your well-log CSV in `Data/` (matching the schema used by `qsiwell2.csv`: DEPTH, VP, VS, RHO, PHI, NPHI, SW, VSH).
2. Install dependencies from `requirements.txt`.
3. Open `main.ipynb` and run cells top to bottom — the workflow is sequential; later stages depend on variables calibrated earlier (matrix density, Vp end members, etc.).
4. Adjust the depth filter, shale-volume thresholds, and fluid/mineral assumptions in the marked cells to fit a different well or interval.

## Known Limitations / Open Items

- Regression-derived quartz/shale Vp end members diverge from mineral-physics (moduli-derived) values at the pure end members (~20–25%), because Wyllie's Time-Average equation requires an *effective*, not physical, matrix velocity when calibrated against real, not-fully-consolidated well data. This is expected and explained in the notebook's *Important Note* section — the two approaches converge near the reservoir's characteristic VSH (~0.25), which is what the workflow actually uses downstream.
- One cell in the end-member validation section (the `porosityKrishna` diagnostic just before the *Important Note*) references `rho_matrix` before it is defined earlier in the notebook — this is a pre-existing cell-ordering issue and still needs to be resolved; the fix depends on which reservoir Vp/porosity values were intended there.
- `Vsh_from_VP` is defined twice (once unused in the original `utils.py`, now removed from there; once inline in the notebook) — see the `utils.py` note above.

## License

Code in this repository is released under the [MIT License](LICENSE). See the Dataset section above for the separate terms covering `Data/qsiwell2.csv`.

## Citation

If you reference this work, please cite:

```
Fahrizi, M. A., & Winardhi, S. (2026). Multilinear Regression–Based Rock Physics
Template Modeling for Sandstone Reservoir Characterization. Scientific
Contribution in Oil and Gas (SCOG). https://doi.org/10.29017/scog.v49i1.2014
```

## Author

Muhammad Alif Fahrizi
# NicheToolkit

Python tools for ecological niche analysis with ArcGIS Pro integration.

## Features

- **Warren's I Niche Overlap**: Calculate niche similarity between species distribution models
- **Agreement Maps**: Visualize where habitat suitability differs between scenarios
- **ArcGIS Pro Integration**: Full Python Toolbox with GUI
- **Robust Raster I/O**: Handles NoData/NaN values, preserves CRS
- **Well-tested**: Tested with real ecological data

## Installation

### For ArcGIS Pro Users

1. Download or clone this repository
2. In ArcGIS Pro Catalog Pane:
   - Right-click "Toolboxes" → "Add Toolbox"
   - Browse to `NicheToolkit.pyt`
   - Use the tools from the GUI!

### For Python Users
```bash
git clone https://github.com/RandomForestz/nichetoolkit.git
cd nichetoolkit
```

## Usage

### In ArcGIS Pro

**Warren's I Tool:**
- Input two raster datasets (e.g., species distribution models)
- Get niche overlap statistic (0-1 scale)

**Agreement Map Tool:**
- Input reference and comparison rasters
- Output shows where suitability is higher/lower/same
- Values: -1 (lower), 0 (same), 1 (higher)

### In Python
```python
from nichetoolkit import warrens_i, read_raster, niche_agreement_map

# Read rasters
current = read_raster("current_habitat.tif")
future = read_raster("future_habitat.tif")

# Calculate overlap
overlap = warrens_i(current, future)
print(f"Niche overlap: {overlap:.3f}")

# Create agreement map
agreement = niche_agreement_map(current, future, tolerance=0.05)
```

## What is Warren's I?

Warren's I is a metric for quantifying niche overlap between two probability distributions (e.g., species distribution models). 

**Formula:** `I = 1 - (1/2) × Σ|p1 - p2|`

- I = 1: Complete niche overlap
- I = 0: No niche overlap

## Use Cases

- **Climate Change Analysis**: Compare current vs. future habitat projections
- **Species Comparison**: Quantify niche similarity between species
- **Conservation Planning**: Identify areas of habitat gain/loss
- **Model Validation**: Compare different SDM algorithms

## Requirements

- ArcGIS Pro (with arcpy) OR
- Python 3.9+ with rasterio

## Development

Contributions welcome! Please open an issue or submit a pull request.

## References

Warren, D.L., Glor, R.E., & Turelli, M. (2008). Environmental niche equivalency versus conservatism: quantitative approaches to niche evolution. *Evolution*, 62(11), 2868-2883.

## Author

Josh Carrell, GISP

## License

MIT
```

---

## Add This to Your Resume

**Under Projects or Selected Experience:**
```
NicheToolkit - Open-Source Geospatial Analysis Tool
- Developed Python package implementing Warren's I niche overlap statistic for ecological analysis
- Built ArcGIS Pro Python Toolbox with GUI for non-technical users
- Engineered robust raster I/O with automatic CRS preservation and NoData handling
- Deployed production-ready tool tested with real species distribution models
- GitHub: github.com/RandomForestz/nichetoolkit


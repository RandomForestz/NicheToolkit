"""
NicheToolkit: Tools for ecological niche analysis.
"""
from .core import warrens_i, normalize_to_probability, niche_agreement_map
from .utils import read_raster, write_raster

__version__ = "0.1.0"
__all__ = [
    "warrens_i", 
    "normalize_to_probability",
    "niche_agreement_map",
    "read_raster",
    "write_raster"
]
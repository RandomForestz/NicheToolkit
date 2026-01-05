"""
Test Warren's I with real raster files.
"""
import sys
import os

# Add parent directory to path so we can import nichetoolkit
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nichetoolkit import warrens_i, read_raster


# file paths
raster1_path = "test_data/current.tif"  
raster2_path = "test_data/future.tif"  

print("Reading rasters...")
try:
    arr1 = read_raster(raster1_path)
    arr2 = read_raster(raster2_path)
    
    print(f"✓ Raster 1 shape: {arr1.shape}")
    print(f"✓ Raster 2 shape: {arr2.shape}")
    
    print("\nCalculating Warren's I...")
    overlap = warrens_i(arr1, arr2)
    
    print(f"\n✓ Warren's I: {overlap:.4f}")
    print(f"  ({overlap*100:.1f}% niche overlap)")
    
except Exception as e:
    print(f"✗ Error: {e}")
    print("\nMake sure:")
    print("1. Raster files exist in test_data/ folder")
    print("2. File paths in script match your actual filenames")
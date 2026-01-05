"""
Example: Create agreement map showing where suitability differs.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nichetoolkit import read_raster, niche_agreement_map, write_raster, warrens_i

# Your raster files
raster1_path = "test_data/current.tif"
raster2_path = "test_data/future.tif"
output_path = "test_data/agreement_map.tif"

print("Reading rasters...")
arr1 = read_raster(raster1_path)
arr2 = read_raster(raster2_path)

print(f"✓ Raster 1 shape: {arr1.shape}")
print(f"✓ Raster 2 shape: {arr2.shape}")

# Calculate overall overlap
print("\nCalculating Warren's I...")
overlap = warrens_i(arr1, arr2)
print(f"✓ Overall niche overlap: {overlap:.4f} ({overlap*100:.1f}%)")

# Create agreement map
print("\nCreating agreement map...")
agreement = niche_agreement_map(arr1, arr2, tolerance=0.05)

# Count pixels in each category
import numpy as np
lower = np.sum(agreement == -1)
same = np.sum(agreement == 0)
higher = np.sum(agreement == 1)
total = lower + same + higher

print(f"\nAgreement breakdown:")
print(f"  Lower suitability (-1):  {lower:6d} pixels ({lower/total*100:5.1f}%)")
print(f"  Same suitability (0):    {same:6d} pixels ({same/total*100:5.1f}%)")
print(f"  Higher suitability (1):  {higher:6d} pixels ({higher/total*100:5.1f}%)")

# Save result
print(f"\nSaving agreement map to: {output_path}")
write_raster(agreement, output_path, reference_raster=raster1_path)
print("✓ Done!")

print("\nInterpretation:")
if higher > lower:
    print(f"→ Raster 2 has MORE suitable habitat overall (+{(higher-lower)/total*100:.1f}%)")
elif lower > higher:
    print(f"→ Raster 2 has LESS suitable habitat overall (-{(lower-higher)/total*100:.1f}%)")
else:
    print("→ Rasters have similar amounts of suitable habitat")
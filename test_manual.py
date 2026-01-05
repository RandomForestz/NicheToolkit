"""
Quick manual test to see if Warren's I works.
"""
import numpy as np
from nichetoolkit.core import warrens_i

print("Testing Warren's I implementation...\n")

# Test 1: Identical distributions should give I = 1
print("Test 1: Identical distributions")
arr = np.random.rand(10, 10)
result = warrens_i(arr, arr)
print(f"Warren's I: {result:.4f}")
print(f"Expected: 1.0000")
print(f"Pass: {abs(result - 1.0) < 0.0001}\n")

# Test 2: Non-overlapping distributions should give I = 0
print("Test 2: No overlap")
arr1 = np.zeros((10, 10))
arr1[:5, :] = 1.0
arr2 = np.zeros((10, 10))
arr2[5:, :] = 1.0
result = warrens_i(arr1, arr2)
print(f"Warren's I: {result:.4f}")
print(f"Expected: 0.0000")
print(f"Pass: {abs(result - 0.0) < 0.0001}\n")

# Test 3: Random distributions
print("Test 3: Random distributions")
arr1 = np.random.rand(10, 10)
arr2 = np.random.rand(10, 10)
result = warrens_i(arr1, arr2)
print(f"Warren's I: {result:.4f}")
print(f"Expected: Between 0 and 1")
print(f"Pass: {0 < result < 1}\n")

print("All tests complete!")
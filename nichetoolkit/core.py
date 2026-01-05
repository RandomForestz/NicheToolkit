"""
Core functions for niche analysis.
"""
import numpy as np


def normalize_to_probability(arr):
    """
    Normalize array so it sums to 1 (probability distribution).
    
    Parameters
    ----------
    arr : numpy.ndarray
        Input array with values >= 0
        
    Returns
    -------
    numpy.ndarray
        Normalized array summing to 1
    """
    arr_sum = np.sum(arr)
    if arr_sum == 0:
        raise ValueError("Cannot normalize array with sum = 0")
    return arr / arr_sum


def warrens_i(arr1, arr2):
    """
    Calculate Warren's I niche overlap statistic.
    
    Warren's I measures niche overlap between two probability distributions.
    I = 1 means complete overlap, I = 0 means no overlap.
    
    Formula: I = 1 - 0.5 * sum(|p1 - p2|)
    
    Parameters
    ----------
    arr1 : numpy.ndarray
        First array (e.g., species distribution model)
    arr2 : numpy.ndarray
        Second array (must be same shape as arr1)
        
    Returns
    -------
    float
        Warren's I statistic, ranging from 0 (no overlap) to 1 (complete overlap)
        
    References
    ----------
    Warren, D.L., et al. (2008). Environmental niche equivalency versus 
    conservatism: quantitative approaches to niche evolution.
    """
    # Check inputs are same shape
    if arr1.shape != arr2.shape:
        raise ValueError(f"Arrays must be same shape. Got {arr1.shape} and {arr2.shape}")
    
    # Flatten arrays and remove NaN/NoData
    arr1_flat = arr1.flatten()
    arr2_flat = arr2.flatten()
    
    # Create mask for valid data
    valid_mask = ~(np.isnan(arr1_flat) | np.isnan(arr2_flat))
    
    # Get valid data only
    arr1_valid = arr1_flat[valid_mask]
    arr2_valid = arr2_flat[valid_mask]
    
    # Check we have data left
    if len(arr1_valid) == 0:
        raise ValueError("No valid data after removing NaN values")
    
    # Normalize to probability distributions
    p1 = normalize_to_probability(arr1_valid)
    p2 = normalize_to_probability(arr2_valid)
    
    # Calculate Warren's I
    i_statistic = 1 - 0.5 * np.sum(np.abs(p1 - p2))
    
    return i_statistic

def niche_agreement_map(arr1, arr2, tolerance=0.05):
    """
    Create a raster showing where niche suitability differs between two arrays.
    
    Useful for comparing:
    - Current vs future climate projections
    - Species A vs Species B habitat
    - Before vs after management
    
    Parameters
    ----------
    arr1 : numpy.ndarray
        First array (e.g., current conditions or species 1)
    arr2 : numpy.ndarray
        Second array (e.g., future conditions or species 2)
    tolerance : float, optional
        Threshold for considering values "the same" (default: 0.05)
        Values within ±tolerance are considered equal
        
    Returns
    -------
    numpy.ndarray
        Agreement raster with values:
        -1 = arr2 is lower (less suitable)
         0 = approximately equal (within tolerance)
         1 = arr2 is higher (more suitable)
         
    Examples
    --------
    >>> current = np.array([[0.8, 0.5], [0.3, 0.9]])
    >>> future = np.array([[0.7, 0.5], [0.6, 0.9]])
    >>> agreement = niche_agreement_map(current, future)
    >>> print(agreement)
    [[-1  0]
     [ 1  0]]
    """
    # Check inputs are same shape
    if arr1.shape != arr2.shape:
        raise ValueError(f"Arrays must be same shape. Got {arr1.shape} and {arr2.shape}")
    
    # Calculate difference
    diff = arr2 - arr1
    
    # Create agreement map
    agreement = np.zeros_like(diff, dtype=np.float32)
    
    # arr2 is significantly lower
    agreement[diff < -tolerance] = -1
    
    # arr2 is approximately equal (within tolerance)
    agreement[np.abs(diff) <= tolerance] = 0
    
    # arr2 is significantly higher
    agreement[diff > tolerance] = 1
    
    # Preserve NaN/NoData
    agreement[np.isnan(arr1) | np.isnan(arr2)] = np.nan
    
    return agreement
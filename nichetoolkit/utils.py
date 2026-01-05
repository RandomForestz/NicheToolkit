"""
Utility functions for raster I/O and processing.
"""
import numpy as np

# Try to import ArcPy (for ArcGIS Pro users)
try:
    import arcpy
    HAS_ARCPY = True
except ImportError:
    HAS_ARCPY = False

# Try to import rasterio (for general Python users)
try:
    import rasterio
    HAS_RASTERIO = True
except ImportError:
    HAS_RASTERIO = False


def write_raster(array, output_path, reference_raster=None):
    """
    Write numpy array to raster file, preserving CRS from reference.
    
    Parameters
    ----------
    array : numpy.ndarray
        2D array to save
    output_path : str
        Output file path
    reference_raster : str, optional
        Reference raster for spatial properties (projection, extent, etc.)
        
    Returns
    -------
    str
        Path to created raster
    """
    if not HAS_ARCPY or not reference_raster:
        raise RuntimeError("Need arcpy and a reference raster")
    
    # Get reference raster object
    ref = arcpy.Raster(reference_raster)
    desc = arcpy.Describe(ref)
    
    # METHOD 1: Try using arcpy.sa.Con with reference raster as template
    # This preserves CRS because it's derived from an existing raster
    try:
        import arcpy.sa as sa
        
        # Create a temporary array-based raster
        lower_left = arcpy.Point(desc.extent.XMin, desc.extent.YMin)
        temp_raster = arcpy.NumPyArrayToRaster(
            array,
            lower_left_corner=lower_left,
            x_cell_size=ref.meanCellWidth,
            y_cell_size=ref.meanCellHeight,
            value_to_nodata=np.nan
        )
        
        # Use Con to create output with reference raster's properties
        # This trick forces it to inherit CRS
        output_raster = sa.Con(temp_raster >= -9999, temp_raster)
        
        # Set spatial reference explicitly
        arcpy.env.outputCoordinateSystem = desc.spatialReference
        
        # Save
        output_raster.save(output_path)
        
        # Double-check and force if needed
        arcpy.management.DefineProjection(output_path, desc.spatialReference)
        
        return output_path
        
    except Exception as e:
        arcpy.AddWarning(f"Method 1 failed: {e}, trying alternate method...")
        
        # METHOD 2: Use Raster Calculator approach
        # Create constant raster, multiply by array values
        try:
            # Save to temp location first
            temp_path = arcpy.env.scratchGDB + r"\temp_array_raster"
            
            lower_left = arcpy.Point(desc.extent.XMin, desc.extent.YMin)
            temp_raster = arcpy.NumPyArrayToRaster(
                array,
                lower_left_corner=lower_left,
                x_cell_size=ref.meanCellWidth,
                y_cell_size=ref.meanCellHeight,
                value_to_nodata=np.nan
            )
            temp_raster.save(temp_path)
            
            # Now project it using the reference
            arcpy.management.ProjectRaster(
                in_raster=temp_path,
                out_raster=output_path,
                out_coor_system=desc.spatialReference,
                resampling_type="NEAREST",
                cell_size=ref.meanCellWidth
            )
            
            # Clean up
            arcpy.management.Delete(temp_path)
            
            return output_path
            
        except Exception as e2:
            raise RuntimeError(f"Both methods failed. Error: {e2}")
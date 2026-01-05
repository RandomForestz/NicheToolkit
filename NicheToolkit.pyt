"""
ArcGIS Pro Python Toolbox for Niche Analysis.
"""
import sys
import os

# Add the package directory to Python path
toolbox_dir = os.path.dirname(__file__)
if toolbox_dir not in sys.path:
    sys.path.insert(0, toolbox_dir)

import arcpy
import numpy as np
from nichetoolkit import warrens_i, niche_agreement_map, read_raster, write_raster


class Toolbox:
    def __init__(self):
        """Define the toolbox."""
        self.label = "Niche Analysis Toolkit"
        self.alias = "nichetoolkit"
        self.tools = [WarrensITool, AgreementMapTool]


class WarrensITool:
    def __init__(self):
        """Define the tool."""
        self.label = "Warren's I Niche Overlap"
        self.description = ("Calculate Warren's I niche overlap statistic "
                           "between two raster datasets")
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions."""
        # Input raster 1
        param0 = arcpy.Parameter(
            displayName="Input Raster 1",
            name="raster1",
            datatype="GPRasterLayer",
            parameterType="Required",
            direction="Input"
        )
        
        # Input raster 2
        param1 = arcpy.Parameter(
            displayName="Input Raster 2",
            name="raster2",
            datatype="GPRasterLayer",
            parameterType="Required",
            direction="Input"
        )
        
        params = [param0, param1]
        return params

    def execute(self, parameters, messages):
        """Execute the tool."""
        raster1_path = parameters[0].valueAsText
        raster2_path = parameters[1].valueAsText
        
        arcpy.AddMessage("Reading rasters...")
        arr1 = read_raster(raster1_path)
        arr2 = read_raster(raster2_path)
        
        arcpy.AddMessage(f"Raster 1 shape: {arr1.shape}")
        arcpy.AddMessage(f"Raster 2 shape: {arr2.shape}")
        
        arcpy.AddMessage("\nCalculating Warren's I...")
        overlap = warrens_i(arr1, arr2)
        
        arcpy.AddMessage(f"\n{'='*50}")
        arcpy.AddMessage(f"Warren's I: {overlap:.4f}")
        arcpy.AddMessage(f"Niche Overlap: {overlap*100:.1f}%")
        arcpy.AddMessage(f"{'='*50}")
        
        # Interpretation
        if overlap > 0.8:
            arcpy.AddMessage("\nInterpretation: Very high niche overlap")
        elif overlap > 0.6:
            arcpy.AddMessage("\nInterpretation: High niche overlap")
        elif overlap > 0.4:
            arcpy.AddMessage("\nInterpretation: Moderate niche overlap")
        elif overlap > 0.2:
            arcpy.AddMessage("\nInterpretation: Low niche overlap")
        else:
            arcpy.AddMessage("\nInterpretation: Very low niche overlap")
        
        return


class AgreementMapTool:
    def __init__(self):
        """Define the tool."""
        self.label = "Niche Agreement Map"
        self.description = ("Create a raster showing where suitability "
                           "differs between two rasters")
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions."""
        # Input raster 1
        param0 = arcpy.Parameter(
            displayName="Input Raster 1 (Reference)",
            name="raster1",
            datatype="GPRasterLayer",
            parameterType="Required",
            direction="Input"
        )
        
        # Input raster 2
        param1 = arcpy.Parameter(
            displayName="Input Raster 2 (Comparison)",
            name="raster2",
            datatype="GPRasterLayer",
            parameterType="Required",
            direction="Input"
        )
        
        # Tolerance
        param2 = arcpy.Parameter(
            displayName="Tolerance",
            name="tolerance",
            datatype="GPDouble",
            parameterType="Optional",
            direction="Input"
        )
        param2.value = 0.05
        
        # Output raster
        param3 = arcpy.Parameter(
            displayName="Output Agreement Raster",
            name="output_raster",
            datatype="DERasterDataset",
            parameterType="Required",
            direction="Output"
        )
        
        params = [param0, param1, param2, param3]
        return params

    def execute(self, parameters, messages):
        """Execute the tool."""
        raster1_path = parameters[0].valueAsText
        raster2_path = parameters[1].valueAsText
        tolerance = parameters[2].value
        output_path = parameters[3].valueAsText
        
        arcpy.AddMessage("Reading rasters...")
        arr1 = read_raster(raster1_path)
        arr2 = read_raster(raster2_path)
        
        arcpy.AddMessage(f"Raster 1 shape: {arr1.shape}")
        arcpy.AddMessage(f"Raster 2 shape: {arr2.shape}")
        
        # Calculate Warren's I first
        arcpy.AddMessage("\nCalculating Warren's I...")
        overlap = warrens_i(arr1, arr2)
        arcpy.AddMessage(f"Overall niche overlap: {overlap:.4f} ({overlap*100:.1f}%)")
        
        # Create agreement map
        arcpy.AddMessage(f"\nCreating agreement map (tolerance={tolerance})...")
        agreement = niche_agreement_map(arr1, arr2, tolerance=tolerance)
        
        # Statistics
        lower = np.sum(agreement == -1)
        same = np.sum(agreement == 0)
        higher = np.sum(agreement == 1)
        total = lower + same + higher
        
        arcpy.AddMessage(f"\nAgreement breakdown:")
        arcpy.AddMessage(f"  Lower suitability (-1):  {lower:6d} pixels ({lower/total*100:5.1f}%)")
        arcpy.AddMessage(f"  Same suitability (0):    {same:6d} pixels ({same/total*100:5.1f}%)")
        arcpy.AddMessage(f"  Higher suitability (1):  {higher:6d} pixels ({higher/total*100:5.1f}%)")
        
        # Save
        arcpy.AddMessage(f"\nSaving to: {output_path}")
        write_raster(agreement, output_path, reference_raster=raster1_path)
        
        arcpy.AddMessage("\n✓ Done!")
        
        # Interpretation
        arcpy.AddMessage("\nInterpretation:")
        if higher > lower:
            arcpy.AddMessage(f"→ Raster 2 has MORE suitable habitat (+{(higher-lower)/total*100:.1f}%)")
        elif lower > higher:
            arcpy.AddMessage(f"→ Raster 2 has LESS suitable habitat (-{(lower-higher)/total*100:.1f}%)")
        else:
            arcpy.AddMessage("→ Rasters have similar amounts of suitable habitat")
        
        return
    
def getParameterInfo(self):
    """Define parameter definitions."""
    # Input raster 1
    param0 = arcpy.Parameter(
        displayName="Input Raster 1 (Reference)",
        name="raster1",
        datatype="GPRasterLayer",
        parameterType="Required",
        direction="Input"
    )
    
    # Input raster 2
    param1 = arcpy.Parameter(
        displayName="Input Raster 2 (Comparison)",
        name="raster2",
        datatype="GPRasterLayer",
        parameterType="Required",
        direction="Input"
    )
    
    # Tolerance
    param2 = arcpy.Parameter(
        displayName="Tolerance",
        name="tolerance",
        datatype="GPDouble",
        parameterType="Optional",
        direction="Input"
    )
    param2.value = 0.05
    
    # Output raster
    param3 = arcpy.Parameter(
        displayName="Output Agreement Raster",
        name="output_raster",
        datatype="DERasterDataset",
        parameterType="Required",
        direction="Output"
    )
    
    # NEW: Output Coordinate System
    param4 = arcpy.Parameter(
        displayName="Output Coordinate System",
        name="output_crs",
        datatype="GPCoordinateSystem",
        parameterType="Optional",
        direction="Input"
    )
    param4.value = None  # Will default to input raster's CRS
    
    params = [param0, param1, param2, param3, param4]
    return params
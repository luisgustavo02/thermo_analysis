import numpy as np
import os

from importlib.resources import files
from PIL import Image

# Create a directory for data storage
def create_data_directory(path : str = "thermo_analysis"):
    """
    Create a data directory for thermo_analysis package if it doesn't exist.

    Parameters
        input:
        path (str): Path where to create the data directory.
    """
    
    # Verify path and create directory
    if path == "thermo_analysis":
        pathToCreate = os.getcwd() + "/" + path
    else:
        pathToCreate = path
    
    if not os.path.exists(pathToCreate):
        os.makedirs(pathToCreate)

# Loading image and creating color scales
def load_thermal_scale():
    """
    Parameters
        
        output:
        image (PIL.Image.Image): Array containing the thermal scale image.
    """
    # Locating the image file
    image_path = files("thermo_analysis.assets").joinpath("thermal_scale.png")

    with Image.open(image_path) as image:
        image = np.array(image)

        # Verify if image is loaded correctly
        if image is None:
            raise ValueError("Failed to load the thermal scale image.")

    return image

# Select and create a color scale
def function_scale(type : str = "standard"):
    """
    Parameters

        input:
        type (str): Type of scale to create.
            - "thermal" or "standard": Standard thermal scale.
            - "spectral" or "nipy.spectral": Nipy spectral scale.
    """
    if type == "thermal" or type == "standard":
        # Locating the image file within the package
        image_path = files("thermo_analysis.assets").joinpath("thermal_scale.png")
        
        # Reading the image and converting to array
        image = Image.open(image_path)
        image_array = np.array(image)

        # Separating the colors index manually
        # We use 11 colors in the thermal scale:
        # Dark purple, Light purple, Dark blue, Light blue, Dark green, Light green, Yellow, Orange, Dark Red, Light red, White
        map_group = np.zeros((11, 2), dtype=int)

        # Defining dark purple range
        map_group[0, 0] = 0
        map_group[0, 1] = 20

        # Defining light purple range
        map_group[1, 0] = 21
        map_group[1, 1] = 55

        # Defining dark blue range
        map_group[2, 0] = 56
        map_group[2, 1] = 85

        # Defining light blue range
        map_group[3, 0] = 86
        map_group[3, 1] = 120

        # Defining dark green range
        map_group[4, 0] = 121
        map_group[4, 1] = 145

        # Defining light green range
        map_group[5, 0] = 146
        map_group[5, 1] = 165

        # Defining yellow range
        map_group[6, 0] = 166
        map_group[6, 1] = 185

        # Defining orange range
        map_group[7, 0] = 186
        map_group[7, 1] = 205

        # Defining dark red range
        map_group[8, 0] = 206
        map_group[8, 1] = 240

        # Defining light red range
        map_group[9, 0] = 241
        map_group[9, 1] = 260

        # Defining white range
        map_group[10, 0] = 261
        map_group[10, 1] = map_group.shape[1] - 1
    
    elif type == "spectral" or type == "nipy.spectral":
        pass
    else:
        raise ValueError("The specified scale type is not recognized.")
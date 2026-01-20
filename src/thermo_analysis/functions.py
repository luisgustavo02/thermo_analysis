import matplotlib.pyplot as plt
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
def function_scale(type : str = "standard", num_colors : int = 256):
    """
    Parameters

        input:
        type (str): Type of scale to create.
            - "thermal" or "standard": Standard thermal scale.
            - "spectral" or "nipy.spectral": Nipy spectral scale.
        
        num_colors (int): Number of colors in the nipy.scale.
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
        first_map_group = np.zeros((11, 2), dtype=int)

        # Defining dark purple range
        first_map_group[0, 0] = 0
        first_map_group[0, 1] = 20

        # Defining light purple range
        first_map_group[1, 0] = 21
        first_map_group[1, 1] = 55

        # Defining dark blue range
        first_map_group[2, 0] = 56
        first_map_group[2, 1] = 85

        # Defining light blue range
        first_map_group[3, 0] = 86
        first_map_group[3, 1] = 120

        # Defining dark green range
        first_map_group[4, 0] = 121
        first_map_group[4, 1] = 145

        # Defining light green range
        first_map_group[5, 0] = 146
        first_map_group[5, 1] = 165

        # Defining yellow range
        first_map_group[6, 0] = 166
        first_map_group[6, 1] = 185

        # Defining orange range
        first_map_group[7, 0] = 186
        first_map_group[7, 1] = 205

        # Defining dark red range
        first_map_group[8, 0] = 206
        first_map_group[8, 1] = 240

        # Defining light red range
        first_map_group[9, 0] = 241
        first_map_group[9, 1] = 260

        # Defining white range
        first_map_group[10, 0] = 261
        first_map_group[10, 1] = map_group.shape[1] - 1

        # Creating the color map and map group
        map = np.empty((0, 3), dtype=float)
        map_group = []

        # Initial index for the map group
        index_group = 0

        for ii in range(first_map_group.shape[0]):
            # Getting the mean color and standard deviation for each color range
            target_colors = image_array[int(first_map_group[ii, 0]): int(first_map_group[ii, 1]) + 1]
            mean_color = np.mean(target_colors, axis=0)
            std_color = np.std(target_colors, axis=0)

            # Getting the colors in the standard deviation range
            for jj in range(target_colors.shape[0]-1, -1, -1):
                # Check the RGB values are within one standard deviation
                for kk in range(3):
                    if not (mean_color[kk] - std_color[kk] <= target_colors[jj, kk] <= mean_color[kk] + std_color[kk]):
                        target_colors = np.delete(target_colors, jj, axis=0)
                        break
            
            # Organizing the colors
            target_colors = np.unique(target_colors, axis=0)

            # Adding to the map group
            map_group.append([index_group, index_group + target_colors.shape[0]])
            index_group += target_colors.shape[0]

            # Adding to the map
            map = np.concatenate((map, target_colors), axis=0)
        
        # Creating gray map and gray map group
        gray_map_group = np.array(map_group).copy()
        gray_map_group[-1, -1] = 255

        gray_map = []

        for ii in range(gray_map_group.shape[0]-1, -1, -1):
            for jj in range(gray_map_group.shape[1]-1, -1, -1):
                if gray_map_group.shape != (ii+1, jj+1):
                    if ii == 0 and jj == 0:
                        gray_map_group[ii, jj] = 0
                    elif jj == 0:
                        gray_map_group[ii, jj] = round(gray_map_group[ii, jj]*255/105)
                    else:
                        gray_map_group[ii, jj] = gray_map_group[ii+1, jj-1] - 1
        
        for ii in range(gray_map_group.shape[0]):
            for jj in range(np.array(map_group).shape[ii, 0], np.array(map_group).shape[ii, 1] + 1):
                gray_map_group.append(round(gray_map[ii, 0] + (jj - np.array(map_group)[ii, 0]) * (gray_map[ii, 1] - gray_map[ii, 0]) / (np.array(map_group)[ii, 1] - np.array(map_group)[ii, 0])))
        
        gray_map[0] = 1

        return map.astype(np.uint8), np.array(map_group, dtype=int), np.array(gray_map, dtype=int), gray_map_group.astype(np.uint8)
    
    elif type == "spectral" or type == "nipy.spectral":
        # Generating nipy spectral scale
        map = (plt.cm.nipy_spectral(np.linspace(0, 1, num_colors))[:, :3] * 255).astype(np.uint8)

        # Separating the colors index manually
        # We use 13 colors in the thermal scale:
        # Very dark purple, Dark purple, Dark blue, Blue, Light blue, Aquamarine, Dark green, Light green, Yellow, Orange, Light red, Dark Red, White
        map_group = np.zeros((13, 2), dtype=float)

        # Defining very dark purple range
        map_group[0, 0] = 0
        map_group[0, 1] = 8

        # Defining dark purple range
        map_group[1, 0] = 9
        map_group[1, 1] = 28

        # Defining dark blue range
        map_group[2, 0] = 29
        map_group[2, 1] = 42

        # Defining blue range
        map_group[3, 0] = 43
        map_group[3, 1] = 62

        # Defining light blue range
        map_group[4, 0] = 63
        map_group[4, 1] = 79

        # Defining aquamarine range
        map_group[5, 0] = 80
        map_group[5, 1] = 103

        # Defining dark green range
        map_group[6, 0] = 104
        map_group[6, 1] = 124

        # Defining light green range
        map_group[7, 0] = 125
        map_group[7, 1] = 162

        # Defining yellow range
        map_group[8, 0] = 163
        map_group[8, 1] = 178

        # Defining orange range
        map_group[9, 0] = 179
        map_group[9, 1] = 204

        # Defining light red range
        map_group[10, 0] = 205
        map_group[10, 1] = 221

        # Defining dark red range
        map_group[11, 0] = 222
        map_group[11, 1] = 245

        # Defining white range
        map_group[12, 0] = 246
        map_group[12, 1] = num_colors - 1

    else:
        raise ValueError("The specified scale type is not recognized.")
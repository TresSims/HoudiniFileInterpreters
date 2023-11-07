import hou
import os
import numpy as np

try:
    import pynrrd
except:
    import sys
    import subprocess

    subprocess.check_call([sys.executable, "-m", "pip", "install", "pynrrd"])
    import nrrd


def read_nrrd(file):
    read_data, header = nrrd.read(file)

    res = header["sizes"]

    x_spacing = abs(max(header["space directions"][0], key=abs))
    y_spacing = abs(max(header["space directions"][1], key=abs))
    z_spacing = abs(max(header["space directions"][2], key=abs))

    center = header["space origin"]

    x_size = x_spacing * res[0]
    y_size = y_spacing * res[1]
    z_size = z_spacing * res[2]

    x_min = center[0] - (x_size / 2)
    y_min = center[1] - (y_size / 2)
    z_min = center[2] - (z_size / 2)

    x_max = center[0] + (x_size / 2)
    y_max = center[1] + (y_size / 2)
    z_max = center[2] + (z_size / 2)

    bounding_box = hou.BoundingBox(x_min, y_min, z_min, x_max, y_max, z_max)

    volume = geo.createVolume(int(res[0]), int(res[1]), int(res[2]), bounding_box)

    flattened_data = read_data.flatten("F")
    all_voxels = tuple(float(val) for val in flattened_data)
    volume.setAllVoxels(all_voxels)


node = hou.pwd()
digital_asset_node = node.parent()
geo = node.geometry()

file = digital_asset_node.parm("file").eval()

file_exists = True

if os.path.isfile(file):
    file_exists = True
elif file != "":
    raise hou.Error("Specified file does not exist")

if file_exists:
    read_nrrd(file)

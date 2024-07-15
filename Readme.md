# Custom File Readers

I created this repository to share some custom file readers I've made for houdini
during my tenure at DASH. Most of these have to do with reading medical or 3D printing
data sets. Hopefully some of you will find this useful!

Feel free to reach out with any questions about installation and use.

1. .3mf Reader
1. NRRD Reader

## .3mf Reader installation and use

This file reader will import meshes from .3mf formatted files, and load them into houidini.

Notably, this only supports meshes. It will not correctly load sliced files, or beam
lattice files.

It will load vertex color and UV coords appropriately, but material assignements and
texture information has to be set up separately.

### Installation
1. Copy the `sop_Read3mf.hda` from the `otls` folder to an `otls` folder on your
`$HOUDINI_PATH`
1. Install the [Lib3MF python library](https://github.com/3MFConsortium/lib3mf/releases)
to a `python3.7libs` folder on your `$HOUDINI_PATH`
1. Place your lib3mf shared object file (generally `.so` for linux or `.dll` for windows)
in an accessible location.

### Usage
1. Search for the `Read_3mf` sop node from the tab menu in your geometry node inside of
houdini.
1. Select your file using the file picker, and load your file.
1. Select your shared object location using the second file picker on the node

[Sample files](https://github.com/3MFConsortium/3mf-samples) taken from
[3MFConsortium](https://github.com/3MFConsortium) on GituHub


## NRRD Reader Installation and use

This file reader will import volumes using the nrrd format, and load them into Houdini.

You have the choice to use either Houdini's built in volumes or VDB's


### Installation

1. Copy the `sop_ReadNRRD.hda` from the `otls` folder to an `otls` folder on your
`$HOUDINI_PATH`
2. Install pynrrd to your houdini environment:

Option 1:  By default, the node will install the `pynrrd` package using pip from within the module itself. To do this:
   - create a new `Read_NRRD` node
   - Try to import a volume, it should faile with a message saying `nrrd` not found.
   - Restart Houdini, and everything should be working. 
  
  
Option 2. Alternatively you can install nrrd manually to your Houdinig Python environment.
   - run `hython -m pip install pynrrd` from a command line to use pip to install the `pynrrd` package

### Usage

1. Search for the `Read_NRRD` sop node from the tab menu in your geometry node inside of
houdini.
1. Select the type of volume you wish to create, VDB or Houdini Volume

(Note: many medical datasets use value ranges outside of what houdini represents by defauly,
if you have issues with the appearence of your volume after importing it, try adjusting
the value range)

[Sample files](https://www.slicer.org/wiki/SampleData) taken from 3D slicers sample dataset.

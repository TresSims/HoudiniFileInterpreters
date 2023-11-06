# Custom File Readers

I created this repository to share some custom file readers I've made for houdini
during my tenure at DASH. Most of these have to do with reading medical or 3D printing
data sets. Hopefully some of you will find this useful!

Feel free to reach out with any questions about installation and use.

1. .3mf Reader

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
houdini. Select your file using the file picker, and load your file.
1. Select your shared object location using the second file picker on the node

[Sample files](https://github.com/3MFConsortium/3mf-samples) taken from
[3MFConsortium](https://github.com/3MFConsortium) on GituHub

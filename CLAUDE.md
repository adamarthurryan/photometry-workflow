A command-line toolset and Python API for performing photometry workflows on sets of astronomical images.

Tools are provided for:

 - screening and selecting images
 - stacking a sequence of images
 - aperture photometry
 - estimating apparent magnitude 
 - differential photometry 

The language is Python, with the astropy/numpy/scipy ecosystem.

Each tool is associated with a terminal command, and also with a callable API function. The CLI handling code and program logic are separated.

Use the micromamba photometry enviroment for all Python tasks.

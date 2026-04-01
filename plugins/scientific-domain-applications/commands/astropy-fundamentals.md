---
description: Work with astronomical data using AstroPy for FITS files, coordinates, units, photometry, spectroscopy, and catalog matching
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# AstroPy Fundamentals

Work with astronomical data using AstroPy and related tools.

## Arguments

$ARGUMENTS — describe the task (e.g., "read this FITS file", "convert RA/Dec to Galactic", "do aperture photometry on image.fits")

## Workflow

1. **Understand the task** from the arguments:
   - FITS I/O (reading headers, images, tables)
   - Coordinate transformations (SkyCoord, frames, WCS)
   - Physical units and constants (astropy.units)
   - Astronomical time handling (astropy.time)
   - Photometry (photutils aperture/PSF)
   - Spectroscopy (specutils)
   - Catalog cross-matching

2. **Explore existing data and code:**
   - Check for FITS files, catalog files, existing analysis scripts
   - Identify data format and structure

3. **Implement** using AstroPy best practices:
   - Use Quantity objects for unit-aware calculations
   - Use SkyCoord for all coordinate handling
   - Proper WCS transformations for image data
   - Appropriate uncertainty handling

4. **Verify** results are physically reasonable.

5. **Report** results and any caveats about the data or analysis.

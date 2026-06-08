---
name: astropy-fundamentals
description: Use when the user asks about astronomical data, FITS files, celestial coordinates, photometry, spectroscopy, or references AstroPy. Work with astronomical data using AstroPy for FITS file I/O, coordinate transformations, physical units, precise time handling, catalog cross-matching, photutils photometry, and specutils spectroscopy.
metadata:
  references:
    - references/common-issues.md
    - references/examples.md
    - references/patterns.md
---

# Astropy Fundamentals

## Quick Reference Card

### Installation
```bash
pixi add astropy photutils specutils   # recommended
pip install astropy[all] photutils specutils
```

### Essential Imports & One-Liners
```python
import astropy.units as u
from astropy.io import fits
from astropy.coordinates import SkyCoord
from astropy.time import Time
from astropy.table import Table, QTable
from astropy.wcs import WCS

# Units
distance = 10 * u.parsec
freq = (5000 * u.angstrom).to(u.Hz, equivalencies=u.spectral())

# FITS I/O
with fits.open('image.fits') as hdul:
    data, header = hdul[0].data, hdul[0].header

# Coordinates
coord = SkyCoord(ra=10.625*u.degree, dec=41.2*u.degree, frame='icrs')
galactic = coord.galactic
sep = coord.separation(other_coord)

# Time
t = Time('2024-01-01T00:00:00', format='isot', scale='utc')
future = t + 1*u.day

# Tables
tbl = QTable([ra_col, dec_col, flux_col], names=['ra', 'dec', 'flux'])
filtered = tbl[tbl['flux'] > 100]

# WCS
wcs = WCS(header)
sky = wcs.pixel_to_world(x_pix, y_pix)   # returns SkyCoord
```

### Module Decision Tree
```
Working with astronomical data?
├─ FITS files             → astropy.io.fits
├─ Celestial coordinates  → astropy.coordinates (SkyCoord)
├─ Physical quantities    → astropy.units
├─ Astronomical time      → astropy.time
├─ Catalogs / tables      → astropy.table (QTable preserves units)
├─ Image pixel ↔ sky      → astropy.wcs
├─ Photometry             → photutils
└─ Spectroscopy           → specutils

Coordinate task?
├─ Transform frame        → SkyCoord.transform_to() or .galactic / .fk5
├─ Angular separation     → SkyCoord.separation()
├─ Cross-match catalogs   → SkyCoord.match_to_catalog_sky()
└─ Alt/Az (needs location + time) → AltAz frame

Unit task?
├─ Convert units          → quantity.to(target_unit)
├─ Wavelength ↔ frequency → u.spectral() equivalency
├─ Doppler shift          → u.doppler_radio() / u.doppler_optical()
└─ Magnitudes             → u.ABmag, quantity.physical
```

---

## Module Reference

Detailed patterns and code for each module are in `references/patterns.md`.

| Module | Key classes / functions | patterns.md section |
|--------|------------------------|---------------------|
| `astropy.io.fits` | `fits.open()`, `HDUList`, `PrimaryHDU`, `ImageHDU` | FITS Manipulation Patterns |
| `astropy.units` | `u.<unit>`, `.to()`, equivalencies | Units and Quantities Patterns |
| `astropy.coordinates` | `SkyCoord`, `EarthLocation`, `AltAz` | Coordinate Patterns |
| `astropy.time` | `Time`, `TimeDelta`, `TimeSeries` | Time Patterns |
| `astropy.table` | `Table`, `QTable`, `join()` | Table Patterns |
| `astropy.wcs` | `WCS`, `Cutout2D` | WCS Patterns |
| `photutils` | `DAOStarFinder`, `CircularAperture`, `aperture_photometry()` | Photometry Patterns |
| `specutils` | `Spectrum1D`, `fit_lines`, `fit_generic_continuum` | Spectroscopy Patterns |

Non-obvious gotchas per module (things Claude won't assume you know):
- **FITS**: `fits.open()` without `memmap=True` loads the whole file into RAM — always use `memmap=True` for files > a few hundred MB.
- **Units**: NumPy ufuncs generally preserve units, but third-party functions often strip them silently — check with `isinstance(result, u.Quantity)`.
- **Coordinates**: `AltAz` requires both `obstime=` and `location=` or it raises `CoordinateFrameError` at transform time, not at construction time.
- **Time**: `UTC` and `TAI` differ by the current leap-second count (~37 s as of 2024). Subtracting two `Time` objects in different scales gives a non-zero `TimeDelta`. Convert to the same scale first.
- **WCS**: `all_pix2world(x, y, 0)` uses Python 0-based convention; `all_pix2world(x, y, 1)` uses FITS 1-based convention. Mixing these off by one is a common silent error.
- **Photutils**: `aperture_photometry()` does not subtract background — always subtract background separately or use `CircularAnnulus` for local background.

See `references/common-issues.md` for full error messages and fixes.

---

## FITS Image Processing Workflow

A complete pipeline with explicit validation checkpoints. See `references/examples.md` for full implementations of this and five other workflows (catalog cross-matching, light curve analysis, SED construction, spectroscopic redshift, observability calculation).

```python
from astropy.io import fits
from astropy.wcs import WCS
from astropy.stats import sigma_clipped_stats, SigmaClip
from astropy.table import QTable
import astropy.units as u
import numpy as np
from photutils.detection import DAOStarFinder
from photutils.aperture import CircularAperture, CircularAnnulus, aperture_photometry
from photutils.background import Background2D, MedianBackground

# ── Step 1: Load ────────────────────────────────────────────────────────────
with fits.open('image.fits', memmap=True) as hdul:
    image = hdul[0].data.astype(float)
    header = hdul[0].header
    wcs = WCS(header)

# Checkpoint 1: confirm image loaded and WCS is valid
assert image is not None, "Image data is None — check HDU index"
assert wcs.is_celestial, "WCS is not celestial — check CTYPE keywords"
print(f"Image shape: {image.shape}, WCS: {wcs.wcs.ctype}")

# ── Step 2: Background subtraction ──────────────────────────────────────────
bkg = Background2D(image, box_size=(50, 50),
                   filter_size=(3, 3),
                   sigma_clip=SigmaClip(sigma=3.0),
                   bkg_estimator=MedianBackground())
image_sub = image - bkg.background

# Checkpoint 2: background level should be close to zero
residual_median = np.median(image_sub)
print(f"Post-subtraction median: {residual_median:.3f}  (target: ~0)")

# ── Step 3: Source detection ─────────────────────────────────────────────────
_, _, std = sigma_clipped_stats(image_sub, sigma=3.0)
sources = DAOStarFinder(fwhm=4.0, threshold=5.0 * std)(image_sub)

# Checkpoint 3: sanity-check source count
assert sources is not None, "No sources detected — lower threshold or check background subtraction"
print(f"Detected {len(sources)} sources")

# ── Step 4: Aperture photometry ───────────────────────────────────────────────
positions = np.transpose([sources['xcentroid'], sources['ycentroid']])
apertures = CircularAperture(positions, r=5.0)
annuli    = CircularAnnulus(positions, r_in=10.0, r_out=15.0)

phot   = aperture_photometry(image_sub, apertures)
annphot = aperture_photometry(image_sub, annuli)

bkg_per_pixel = annphot['aperture_sum'] / annuli.area
flux = phot['aperture_sum'] - bkg_per_pixel * apertures.area

# Checkpoint 4: fluxes should be mostly positive
neg_frac = (flux < 0).sum() / len(flux)
print(f"Negative-flux fraction: {neg_frac:.1%}  (expect < 5%)")

# ── Step 5: Sky coordinates + output catalog ─────────────────────────────────
sky = wcs.pixel_to_world(phot['xcenter'], phot['ycenter'])

catalog = QTable()
catalog['ra']    = sky.ra
catalog['dec']   = sky.dec
catalog['flux']  = flux * u.ct
catalog['mag']   = -2.5 * np.log10(flux / header.get('EXPTIME', 1.0)) * u.mag

catalog.write('sources.fits', overwrite=True)
print(f"Catalog written: {len(catalog)} sources")
```

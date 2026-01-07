# Advanced Patterns

This document provides detailed patterns for advanced Astropy usage beyond the basics.

## Table of Contents

1. [FITS Manipulation Patterns](#fits-manipulation-patterns)
2. [Units and Quantities Patterns](#units-and-quantities-patterns)
3. [Coordinate Patterns](#coordinate-patterns)
4. [Time Patterns](#time-patterns)
5. [Table Patterns](#table-patterns)
6. [WCS Patterns](#wcs-patterns)
7. [Photometry Patterns](#photometry-patterns)
8. [Spectroscopy Patterns](#spectroscopy-patterns)

## FITS Manipulation Patterns

### Multi-Extension FITS Handling

```python
from astropy.io import fits
import numpy as np

# Create multi-extension FITS with proper structure
def create_multiext_fits(image_data, variance_data, mask_data, filename):
    """Create a multi-extension FITS file with science, variance, and mask."""

    # Primary HDU (often empty for multi-extension files)
    primary = fits.PrimaryHDU()
    primary.header['ORIGIN'] = 'My Pipeline'
    primary.header['DATE'] = '2024-01-01'

    # Science extension
    sci_hdu = fits.ImageHDU(data=image_data, name='SCI')
    sci_hdu.header['BUNIT'] = 'electron/s'
    sci_hdu.header['EXTNAME'] = 'SCI'

    # Variance extension
    var_hdu = fits.ImageHDU(data=variance_data, name='VAR')
    var_hdu.header['BUNIT'] = '(electron/s)^2'
    var_hdu.header['EXTNAME'] = 'VAR'

    # Mask extension (integer type)
    mask_hdu = fits.ImageHDU(data=mask_data.astype(np.uint8), name='MASK')
    mask_hdu.header['EXTNAME'] = 'MASK'

    # Combine into HDUList
    hdul = fits.HDUList([primary, sci_hdu, var_hdu, mask_hdu])
    hdul.writeto(filename, overwrite=True)

    return hdul

# Read multi-extension FITS
def read_multiext_fits(filename):
    """Read all extensions from multi-extension FITS."""

    with fits.open(filename) as hdul:
        # Access by extension name
        science = hdul['SCI'].data
        variance = hdul['VAR'].data
        mask = hdul['MASK'].data

        # Or by index
        science = hdul[1].data

        return science, variance, mask
```

### Header Inheritance and Propagation

```python
def propagate_header(input_fits, output_data, output_fits, preserve_keys=None):
    """Copy selected header keywords from input to output."""

    if preserve_keys is None:
        # Standard keywords to preserve
        preserve_keys = ['OBJECT', 'TELESCOP', 'INSTRUME', 'FILTER',
                        'EXPTIME', 'DATE-OBS', 'RA', 'DEC', 'EQUINOX']

    with fits.open(input_fits) as hdul:
        header = hdul[0].header.copy()

        # Create new HDU
        new_hdu = fits.PrimaryHDU(data=output_data)

        # Copy selected keywords
        for key in preserve_keys:
            if key in header:
                new_hdu.header[key] = (header[key], header.comments[key])

        # Add processing history
        new_hdu.header['HISTORY'] = 'Processed from ' + input_fits
        new_hdu.header['HISTORY'] = 'Processing date: 2024-01-01'

        new_hdu.writeto(output_fits, overwrite=True)
```

### Handling Large FITS Files

```python
def process_large_fits(filename, chunk_size=1000):
    """Process large FITS file in chunks to manage memory."""

    with fits.open(filename, memmap=True) as hdul:
        data = hdul[0].data
        nrows, ncols = data.shape

        # Process in horizontal strips
        results = []
        for i in range(0, nrows, chunk_size):
            chunk = data[i:i+chunk_size, :]

            # Process chunk (e.g., background subtraction)
            processed = chunk - np.median(chunk)
            results.append(processed)

        # Combine results
        return np.vstack(results)

# Alternative: Use memory-mapped arrays directly
def mmap_fits_processing(filename):
    """Process FITS using memory mapping."""

    hdul = fits.open(filename, memmap=True, mode='update')

    # Modify in place (changes written to disk)
    hdul[0].data *= 2.0

    hdul.flush()
    hdul.close()
```

### Updating FITS Headers Without Loading Data

```python
def update_header_only(filename, updates):
    """Update FITS header without loading image data."""

    # Use mode='update' to modify in place
    with fits.open(filename, mode='update') as hdul:
        for key, (value, comment) in updates.items():
            hdul[0].header[key] = (value, comment)

        # Changes automatically flushed on close

# Example usage
updates = {
    'OBSERVER': ('Jane Smith', 'Observer name'),
    'AIRMASS': (1.23, 'Airmass at observation'),
    'SEEING': (0.8, 'Seeing FWHM in arcsec')
}
update_header_only('observation.fits', updates)
```

## Units and Quantities Patterns

### Custom Unit Definitions

```python
import astropy.units as u

# Define custom unit
my_unit = u.def_unit('my_flux_unit', 1e-17 * u.erg / u.s / u.cm**2 / u.angstrom)

# Enable use in quantities
u.add_enabled_units([my_unit])

flux = 5.0 * my_unit
flux_si = flux.to(u.W / u.m**3)

# Custom equivalency
def my_equivalency():
    """Define custom equivalency for specific physical relationship."""
    return [(u.Jy, u.mag,
             lambda x: -2.5 * np.log10(x / 3631),
             lambda x: 3631 * 10**(-x / 2.5))]

# Use custom equivalency
flux_jy = 1.0 * u.Jy
flux_mag = flux_jy.to(u.mag, equivalencies=my_equivalency())
```

### Handling Logarithmic Units

```python
import astropy.units as u
from astropy.units import LogUnit, dex

# Magnitude units
m_ab = 15.0 * u.ABmag
m_st = 15.0 * u.STmag

# Convert magnitude to linear flux
flux = m_ab.physical  # Get linear flux

# Decibels
power_db = 10 * u.dB(u.mW)
power_linear = power_db.physical

# Logarithmic column density
log_nh = 21.5 * dex(u.cm**-2)
nh = log_nh.physical  # 10^21.5 cm^-2
```

### Unit Conversion with Spectral Equivalencies

```python
import astropy.units as u
import astropy.constants as const

# Wavelength to frequency
wavelength = 5000 * u.angstrom
frequency = wavelength.to(u.Hz, equivalencies=u.spectral())

# Wavelength to energy
energy = wavelength.to(u.eV, equivalencies=u.spectral())

# Wavelength to wavenumber
wavenumber = wavelength.to(u.cm**-1, equivalencies=u.spectral())

# Doppler equivalencies (radio convention)
rest_freq = 1420.4 * u.MHz
velocity = (1419 * u.MHz).to(u.km/u.s,
                              equivalencies=u.doppler_radio(rest_freq))

# Optical doppler
rest_wave = 656.3 * u.nm
vel_optical = (656.5 * u.nm).to(u.km/u.s,
                                 equivalencies=u.doppler_optical(rest_wave))
```

### Structured Arrays with Units

```python
from astropy.table import QTable
import astropy.units as u

# Create structured array with units
def create_source_catalog():
    """Create catalog with proper units."""

    sources = QTable()
    sources['id'] = [1, 2, 3]
    sources['ra'] = [10.5, 20.3, 30.1] * u.deg
    sources['dec'] = [5.2, -15.7, 45.3] * u.deg
    sources['flux'] = [123.4, 456.7, 789.0] * u.microJy
    sources['distance'] = [10.0, 25.0, 50.0] * u.parsec

    # Units preserved through operations
    sources['luminosity'] = sources['flux'] * 4 * np.pi * sources['distance']**2

    return sources
```

## Coordinate Patterns

### Custom Coordinate Frames

```python
from astropy.coordinates import BaseCoordinateFrame, Attribute
from astropy.coordinates import representation as r
from astropy.coordinates.matrix_utilities import rotation_matrix
import astropy.units as u

# Define custom frame
class MyFrame(BaseCoordinateFrame):
    """Custom coordinate frame with specific rotation."""

    default_representation = r.SphericalRepresentation
    default_differential = r.SphericalCosLatDifferential

    # Frame attributes
    equinox = Attribute(default='J2000')

    # Define transformation to ICRS
    @staticmethod
    def to_icrs(my_coord):
        """Transform to ICRS."""
        # Example: simple rotation
        lon = my_coord.lon
        lat = my_coord.lat

        # Apply rotation (example values)
        rot = rotation_matrix(45*u.deg, 'z')
        # ... transformation logic

        return ICRS(ra=lon, dec=lat)
```

### Efficient Catalog Cross-Matching

```python
from astropy.coordinates import SkyCoord, match_coordinates_sky
import astropy.units as u

def cross_match_catalogs(cat1_ra, cat1_dec, cat2_ra, cat2_dec,
                         max_sep=1.0*u.arcsec):
    """Efficiently cross-match two large catalogs."""

    # Create SkyCoord objects
    cat1 = SkyCoord(ra=cat1_ra*u.deg, dec=cat1_dec*u.deg)
    cat2 = SkyCoord(ra=cat2_ra*u.deg, dec=cat2_dec*u.deg)

    # Find nearest matches
    idx, sep2d, dist3d = cat1.match_to_catalog_sky(cat2)

    # Filter by maximum separation
    matches = sep2d < max_sep

    # Indices of matches in cat2
    matched_idx = idx[matches]

    # Build matched catalog
    cat1_matched = cat1[matches]
    cat2_matched = cat2[matched_idx]
    separations = sep2d[matches]

    return cat1_matched, cat2_matched, separations

# Handling multiple matches within radius
def find_all_matches_within_radius(target, catalog, radius=5*u.arcsec):
    """Find all catalog sources within radius of target."""

    separations = target.separation(catalog)
    matches = separations < radius

    matched_sources = catalog[matches]
    matched_seps = separations[matches]

    # Sort by separation
    sort_idx = matched_seps.argsort()

    return matched_sources[sort_idx], matched_seps[sort_idx]
```

### Observer-Dependent Coordinates

```python
from astropy.coordinates import EarthLocation, AltAz, get_sun, get_moon
from astropy.time import Time
import astropy.units as u

def calculate_observability(target_coord, location, time):
    """Calculate target observability from specific location and time."""

    # Define observing frame
    altaz_frame = AltAz(obstime=time, location=location)

    # Transform to AltAz
    target_altaz = target_coord.transform_to(altaz_frame)

    # Get sun and moon positions
    sun_altaz = get_sun(time).transform_to(altaz_frame)
    moon_altaz = get_moon(time).transform_to(altaz_frame)

    # Calculate separations
    sun_sep = target_altaz.separation(sun_altaz)
    moon_sep = target_altaz.separation(moon_altaz)

    # Observability criteria
    observable = (target_altaz.alt > 30*u.deg and  # Above 30 degrees
                 sun_altaz.alt < -18*u.deg and      # Astronomical twilight
                 sun_sep > 45*u.deg)                # Away from sun

    return {
        'altitude': target_altaz.alt,
        'azimuth': target_altaz.az,
        'airmass': target_altaz.secz,
        'sun_separation': sun_sep,
        'moon_separation': moon_sep,
        'observable': observable
    }
```

### Proper Motion and Radial Velocity

```python
from astropy.coordinates import SkyCoord
import astropy.units as u

# Coordinates with proper motion and radial velocity
star = SkyCoord(
    ra=10.68470833*u.deg, dec=41.26875*u.deg,
    distance=2.64*u.parsec,
    pm_ra_cosdec=800*u.mas/u.yr,
    pm_dec=-1000*u.mas/u.yr,
    radial_velocity=50*u.km/u.s,
    obstime='J2000'
)

# Propagate to different epoch
new_epoch = '2024-01-01'
star_2024 = star.apply_space_motion(new_obstime=new_epoch)

print(f"Position at J2000: RA={star.ra}, Dec={star.dec}")
print(f"Position at 2024: RA={star_2024.ra}, Dec={star_2024.dec}")
```

## Time Patterns

### High-Precision Time Arithmetic

```python
from astropy.time import Time, TimeDelta
import astropy.units as u

# Handle leap seconds correctly
t_utc = Time('2024-01-01T00:00:00', format='isot', scale='utc')
t_tai = t_utc.tai

# Difference accounts for leap seconds
print(f"TAI - UTC = {(t_tai - t_utc).sec} seconds")

# Barycentric time for exoplanet observations
from astropy.coordinates import SkyCoord, EarthLocation

target = SkyCoord(ra=10*u.deg, dec=20*u.deg)
location = EarthLocation(lat=40*u.deg, lon=-70*u.deg, height=0*u.m)

# Light travel time to Solar System barycenter
ltt_bary = t_utc.light_travel_time(target, 'barycentric', location=location)
t_tdb = t_utc.tdb + ltt_bary

print(f"Barycentric correction: {ltt_bary.to(u.second)}")
```

### Time Series Analysis

```python
from astropy.time import Time
from astropy.timeseries import TimeSeries
import astropy.units as u

# Create time series
times = Time('2024-01-01', format='iso', scale='utc') + np.arange(100) * u.day
flux = np.random.randn(100) * u.Jy

ts = TimeSeries(time=times)
ts['flux'] = flux

# Binning
from astropy.timeseries import aggregate_downsample
ts_binned = aggregate_downsample(ts, time_bin_size=10*u.day)

# Folding for periodic signals
from astropy.timeseries import TimeSeries
period = 5.3 * u.day
ts_folded = ts.fold(period=period, epoch_time=times[0])
```

### Time Zone Handling

```python
from astropy.time import Time
from datetime import datetime
import pytz

# Convert to specific timezone
utc_time = Time('2024-01-01 12:00:00', scale='utc')

# To datetime with timezone
tz = pytz.timezone('US/Pacific')
local_dt = utc_time.to_datetime(timezone=tz)

print(f"UTC: {utc_time.iso}")
print(f"Local: {local_dt}")

# From timezone-aware datetime
aware_dt = datetime(2024, 1, 1, 12, 0, 0, tzinfo=tz)
astropy_time = Time(aware_dt)
```

## Table Patterns

### Masked Tables for Missing Data

```python
from astropy.table import Table, MaskedColumn
import numpy as np

# Create table with masked data
data = np.array([1.0, 2.0, -999, 4.0, -999])
mask = data == -999

col = MaskedColumn(data=data, mask=mask, name='flux')
tbl = Table([col])

# Operations ignore masked values
print(f"Mean (ignoring masked): {tbl['flux'].mean()}")

# Fill masked values
filled = tbl['flux'].filled(fill_value=0.0)
```

### Table Joins with Multiple Keys

```python
from astropy.table import Table, join

# Create tables
left = Table({
    'source_id': [1, 2, 3],
    'field': ['A', 'B', 'A'],
    'magnitude': [12.5, 13.2, 11.8]
})

right = Table({
    'source_id': [1, 2, 4],
    'field': ['A', 'B', 'C'],
    'color': [0.5, 0.7, 0.3]
})

# Join on multiple keys
joined = join(left, right, keys=['source_id', 'field'], join_type='inner')

# Left/right/outer joins
left_join = join(left, right, keys='source_id', join_type='left')
outer_join = join(left, right, keys='source_id', join_type='outer')
```

### Table Metadata and Column Descriptions

```python
from astropy.table import QTable
import astropy.units as u

# Create table with complete metadata
tbl = QTable()
tbl['ra'] = [10.0, 20.0] * u.deg
tbl['dec'] = [5.0, -15.0] * u.deg
tbl['flux'] = [100.0, 200.0] * u.microJy

# Add column descriptions
tbl['ra'].description = 'Right Ascension (J2000)'
tbl['dec'].description = 'Declination (J2000)'
tbl['flux'].description = 'Integrated flux'

# Add table metadata
tbl.meta['description'] = 'Source catalog from observation'
tbl.meta['date'] = '2024-01-01'
tbl.meta['telescope'] = 'VLT'

# Metadata persists through I/O
tbl.write('catalog_with_metadata.fits', overwrite=True)
tbl_read = QTable.read('catalog_with_metadata.fits')
print(tbl_read.meta)
```

### Fast Table Indexing

```python
from astropy.table import Table
import numpy as np

# Create large table
n = 1000000
tbl = Table({
    'id': np.arange(n),
    'value': np.random.randn(n)
})

# Add index for fast lookup
tbl.add_index('id')

# Fast row retrieval by indexed column
row = tbl.loc[500000]  # Much faster than tbl[tbl['id'] == 500000]

# Index on multiple columns
tbl.add_index(['id', 'value'])

# Range queries
subset = tbl.loc[100:200]  # Fast slice on indexed column
```

## WCS Patterns

### WCS from Astrometry Solutions

```python
from astropy.wcs import WCS
import astropy.units as u

def create_wcs_from_solution(ref_ra, ref_dec, ref_x, ref_y,
                              pixel_scale, rotation_angle,
                              image_shape):
    """Create WCS from astrometry solution."""

    w = WCS(naxis=2)

    # Reference point
    w.wcs.crpix = [ref_x, ref_y]
    w.wcs.crval = [ref_ra, ref_dec]

    # Pixel scale with rotation
    # CD matrix combines pixel scale and rotation
    cos_rot = np.cos(rotation_angle)
    sin_rot = np.sin(rotation_angle)

    w.wcs.cd = pixel_scale * np.array([
        [-cos_rot, -sin_rot],
        [sin_rot, -cos_rot]
    ])

    # Coordinate types
    w.wcs.ctype = ['RA---TAN', 'DEC--TAN']

    # Image dimensions
    w.array_shape = image_shape

    return w
```

### SIP Distortion Polynomials

```python
from astropy.wcs import WCS

def add_sip_distortion(wcs, a_coeffs, b_coeffs):
    """Add SIP polynomial distortion to WCS."""

    wcs.sip = Sip(
        a=a_coeffs,  # Forward distortion in x
        b=b_coeffs,  # Forward distortion in y
        crpix=wcs.wcs.crpix
    )

    wcs.wcs.ctype = ['RA---TAN-SIP', 'DEC--TAN-SIP']

    return wcs
```

### Cutout with WCS Preservation

```python
from astropy.wcs import WCS
from astropy.nddata import Cutout2D
from astropy.coordinates import SkyCoord
import astropy.units as u

def extract_cutout_with_wcs(image, wcs, center_coord, size):
    """Extract cutout preserving WCS."""

    # Create cutout
    cutout = Cutout2D(image, center_coord, size, wcs=wcs)

    # Cutout includes updated WCS
    cutout_image = cutout.data
    cutout_wcs = cutout.wcs

    return cutout_image, cutout_wcs

# Usage
from astropy.io import fits

with fits.open('image.fits') as hdul:
    image = hdul[0].data
    wcs = WCS(hdul[0].header)

center = SkyCoord(ra=150*u.deg, dec=2*u.deg)
size = (100, 100)  # pixels

cutout_img, cutout_wcs = extract_cutout_with_wcs(image, wcs, center, size)
```

## Photometry Patterns

### PSF Photometry

```python
from photutils.psf import IntegratedGaussianPRF, DAOPhotPSFPhotometry
from photutils.background import MMMBackground, MADStdBackgroundRMS
from astropy.modeling.fitting import LevMarLSQFitter

# Estimate background
bkg_estimator = MMMBackground()
bkgrms_estimator = MADStdBackgroundRMS()

# Define PSF model
psf_model = IntegratedGaussianPRF(sigma=2.0)

# Fitter
fitter = LevMarLSQFitter()

# PSF photometry
photometry = DAOPhotPSFPhotometry(
    crit_separation=10,
    threshold=5.0,
    fwhm=4.0,
    psf_model=psf_model,
    fitshape=(11, 11),
    fitter=fitter,
    aperture_radius=5.0
)

# Perform photometry
result_tab = photometry(image=image_data)
```

### Grouped Source Photometry

```python
from photutils import DAOStarFinder
from photutils.psf import IterativelySubtractedPSFPhotometry
from photutils.background import MMMBackground

# Find sources
finder = DAOStarFinder(threshold=5.0, fwhm=3.0)
sources = finder(image_data - np.median(image_data))

# Iteratively fit and subtract sources
photometry = IterativelySubtractedPSFPhotometry(
    finder=finder,
    psf_model=psf_model,
    fitter=fitter,
    fitshape=(11, 11),
    aperture_radius=5.0
)

result = photometry(image_data)
residual_image = photometry.get_residual_image()
```

## Spectroscopy Patterns

### Spectral Line Fitting

```python
from specutils import Spectrum1D
from specutils.fitting import fit_lines
from astropy.modeling import models
import astropy.units as u

# Define line models
g_init = models.Gaussian1D(amplitude=10*u.Jy, mean=6563*u.angstrom, stddev=2*u.angstrom)

# Fit line
spectrum_fit = fit_lines(spectrum, g_init)
fitted_line = spectrum_fit(spectrum.spectral_axis)

# Multiple line fitting
h_alpha = models.Gaussian1D(amplitude=10*u.Jy, mean=6563*u.angstrom, stddev=2*u.angstrom)
h_beta = models.Gaussian1D(amplitude=5*u.Jy, mean=4861*u.angstrom, stddev=2*u.angstrom)

multi_line = h_alpha + h_beta
spectrum_fit = fit_lines(spectrum, multi_line)
```

### Continuum Normalization

```python
from specutils.fitting import fit_generic_continuum

# Fit continuum
fitted_continuum = fit_generic_continuum(spectrum)
continuum_model = fitted_continuum(spectrum.spectral_axis)

# Normalize
normalized_spectrum = spectrum / continuum_model

# Alternative: polynomial continuum
from astropy.modeling import models
poly_continuum = models.Polynomial1D(degree=3)
fitted_poly = fit_generic_continuum(spectrum, model=poly_continuum)
```

### Redshift Measurement

```python
from specutils.analysis import template_correlate
from specutils import Spectrum1D

# Cross-correlate with template
observed_spectrum = Spectrum1D.read('observed_spec.fits')
template_spectrum = Spectrum1D.read('template_spec.fits')

# Calculate redshift
result = template_correlate(observed_spectrum, template_spectrum)
redshift = result[0]
redshift_error = result[2]

print(f"Redshift: {redshift:.4f} +/- {redshift_error:.4f}")
```

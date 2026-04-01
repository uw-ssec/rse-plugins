# Common Issues and Solutions

Troubleshooting guide for common Astropy problems and their solutions.

## Table of Contents

1. [FITS I/O Issues](#fits-io-issues)
2. [Unit and Quantity Problems](#unit-and-quantity-problems)
3. [Coordinate Transformation Issues](#coordinate-transformation-issues)
4. [Time Handling Problems](#time-handling-problems)
5. [Table Issues](#table-issues)
6. [WCS Problems](#wcs-problems)
7. [Memory and Performance](#memory-and-performance)
8. [Deprecation Warnings](#deprecation-warnings)

## FITS I/O Issues

### Issue: "VerifyError: Verification option must be one of..."

**Problem:**
```python
fits.open('file.fits', verify='fix')
# VerifyError: Verification option must be one of...
```

**Solution:**
```python
# Correct verification options: 'ignore', 'silentfix', 'fix', 'exception', 'warn'
hdul = fits.open('file.fits', ignore_blank=True, ignore_missing_end=True)

# Or fix common errors silently
hdul = fits.open('file.fits', mode='readonly', output_verify='silentfix')
```

### Issue: "KeyError: Keyword 'XTENSION' not found"

**Problem:**
Non-standard FITS file with missing required keywords.

**Solution:**
```python
from astropy.io import fits

# Read with relaxed verification
hdul = fits.open('nonstandard.fits', ignore_missing_simple=True,
                 ignore_missing_end=True)

# Or update header before writing
header = hdul[0].header
if 'SIMPLE' not in header:
    header['SIMPLE'] = True
```

### Issue: "Memory Error when opening large FITS"

**Problem:**
```python
hdul = fits.open('huge.fits')  # Tries to load entire file into RAM
```

**Solution:**
```python
# Use memory mapping
hdul = fits.open('huge.fits', memmap=True)

# Data accessed on-demand, not loaded into memory
data_subset = hdul[0].data[100:200, 100:200]

# For writing, use mode='update' for in-place modification
hdul = fits.open('huge.fits', mode='update', memmap=True)
hdul[0].data *= 2  # Modified on disk
hdul.flush()
```

### Issue: "OSError: File already exists"

**Problem:**
```python
hdul.writeto('output.fits')
# OSError: File 'output.fits' already exists
```

**Solution:**
```python
# Use overwrite parameter
hdul.writeto('output.fits', overwrite=True)

# Or check existence first
import os
if not os.path.exists('output.fits'):
    hdul.writeto('output.fits')
else:
    os.remove('output.fits')
    hdul.writeto('output.fits')
```

### Issue: Compressed FITS files

**Problem:**
```python
# Cannot read .fits.gz or .fits.fz files
```

**Solution:**
```python
# Astropy handles compressed FITS automatically
hdul = fits.open('image.fits.gz')  # Works for gzip
hdul = fits.open('image.fits.fz')  # Works for fpack compression

# Writing compressed FITS
hdul.writeto('output.fits.gz', overwrite=True)

# Or use explicit compression
from astropy.io.fits import CompImageHDU
compressed_hdu = CompImageHDU(data=image_data, compression_type='RICE_1')
```

## Unit and Quantity Problems

### Issue: "UnitConversionError: ... and ... are not convertible"

**Problem:**
```python
length = 10 * u.meter
time = 5 * u.second
result = length.to(u.second)  # Cannot convert length to time!
```

**Solution:**
```python
# Only convert between compatible units
length = 10 * u.meter
length_km = length.to(u.km)  # OK: both are lengths

# For wavelength/frequency conversion, use equivalencies
wavelength = 500 * u.nm
frequency = wavelength.to(u.Hz, equivalencies=u.spectral())  # Now works!

# Common equivalencies:
# - u.spectral(): wavelength <-> frequency <-> energy
# - u.doppler_optical(): wavelength <-> velocity
# - u.doppler_radio(): frequency <-> velocity
# - u.brightness_temperature(): flux <-> temperature
```

### Issue: "Unit arithmetic produces unexpected results"

**Problem:**
```python
distance = 10 * u.m
time = 2 * u.s
speed = distance / time
print(speed.unit)  # Shows 'm / s' instead of simplified unit
```

**Solution:**
```python
# Use .to() to convert to desired unit
speed = (distance / time).to(u.km / u.hour)

# Or use .decompose() to get SI base units
result = speed.decompose()  # Returns in m/s

# Or .compose() to find recognized compound units
compound = (u.kg * u.m**2 / u.s**2).compose()
# Returns units like J (joule)
```

### Issue: "Quantity arrays losing units after operations"

**Problem:**
```python
distances = [10, 20, 30] * u.parsec
mean_dist = np.mean(distances)  # Loses unit!
```

**Solution:**
```python
# NumPy operations on Quantities should preserve units
distances = [10, 20, 30] * u.parsec
mean_dist = np.mean(distances)  # Should preserve unit

# If units are lost, explicitly recreate Quantity
if not isinstance(mean_dist, u.Quantity):
    mean_dist = mean_dist * u.parsec

# Or use Quantity methods when available
mean_dist = distances.mean()  # Preserves unit
```

### Issue: "Logarithmic units confusion"

**Problem:**
```python
mag = 15.0 * u.mag
flux = mag.to(u.Jy)  # Error: magnitudes need context
```

**Solution:**
```python
# For AB magnitudes, first convert to physical units
mag = 15.0 * u.ABmag
flux = mag.physical  # Returns flux in appropriate units

# For other magnitude systems
mag_st = 15.0 * u.STmag
flux_st = mag_st.physical

# Converting flux to magnitude
flux = 100 * u.Jy
mag_ab = u.ABmag.from_physical(flux)  # Error - need to specify

# Correct way:
flux = 100 * u.Jy
mag_ab = flux.to(u.ABmag, equivalencies=u.spectral_density(5000*u.angstrom))
```

## Coordinate Transformation Issues

### Issue: "Frame attribute mismatch in transformation"

**Problem:**
```python
c1 = SkyCoord(ra=10*u.deg, dec=20*u.deg, frame='fk5', equinox='J2000')
c2 = SkyCoord(ra=11*u.deg, dec=21*u.deg, frame='fk5', equinox='J1950')
sep = c1.separation(c2)  # Uses different equinoxes!
```

**Solution:**
```python
# Ensure frames match before operations
c1 = SkyCoord(ra=10*u.deg, dec=20*u.deg, frame='fk5', equinox='J2000')
c2 = SkyCoord(ra=11*u.deg, dec=21*u.deg, frame='fk5', equinox='J1950')

# Transform c2 to same frame as c1
c2_j2000 = c2.transform_to(c1.frame)
sep = c1.separation(c2_j2000)  # Now consistent
```

### Issue: "AltAz transformation requires location and time"

**Problem:**
```python
c = SkyCoord(ra=10*u.deg, dec=20*u.deg)
altaz = c.transform_to('altaz')
# CoordinateFrameError: AltAz frame requires obstime and location
```

**Solution:**
```python
from astropy.coordinates import EarthLocation, AltAz
from astropy.time import Time

# Specify location and time
location = EarthLocation(lat=40*u.deg, lon=-70*u.deg, height=0*u.m)
obstime = Time('2024-01-01 00:00:00')

# Create AltAz frame
altaz_frame = AltAz(obstime=obstime, location=location)

# Transform
c = SkyCoord(ra=10*u.deg, dec=20*u.deg)
c_altaz = c.transform_to(altaz_frame)
```

### Issue: "Large angular separations give incorrect results"

**Problem:**
```python
# Separation between opposite points on sky
c1 = SkyCoord(ra=0*u.deg, dec=0*u.deg)
c2 = SkyCoord(ra=180*u.deg, dec=0*u.deg)
sep = c1.separation(c2)  # Should be 180 degrees
```

**Solution:**
```python
# separation() uses great circle distance (correct)
sep = c1.separation(c2)
print(sep.deg)  # 180.0 degrees

# If getting unexpected results, check:
# 1. Coordinate units (degree vs hourangle)
c_wrong = SkyCoord(ra=12, dec=0, unit='deg')  # ra should be in hours?
c_right = SkyCoord(ra=12, dec=0, unit=(u.hourangle, u.deg))

# 2. Frame consistency
c1_icrs = c1.icrs
c2_fk5 = c2.fk5
# Transform to same frame first
sep = c1_icrs.separation(c2_fk5.icrs)
```

### Issue: "Coordinate matching performance"

**Problem:**
```python
# Slow matching of large catalogs
for coord1 in catalog1:
    for coord2 in catalog2:
        sep = coord1.separation(coord2)  # Very slow!
```

**Solution:**
```python
# Use vectorized matching
from astropy.coordinates import match_coordinates_sky

catalog1 = SkyCoord(ra=cat1_ra*u.deg, dec=cat1_dec*u.deg)
catalog2 = SkyCoord(ra=cat2_ra*u.deg, dec=cat2_dec*u.deg)

# Fast matching
idx, sep2d, dist3d = catalog1.match_to_catalog_sky(catalog2)

# idx[i] is the index of nearest catalog2 source to catalog1[i]
# sep2d[i] is the angular separation
matches = sep2d < 1*u.arcsec
```

## Time Handling Problems

### Issue: "Time scale confusion"

**Problem:**
```python
t1 = Time('2024-01-01', scale='utc')
t2 = Time('2024-01-01', scale='tai')
delta = t2 - t1
print(delta.sec)  # Not zero! Different time scales
```

**Solution:**
```python
# Always be explicit about time scale
t_utc = Time('2024-01-01', scale='utc')
t_tai = Time('2024-01-01', scale='tai')

# Convert to same scale before comparison
t_tai_as_utc = t_tai.utc
delta = t_tai_as_utc - t_utc

# Common scales:
# - 'utc': Coordinated Universal Time (for observations)
# - 'tai': International Atomic Time (no leap seconds)
# - 'tt': Terrestrial Time (for ephemerides)
# - 'tdb': Barycentric Dynamical Time (for dynamics)
```

### Issue: "ISO format parsing ambiguity"

**Problem:**
```python
t = Time('2024-01-01')
print(t.format)  # Shows 'iso' but could mean different things
```

**Solution:**
```python
# Be explicit about format
t = Time('2024-01-01', format='iso', scale='utc')

# Common formats:
t_isot = Time('2024-01-01T00:00:00', format='isot')  # ISO with T separator
t_jd = Time(2460311.5, format='jd')  # Julian Date
t_mjd = Time(60311.0, format='mjd')  # Modified Julian Date

# Check format and scale
print(f"Format: {t.format}, Scale: {t.scale}")
```

### Issue: "Time array vs scalar confusion"

**Problem:**
```python
times = Time(['2024-01-01', '2024-01-02'])
delta = 1 * u.day
new_times = times + delta  # Works
new_time = times[0] + delta  # Also works, but need to be careful
```

**Solution:**
```python
# Time objects can be scalar or arrays
t_scalar = Time('2024-01-01', scale='utc')
t_array = Time(['2024-01-01', '2024-01-02'], scale='utc')

# Check shape
print(t_scalar.shape)  # ()
print(t_array.shape)   # (2,)

# Both support arithmetic
t_scalar_new = t_scalar + 1*u.day
t_array_new = t_array + 1*u.day

# Indexing gives scalar
t_element = t_array[0]
print(t_element.shape)  # ()
```

### Issue: "Precision loss in time calculations"

**Problem:**
```python
# Need sub-microsecond precision over decades
t = Time('2000-01-01', scale='utc')
t_future = t + 10*u.year + 1*u.microsecond
# Precision loss?
```

**Solution:**
```python
# Astropy Time maintains sub-nanosecond precision
# Uses two 64-bit floats internally (jd1, jd2)

t = Time('2000-01-01', scale='utc', precision=9)  # nanosecond precision
t_future = t + 10*u.year + 1*u.microsecond

# Precision is maintained
print(t_future.iso)  # Shows full precision

# For very precise calculations, use appropriate time scale
t_tdb = t.tdb  # Barycentric Dynamical Time (no leap seconds)
```

## Table Issues

### Issue: "Column type mismatch when adding to table"

**Problem:**
```python
tbl = Table({'a': [1, 2, 3]})
tbl['a'] = [1.5, 2.5, 3.5]  # Trying to assign floats to int column
```

**Solution:**
```python
# Option 1: Remove and re-add column
tbl.remove_column('a')
tbl['a'] = [1.5, 2.5, 3.5]

# Option 2: Create new table with correct dtype
tbl = Table({'a': [1, 2, 3]}, dtype=[float])

# Option 3: Explicitly cast
tbl['a'] = np.array([1.5, 2.5, 3.5], dtype=float)

# Check column dtype
print(tbl['a'].dtype)
```

### Issue: "Units lost when writing to CSV"

**Problem:**
```python
qtbl = QTable({'flux': [1, 2, 3] * u.Jy})
qtbl.write('data.csv', format='csv')
# Units not preserved in CSV
```

**Solution:**
```python
# CSV format doesn't preserve units
# Options:

# 1. Use FITS or HDF5 for unit preservation
qtbl.write('data.fits', format='fits', overwrite=True)
qtbl_read = QTable.read('data.fits')  # Units preserved

# 2. Add unit information to metadata/header
qtbl.write('data.csv', format='csv', overwrite=True)
# Document units in separate file or header comments

# 3. Use ECSV (Enhanced CSV) format
qtbl.write('data.ecsv', format='ascii.ecsv', overwrite=True)
qtbl_read = QTable.read('data.ecsv', format='ascii.ecsv')  # Units preserved!
```

### Issue: "Joining tables with different column names"

**Problem:**
```python
left = Table({'id': [1, 2], 'val': [10, 20]})
right = Table({'source_id': [1, 2], 'other': [30, 40]})
joined = join(left, right, keys='id')  # KeyError: 'id' not in right table
```

**Solution:**
```python
from astropy.table import join

# Rename column to match
right.rename_column('source_id', 'id')
joined = join(left, right, keys='id')

# Or specify different keys for each table
right = Table({'source_id': [1, 2], 'other': [30, 40]})
joined = join(left, right, keys_left='id', keys_right='source_id')
```

### Issue: "Masked values in tables"

**Problem:**
```python
# Missing values showing as weird numbers
tbl = Table([[1, 2, -999, 4]], names=['flux'])
mean_flux = tbl['flux'].mean()  # Includes -999!
```

**Solution:**
```python
from astropy.table import Table, MaskedColumn
import numpy as np

# Create masked column
data = np.array([1, 2, -999, 4])
mask = data == -999
col = MaskedColumn(data=data, mask=mask, name='flux')

tbl = Table([col])

# Operations automatically ignore masked values
mean_flux = tbl['flux'].mean()  # Excludes masked value

# Fill masked values
filled = tbl['flux'].filled(fill_value=0)

# Check for masked values
has_masked = tbl['flux'].mask.any()
```

## WCS Problems

### Issue: "WCS transformation gives NaN"

**Problem:**
```python
wcs = WCS(header)
ra, dec = wcs.all_pix2world(x, y, 0)
# Returns NaN
```

**Solution:**
```python
# Check WCS is valid
print(wcs)  # Look for errors or warnings

# Verify pixel coordinates are within image bounds
naxis1 = header['NAXIS1']
naxis2 = header['NAXIS2']
if x < 0 or x >= naxis1 or y < 0 or y >= naxis2:
    print("Pixel coordinates out of bounds")

# Check for missing WCS keywords
required = ['CTYPE1', 'CTYPE2', 'CRPIX1', 'CRPIX2', 'CRVAL1', 'CRVAL2']
for key in required:
    if key not in header:
        print(f"Missing required WCS keyword: {key}")

# Validate WCS
from astropy.wcs import WCS
try:
    wcs = WCS(header, fix=True)  # Attempt to fix common errors
except Exception as e:
    print(f"WCS error: {e}")
```

### Issue: "Pixel origin convention confusion"

**Problem:**
```python
# Different results with origin=0 vs origin=1
ra, dec = wcs.all_pix2world(100, 200, 0)
ra2, dec2 = wcs.all_pix2world(100, 200, 1)
# Different results!
```

**Solution:**
```python
# origin=0: Python/C convention (0-indexed, pixel center at 0.5)
# origin=1: FITS convention (1-indexed, pixel center at 1.0)

# For FITS pixel coordinates (1-indexed)
x_fits, y_fits = 100, 200
ra, dec = wcs.all_pix2world(x_fits, y_fits, 1)

# For Python array indices (0-indexed)
x_python, y_python = 99, 199  # Equivalent to FITS 100, 200
ra, dec = wcs.all_pix2world(x_python, y_python, 0)

# Be consistent throughout your code!
# Recommendation: use origin=0 with Python arrays
```

### Issue: "WCS with SIP distortions"

**Problem:**
```python
# WCS includes SIP polynomial distortions
# Standard transformations don't apply distortion
```

**Solution:**
```python
from astropy.wcs import WCS

# WCS automatically handles SIP if present in header
wcs = WCS(header)

# Check for SIP
if wcs.sip is not None:
    print("WCS includes SIP distortion")

# Transformations automatically apply SIP
ra, dec = wcs.all_pix2world(x, y, 0)  # Includes SIP distortion

# To ignore SIP (use only linear WCS):
wcs_no_sip = WCS(header, relax=False)
```

## Memory and Performance

### Issue: "Out of memory with large FITS files"

**Problem:**
```python
hdul = fits.open('large_cube.fits')  # Loads entire 10GB file into RAM
data = hdul[0].data
```

**Solution:**
```python
# Use memory mapping
hdul = fits.open('large_cube.fits', memmap=True)

# Access only needed portion
data_slice = hdul[0].data[100:200, :, :]  # Loads only this slice

# Process in chunks
def process_in_chunks(filename, chunk_size=100):
    with fits.open(filename, memmap=True) as hdul:
        data = hdul[0].data
        nz, ny, nx = data.shape

        for z_start in range(0, nz, chunk_size):
            z_end = min(z_start + chunk_size, nz)
            chunk = data[z_start:z_end, :, :]
            # Process chunk
            result = process_chunk(chunk)
            yield result
```

### Issue: "Slow coordinate transformations"

**Problem:**
```python
# Transforming millions of coordinates
for i in range(len(ra_array)):
    c = SkyCoord(ra=ra_array[i]*u.deg, dec=dec_array[i]*u.deg)
    c_gal = c.galactic  # Very slow in loop!
```

**Solution:**
```python
# Use vectorized operations
coords = SkyCoord(ra=ra_array*u.deg, dec=dec_array*u.deg)
coords_gal = coords.galactic  # Much faster!

# For very large arrays (>1 million points), process in chunks
def transform_in_chunks(ra, dec, chunk_size=100000):
    n = len(ra)
    results = []

    for i in range(0, n, chunk_size):
        chunk_coords = SkyCoord(ra=ra[i:i+chunk_size]*u.deg,
                                dec=dec[i:i+chunk_size]*u.deg)
        chunk_gal = chunk_coords.galactic
        results.append(chunk_gal)

    # Combine results
    return SkyCoord(np.concatenate([r.l.deg for r in results])*u.deg,
                    np.concatenate([r.b.deg for r in results])*u.deg,
                    frame='galactic')
```

### Issue: "Table operations slow for large tables"

**Problem:**
```python
# Filtering large table
large_tbl = Table.read('huge_catalog.fits')  # 10 million rows
filtered = large_tbl[large_tbl['magnitude'] < 15]  # Slow
```

**Solution:**
```python
# Use indexing for faster queries
large_tbl.add_index('magnitude')
filtered = large_tbl.loc_indices[large_tbl['magnitude'] < 15]

# For very large tables, consider using databases
# or HDF5 with pytables for out-of-core operations

# Process in chunks
def filter_in_chunks(filename, condition, chunk_size=100000):
    full_tbl = Table.read(filename)
    n_rows = len(full_tbl)

    filtered_chunks = []
    for i in range(0, n_rows, chunk_size):
        chunk = full_tbl[i:i+chunk_size]
        filtered_chunk = chunk[condition(chunk)]
        filtered_chunks.append(filtered_chunk)

    from astropy.table import vstack
    return vstack(filtered_chunks)
```

## Deprecation Warnings

### Issue: "FutureWarning or DeprecationWarning"

**Problem:**
```python
# Using deprecated function
from astropy.coordinates import ICRS
c = ICRS(ra=10, dec=20)  # DeprecationWarning
```

**Solution:**
```python
# Check Astropy changelog for migration guide
# Common deprecated patterns and replacements:

# Old: Direct frame classes
from astropy.coordinates import ICRS
c = ICRS(ra=10*u.deg, dec=20*u.deg)

# New: Use SkyCoord
c = SkyCoord(ra=10*u.deg, dec=20*u.deg, frame='icrs')

# Old: cython_version
from astropy import cython_version  # Deprecated

# New: Not needed, Cython compilation automatic

# Check your Astropy version
import astropy
print(astropy.__version__)

# Update Astropy to get latest features
# pip install --upgrade astropy
```

### Issue: "fits.update() deprecated"

**Problem:**
```python
fits.update('file.fits', data, 0)  # DeprecationWarning
```

**Solution:**
```python
# Use mode='update' with fits.open
with fits.open('file.fits', mode='update') as hdul:
    hdul[0].data = new_data
    # Changes flushed automatically on close

# Or use writeto with overwrite
hdul = fits.open('file.fits')
hdul[0].data = new_data
hdul.writeto('file.fits', overwrite=True)
```

## General Troubleshooting Tips

1. **Check Astropy version**: Many issues are fixed in newer versions
   ```python
   import astropy
   print(astropy.__version__)
   ```

2. **Enable warnings**: See all warnings during development
   ```python
   import warnings
   warnings.simplefilter('always')
   ```

3. **Check documentation**: Astropy docs are comprehensive
   - https://docs.astropy.org/

4. **Search GitHub issues**: Your problem may already be reported
   - https://github.com/astropy/astropy/issues

5. **Ask for help**: Community is active and helpful
   - Astropy Discourse: https://community.openastronomy.org/c/astropy
   - Stack Overflow: Tag `astropy`

6. **Test with minimal example**: Isolate the problem
   ```python
   # Create minimal reproducible example
   import astropy.units as u
   from astropy.coordinates import SkyCoord

   # Minimal test case
   c = SkyCoord(ra=10*u.deg, dec=20*u.deg)
   print(c)
   ```

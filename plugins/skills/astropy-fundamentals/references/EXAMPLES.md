# Real-World Examples

Complete workflows demonstrating Astropy in realistic astronomical scenarios.

## Table of Contents

1. [Telescope Image Processing Pipeline](#telescope-image-processing-pipeline)
2. [Catalog Cross-Matching](#catalog-cross-matching)
3. [Light Curve Analysis](#light-curve-analysis)
4. [Multi-Wavelength SED Construction](#multi-wavelength-sed-construction)
5. [Spectroscopic Redshift Measurement](#spectroscopic-redshift-measurement)
6. [Observability Calculation](#observability-calculation)

## Telescope Image Processing Pipeline

Complete pipeline for processing a telescope image: loading FITS, background subtraction, source detection, aperture photometry, and catalog creation with WCS.

```python
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from astropy.stats import sigma_clipped_stats, SigmaClip
from astropy.table import QTable
from astropy.coordinates import SkyCoord
import astropy.units as u

from photutils.detection import DAOStarFinder
from photutils.aperture import CircularAperture, CircularAnnulus, aperture_photometry
from photutils.background import Background2D, MedianBackground

def process_astronomical_image(filename, output_catalog='sources.fits'):
    """
    Complete image processing pipeline.

    Parameters
    ----------
    filename : str
        Path to FITS image
    output_catalog : str
        Output catalog filename

    Returns
    -------
    sources : QTable
        Detected sources with photometry
    """

    # 1. Load FITS file
    print("Loading FITS file...")
    with fits.open(filename) as hdul:
        image_data = hdul[0].data
        header = hdul[0].header
        wcs = WCS(header)

        # Get observation metadata
        exptime = header.get('EXPTIME', 1.0)
        filter_name = header.get('FILTER', 'Unknown')

    # 2. Background estimation and subtraction
    print("Estimating background...")
    sigma_clip = SigmaClip(sigma=3.0, maxiters=10)
    bkg_estimator = MedianBackground()

    bkg = Background2D(image_data, box_size=(50, 50),
                       filter_size=(3, 3),
                       sigma_clip=sigma_clip,
                       bkg_estimator=bkg_estimator)

    image_subtracted = image_data - bkg.background

    # 3. Source detection
    print("Detecting sources...")
    mean, median, std = sigma_clipped_stats(image_subtracted, sigma=3.0)

    daofind = DAOStarFinder(fwhm=4.0, threshold=5.0 * std)
    sources = daofind(image_subtracted)

    print(f"Found {len(sources)} sources")

    # 4. Aperture photometry
    print("Performing aperture photometry...")
    positions = np.transpose([sources['xcentroid'], sources['ycentroid']])

    # Define apertures
    apertures = CircularAperture(positions, r=5.0)
    annulus = CircularAnnulus(positions, r_in=10.0, r_out=15.0)

    # Measure fluxes
    phot_table = aperture_photometry(image_subtracted, apertures)
    bkg_table = aperture_photometry(image_subtracted, annulus)

    # Background-subtracted flux
    bkg_mean = bkg_table['aperture_sum'] / annulus.area
    final_sum = phot_table['aperture_sum'] - bkg_mean * apertures.area

    phot_table['flux_bkg_subtracted'] = final_sum
    phot_table['flux_bkg_subtracted'].unit = u.count

    # 5. Convert to sky coordinates
    print("Converting to sky coordinates...")
    x_pix = phot_table['xcenter']
    y_pix = phot_table['ycenter']
    sky_coords = wcs.pixel_to_world(x_pix, y_pix)

    # 6. Create output catalog
    print("Creating output catalog...")
    catalog = QTable()
    catalog['id'] = np.arange(1, len(phot_table) + 1)
    catalog['ra'] = sky_coords.ra
    catalog['dec'] = sky_coords.dec
    catalog['x_pix'] = x_pix
    catalog['y_pix'] = y_pix
    catalog['flux'] = phot_table['flux_bkg_subtracted']
    catalog['flux_err'] = np.sqrt(phot_table['flux_bkg_subtracted'].value) * u.count

    # Convert to magnitude (instrumental)
    with np.errstate(divide='ignore', invalid='ignore'):
        catalog['magnitude'] = -2.5 * np.log10(catalog['flux'].value / exptime) * u.mag
        catalog['mag_err'] = (2.5 / np.log(10)) * (catalog['flux_err'] / catalog['flux'])

    # Add metadata
    catalog.meta['FILTER'] = filter_name
    catalog.meta['EXPTIME'] = exptime
    catalog.meta['FILENAME'] = filename
    catalog.meta['NSOURCES'] = len(catalog)

    # Column descriptions
    catalog['ra'].description = 'Right Ascension (J2000)'
    catalog['dec'].description = 'Declination (J2000)'
    catalog['flux'].description = 'Background-subtracted aperture flux'
    catalog['magnitude'].description = 'Instrumental magnitude'

    # 7. Write output
    catalog.write(output_catalog, overwrite=True)
    print(f"Catalog saved to {output_catalog}")

    return catalog

# Example usage
if __name__ == '__main__':
    sources = process_astronomical_image('observation.fits', 'detected_sources.fits')
    print(sources[:10])  # Show first 10 sources
```

## Catalog Cross-Matching

Cross-match two astronomical catalogs with coordinate transformations and quality filtering.

```python
from astropy.table import Table, QTable, join
from astropy.coordinates import SkyCoord, match_coordinates_sky
import astropy.units as u
import numpy as np

def cross_match_catalogs(catalog1_file, catalog2_file,
                         max_separation=1.0*u.arcsec,
                         output_file='matched_catalog.fits'):
    """
    Cross-match two catalogs and combine data.

    Parameters
    ----------
    catalog1_file : str
        First catalog (FITS)
    catalog2_file : str
        Second catalog (FITS)
    max_separation : Quantity
        Maximum matching radius
    output_file : str
        Output matched catalog

    Returns
    -------
    matched : QTable
        Matched sources with combined data
    """

    # 1. Read catalogs
    print("Reading catalogs...")
    cat1 = QTable.read(catalog1_file)
    cat2 = QTable.read(catalog2_file)

    print(f"Catalog 1: {len(cat1)} sources")
    print(f"Catalog 2: {len(cat2)} sources")

    # 2. Create SkyCoord objects
    coords1 = SkyCoord(ra=cat1['ra'], dec=cat1['dec'])
    coords2 = SkyCoord(ra=cat2['ra'], dec=cat2['dec'])

    # 3. Perform matching
    print(f"Matching with {max_separation.to(u.arcsec)} radius...")
    idx, sep2d, dist3d = coords1.match_to_catalog_sky(coords2)

    # 4. Filter by separation
    matches = sep2d < max_separation
    n_matches = matches.sum()

    print(f"Found {n_matches} matches ({100*n_matches/len(cat1):.1f}% of catalog 1)")

    # 5. Build matched catalog
    matched = QTable()

    # Source ID
    matched['source_id'] = cat1['id'][matches]

    # Coordinates (average of matched positions)
    matched['ra'] = coords1[matches].ra
    matched['dec'] = coords1[matches].dec

    # Separation
    matched['match_separation'] = sep2d[matches]

    # Data from catalog 1
    matched['flux_cat1'] = cat1['flux'][matches]
    matched['mag_cat1'] = cat1['magnitude'][matches]

    # Data from catalog 2 (matched entries)
    matched_idx = idx[matches]
    matched['flux_cat2'] = cat2['flux'][matched_idx]
    matched['mag_cat2'] = cat2['magnitude'][matched_idx]

    # Calculate color (if different filters)
    if 'FILTER' in cat1.meta and 'FILTER' in cat2.meta:
        filter1 = cat1.meta['FILTER']
        filter2 = cat2.meta['FILTER']

        if filter1 != filter2:
            color_name = f"{filter1}-{filter2}"
            matched[color_name] = matched['mag_cat1'] - matched['mag_cat2']
            matched[color_name].unit = u.mag

    # 6. Add quality flags
    # Flag sources with large positional uncertainties
    matched['quality_flag'] = 0

    # Large separation (>0.5 arcsec)
    matched['quality_flag'][matched['match_separation'] > 0.5*u.arcsec] |= 1

    # Faint in either band (mag > 20)
    faint = (matched['mag_cat1'] > 20*u.mag) | (matched['mag_cat2'] > 20*u.mag)
    matched['quality_flag'][faint] |= 2

    # 7. Add metadata
    matched.meta['CAT1_FILE'] = catalog1_file
    matched.meta['CAT2_FILE'] = catalog2_file
    matched.meta['MAX_SEP'] = max_separation.to(u.arcsec).value
    matched.meta['N_MATCHES'] = n_matches
    matched.meta['MATCH_RATE'] = n_matches / len(cat1)

    # 8. Save output
    matched.write(output_file, overwrite=True)
    print(f"Matched catalog saved to {output_file}")

    return matched

# Example usage
if __name__ == '__main__':
    matched = cross_match_catalogs(
        'catalog_filter1.fits',
        'catalog_filter2.fits',
        max_separation=1.0*u.arcsec,
        output_file='matched_multiband.fits'
    )

    # Show statistics
    print(f"\nMatch statistics:")
    print(f"  Mean separation: {matched['match_separation'].mean():.3f}")
    print(f"  Good quality matches: {(matched['quality_flag'] == 0).sum()}")
```

## Light Curve Analysis

Analyze time-series photometry with proper time handling and period search.

```python
from astropy.time import Time
from astropy.timeseries import TimeSeries, LombScargle
from astropy.table import QTable
import astropy.units as u
import numpy as np
import matplotlib.pyplot as plt

def analyze_light_curve(time_bjd, magnitude, mag_err,
                        period_range=(0.1, 10)*u.day):
    """
    Analyze variable star light curve.

    Parameters
    ----------
    time_bjd : array-like
        Barycentric Julian Date
    magnitude : array-like
        Magnitude measurements
    mag_err : array-like
        Magnitude uncertainties
    period_range : tuple of Quantity
        Period search range

    Returns
    -------
    results : dict
        Analysis results including best period
    """

    # 1. Create TimeSeries object
    print("Creating time series...")
    ts = TimeSeries(time=Time(time_bjd, format='jd', scale='tdb'))
    ts['magnitude'] = magnitude * u.mag
    ts['mag_err'] = mag_err * u.mag

    # 2. Basic statistics
    mean_mag = np.mean(ts['magnitude'])
    std_mag = np.std(ts['magnitude'])
    amplitude = (np.max(ts['magnitude']) - np.min(ts['magnitude'])) / 2

    print(f"Mean magnitude: {mean_mag:.3f}")
    print(f"Std deviation: {std_mag:.3f}")
    print(f"Amplitude: {amplitude:.3f}")

    # 3. Period search with Lomb-Scargle
    print("Searching for periods...")
    ls = LombScargle(ts.time.jd, ts['magnitude'].value, ts['mag_err'].value)

    frequency, power = ls.autopower(
        minimum_frequency=1/period_range[1].to(u.day).value,
        maximum_frequency=1/period_range[0].to(u.day).value,
        samples_per_peak=10
    )

    # Best period
    best_frequency = frequency[np.argmax(power)]
    best_period = (1 / best_frequency) * u.day
    false_alarm_prob = ls.false_alarm_probability(power.max())

    print(f"Best period: {best_period:.6f}")
    print(f"False alarm probability: {false_alarm_prob:.2e}")

    # 4. Fold light curve on best period
    print("Folding light curve...")
    epoch = ts.time[0]  # Use first observation as epoch
    phase = ((ts.time - epoch).jd % best_period.value) / best_period.value

    # Sort by phase
    sort_idx = np.argsort(phase)
    phase_sorted = phase[sort_idx]
    mag_sorted = ts['magnitude'][sort_idx]
    err_sorted = ts['mag_err'][sort_idx]

    # 5. Bin by phase
    n_bins = 20
    phase_bins = np.linspace(0, 1, n_bins + 1)
    binned_phase = []
    binned_mag = []
    binned_err = []

    for i in range(n_bins):
        mask = (phase_sorted >= phase_bins[i]) & (phase_sorted < phase_bins[i + 1])
        if mask.sum() > 0:
            binned_phase.append(phase_bins[i] + 0.5 / n_bins)
            binned_mag.append(np.mean(mag_sorted[mask]))
            binned_err.append(np.std(mag_sorted[mask]) / np.sqrt(mask.sum()))

    binned_phase = np.array(binned_phase)
    binned_mag = np.array(binned_mag) * u.mag
    binned_err = np.array(binned_err) * u.mag

    # 6. Create output table
    folded_lc = QTable()
    folded_lc['phase'] = phase_sorted
    folded_lc['magnitude'] = mag_sorted
    folded_lc['mag_err'] = err_sorted

    folded_lc.meta['PERIOD'] = best_period.value
    folded_lc.meta['EPOCH'] = epoch.jd
    folded_lc.meta['AMPLITUDE'] = amplitude.value
    folded_lc.meta['FAP'] = false_alarm_prob

    # 7. Plot results
    fig, axes = plt.subplots(2, 1, figsize=(10, 8))

    # Periodogram
    axes[0].plot(1/frequency, power, 'k-', linewidth=0.5)
    axes[0].axvline(best_period.value, color='r', linestyle='--',
                    label=f'P={best_period:.3f}')
    axes[0].set_xlabel('Period (days)')
    axes[0].set_ylabel('Lomb-Scargle Power')
    axes[0].legend()
    axes[0].set_title('Periodogram')

    # Folded light curve
    axes[1].errorbar(phase_sorted, mag_sorted.value, yerr=err_sorted.value,
                     fmt='k.', alpha=0.3, label='Individual points')
    axes[1].errorbar(binned_phase, binned_mag.value, yerr=binned_err.value,
                     fmt='ro', markersize=8, label='Binned')
    # Plot twice to show phase wrapping
    axes[1].errorbar(binned_phase + 1, binned_mag.value, yerr=binned_err.value,
                     fmt='ro', markersize=8)
    axes[1].set_xlabel('Phase')
    axes[1].set_ylabel('Magnitude')
    axes[1].set_xlim(0, 2)
    axes[1].invert_yaxis()
    axes[1].legend()
    axes[1].set_title(f'Folded Light Curve (P={best_period:.6f})')

    plt.tight_layout()
    plt.savefig('light_curve_analysis.png', dpi=150)
    print("Plot saved to light_curve_analysis.png")

    return {
        'period': best_period,
        'epoch': epoch,
        'amplitude': amplitude,
        'false_alarm_prob': false_alarm_prob,
        'folded_lc': folded_lc,
        'binned_phase': binned_phase,
        'binned_mag': binned_mag,
        'binned_err': binned_err
    }

# Example usage
if __name__ == '__main__':
    # Load light curve data
    lc_data = QTable.read('light_curve.fits')

    results = analyze_light_curve(
        time_bjd=lc_data['bjd'],
        magnitude=lc_data['magnitude'].value,
        mag_err=lc_data['mag_err'].value,
        period_range=(0.5, 5)*u.day
    )

    print(f"\nBest period: {results['period']}")
    print(f"Amplitude: {results['amplitude']}")
```

## Multi-Wavelength SED Construction

Build spectral energy distribution from multi-band photometry with proper unit handling.

```python
from astropy.table import QTable
from astropy.coordinates import SkyCoord
import astropy.units as u
import astropy.constants as const
import numpy as np
import matplotlib.pyplot as plt

def build_sed(source_coord, catalog_files, output_file='sed.fits'):
    """
    Build SED from multiple catalogs.

    Parameters
    ----------
    source_coord : SkyCoord
        Target source coordinates
    catalog_files : dict
        Dictionary mapping filter names to catalog files
    output_file : str
        Output SED table

    Returns
    -------
    sed : QTable
        SED table with wavelengths and fluxes
    """

    # 1. Match source across catalogs
    print(f"Building SED for source at {source_coord.to_string('hmsdms')}")

    sed_data = []

    for filter_name, catalog_file in catalog_files.items():
        print(f"Processing {filter_name}...")

        # Read catalog
        catalog = QTable.read(catalog_file)
        cat_coords = SkyCoord(ra=catalog['ra'], dec=catalog['dec'])

        # Find nearest source
        idx, sep2d, _ = source_coord.match_to_catalog_sky(cat_coords)

        if sep2d < 1*u.arcsec:
            # Get flux and convert to physical units
            flux_counts = catalog['flux'][idx]
            exptime = catalog.meta.get('EXPTIME', 1.0)

            # Get filter properties (simplified - would use filter curves in reality)
            filter_info = get_filter_info(filter_name)

            # Convert counts to flux density
            # Using AB magnitude system
            mag = catalog['magnitude'][idx]
            flux_density = (10**(-0.4 * (mag.value + 48.6))) * u.erg / u.s / u.cm**2 / u.Hz

            # Convert to fλ
            flux_lambda = flux_density * const.c / filter_info['wavelength']**2
            flux_lambda = flux_lambda.to(u.erg / u.s / u.cm**2 / u.angstrom)

            sed_data.append({
                'filter': filter_name,
                'wavelength': filter_info['wavelength'],
                'flux': flux_lambda,
                'flux_err': flux_lambda * 0.1,  # Assume 10% error
                'magnitude': mag,
                'separation': sep2d
            })

    # 2. Build SED table
    sed = QTable()
    sed['filter'] = [d['filter'] for d in sed_data]
    sed['wavelength'] = u.Quantity([d['wavelength'] for d in sed_data])
    sed['flux'] = u.Quantity([d['flux'] for d in sed_data])
    sed['flux_err'] = u.Quantity([d['flux_err'] for d in sed_data])
    sed['magnitude'] = u.Quantity([d['magnitude'] for d in sed_data])

    # Sort by wavelength
    sed.sort('wavelength')

    # 3. Add metadata
    sed.meta['RA'] = source_coord.ra.value
    sed.meta['DEC'] = source_coord.dec.value
    sed.meta['N_BANDS'] = len(sed)

    # 4. Calculate derived quantities
    # Bolometric flux (trapezoid integration)
    sed['log_wavelength'] = np.log10(sed['wavelength'].to(u.angstrom).value)
    sed['log_flux'] = np.log10(sed['flux'].to(u.erg/u.s/u.cm**2/u.angstrom).value)

    # 5. Plot SED
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.errorbar(sed['wavelength'].to(u.micron).value,
                sed['flux'].to(u.erg/u.s/u.cm**2/u.angstrom).value,
                yerr=sed['flux_err'].to(u.erg/u.s/u.cm**2/u.angstrom).value,
                fmt='ro', markersize=8, capsize=5)

    ax.set_xlabel('Wavelength (μm)')
    ax.set_ylabel(r'$f_\lambda$ (erg s$^{-1}$ cm$^{-2}$ Å$^{-1}$)')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_title(f'SED for {source_coord.to_string("hmsdms")}')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('sed.png', dpi=150)
    print("SED plot saved to sed.png")

    # 6. Save table
    sed.write(output_file, overwrite=True)
    print(f"SED table saved to {output_file}")

    return sed

def get_filter_info(filter_name):
    """Get filter central wavelength (simplified)."""
    filters = {
        'U': 365 * u.nm,
        'B': 445 * u.nm,
        'V': 551 * u.nm,
        'R': 658 * u.nm,
        'I': 806 * u.nm,
        'J': 1.22 * u.micron,
        'H': 1.63 * u.micron,
        'K': 2.19 * u.micron,
    }
    return {'wavelength': filters.get(filter_name, 500*u.nm)}

# Example usage
if __name__ == '__main__':
    target = SkyCoord(ra=150.123*u.deg, dec=2.456*u.deg)

    catalogs = {
        'B': 'catalog_B.fits',
        'V': 'catalog_V.fits',
        'R': 'catalog_R.fits',
        'I': 'catalog_I.fits',
    }

    sed = build_sed(target, catalogs)
    print(sed)
```

## Spectroscopic Redshift Measurement

Measure redshift from spectrum using line identification and cross-correlation.

```python
from specutils import Spectrum1D
from specutils.analysis import template_correlate
from specutils.manipulation import spectral_slab
from astropy.io import fits
import astropy.units as u
import numpy as np

def measure_redshift(spectrum_file, template_file=None):
    """
    Measure spectroscopic redshift.

    Parameters
    ----------
    spectrum_file : str
        Observed spectrum FITS file
    template_file : str, optional
        Template spectrum for cross-correlation

    Returns
    -------
    results : dict
        Redshift measurement results
    """

    # 1. Load observed spectrum
    print("Loading observed spectrum...")
    spectrum = Spectrum1D.read(spectrum_file)

    # 2. Identify emission lines (simple peak finding)
    print("Identifying emission lines...")

    # Common rest-frame emission lines (Angstroms)
    rest_lines = {
        'Lyα': 1215.67,
        'CIV': 1549.06,
        'CIII]': 1908.73,
        'MgII': 2798.75,
        '[OII]': 3727.42,
        'Hβ': 4861.33,
        '[OIII]': 5006.84,
        'Hα': 6562.82,
    }

    # Find peaks in spectrum
    from scipy.signal import find_peaks

    flux = spectrum.flux.value
    wavelength = spectrum.spectral_axis.to(u.angstrom).value

    # Smooth spectrum for peak finding
    from scipy.ndimage import gaussian_filter1d
    smoothed = gaussian_filter1d(flux, sigma=3)

    # Find peaks
    peaks, properties = find_peaks(smoothed, prominence=0.1*np.max(smoothed))
    peak_wavelengths = wavelength[peaks]

    print(f"Found {len(peaks)} peaks")

    # 3. Match peaks to known lines
    redshift_estimates = []

    for peak_wave in peak_wavelengths[:5]:  # Check top 5 peaks
        for line_name, rest_wave in rest_lines.items():
            z = (peak_wave / rest_wave) - 1

            if 0 < z < 6:  # Reasonable redshift range
                redshift_estimates.append({
                    'line': line_name,
                    'rest_wavelength': rest_wave,
                    'observed_wavelength': peak_wave,
                    'redshift': z
                })

    # Find most common redshift (within tolerance)
    if len(redshift_estimates) > 0:
        redshifts = np.array([est['redshift'] for est in redshift_estimates])
        # Cluster redshifts
        median_z = np.median(redshifts)
        consistent = np.abs(redshifts - median_z) < 0.01
        best_z = np.mean(redshifts[consistent])

        print(f"Initial redshift estimate: z = {best_z:.4f}")
        print(f"Based on {consistent.sum()} consistent lines")
    else:
        best_z = None
        print("Could not identify emission lines")

    # 4. Refine with template cross-correlation (if template provided)
    if template_file and best_z:
        print("Refining redshift with template correlation...")

        template = Spectrum1D.read(template_file)

        # Shift template to approximate redshift
        template_shifted = Spectrum1D(
            spectral_axis=template.spectral_axis * (1 + best_z),
            flux=template.flux
        )

        # Cross-correlate in overlapping region
        wave_min = max(spectrum.spectral_axis[0], template_shifted.spectral_axis[0])
        wave_max = min(spectrum.spectral_axis[-1], template_shifted.spectral_axis[-1])

        if wave_max > wave_min:
            # Extract overlapping regions
            spec_region = spectral_slab(spectrum, wave_min, wave_max)
            template_region = spectral_slab(template_shifted, wave_min, wave_max)

            # Correlate
            result = template_correlate(spec_region, template_region,
                                        redshift_range=(best_z-0.1, best_z+0.1),
                                        redshift_step=0.0001)

            refined_z = result[0]
            print(f"Refined redshift: z = {refined_z:.4f}")
        else:
            refined_z = best_z
            print("Insufficient wavelength overlap for correlation")
    else:
        refined_z = best_z

    # 5. Compile results
    results = {
        'redshift': refined_z,
        'n_lines_identified': len(redshift_estimates),
        'identified_lines': redshift_estimates,
        'peak_wavelengths': peak_wavelengths
    }

    return results

# Example usage
if __name__ == '__main__':
    results = measure_redshift('galaxy_spectrum.fits',
                               template_file='template_elliptical.fits')

    print(f"\nFinal redshift: z = {results['redshift']:.4f}")
    print(f"Identified {results['n_lines_identified']} emission lines")
```

## Observability Calculation

Calculate target observability from a specific location over time.

```python
from astropy.coordinates import SkyCoord, EarthLocation, AltAz, get_sun, get_moon
from astropy.time import Time
import astropy.units as u
import numpy as np
import matplotlib.pyplot as plt

def calculate_observability(target_coord, location, date,
                           min_altitude=30*u.deg,
                           max_airmass=2.0):
    """
    Calculate target observability for one night.

    Parameters
    ----------
    target_coord : SkyCoord
        Target coordinates
    location : EarthLocation
        Observatory location
    date : str
        Observation date (YYYY-MM-DD)
    min_altitude : Quantity
        Minimum altitude for observation
    max_airmass : float
        Maximum acceptable airmass

    Returns
    -------
    observability : dict
        Observability information
    """

    # 1. Set up time array for the night
    print(f"Calculating observability for {date} at {location.geodetic}")

    # Create time array (every 10 minutes for 24 hours)
    time_start = Time(date + ' 12:00:00')  # Start at noon local
    delta_t = np.arange(0, 24, 10/60) * u.hour
    times = time_start + delta_t

    # 2. Calculate target altitude over time
    altaz_frame = AltAz(obstime=times, location=location)
    target_altaz = target_coord.transform_to(altaz_frame)

    # 3. Calculate sun and moon positions
    sun_altaz = get_sun(times).transform_to(altaz_frame)
    moon_altaz = get_moon(times).transform_to(altaz_frame)

    # Moon illumination (simplified)
    from astropy.coordinates import get_body
    moon_phase = ((times.jd - 2451550.1) % 29.53) / 29.53  # Approximate

    # 4. Calculate observability criteria
    # Target above minimum altitude
    target_up = target_altaz.alt > min_altitude

    # Sun below -18 degrees (astronomical twilight)
    astronomical_night = sun_altaz.alt < -18*u.deg

    # Target away from sun
    sun_sep = target_altaz.separation(sun_altaz)
    away_from_sun = sun_sep > 45*u.deg

    # Airmass acceptable
    airmass = target_altaz.secz
    good_airmass = airmass < max_airmass

    # Combined observability
    observable = target_up & astronomical_night & away_from_sun & good_airmass

    # 5. Find observability windows
    # Find rising/setting times
    observable_times = times[observable]

    if len(observable_times) > 0:
        start_time = observable_times[0]
        end_time = observable_times[-1]
        duration = end_time - start_time

        print(f"Observable from {start_time.iso} to {end_time.iso}")
        print(f"Duration: {duration.to(u.hour):.1f}")

        # Best time (highest altitude during observable window)
        best_idx = observable_times[np.argmax(target_altaz.alt[observable])]
        best_alt = np.max(target_altaz.alt[observable])
        best_airmass = np.min(airmass[observable])

        print(f"Best time: {best_idx.iso}")
        print(f"  Altitude: {best_alt:.1f}")
        print(f"  Airmass: {best_airmass:.2f}")
    else:
        print("Target not observable on this night")
        start_time = None
        end_time = None
        duration = 0*u.hour
        best_idx = None

    # 6. Create visibility plot
    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    # Plot altitude
    hours = (times - time_start).to(u.hour).value

    axes[0].plot(hours, target_altaz.alt.deg, 'b-', linewidth=2, label='Target')
    axes[0].axhline(min_altitude.deg, color='r', linestyle='--',
                    label=f'Min altitude ({min_altitude})')
    axes[0].fill_between(hours, 0, 90,
                          where=astronomical_night,
                          alpha=0.2, color='gray', label='Night')
    axes[0].fill_between(hours, 0, 90,
                          where=observable,
                          alpha=0.3, color='green', label='Observable')
    axes[0].set_ylabel('Altitude (deg)')
    axes[0].set_ylim(0, 90)
    axes[0].legend(loc='upper right')
    axes[0].grid(True, alpha=0.3)
    axes[0].set_title(f'Visibility for {target_coord.to_string("hmsdms")}')

    # Plot airmass
    # Only plot when target is above horizon
    above_horizon = target_altaz.alt > 0*u.deg
    airmass_plot = np.where(above_horizon, airmass, np.nan)

    axes[1].plot(hours, airmass_plot, 'b-', linewidth=2)
    axes[1].axhline(max_airmass, color='r', linestyle='--',
                    label=f'Max airmass ({max_airmass})')
    axes[1].fill_between(hours, 0, 5,
                          where=observable,
                          alpha=0.3, color='green', label='Observable')
    axes[1].set_xlabel('Hours from Noon (local)')
    axes[1].set_ylabel('Airmass')
    axes[1].set_ylim(1, 5)
    axes[1].invert_yaxis()
    axes[1].legend(loc='upper right')
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('observability.png', dpi=150)
    print("Plot saved to observability.png")

    return {
        'observable': len(observable_times) > 0,
        'start_time': start_time,
        'end_time': end_time,
        'duration': duration,
        'best_time': best_idx,
        'best_altitude': best_alt if best_idx else None,
        'best_airmass': best_airmass if best_idx else None,
        'times': times,
        'altitudes': target_altaz.alt,
        'airmass': airmass,
        'observable_mask': observable
    }

# Example usage
if __name__ == '__main__':
    # Target: M31
    target = SkyCoord.from_name('M31')

    # Location: Mauna Kea
    observatory = EarthLocation(lat=19.8283*u.deg,
                               lon=-155.4783*u.deg,
                               height=4207*u.m)

    # Calculate for tonight
    obs_info = calculate_observability(
        target,
        observatory,
        '2024-01-15',
        min_altitude=30*u.deg,
        max_airmass=2.0
    )

    if obs_info['observable']:
        print(f"\nTarget is observable for {obs_info['duration']:.1f}")
    else:
        print("\nTarget is not observable")
```

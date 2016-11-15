#!/usr/bin/env python
import os

from astropy.table import Table

import lsst.afw.image as afwImage
import lsst.afw.image.utils as afwImageUtils
import lsst.daf.persistence as dafPersist

from forcedPhotExternalCatalog import ForcedPhotExternalCatalogTask
from sub_twinkles import transient_objects, repo_dir, find_science_dataIds, filename_to_visit

def run_forced_photometry(dataId, coord_file, repo_dir, dataset='calexp', verbose=True):
    # Should expand out dataId to be more detailed than just visit.
    args = [repo_dir,
            '--id', 'visit={:d}'.format(dataId['visit']),
            '--dataset', '{}'.format(dataset),
            '--coord_file', '{}'.format(coord_file),
            '--output', '{}'.format(repo_dir),
            '--clobber-config', '--clobber-versions',
           ]
    if verbose:
        print(args)
    ForcedPhotExternalCatalogTask.parseAndRun(args=args)


def assemble_catalogs_into_lightcurve(dataIds_by_filter, repo_dir, dataset='calexp', DEBUG=False):
    """Return Table with measurements."""
    butler = dafPersist.Butler(repo_dir)

    names_to_copy = ['objectId', 'coord_ra', 'coord_dec', 'parentObjectId',
                     'base_RaDecCentroid_x', 'base_RaDecCentroid_y',
                     'base_PsfFlux_flux', 'base_PsfFlux_fluxSigma']
    # flux_zp25 is flux normalized to a zeropoint of 25.
    # This convention is useful and appropriate for transient sources
    # that are expected to be negative as well as positive
    # for a given lightcurve.
    names_to_generate = ['filter', 'mjd',
                         'base_PsfFlux_mag', 'base_PsfFlux_magSigma',
                         'base_PsfFlux_flux_zp25', 'base_PsfFlux_fluxSigma_zp25']
    this_source = 0  # Take just the first source.

    names = names_to_generate + names_to_copy
    dtype = (str, float,
             float, float,
             float, float,
             long, float, float, long,
             float, float,
             float, float)
    table = Table(names=names, dtype=dtype)

    if dataset == 'deepDiff_differenceExp':
        prefix = 'deepDiff_'
    else:
        prefix = ''
    forced_dataset = prefix+'forcedRaDec_src'
    if DEBUG:
        print("FORCED_DATASET: ", forced_dataset)

    for f, dataIds in dataIds_by_filter.items():
        for dataId in dataIds:
            # Can grab filter, mjd from 'calexp_md' call on visit
            md = butler.get('calexp_md', dataId=dataId, immediate=True)
            mjd = md.get('MJD-OBS')
    #        filt = md.get('FILTER')  # But that's not being set right now so we'll keep using f

            this_measurement = butler.get(forced_dataset, dataId)
            # 'this_measurement' is a table, but we're only extracting the first entry from each column
            cols_for_new_row = {n: this_measurement[n][this_source] for n in names_to_copy}
    #        cols_for_new_row['filter'] = dataId['filter']
            cols_for_new_row['filter'] = f
            cols_for_new_row['mjd'] = mjd

            # Calibrate to magnitudes
            # The calibration information for the calexp
            # should still apply to the difference image
            calib = afwImage.Calib(md)
            with afwImageUtils.CalibNoThrow():
                cols_for_new_row['base_PsfFlux_mag'], cols_for_new_row['base_PsfFlux_magSigma'] = \
                    calib.getMagnitude(cols_for_new_row['base_PsfFlux_flux'],
                                       cols_for_new_row['base_PsfFlux_fluxSigma'])
            flux_mag_0, flux_magSigma_0 = calib.getFluxMag0()
            flux_mag_25 = 10**(-0.4*25) * flux_mag_0
            flux_norm = 1/flux_mag_25
            cols_for_new_row['base_PsfFlux_flux_zp25'] = flux_norm * cols_for_new_row['base_PsfFlux_flux']
            cols_for_new_row['base_PsfFlux_fluxSigma_zp25'] = flux_norm * cols_for_new_row['base_PsfFlux_fluxSigma']

            table.add_row(cols_for_new_row)

    return table


def test_assemble_catalogs_into_lightcurves():
    """Needs to have a run already existing to work."""
    # repo_dir  # From Global import above
    science_visits = {'r': [
        '255276',
        '2221459'
#        'v255276-fr',
#        'v2221459-fr'
        ]}
    obs = assemble_catalogs_into_lightcurve(science_visits, repo_dir)
    print(obs)


def test_find_science_images(name='Test1', verbose=True):
    """Did our search find any image."""
    for f in ('r'):
        obs = find_science_images(name, f, repo_dir)

    if verbose:
        print(obs)

    assert len(obs) >= 1


def make_catalogs(lightcurve_visits_for_sn, repo_dir, dataset='calexp'):
    for name, info in lightcurve_visits_for_sn.items():
        out_file = '{}_{}_lc.fits'.format(name, dataset)
        sn_lc = assemble_catalogs_into_lightcurve(lightcurve_visits_for_sn, repo_dir, dataset=dataset)
        sn_lc.write(out_file, overwrite=True)


def run_photometry(transient_objects, repo_dir, dataset='calexp',
                   RUN_PHOT=True, DEBUG=False):
    """Run photometry for given set of objects on all available images.

    RUN_PHOT : Run photometry.  If False then photometry is not run, but visits are gathered
    """
    lightcurve_visits = {}
    for name, sn in transient_objects.items():
        coord_file = '{}_ra_dec.txt'.format(name)

        lightcurve_visits_for_sn = {}
        print("Processing photometry for {}".format(name))
        for f in sn.keys():
            if VERBOSE:
                print("FILTER: ", f)
                print(name, f, repo_dir, dataset)
            lightcurve_visits_for_sn[f] = []
            dataIds = find_science_dataIds(name, f, repo_dir, dataset=dataset)
            # Restrict to first N, if requested
            if LIMIT_N:
                # If LIMIT_N > len(dataIds), that's fine.  [:LIMIT_N] will just get the full array.
                dataIds = dataIds[:LIMIT_N]

            if DEBUG:
                print("DATA IDS: ", dataIds)
            for dataId in dataIds:
                lightcurve_visits_for_sn[f].append(dataId)
                if RUN_PHOT:
                    run_forced_photometry(dataId, coord_file, repo_dir, dataset=dataset)
        lightcurve_visits[name] = lightcurve_visits_for_sn

    return lightcurve_visits_for_sn


if __name__ == "__main__":
    RUN_PHOT = False
    LIMIT_N = 10

    VERBOSE = True
    DEBUG = True

#    dataset = 'calexp'
    dataset = 'deepDiff_differenceExp'

    lightcurve_visits_for_sn = run_photometry(transient_objects, repo_dir, dataset, RUN_PHOT=RUN_PHOT)
    make_catalogs(lightcurve_visits_for_sn, repo_dir, dataset=dataset)

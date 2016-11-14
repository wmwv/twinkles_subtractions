#!/usr/bin/env python
import os

from astropy.table import Table

import lsst.daf.persistence as dafPersist

from forcedPhotExternalCatalog import ForcedPhotExternalCatalogTask
from sub_twinkles import transient_objects, repo_dir, calexp_repo_dir, forced_repo_dir, find_science_dataIds, filename_to_visit

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


def assemble_catalogs_into_lightcurve(dataIds_by_filter, repo_dir, dataset='calexp'):
    """Return Table with measurements."""
    butler = dafPersist.Butler(repo_dir)

    names_to_copy = ['objectId', 'coord_ra', 'coord_dec', 'parentObjectId',
                     'base_RaDecCentroid_x', 'base_RaDecCentroid_y',
                     'base_PsfFlux_flux', 'base_PsfFlux_fluxSigma']
    names_to_generate = ['filter', 'mjd']
    this_source = 0  # Take just the first source.

    names = names_to_generate + names_to_copy
    dtype = (str, float, long, float, float, long, float, float, float, float)
    table = Table(names=names, dtype=dtype)

    for f, dataIds in dataIds_by_filter.items():
        for dataId in dataIds:
            # Can grab filter, mjd from 'calexp_md' call on visit
            md = butler.get('calexp_md', dataId=dataId, immediate=True)
            mjd = md.get('MJD-OBS')
    #        filt = md.get('FILTER')  # But that's not being set right now so we'll keep using f

            this_measurement = butler.get('forcedRaDec_src', dataId)
            # 'this_measurement' is a table, but we're only extracting the first entry from each column
            cols_for_new_row = {n: this_measurement[n][this_source] for n in names_to_copy}
    #        cols_for_new_row['filter'] = dataId['filter']
            cols_for_new_row['filter'] = f
            cols_for_new_row['mjd'] = mjd
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


if __name__ == "__main__":
    RUN_PHOT = True
    LIMIT_N = None

    VERBOSE = True
    DEBUG = True

#    dataset = 'calexp'
    dataset = 'deepDiff_differenceExp'
    for name, sn in transient_objects.items():
        coord_file = '{}_ra_dec.txt'.format(name)
        out_file = '{}_{}_lc.fits'.format(name, dataset)

        print("Processing photometry for {}".format(name))
        lightcurve_visits_for_sn = {}
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

        sn_lc = assemble_catalogs_into_lightcurve(lightcurve_visits_for_sn, forced_repo_dir, dataset=dataset)
        sn_lc.write(out_file, overwrite=True)

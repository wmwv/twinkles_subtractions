#!/usr/bin/env python

import argparse
import sys

import numpy as np
import matplotlib.pyplot as plt

from astropy.table import Table

if __name__ == "__main__":
    description = """
    Plot a FITS binary table lightcurve.  
    Requires columns of 'base_PsfFlux_mag', 'base_PsfFlux_magSigma'
    'base_PsfFlux_flux_zp25', 'base_PsfFlux_fluxSigma_zp25'
    where 'zp25' means the flux has been calibrated to a zp of 25.
    I.e., for positive flux values:
    mag = -2.5*log10(flux) + 25
    """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('plot_file', type=str, help="Lightcurve file to plot.")
    parser.add_argument('--mag', dest='plot_mag', default=False, action='store_true',
                        help='Plot magnitudes')
    parser.add_argument('--no_mag', dest='plot_mag', action='store_false')
    parser.add_argument('--flux', dest='plot_flux', default=True, action='store_true',
                        help='Plot normalized flux (zp=25).')
    parser.add_argument('--no_flux', dest='plot_flux', default=True, action='store_false')

    args = parser.parse_args()

    data = Table.read(args.plot_file)

    color = {'u': 'cyan', 'g': 'blue', 'r': 'green', 'i': 'red', 'z': 'm', 'y': 'black'}
    filters = ['u', 'g', 'r', 'i', 'z', 'y']
    if args.plot_mag:
        for f in filters:
            wf, = np.where(data['filter'] == f)
            if len(wf) < 1:
                continue
            dataf = data[wf]
            plt.errorbar(dataf['mjd'], dataf['base_PsfFlux_mag'], dataf['base_PsfFlux_magSigma'], linestyle='none', color=color[f])

        plt.xlabel('MJD')
        plt.ylabel('base_PsfFlux_mag')
        ylim = plt.ylim()
        plt.ylim(max(ylim), min(ylim))
        plt.show()

    if args.plot_flux:
        for f in filters:
            wf, = np.where(data['filter'] == f)
            if len(wf) < 1:
                continue
            dataf = data[wf]
            plt.errorbar(dataf['mjd'], dataf['base_PsfFlux_flux_zp25'], dataf['base_PsfFlux_fluxSigma_zp25'], linestyle='none', color=color[f])
        plt.xlabel('MJD')
        plt.ylabel('flux_zp25  [mag = -2.5*log10(flux) + 25]')
        plt.show()


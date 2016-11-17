#!/usr/bin/env python

import argparse
import os
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
    parser.add_argument('--png', default=False, action="store_true",
                        help="Save plot as PNG file")
    parser.add_argument('--pdf', default=False, action="store_true",
                        help="Save plot as PDF file")
    parser.add_argument('--show', dest='show', default=True, action="store_true",
                        help="Show plots to the screen")
    parser.add_argument('--noshow', dest='show', action="store_false",
                        help="Don't show plots to the screen")

    args = parser.parse_args()

    suffixes = []
    if args.png:
        suffixes.append('.png')
    if args.pdf:
        suffixes.append('.pdf')

    plotbase, _ = os.path.splitext(args.plot_file)

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
        plt.ylim(27,15)
        ylim = plt.ylim()
        plt.ylim(max(ylim), min(ylim))

        plotname = plotbase+'_mag'
        for s in suffixes:
            plt.savefig(plotname+s)

        if args.show:
            plt.show()
        plt.clf()

    if args.plot_flux:
        for f in filters:
            wf, = np.where(data['filter'] == f)
            if len(wf) < 1:
                continue
            dataf = data[wf]
            plt.errorbar(dataf['mjd'], dataf['base_PsfFlux_flux_zp25'], dataf['base_PsfFlux_fluxSigma_zp25'], linestyle='none', color=color[f])
        plt.xlabel('MJD')
        plt.ylabel('flux_zp25  [mag = -2.5*log10(flux) + 25]')

        plotname = plotbase+'_flux'
        for s in suffixes:
            plt.savefig(plotname+s)

        if args.show:
            plt.show()
        plt.clf()

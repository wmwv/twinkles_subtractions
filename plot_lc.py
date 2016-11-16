#!/usr/bin/env python

import sys

import matplotlib.pyplot as plt

from astropy.table import Table

if __name__ == "__main__":
    plot_file = sys.argv[1]

    plot_mag = True
    plot_flux = True

    data = Table.read(plot_file)

    if plot_mag:
        plt.errorbar(data['mjd'], data['base_PsfFlux_mag'], data['base_PsfFlux_magSigma'], linestyle='none')
        plt.xlabel('MJD')
        plt.ylabel('base_PsfFlux_mag')
        ylim = plt.ylim()
        plt.ylim(max(ylim), min(ylim))
        plt.show()

    if plot_flux:
        plt.errorbar(data['mjd'], data['base_PsfFlux_flux_zp25'], data['base_PsfFlux_fluxSigma_zp25'], linestyle='none')
        plt.xlabel('MJD')
        plt.ylabel('flux_zp25  [mag = -2.5*log10(flux) + 25]')
        plt.show()


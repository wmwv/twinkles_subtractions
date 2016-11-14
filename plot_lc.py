#!/usr/bin/env python

import sys

import matplotlib.pyplot as plt

from astropy.table import Table

if __name__ == "__main__":
    plot_file = sys.argv[1]

    data = Table.read(plot_file)

    plt.errorbar(data['mjd'], data['base_PsfFlux_flux'], data['base_PsfFlux_fluxSigma'], linestyle='none')
    plt.xlabel('MJD')
    plt.ylabel('base_PsfFlux_flux')

    plt.show()

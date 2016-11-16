#!/usr/bin/env python

from twinkles_forcedPhotExternalCatalog import create_coord_file_from_diaSrc
from sub_twinkles import repo_dir

dataId = {'visit': 2210949, 'filter': 'r'}

create_coord_file_from_diaSrc(dataId, repo_dir, out_file='coord_ra_dec.csv')

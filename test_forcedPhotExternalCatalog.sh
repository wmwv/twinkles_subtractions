#!/bin/bash

source /global/common/cori/contrib/lsst/lsstDM/setupStack-12_1.sh
setup -j -r /global/homes/w/wmwv/lsst/obs_lsstSim
setup -j -r /global/homes/w/wmwv/lsst/meas_base

TMP=/global/homes/w/wmwv/Twinkles
OUTREPO=${TMP}/Run1.1

SCIENCE_IMAGE=1940246
TEMPLATE_IMAGE=255276

coord_file=test_ra_dec.txt

# Single epoch science stack
python forcedPhotExternalCatalog.py "${OUTREPO}" --output "${OUTREPO}" --id visit="${SCIENCE_IMAGE}" --coord_file "${coord_file}" --clobber-versions
# Subtraction
#  Should add a dataset option or something to select 'diffim' instead of 'exposure'
# python forcedPhotExternalCatalog.py "${OUTREPO}" --output "${OUTREPO}" --id visit="${SCIENCE_IMAGE}" --coord_file "${coord_file}" --clobber-versions

Twinkles single-image subtractions and forced photometry 

Explorations by Michael Wood-Vasey <wmwv@pitt.edu>


source /global/common/cori/contrib/lsst/lsstDM/setupStack-12_1.sh
setup lsst_apps
setup ip_diffim
setup -j -r /global/homes/w/wmwv/lsst/obs_lsstSim
# SHA1 8d21232
setup -j -r /global/homes/w/wmwv/lsst/meas_base
# SHA1 70cb64f


1. Run a set of r-band subtractions against the first r-band image for Run 1.1
sh run_imageDifference_run1.1.sh

2. Run forced-photometry on the calexp images
python twinkles_forcedPhotExternalCatalog.py

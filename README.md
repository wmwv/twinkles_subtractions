Twinkles single-image subtractions and forced photometry 

Explorations by Michael Wood-Vasey <wmwv@pitt.edu>

```
source /global/common/cori/contrib/lsst/lsstDM/setupStack-12_1.sh
setup -j -r /global/homes/w/wmwv/lsst/obs_lsstSim
# SHA1 8d21232
setup -j -r /global/homes/w/wmwv/lsst/meas_base
# SHA1 70cb64f
```


1. Run a set of r-band subtractions against the first r-band image for Run 1.1
```
sh run_imageDifference_run1.1.sh
```

2. Generate a catalog from a selected diaSrc for a arbitrarily seleted r-band visit
```
python make_coord_file.py
```

Currently visit and outfile are hardcoded.  Would like to eventually expand make_coord_file.py to accept argument, such as

```
python make_coord_file.py --out_file coord_ra_dec.csv --id visit=2210949 filter=r
```

3. Run forced-photometry on the calexp images
```
python twinkles_forcedPhotExternalCatalog.py coord_ra_dec.csv --dataset calexp 
python twinkles_forcedPhotExternalCatalog.py coord_ra_dec.csv --dataset deepDiff_differenceExp
```

This will take a while, so if you're running interactively, you may wish to use `nohup`.  E.g.,

```
nohup python twinkles_forcedPhotExternalCatalog.py coord_ra_dec.csv --dataset deepDiff_differenceExp > phot_all.log 2>&1 < /dev/null &
```

#!/bin/bash

REPO=/global/u1/j/jchiang8/twinkles/Run1.1
# SCIENCE_IMAGE=v1940246-fr
# TEMPLATE_IMAGE=v255276-fr
SCIENCE_IMAGE=1940246
TEMPLATE_IMAGE=255276

TMP=/global/homes/w/wmwv/Twinkles
OUTREPO=${TMP}/Run1.1
imageDifference.py ${REPO} @science_image.ids --templateId visit=${TEMPLATE_IMAGE} --output ${OUTREPO} --configfile diffimconfig.py --clobber-config --no-versions > Run1.1_diff_r.log 2>&1 
# imageDifference.py ${REPO} --id visit=1172797 filter=r --templateId visit=${TEMPLATE_IMAGE} --output ${OUTREPO} --configfile diffimconfig.py --clobber-config --no-versions > Run1.1_diff_r.log 2>&1 
# imageDifference.py ${REPO} --id @science_image.ids filter=r --templateId visit=${TEMPLATE_IMAGE} --output ${OUTREPO} --configfile diffimconfig.py --clobber-config --no-versions > Run1.1_diff_r.log 2>&1 
#imageDifference.py ${REPO} --id r${SCIENCE_IMAGE}^2171023^959459 --templateId visit=${TEMPLATE_IMAGE} --output ${OUTREPO} --configfile diffimconfig.py > ${SCIENCE_IMAGE}_${TEMPLATE_IMAGE}.log --clobber-config --no-versions 2>&1 

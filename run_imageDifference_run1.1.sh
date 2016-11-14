#!/bin/bash

REPO=/global/u1/j/jchiang8/twinkles/Run1.1
TEMPLATE_IMAGE_u=999525
TEMPLATE_IMAGE_g=997764
TEMPLATE_IMAGE_r=255276
TEMPLATE_IMAGE_i=997774
TEMPLATE_IMAGE_z=997794
TEMPLATE_IMAGE_y=997820

TMP=/global/homes/w/wmwv/Twinkles
OUTREPO=${TMP}/Run1.1
imageDifference.py ${REPO} @science_image_u.ids --templateId visit=${TEMPLATE_IMAGE_u} --output ${OUTREPO} --configfile diffimconfig.py --clobber-config --no-versions > Run1.1_diff_u.log 2>&1 
imageDifference.py ${REPO} @science_image_g.ids --templateId visit=${TEMPLATE_IMAGE_g} --output ${OUTREPO} --configfile diffimconfig.py --clobber-config --no-versions > Run1.1_diff_g.log 2>&1 
imageDifference.py ${REPO} @science_image_r.ids --templateId visit=${TEMPLATE_IMAGE_r} --output ${OUTREPO} --configfile diffimconfig.py --clobber-config --no-versions > Run1.1_diff_r.log 2>&1 
imageDifference.py ${REPO} @science_image_i.ids --templateId visit=${TEMPLATE_IMAGE_i} --output ${OUTREPO} --configfile diffimconfig.py --clobber-config --no-versions > Run1.1_diff_i.log 2>&1 
imageDifference.py ${REPO} @science_image_z.ids --templateId visit=${TEMPLATE_IMAGE_z} --output ${OUTREPO} --configfile diffimconfig.py --clobber-config --no-versions > Run1.1_diff_z.log 2>&1 
imageDifference.py ${REPO} @science_image_y.ids --templateId visit=${TEMPLATE_IMAGE_y} --output ${OUTREPO} --configfile diffimconfig.py --clobber-config --no-versions > Run1.1_diff_y.log 2>&1 

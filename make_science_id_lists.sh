for f in u g r i z y; do
    ls Run1.1/_parent/calexp/ | grep -- -f${f} | sed -e 's/v\(.*\)-f[ugrizy]/\1/' | awk '{printf "--id visit=%s\n", $1}' > science_image_${f}.ids
done

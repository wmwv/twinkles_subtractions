import glob
import os

# The following supernovae need host-galaxy subtractions
# and the templates are available as of DR1.
transient_objects = {
     'test':                   {'r': '255276'},
}
repo_dir = os.path.join(os.getenv('HOME'), 'Twinkles', 'Run1.1')
forced_repo_dir = repo_dir
calexp_repo_dir = os.path.join(forced_repo_dir, '_parent')


def find_science_images(sn, f, repo_dir):
    """
    >>> repo_dir = '/global/u1/j/jchiang8/twinkles/Run1.1'
    >>> images = find_science_images(None, 'r', repo_dir)
    >>> len(images) > 1
    True
    """
    sn_search_regex = os.path.join(repo_dir, 'calexp', '*-f{}'.format(f), 'R22', 'S11.fits')
    sn_files = glob.glob(sn_search_regex)
    return sn_files


def filename_to_visit(filename):
    """
    >>> visit = filename_to_visit('/global/u1/j/jchiang8/twinkles/Run1.1/calexp/v2221459-fr/R22/S11.fits')
    >>> print(visit)
    2221459
    """
    import re

    visit_dirname = os.path.basename(os.path.dirname(os.path.dirname(filename)))
    visit = re.findall('v([0-9]+)-fr', visit_dirname)[0]
    return int(visit)


def run_repo_based_subtraction(science_file, template_file, repo_dir, verbose=True):
    """Run a subtraction using the Butler"""
    science_fileroot = filename_to_fileroot(science_file)
    template_fileroot = filename_to_fileroot(template_file)
    args = [repo_dir,
            '--id', 'fileroot={}'.format(science_fileroot),
            '--templateId', 'fileroot={}'.format(template_fileroot),
            '--output', repo_dir,
            '--configfile', 'diffimconfig.py',
            '--logdest', 'wiyn_imageDifference.log',
            '--clobber-config', '--clobber-versions',
           ]
    from lsst.pipe.tasks.imageDifference import ImageDifferenceTask

    if verbose:
        print("Running ImageDifferenceTask.parseAndrun with args:")
        print(args)
    ImageDifferenceTask.parseAndRun(args=args)


if __name__ == "__main__":
#    for sn in transient_objects:
#        find_and_generate_lsst_files(sn)

    # Do we run subtraction directly from files
    # or use the repo-based Butler interface
    repo_based = True

    for name, templates in transient_objects.items():
        print("Processing {}".format(name))
        for f in templates.keys():
            template_file = os.path.join(repo_dir, 'calexp', templates[f])
            for science_file in find_science_images(name, f, calexp_repo_dir):
                if science_file == template_file:
                    continue

                run_repo_based_subtraction(science_file, template_file, repo_dir)


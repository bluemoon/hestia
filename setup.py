from setuptools import setup, find_packages
from dulwich.repo import Repo
import os

def version(version):
    version = get_version(version)
    write_version(version)
    return version

def get_version(version):
    repo = Repo(".")
    commit_count = len(repo.revision_history(repo.head())) + 1
    return version + ".%da" % commit_count
    
def write_version(version):
    from hestia.__version__ import version as version_
    if version == version_:
        return
    
    directory = os.path.dirname(__file__)
    f = open(os.path.join(directory, 'py', 'hestia', '__version__.py'), 'w')
    f.write("# This file is auto-generated.\n")
    f.write("version = %r\n" % version)
    f.close()


setup(
    name = "hestia",
    version = version("0.0.5"),
    packages = find_packages('py'),
    package_dir = {'':'py'},
    data_files = [ ("share/notifier/icons", ['data/24-em-check.png','data/24-em-cross.png']) ],
    zip_safe=False,
    include_package_data=True,
    license='GPL',
    author='Alex Toney',
    author_email='toneyalex@gmail.com',
    test_suite="nose.collector",
    tests_require="nose",
    entry_points = {
        'console_scripts': [
            'hestia = hestia.main:main',
            ],
        #'hestia.ui' : ['hestia.ui=hestia.ui']
        }
)

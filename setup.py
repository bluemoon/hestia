from setuptools import setup, find_packages
from dulwich.repo import Repo
import os
import sys

VERSION = "0.5"


class file_versions:
    def __init__(self, file_name, increment=True, base="", string_format=".b%d"):
        self.file_name = file_name
        self.autoincrement = increment
        self.formatting_string = string_format
        self.base_version = base
        
    def get_version(self):
        if not os.path.exists(self.file_name):
            return 0
        else:
            fhandle = open(self.file_name, 'r')
            line = fhandle.readline()
            build = int(line)
            fhandle.close()
            
        return build
    
    def write_version(self, version=0):
        fhandle = open(self.file_name, 'w')
        fhandle.write(str(version))
        fhandle.close()

    def _version(self):
        version = self.get_version()
        if self.autoincrement and 'install' in sys.argv:
            version += 1
        self.write_version(version)
        return self.base_version + self.formatting_string % (version)

    def version(self):
        return self._version()

    def __add__(self, other):
        return self.version() + other.version()

class repo_versions(file_versions):
    def get_version(self):
        repo = Repo(".")
        commit_count = len(repo.revision_history(repo.head())) + 1
        return commit_count
    
    def write_version_file(self, version):
        directory = os.path.dirname(__file__)
        f = open(os.path.join(directory, 'src', 'hestia', '__version__.py'), 'w')
        f.write("# This file is auto-generated.\n")
        f.write("version = %r\n" % version)
        f.close()        


    
build_version = file_versions('.build_num')
repo_version = repo_versions('.repo_num', base=VERSION, string_format=".%s", increment=False)
repo_version.write_version_file(repo_version + build_version)

setup(
    name = "hestia",
    version = repo_version + build_version,
    packages = find_packages('src'),
    package_dir = {'':'src'},
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

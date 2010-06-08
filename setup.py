from setuptools import setup, find_packages
from dulwich.repo import Repo
import os
import sys

class file_versions:
    def __init__(self, file_name, autoincrement=True):
        self.file_name = file_name
        self.autoincrement = autoincrement
        self.formatting_string = ".b%d"
        
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

    def version(self):
        version = self.get_version()
        if self.autoincrement:
            version += 1
        self.write_version(version)
        return self.formatting_string % (version)


build_version = file_versions('.build_num')

def version(version):
    version = get_version(version)
    write_version(version)
    return version

def get_build():
    file_name = '.build_num'
    if not os.path.exists(file_name):
        return 0
    else:
        fhandle = open(file_name, 'r')
        line = fhandle.readline()
        build = int(line)
        fhandle.close()
        
    return build

def write_build(build=0):
    file_name = '.build_num'
    fhandle = open(file_name, 'w')
    fhandle.write(str(build))
    fhandle.close()

def build():
    build = get_build()
    if 'install' in sys.argv:
        build += 1        

    write_build(build)
    return ".b%d" % (build)

def get_version(version):
    repo = Repo(".")
    commit_count = len(repo.revision_history(repo.head())) + 1
    return version + ".%d" % commit_count
    
def write_version(version):
    from hestia.__version__ import version as version_
    if version == version_:
        return
    
    directory = os.path.dirname(__file__)
    f = open(os.path.join(directory, 'src', 'hestia', '__version__.py'), 'w')
    f.write("# This file is auto-generated.\n")
    f.write("version = %r\n" % version)
    f.close()


setup(
    name = "hestia",
    version = version("0.5") + build(),
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

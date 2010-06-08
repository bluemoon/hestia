from setuptools import setup, find_packages
from dulwich.repo import Repo

repo = Repo(".")
commit_count = len(repo.revision_history(repo.head()))
setup(
    name = "hestia",
    version = "0.0.5" + ".%da" % commit_count,
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
            ]
        }
)

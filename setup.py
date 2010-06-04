from setuptools import setup, find_packages
setup(
    name = "hestia",
    version = "0.0.0.2a",
    packages = find_packages(),
    data_files = [ ("share/notifier/icons", ['data/24-em-check.png','data/24-em-cross.png']) ],
    author='Alex Toney',
    author_email='toneyalex@gmail.com',
)

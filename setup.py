from setuptools import setup, find_packages
setup(
    name = "hestia",
    version = "0.0.0.3b",
    packages = find_packages('py'),
    package_dir = {'':'py'},
    data_files = [ ("share/notifier/icons", ['data/24-em-check.png','data/24-em-cross.png']) ],
    zip_safe=False,
    license='GPL',
    author='Alex Toney',
    author_email='toneyalex@gmail.com',
    entry_points = {
        'console_scripts': [
            'hestia = hestia.main:main',
            ]
        }
)

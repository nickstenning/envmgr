import sys

from setuptools import setup, find_packages

from envmgr import __version__

if sys.version_info < (2, 7):
    install_requires = ['argparse']
else:
    install_requires = []

setup(
    name='envmgr',
    version=__version__,
    packages=find_packages(),

    # metadata for upload to PyPI
    author='Nick Stenning',
    author_email='nick@whiteink.com',
    url='https://github.com/nickstenning/envmgr',
    description='envmgr: control the environment of spawned programs with config files',
    license='MIT',
    keywords='sysadmin process environment',
    test_suite='test',
    install_requires=install_requires,

    entry_points={
        'console_scripts': [
            'envmgr = envmgr.command:envmgr'
        ]
    }
)

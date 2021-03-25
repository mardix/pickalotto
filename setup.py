"""
PickALotto

Want to win the lottery? Great!

PickALotto will randomly select unique numbers for you to play in Powerball and
MegaMillion Lottery. The numbers can then be saved in .CSV file to be checked
later on after the winning number comes out.

DISCLAIMER: We should not be held responsible for any loss of money. Gamble responsibly
PickALotto doesn't guarantee any win. Most likely you will lose.
Actually, even before you start playing you are already at a loss. But this script is a fun exercise.
But if in case you win any money, don't forget about me :). Email me at: mardix@pylot.io


License: MIT

"""

from setuptools import setup
import pickalotto

PACKAGE = pickalotto

setup(
    name=PACKAGE.NAME,
    version=PACKAGE.__version__,
    license="MIT",
    author="Mardix",
    author_email="mardix@pylot.io",
    description="This program helps you randomly pick lottery numbers for Powerball and Megamillions",
    long_description=__doc__,
    url='http://github.com/mardix/pickalotto/',
    download_url='http://github.com/mardix/pickalotto/tarball/master',
    py_modules=['pickalotto'],
    entry_points=dict(console_scripts=['pickalotto=pickalotto:main']),
    keywords=['lottery', 'powerball', 'megamillion'],
    platforms='any',
    install_requires=['pyyaml==5.4'],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    zip_safe=False
)
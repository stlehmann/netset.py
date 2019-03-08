from setuptools import setup
from netset import __version__


setup(
    name='netset',
    version=__version__,
    description='A network configuration tool for the commandline, written '
                'in Python.',
    url='https://github.com/MrLeeh/netset.py',
    license='MIT',
    keywords='network',
    install_requires=[
        'click>=6.7',
        'pywin32>=220',
        'tabulate>=0.7.7',
        'wmi>=1.4.9'
    ],
    py_modules=['netset'],
    entry_points={
        'console_scripts': [
            'netset=netset:main'
        ]
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.6',
        'Topic :: System :: Networking',
        'Topic :: Utilities'
    ]
)

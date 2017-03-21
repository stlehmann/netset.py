from setuptools import setup


setup(
    name='netset',
    version='0.0.1',
    description='A network configuration tool for the commandline, written'
                'in Python',
    url='https://github.com/MrLeeh/netset.py',
    license='MIT',
    keywords='network',
    install_requires=[
        'click>=6.7',
        'pypiwin32>=220',
        'tabulate>=0.7.7',
        'wmi>=1.4.9'
    ],
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

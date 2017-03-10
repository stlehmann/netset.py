from setuptools import setup


setup(
    name='netset',
    version='0.0.1',
    description='A network configuration tool for the commandline, written'
                'in Python',
    url='',
    license='MIT',
    classifiers=[],
    keywords='network',
    entry_points={
        'console_scripts': [
            'netset=netset:main'
        ]
    }
)
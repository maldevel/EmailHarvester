from setuptools import setup, find_packages

from email_harvester import __version__


with open('README.md', 'r') as f:
    long_description = f.read()


with open('requirements.txt', 'r') as f:
    dependencies = f.read().splitlines()


setup(
    name='email_harvester',
    version=__version__,
    packages=find_packages(),
    install_requires=dependencies,
    description='Email Harvester by maldevel',
    long_description=long_description,
    long_description_contest_type='text/markdown',
    author='maldevel',
    url='https://github.com/maldevel/EmailHarvester',
    entry_points={
        'console_scripts': [
            'email_harvester = email_harvester.cli:main'
        ]
    },
    python_requires='>=3.0.0'
)

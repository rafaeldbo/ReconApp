import os
from setuptools import setup, find_packages


PATH = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(PATH, 'requirements.txt'), 'r') as file:
    requirements = file.readlines()

setup(
    name='recon-app',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'recon=recon.main:main',
        ],
    },
)

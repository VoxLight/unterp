from setuptools import setup, find_packages

setup(
    name='unterp',
    description='Minimalistic Python interpreter',

    version='0.1.0',
    author='VoxLight',

    packages=find_packages(),

    install_requires=[
        'pygments',
    ],

    entry_points={
        'console_scripts': [
            'unterp=unterp.__main__:main',
        ],
    },

)

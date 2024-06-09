from setuptools import setup, find_packages

setup(
    name='unterp',
    version='1.0.1',
    description='Minimalistic Python Interpreter with a GUI',
    author='VoxLight',
    author_email='tkkt392@gmail.com',
    url='https://github.com/VoxLight/unterp',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['icons/*.ico', 'icons/*.png'],
    },
    install_requires=[
        'Pillow',
        'Pygments',
    ],
    entry_points={
        'console_scripts': [
            'unterp=unterp.__main__:main',
        ],
    },
)

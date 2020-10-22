from setuptools import find_packages, setup

setup(
    name='pypairing',
    packages=find_packages(include=['pypairing']),
    version='0.0.1',
    description='Create stable pairs',
    author='Clarence Ho',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)
from setuptools import setup, find_packages

with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

setup(
        name='beblue.replicator',
        version='0.1',
        packages=find_packages('src'),
        install_requires=requirements,
        package_dir = {'': 'src'},
        namespace_packages = ['beblue'],
        entry_points={
            'console_scripts': [
                'start_replication=beblue.replicator.main:run',
                ],
            },
)

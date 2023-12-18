from setuptools import setup, find_packages


with open('README.md') as file:
    description = file.read()

with open('requirements.txt') as file:
    requirements = [_.strip() for _ in file]


setup(
    name='hse_normalizer',
    version='1.0.0',
    description='Converts text from written form into its verbalized form',
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.11',
    ],
    packages=find_packages(),
    install_requires=requirements,
)

from setuptools import setup, find_packages

with open('README') as f:
    long_description = ''.join(f.readlines())


setup(
    name='npimp',
    version='0.1',
    description='Regualate serveral notebook params',
    long_description=long_description,
    author='Tomáš Kukrál',
    author_email='tomas.kukral@6shore.net',
    license='MIT',
    url='https://github.com/tomkukral/ntbpimp/',
    packages=find_packages(),
    zip=False,
    install_requires=['paho-mqtt']
)

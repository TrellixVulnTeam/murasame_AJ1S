## ============================================================================
##             **** Murasame Application Development Framework ****
##                Copyright (C) 2019-2021, Suisei Entertainment
## ============================================================================
##
##  Licensed under the Apache License, Version 2.0 (the "License");
##  you may not use this file except in compliance with the License.
##  You may obtain a copy of the License at
##
##      http://www.apache.org/licenses/LICENSE-2.0
##
##  Unless required by applicable law or agreed to in writing, software
##  distributed under the License is distributed on an "AS IS" BASIS,
##  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##  See the License for the specific language governing permissions and
##  limitations under the License.
##
## ============================================================================

"""
Contains the setup script of the package.
"""

## ============================================================================
##     THIS IS A GENERATED FILE. DO NOT MODIFY IT MANUALLY.
## ============================================================================

# Platform Imports
import os
from setuptools import Command, setup

class CleanCommand(Command):

    """
    Custom clean command to remove unwanted files and directories after the
    build.
    """
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        os.system('rm -vrf ./build ./*.egg-info')

with open('./README.md', 'r') as readme_file:
    long_description = readme_file.read()

setup(
    name='murasame',
    version='0.1.0',
    author='Suisei Entertainment',
    author_email='info@suiseientertainment.com',
    description='Python application development framework used by Suisei '
                'Entertainment.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/suisei-entertainment/murasame',
    python_requires='>=3.8',
    namespace_packages=['murasame'],
    packages=['murasame', 'murasame.utils'],
    install_requires=['py-cpuinfo>=4.0.0', 'psutil>=5.4.8', 'netifaces>=0.10.7', 'distro>=1.3.0', 'wget>=3.2', 'requests>=2.23.0', 'geoip2', 'cryptography>=2.4.2', 'bcrypt>=3.1.7', 'protobuf>=3.11.2', 'termcolor>=1.1.0', 'coloredlogs>=10.0', 'flask>=1.1.1', 'Flask-Session>=0.3.1', 'sentry-sdk', 'influxdb>=5.3.0', 'redis>=3.5.2'],
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Topic :: Games/Entertainment',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Development Status :: 2 - Pre-Alpha'
    ],
    cmdclass={
        'clean': CleanCommand
    }
    )

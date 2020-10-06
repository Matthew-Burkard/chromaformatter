# Copyright © 2020 Matthew Burkard
#
# This file is part of Chroma Logging.
#
# Chroma Logging is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Chroma Logging is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Chroma Logging.  If not, see <https://www.gnu.org/licenses/>.

from setuptools import setup

setup(
    name='chromalogging',
    version='1.0.0',
    url='https://gitlab.com/mburkard/chroma-logging',
    license='MIT',
    author='Matthew Burkard',
    author_email='matthewjburkard@gmail.com',
    description='Wrapper for the Python logging module to add color.',
    package_dir={'': 'src'},
    packages=['chromalogging'],
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GPL-3 License'
    ],
    install_requires=['colorama'],
    zip_safe=False
)

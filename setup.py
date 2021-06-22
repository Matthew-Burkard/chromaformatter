# Copyright © 2020 Matthew Burkard
#
# This file is part of Chroma Formatter.
#
# Chroma Formatter is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Chroma Formatter is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Chroma Formatter.  If not, see <https://www.gnu.org/licenses/>.

from setuptools import setup

setup(
    name='chromaformatter',
    version='5.0.3',
    url='https://gitlab.com/mburkard/chroma-formatter',
    license='GNU General Public License v3 (GPLv3)',
    author='Matthew Burkard',
    author_email='matthewjburkard@gmail.com',
    description='Wrapper for the Python logging module to add color.',
    package_dir={'': 'src'},
    packages=['chromaformatter'],
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
    ],
    install_requires=['colorama'],
    zip_safe=False
)

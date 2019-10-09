from setuptools import setup

setup(
    name='chromalogging',
    version='0.0.1',
    url='https://gitlab.com/mburkard/chroma-logging',
    license='MIT',
    author='Matthew Burkard',
    author_email='matthewjburkard@gmail.com',
    description='Python logging module wrapper with colored output.',
    package_dir={'': 'src'},
    packages=['chromalogging'],
    long_description=open('README.md').read(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
    ],
    install_requires=['sty'],
    zip_safe=False
)
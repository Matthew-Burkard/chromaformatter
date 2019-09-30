from setuptools import setup

setup(
    name='chroma-logging',
    version='1.0',
    url='https://gitlab.com/mburkard/chroma-logging',
    license='MIT',
    author='Matthew Burkard',
    author_email='matthewjburkard@gmail.com',
    description='Python logging module with colored output.',
    package_dir={'': 'src'},
    packages=['chromalogging'],
    long_description=open('README.rst').read(),
    zip_safe=False,
    install_requires=['sty']
)

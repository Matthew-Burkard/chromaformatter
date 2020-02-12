from setuptools import setup

setup(
    name='chromalogging',
    version='0.1.2',
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
        'License :: OSI Approved :: MIT License'
    ],
    install_requires=['colorama'],
    zip_safe=False
)

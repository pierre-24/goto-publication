# adapted over https://github.com/pypa/sampleproject/blob/master/setup.py

from setuptools import setup, find_packages
from os import path

import goto_publication

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md')) as f:
    long_description = f.read()

with open(path.join(here, 'requirements/requirements.in')) as f:
    requirements = f.readlines()

with open(path.join(here, 'requirements/requirements-dev.in')) as f:
    requirements_dev = f.readlines()[1:]

setup(
    name='goto-publication',
    version=goto_publication.__version__,

    # Description
    description=goto_publication.__doc__,
    long_description=long_description,
    long_description_content_type='text/markdown',

    project_urls={
        'Bug Reports': 'https://github.com/pierre-24/goto-publication/issues',
        'Source': 'https://github.com/pierre-24/goto-publication',
    },

    url='https://github.com/pierre-24/goto-publication',
    author=goto_publication.__author__,

    # Classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',

        # Specify the Python versions:
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    packages=find_packages(exclude=('*tests',)),
    python_requires='>=3.5',

    # requirements
    install_requires=requirements,

    extras_require={  # Optional
        'dev': requirements_dev,
    },
)

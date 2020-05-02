"""
goto-publication: citation-based DOI searches
"""

import pathlib
import os
from os import path

__version__ = '0.2.1'
__author__ = 'Pierre Beaujean'
__maintainer__ = 'Pierre Beaujean'
__email__ = 'pierre.beaujean@unamur.be'
__status__ = 'Development'

JOURNAL_REGISTRY = pathlib.Path(path.abspath(path.dirname(__file__)), 'journal_registry.yml')


def create_providers():
    from goto_publication import providers

    # TODO: strongly opinionated list of providers and concept, there. Should change that.

    providers_ = [  # please keep this alphabetic
        providers.ACS(),
        providers.APS(),
        providers.AIP(),
        providers.IOP(),
        providers.Nature(),
        providers.RSC(),
        providers.Springer(concepts=['Chemistry', 'Physics']),
        providers.Wiley(concepts=[93, 43]),
    ]

    if 'SD_API_KEY' not in os.environ:
        providers_.append(providers.ScienceDirect(concepts=['CHEM', 'PHYS']))
    else:
        providers_.append(providers.ScienceDirectAPI(os.environ.get('SD_API_KEY'), concepts=['CHEM', 'PHYS']))

    return providers_

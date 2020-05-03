"""
Represent a given journal, with

+ A name (title)
+ An abbreviation (that may be auto-generated from the previous field)
+ An internal identifier (that the provider uses in its URLs and/or forms)

A journal may be (de)serialized in the form of a dictionary (containing the 3 above information, plus its provider).
"""

from typing import Any, Dict
import iso4

import goto_publication


class JournalError(Exception):
    def __init__(self, j, v, *args):
        super().__init__('{} ({})'.format(v, j), *args)


class AccessError(JournalError):
    def __init__(self, p, j, v):
        super().__init__(j + ' [' + p + ']', v)


class Journal:
    """Define a journal, containing different articles, which have an URL and a DOI (if valid).
    """

    def __init__(self, name: str, identifier: Any, provider: 'goto_publication.providers.Provider', abbr: str = None):
        self.name = name
        self.identifier = identifier
        self.abbr = abbr

        if self.abbr is None:
            self.abbr = iso4.abbreviate(self.name, periods=False, disambiguation_langs=set('en'))

        self.provider = provider

    def serialize(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'identifier': self.identifier,
            'provider': self.provider.CODE,
            'abbr': self.abbr
        }

    @classmethod
    def deserialize(cls, d: Dict[str, Any], provider: 'goto_publication.providers.Provider') -> 'Journal':
        """
        Deserialize a dictionary into a journal

        :param d: the dictionary.
        :param provider: the provider from which the journal is issued.
        """
        return cls(d.get('name'), d.get('identifier'), provider, d.get('abbr', None))

    def get_url(self, volume: [int, str], page: [int, str], **kwargs: dict) -> str:
        """Get the corresponding url"""

        # avoid cyclic imports
        from goto_publication import providers

        try:
            return self.provider.get_url(self.identifier, volume, page, **kwargs)
        except providers.ProviderError as e:
            raise AccessError(self.provider.CODE, self.name, str(e))
        except NotImplementedError:
            raise AccessError(self.provider.CODE, self.name, 'Not yet implemented')

    def get_doi(self, volume: [int, str], page: [int, str], **kwargs: dict) -> str:
        """Get the corresponding DOI"""

        # avoid cyclic imports
        from goto_publication import providers

        try:
            return self.provider.get_doi(self.identifier, volume, page, **kwargs)
        except providers.ProviderError as e:
            raise AccessError(self.provider.CODE, self.name, str(e))
        except NotImplementedError:
            raise AccessError(self.provider.CODE, self.name, 'Not yet implemented')

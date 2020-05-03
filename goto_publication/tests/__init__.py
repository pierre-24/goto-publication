from typing import Any, List

from goto_publication import providers
from goto_publication import journal


class FakeProvider(providers.Provider):
    CODE = 'Fake'
    NAME = 'Fake provider'
    WEBSITE_URL = 'http://test.com'
    ICON_URL = 'http://test.com/fav.ico'

    def get_url(self, journal_identifier: Any, volume: [str, int], page: str, **kwargs: dict) -> str:
        return '{}/{}/{}/{}/'.format(self.WEBSITE_URL, journal_identifier, volume, page)

    def get_doi(self, journal_identifier: Any, volume: [str, int], page: str, **kwargs: dict) -> str:
        return '10.0000/fake.{}-{}-{}'.format(journal_identifier, volume, page)

    def get_journals(self, **kwargs: dict) -> List[journal.Journal]:
        return [
            journal.Journal('Journal of Fancy Trees', 1, self, 'J. fanc. tree'),
            journal.Journal('Journal of Tasty Bananas', 2, self, 'J. tast. banan.'),
            journal.Journal('Journal of Toxic Frogs', 3, self, 'J. tox. frog')
        ]

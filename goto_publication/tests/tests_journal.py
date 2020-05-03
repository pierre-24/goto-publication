import unittest

from goto_publication import journal
from goto_publication.tests import FakeProvider


class TestJournal(unittest.TestCase):
    """Check if journal behave
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.provider = FakeProvider()

        self.name = 'Journal of Fancy Trees'
        self.abbr = 'J. fanc. tree'
        self.a_journal = journal.Journal(self.name, 0, self.provider, self.abbr)

    def test_journal_serialization(self):

        j_p = journal.Journal.deserialize(self.a_journal.serialize(), self.provider)

        self.assertEqual(j_p.name, self.a_journal.name)
        self.assertEqual(j_p.identifier, self.a_journal.identifier)
        self.assertEqual(j_p.abbr, self.a_journal.abbr)

    def test_journal_get(self):

        volume = '1'
        page = '1'

        self.assertEqual(
            self.a_journal.get_url(volume, page),
            self.provider.get_url(self.a_journal.identifier, volume, page)
        )

        self.assertEqual(
            self.a_journal.get_doi(volume, page),
            self.provider.get_doi(self.a_journal.identifier, volume, page)
        )

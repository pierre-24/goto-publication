import unittest

from goto_publication import registry
from goto_publication.tests import FakeProvider


class TestRegistry(unittest.TestCase):
    """Check if registry behave
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.providers = [FakeProvider(), ]
        self.registry = registry.Registry(self.providers)

        first = True
        for j in self.providers[0].get_journals():
            self.registry.add_journal(j)
            if first:
                self.a_journal = j
                first = False

    def test_suggest(self):

        # default cutoff
        out = self.registry.suggest_journals(self.a_journal.name)
        self.assertEqual(out[0], self.a_journal.name)
        self.assertEqual(len(out), 3)

        # stronger cutoff
        out = self.registry.suggest_journals(self.a_journal.name, cutoff=0.8)
        self.assertEqual(out[0], self.a_journal.name)
        self.assertEqual(len(out), 1)

        # abbr
        out = self.registry.suggest_journals(self.a_journal.abbr, source='abbr')
        self.assertEqual(out[0], self.a_journal.name)
        self.assertEqual(len(out), 1)

        # abbr, loose cutoff
        out = self.registry.suggest_journals(self.a_journal.abbr, source='abbr', cutoff=0.1)
        self.assertEqual(out[0], self.a_journal.name)
        self.assertEqual(len(out), 3)

    def test_get(self):

        volume = '1'
        page = '1'

        out = self.registry.get_url(self.a_journal.name, volume, page)
        self.assertEqual(out['url'], self.providers[0].get_url(self.a_journal.identifier, volume, page))

        out = self.registry.get_doi(self.a_journal.name, volume, page)
        self.assertEqual(out['doi'], self.providers[0].get_doi(self.a_journal.identifier, volume, page))

        # test raises
        with self.assertRaises(registry.RegistryError):
            self.registry.get_url(self.a_journal.name + 'x', volume, page)

        with self.assertRaises(registry.RegistryError):
            self.registry.get_doi(self.a_journal.name + 'x', volume, page)

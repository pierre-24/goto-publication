import unittest
import tempfile
import shutil
import subprocess
import json
import os
import yaml

from goto_publication import create_providers, providers, journal


class TestCLI(unittest.TestCase):
    """Check if CLI behaves correctly
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.temporary_directory = tempfile.mkdtemp()
        self.providers = create_providers()

        # create a small list of imaginary journals
        a_provider = providers.ACS()  # acs does not require request for simple url

        self.journals = [
            journal.Journal('Journal of Trees', 1, a_provider, 'J. tree'),
            journal.Journal('Journal of Banana', 2, a_provider, 'J. banan.'),
            journal.Journal('Journal of toxic frogs', 3, a_provider, 'J. tox. frog')
        ]

        self.alternate_journal_list = os.path.join(self.temporary_directory, 'list.yaml')
        with open(self.alternate_journal_list, 'w') as f:
            yaml.dump([j.serialize() for j in self.journals], f)

    def tearDown(self):
        shutil.rmtree(self.temporary_directory)

    @staticmethod
    def run_command(
            path: str, args: list = None,
            in_pipe=subprocess.DEVNULL, out_pipe=subprocess.DEVNULL, err_pipe=subprocess.DEVNULL) -> subprocess.Popen:
        """
        :param path: path to the script, with respect to the top of the package
        :param args: the args
        :param in_pipe: the input pipe (set to subprocess.PIPE for communication)
        :param out_pipe: the output pipe (set to subprocess.PIPE for communication)
        :param err_pipe: the error pipe (set to subprocess.PIPE for communication)
        """

        cmd = [path]
        if args:
            cmd.extend(str(a) for a in args)

        return subprocess.Popen(cmd, stdin=in_pipe, stdout=out_pipe, stderr=err_pipe)

    def run_gt(self, params: list) -> str:

        # test whole list
        process = self.run_command(
            'goto-publication',
            params,
            out_pipe=subprocess.PIPE,
            err_pipe=subprocess.PIPE)

        stdout_t, stderr_t = process.communicate()

        self.assertIsNotNone(stderr_t)
        self.assertEqual(len(stderr_t), 0, msg=stderr_t.decode())
        self.assertIsNotNone(stdout_t)
        self.assertNotEqual(len(stdout_t), 0)

        return stdout_t.decode()

    def test_output(self):
        """Test the YAML and JSON output
        """

        out1 = yaml.load(self.run_gt(['-f' 'yaml', 'providers', '-c', 2]), Loader=yaml.Loader)
        out2 = json.loads(self.run_gt(['-f' 'json', 'providers', '-c', 2]))
        self.assertEqual(out1, out2)

    def test_list_providers(self):
        provider_names = [p.get_info()['providerName'] for p in self.providers]

        # test whole list
        out = yaml.load(
            self.run_gt(['-J', self.alternate_journal_list, 'providers', '-c', len(self.providers)]),
            Loader=yaml.Loader)

        for p in out['providers']:
            self.assertIn(p['providerName'], provider_names)

        self.assertEqual(len(self.providers), out['total'])

        # test start and count
        out = yaml.load(
            self.run_gt(['-J', self.alternate_journal_list, 'providers', '-s', 2, '-c', 2]),
            Loader=yaml.Loader)

        self.assertEqual(len(out['providers']), 2)

        for p in out['providers']:
            self.assertIn(p['providerName'], provider_names[2:4])

    def test_list_journals(self):
        """Test the list of journals"""

        journal_names = [j.name for j in self.journals]

        # test whole list
        out = yaml.load(self.run_gt(['-J', self.alternate_journal_list, 'journals']), Loader=yaml.Loader)

        for j in out['journals']:
            self.assertIn(j['journal'], journal_names)

        self.assertEqual(len(self.journals), out['total'])

        # test last journal
        out = yaml.load(
            self.run_gt(['-J', self.alternate_journal_list, 'journals', '-c 1', '-s', 2]), Loader=yaml.Loader)

        self.assertEqual(len(out['journals']), 1)
        j_info = out['journals'][0]
        j = self.journals[-1]
        self.assertEqual(j_info['journal'], j.name)
        self.assertEqual(j_info['abbreviation'], j.abbr)
        self.assertEqual(j_info['providerName'], j.provider.NAME)

    def test_suggests(self):
        """Test suggestions"""

        # default cutoff with suggestions
        out = yaml.load(
            self.run_gt(['-J', self.alternate_journal_list, 'suggest', self.journals[0].abbr]),
            Loader=yaml.Loader)

        self.assertEqual(out['suggestions'][0], self.journals[0].name)
        self.assertEqual(len(out['suggestions']), 1)

        # small cutoff
        out = yaml.load(
            self.run_gt(['-J', self.alternate_journal_list, 'suggest', self.journals[0].abbr, '-C', 0.1]),
            Loader=yaml.Loader)

        self.assertEqual(out['suggestions'][0], self.journals[0].name)
        self.assertEqual(len(out['suggestions']), len(self.journals))  # all the other journals

        # default cutoff and name
        out = yaml.load(
            self.run_gt(['-J', self.alternate_journal_list, 'suggest', self.journals[0].name, '-S', 'name']),
            Loader=yaml.Loader)

        self.assertEqual(out['suggestions'][0], self.journals[0].name)
        self.assertEqual(len(out['suggestions']), 3)

        # stronger cutoff and name
        out = yaml.load(
            self.run_gt(
                ['-J', self.alternate_journal_list, 'suggest', self.journals[0].name, '-S', 'name', '-C', 0.8]),
            Loader=yaml.Loader)

        self.assertEqual(out['suggestions'][0], self.journals[0].name)
        self.assertEqual(len(out['suggestions']), 1)

    def test_journal(self):
        """Test journal by its name"""

        j = self.journals[0]

        out = yaml.load(
            self.run_gt(['-J', self.alternate_journal_list, 'journal', j.name]),
            Loader=yaml.Loader)

        self.assertEqual(out['journal'], j.name)
        self.assertEqual(out['abbreviation'], j.abbr)
        self.assertEqual(out['providerName'], j.provider.NAME)

    def test_get(self):
        """Test get"""

        j = self.journals[0]
        volume = 1
        page = 1

        out = yaml.load(
            self.run_gt(['-J', self.alternate_journal_list, 'get', j.name, volume, page]),
            Loader=yaml.Loader)

        self.assertEqual(out['url'], j.provider.get_url(j.identifier, volume, page))

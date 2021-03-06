import argparse
import json
import yaml

from typing import Dict
from goto_publication import registry
from goto_publication import create_providers, JOURNAL_REGISTRY, __version__ as p_version


def make_error(msg: str, arg: str) -> dict:
    return {'message': {arg: msg}}


def list_providers(args: argparse.Namespace, journal_registry: registry.Registry) -> Dict:
    """
    :param args: Arguments
    :param journal_registry: journal registry
    """

    start = args.start
    count = args.count

    li = list(p.get_info() for p in journal_registry.providers.values())[start:start + count]

    response = {
        'total': len(journal_registry.providers),
        'providers': li
    }

    if args.repeat_input:
        response.update({
            'count': len(li),
            'start': start,
        })

    return response


def list_journals(args: argparse.Namespace, journal_registry: registry.Registry) -> Dict:
    """
    :param args: Arguments
    :param journal_registry: journal registry
    """

    start = args.start
    count = args.count

    journals = []

    for j in list(journal_registry.journals.values())[start:start + count]:
        info = {
            'journal': j.name,
            'abbreviation': j.abbr
        }

        info.update(**j.provider.get_info())
        journals.append(info)

    response = {
        'total': len(journal_registry.journals),
        'journals': journals
    }

    if args.repeat_input:
        response.update({
            'count': len(journals),
            'start': start,
        })

    return response


def suggests(args: argparse.Namespace, journal_registry: registry.Registry) -> Dict:
    """
    :param args: Arguments
    :param journal_registry: journal registry
    """

    try:
        response = {
            'suggestions': journal_registry.suggest_journals(args.q, args.source, args.count, args.cutoff)
        }
    except registry.RegistryError as e:
        return make_error(e.what, e.var)

    if args.repeat_input:
        response.update({
            'request': args.q,
            'source': args.source,
            'count': args.count,
            'cutoff': args.cutoff,
        })

    return response


def journal(args: argparse.Namespace, journal_registry: registry.Registry) -> Dict:
    """
    :param args: Arguments
    :param journal_registry: journal registry
    """

    if args.q in journal_registry.journals:
        j = journal_registry.journals[args.q]
        response = {
            'journal': j.name,
            'abbreviation': j.abbr,
        }

        response.update(**j.provider.get_info())
    else:
        return make_error('unknown journal', 'q')

    return response


def get_info(args: argparse.Namespace, journal_registry: registry.Registry) -> Dict:
    """
    :param args: Arguments
    :param journal_registry: journal registry
    """

    callback = journal_registry.get_url
    if args.doi:
        callback = journal_registry.get_doi

    try:
        response = callback(args.journal, args.volume, args.page)
    except registry.RegistryError as e:
        return make_error(e.what, e.var)

    if args.repeat_input:
        response.update({
            'journal': args.journal,
            'volume': args.volume,
            'page': args.page,
        })

    return response


def get_arguments_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + p_version)
    parser.add_argument('-f', '--format', help='output format (json, yaml)', choices=('json', 'yaml'), default='yaml')
    parser.add_argument('-r', '--repeat-input', help='repeat input in the output', action='store_true')
    parser.add_argument('-J', '--journal-registry', help='path to the journal registry', default=JOURNAL_REGISTRY)

    subparsers = parser.add_subparsers(dest='search_section', help='search section')

    # list providers
    parser_list_providers = subparsers.add_parser('providers')
    parser_list_providers.add_argument('-s', '--start', help='result offset', type=int, default=0)
    parser_list_providers.add_argument('-c', '--count', help='Maximum number of results', type=int, default=10)

    # list journals
    parser_list_journals = subparsers.add_parser('journals')
    parser_list_journals.add_argument('-s', '--start', help='result offset', type=int, default=0)
    parser_list_journals.add_argument('-c', '--count', help='Maximum number of results', type=int, default=10)

    # suggests journal
    parser_suggest = subparsers.add_parser('suggest')
    parser_suggest.add_argument('q', help='query')
    parser_suggest.add_argument(
        '-S', '--source',
        choices=('name', 'abbr'),
        help='search in journal title (name) or abbreviation (abbr, default)',
        default='abbr'
    )
    parser_suggest.add_argument('-c', '--count', help='Maximum number of results', type=int, default=10)
    parser_suggest.add_argument(
        '-C', '--cutoff',
        type=float,
        help='Severity cutoff on the results (must be between 0 and 1, the larger, the severer)',
        default=0.6)

    # get journal info
    parser_journal = subparsers.add_parser('journal')
    parser_journal.add_argument('q', help='journal name')

    # get article url/doi
    parser_get = subparsers.add_parser('get')
    parser_get.add_argument('journal', help='full journal name')
    parser_get.add_argument('volume', help='article volume')
    parser_get.add_argument('page', help='article (starting) page')

    parser_get.add_argument('-d', '--doi', help='get DOI instead of url (slower but safer)', action='store_true')

    return parser


def dumps(args: argparse.Namespace, out: Dict):
    """
    :param args: the arguments
    :param out: the dict to output
    """

    if args.format == 'json':
        print(json.dumps(out, indent=2))
    else:
        print(yaml.dump(out))


def main():
    parser = get_arguments_parser()
    args = parser.parse_args()

    # create journal registry
    try:
        journal_registry = registry.Registry(create_providers(), args.journal_registry)
    except registry.RegistryError as e:
        print(make_error(e.what, e.var))
        return 1

    # output what was requested
    if args.search_section == 'providers':
        dumps(args, list_providers(args, journal_registry))
    elif args.search_section == 'journals':
        dumps(args, list_journals(args, journal_registry))
    elif args.search_section == 'suggest':
        dumps(args, suggests(args, journal_registry))
    elif args.search_section == 'journal':
        dumps(args, journal(args, journal_registry))
    elif args.search_section == 'get':
        dumps(args, get_info(args, journal_registry))

    return 0


if __name__ == '__main__':
    exit(main())

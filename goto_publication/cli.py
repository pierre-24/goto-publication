import argparse
import json
import yaml

from typing import Dict
from goto_publication import registry
from goto_publication import create_providers, JOURNAL_REGISTRY, __version__ as p_version


def list_providers(args: argparse.Namespace, journal_registry: registry.Registry):
    """
    :param args: Arguments
    :param journal_registry: journal registry
    """

    start = args.start
    count = args.count

    li = list(p.get_info() for p in journal_registry.providers.values())[start:start + count]

    return {
        'start': start,
        'count': len(li),
        'total': len(journal_registry.providers),
        'providers': li
    }


def list_journals(args: argparse.Namespace, journal_registry: registry.Registry):
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

    return {
        'start': start,
        'count': len(journals),
        'total': len(journal_registry.journals),
        'journals': journals
    }


def get_arguments_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + p_version)
    parser.add_argument('-f', '--format', help='output format (json, yaml)', choices=('json', 'yaml'), default='json')

    subparsers = parser.add_subparsers(dest='search_section', help='search section')

    # list providers
    parser_list_providers = subparsers.add_parser('providers')
    parser_list_providers.add_argument('-s', '--start', help='result offset', type=int, default=0)
    parser_list_providers.add_argument('-c', '--count', help='Maximum number of results', type=int, default=10)

    parser_list_journals = subparsers.add_parser('journals')
    parser_list_journals.add_argument('-s', '--start', help='result offset', type=int, default=0)
    parser_list_journals.add_argument('-c', '--count', help='Maximum number of results', type=int, default=10)

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
    journal_registry = registry.Registry(JOURNAL_REGISTRY, create_providers())

    # output what was requested
    if args.search_section == 'providers':
        dumps(args, list_providers(args, journal_registry))
    elif args.search_section == 'journals':
        dumps(args, list_journals(args, journal_registry))


if __name__ == '__main__':
    main()


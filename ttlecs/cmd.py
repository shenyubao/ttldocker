import os
import argparse
import pkgutil

from ttlecs.provider.aliyun import Aliyun
from ttlecs.config_template import template_aliyun

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_ascart():
    print(''' 
  ______________    _________________
 /_  __/_  __/ /   / ____/ ____/ ___/
  / /   / / / /   / __/ / /    \__ \ 
 / /   / / / /___/ /___/ /___ ___/ / 
/_/   /_/ /_____/_____/\____//____/  
            ''')


def parse_opts(parser):
    subparsers = parser.add_subparsers(help='sub-command help', dest="action")

    parse_run = subparsers.add_parser('run', help='create the ttl ecs')
    parse_run.add_argument('--config', dest="config_file", help="the config file path", required=True)

    parse_dry_run = subparsers.add_parser('dryrun', help='check the config file, not create ecs')
    parse_dry_run.add_argument('--config', dest="config_file", help="the config file path", required=True)

    parse_list = subparsers.add_parser('list', help='list the running ecs instance')
    parse_list.add_argument('--config', dest="config_file", help="the config file path", required=True)
    parse_list.add_argument('--page_size', default=10, dest="page_size", help="the size of page")
    parse_list.add_argument('--page_number', default=1, dest="page_number", help="the number of page")

    parse_template = subparsers.add_parser('template', help='list the docker template list')

    return parser.parse_args()


def execute():
    parser = argparse.ArgumentParser(description="ttlecs - the tool for create ttl(time to alive) ecs(Elastic Compute "
                                                 "Service)", epilog="%prog [options]")
    parser.add_argument("-v", "--verbose", help="print debug log", dest='verbose', action='store_true')

    args = parse_opts(parser)
    # TODO: Switch Provider
    if args.action == "dryrun":
        Aliyun(args.config_file).dry_run_instance()
    elif args.action == "run":
        Aliyun(args.config_file).run_instance()
    elif args.action == "list":
        Aliyun(args.config_file).desc_instance(tag_id='ttlecs', page_size=args.page_size,
                                               page_number=args.page_number)
    elif args.action == "template":
        print(template_aliyun)

    else:
        print(os.path)
        print_ascart()
        parser.print_help()


if __name__ == '__main__':
    execute()

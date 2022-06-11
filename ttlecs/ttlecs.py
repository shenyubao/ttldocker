import argparse


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
,--------. ,--------. ,--.    ,------.                  ,--.                     
'--.  .--' '--.  .--' |  |    |  .-.  \   ,---.   ,---. |  |,-.   ,---.  ,--.--. 
   |  |       |  |    |  |    |  |  \  : | .-. | | .--' |     /  | .-. : |  .--' 
   |  |       |  |    |  '--. |  '--'  / ' '-' ' \ `--. |  \  \  \   --. |  |    
   `--'       `--'    `-----' `-------'   `---'   `---' `--'`--'  `----' `--'    
            ''')


def parse_opts(parser):
    subparsers = parser.add_subparsers(help='sub-command help', dest="action")

    parse_spots = subparsers.add_parser('spots', help="display the spots resources and prices")
    parse_spots.add_argument('--provider', dest="provider", help="require the spot provider")

    parse_run = subparsers.add_parser('run', help='run the ttl docker template on spots')
    parse_run.add_argument('--provider', dest="provider", help="require the spot provider")

    parse_list = subparsers.add_parser('list', help='list the running docker instance on spots')
    parse_list.add_argument('--provider', dest="provider", help="require the spot provider")

    parse_template = subparsers.add_parser('template', help='list the docker template list')

    return parser.parse_args()


def execute():
    parser = argparse.ArgumentParser(description="ttlecs - the tool for create ttl(time to alive) ecs(Elastic Compute Service)", epilog="%prog [options]")
    parser.add_argument("-v", "--verbose", help="print debug log", dest='verbose', action='store_true')

    args = parse_opts(parser)
    if args.action == "run":
        pass
    else:
        print_ascart()
        parser.print_help()

if __name__ == '__main__':
    execute()

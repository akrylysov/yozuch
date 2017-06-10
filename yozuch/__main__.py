"""
Command line processor.
"""

import argparse
import sys
import os
from yozuch import builder, server, project_init, __version__ as version


def parse_args():
    parser = argparse.ArgumentParser(usage='''yozuch <command> [project_directory] [options]

list of commands:
  init               create initial project structure
  serve              run development server
  build              build project
''')
    parser.add_argument('command', choices=['init', 'build', 'version', 'serve'], help=argparse.SUPPRESS)
    parser.add_argument('project_directory', nargs='?', default=os.getcwd(),
                        help='directory which contains your config.py and content')
    parser.add_argument('-v', '--validate', action='store_true', help='check output for broken internal URLs')
    parser.add_argument('-p', '--port', type=int, default=8000, help='server port')
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()
    args.ports = args.port, args.port + 1
    args.debug = False
    return args


def build(args, output_dir=None):
    kwargs = {
        'validate': args.validate,
    }
    if output_dir is not None:
        kwargs['output_dir'] = output_dir
    config = {
        'DEBUG': args.debug,
        'SERVER_PORT': args.ports[0],
        'NOTIFICATION_SERVER_PORT': args.ports[1],
    }
    return builder.build(args.project_directory, config, **kwargs)


def run(args):
    if args.command == 'init':
        project_init.init(args.project_directory)
    elif args.command == 'build':
        build(args)
    elif args.command == 'version':
        print(version)
    elif args.command == 'serve':
        args.debug = True
        server.serve(args.project_directory, lambda output_dir: build(args, output_dir), ports=args.ports)


def main():
    run(parse_args())


if __name__ == '__main__':
    main()

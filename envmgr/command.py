import argparse
import logging
import os
import sys

from envmgr.parser import EnvConfParser

logging.basicConfig()

parser = argparse.ArgumentParser(description='Spawn processes in a controlled environment.')
parser.add_argument('--name', '-n',
                    help='name of environment config to load')
parser.add_argument('--root', '-r', default='/etc/envmgr',
                    help='envmgr configuration root directory')
parser.add_argument('command', nargs=argparse.REMAINDER)


def envmgr():
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.name is None:
        args.name = os.path.basename(args.command[0])

    env = EnvConfParser(args.name, args.root)

    os.execvpe(args.command[0], args.command, env.parse())

if __name__ == '__main__':
    envmgr()

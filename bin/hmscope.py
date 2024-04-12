#!/usr/bin/env python3

import os
import sys
import argparse

def main(argv=None):
    description = \
            '''
            Welcome to HMC 3D Printed Microscope tool!
            '''
    parser = argparse.ArgumentParser(
            prog = 'hmscope',
            description = description,
            )

    subparsers = parser.add_subparsers(dest = "operation")

    parser_process = subparsers.add_parser('process', help = 'processes datasets')

    args = parser.parse_args(argv)
    if args.operation is None:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()

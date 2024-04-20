#!/usr/bin/env python3

import os
import sys
import argparse
import subprocess

def subcommand_process(args):
    cwd = os.getcwd()
    if(not os.path.exists(args.module)):
        print(f'Processing module {args.module} does not exist')
        sys.exit(1)
    if(not os.path.exists(args.dataset)):
        print(f'Dataset {args.dataset} does not exist')
        sys.exit(1)

    exec = os.path.join(cwd,args.module,'process','main_script.py')
    subprocess.run(['python3',exec,args.dataset])


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
    parser_process.add_argument('module', type=str, help='processing module')
    parser_process.add_argument('dataset', type=str, help='dataset to process')
    parser_process.set_defaults(handler=subcommand_process)

    args = parser.parse_args(argv)
    if args.operation is None:
        parser.print_help()
        sys.exit(1)
    args.handler(args)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import os
import sys
import argparse
import subprocess
import paramiko

username = 'hmcbiophotonics'
hostname = 'hmcpi0.local'

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

def subcommand_rpi_connect(args):
    client = paramiko.client.SSHClient()
    client.load_system_host_keys()
    client.connect(hostname=hostname,
                   username=username,
                   )
    stdin, stdout, stderr = client.exec_command('ls -l')

def subcommand_rpi_sync(args):
    # any remote rpi commands should go here
    print("Syncing into pi")

def subcommand_rpi_capture(args):
    print("Capturing module")

def subcommand_simulate(args):
    print('Simulating module')



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
    
    # PROCESS
    parser_process = subparsers.add_parser('process', help = 'processes datasets')
    parser_process.add_argument('module', type=str, help='processing module')
    parser_process.add_argument('dataset', type=str, help='dataset to process')
    parser_process.set_defaults(handler=subcommand_process)

    # RPI
    parser_rpi = subparsers.add_parser('rpi', help = 'remote rpi commands')
    subparsers_rpi = parser_rpi.add_subparsers(dest = 'rpi_operation')

    subparser_rpi_sync = subparsers_rpi.add_parser('sync', help = 'syncs with rpi')
    subparser_rpi_sync.set_defaults(handler=subcommand_rpi_sync)

    subparser_rpi_capture = subparsers_rpi.add_parser('capture', help = 'captures based on module')
    subparser_rpi_capture.add_argument('module', type=str, help = 'capture module')
    subparser_rpi_capture.set_defaults(handler=subcommand_rpi_capture)

    subparser_rpi_connect = subparsers_rpi.add_parser('connect')
    subparser_rpi_connect.set_defaults(handler=subcommand_rpi_connect)

    # SIMULATE
    parser_simulate = subparsers.add_parser('simulate', help = 'simulate')
    parser_simulate.add_argument('module', type=str, help='simulating module')
    parser_simulate.set_defaults(handler=subcommand_simulate)

    args = parser.parse_args(argv)
    if args.operation is None:
        parser.print_help()
        sys.exit(1)
    if args.operation == 'rpi' and args.rpi_operation is None:
        parser_rpi.print_help()
        sys.exit(1)
    args.handler(args)

if __name__ == "__main__":
    main()

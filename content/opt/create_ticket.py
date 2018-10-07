#!/usr/bin/env python3
import sys

import requests
import requests.auth
import platform
import argparse
import subprocess


def get_ticket_salt(
    icinga_host,
    username,
    password,
):
    response = requests.post(
        url='https://{icinga_host}:5665/v1/actions/generate-ticket'.format(
            icinga_host=icinga_host,
            hostname=platform.node(),
        ),
        json={
            'cn': platform.node(),
        },
        headers={
            'Accept': 'application/json',
        },
        verify=False,
        auth=requests.auth.HTTPBasicAuth(
            username=username,
            password=password,
        ),
    ).json()
    print(response)
    ticket_salt = response['results'][0]['ticket']

    print(
        'Ticket salt is {ticket_salt}'.format(
            ticket_salt=ticket_salt
        ),
    )
    return ticket_salt


def parse_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        '-H',
        '--icinga-hostname',
        help='The hostname of the Icinga API instance',
    )
    arg_parser.add_argument(
        '-u',
        '--username',
        help='The API username for icinga',
    )

    arg_parser.add_argument(
        '-p',
        '--password',
        help='The API password for icinga',
    )

    return arg_parser.parse_args()


def main():
    args = parse_args()

    ticket_salt = get_ticket_salt(
        icinga_host=args.icinga_hostname,
        username=args.username,
        password=args.password,
    )
    subprocess.check_call(
        ['icinga2',
         'pki',
         'save-cert',
         '--host',
         args.icinga_hostname,
         '--port',
         '5665',
         '--key',
         '/etc/icinga2/pki/{hostname}.key'.format(
             hostname=platform.node(),
         ),
         '--cert',
         '/etc/icinga2/pki/{hostname}.crt'.format(
             hostname=platform.node(),
         ),
         '--trustedcert',
         '/etc/icinga2/pki/trusted-master.crt',
         ],
        stdout=sys.stdout,
    )
    subprocess.check_call(
        [
            'icinga2',
            'node',
            'setup',
            '--ticket',
            ticket_salt,
            '--endpoint',
            args.icinga_hostname,
            '--accept-config',
            '--accept-commands',
            '--zone',
            platform.node(),
            '--master_host',
            args.icinga_hostname,
            '--cn',
            platform.node(),
            '--trustedcert',
            '/etc/icinga2/pki/trusted-master.crt',
        ],
        stdout=sys.stdout,
    )


if __name__ == '__main__':
    main()

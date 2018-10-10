#!/usr/bin/env python3
import sys

import requests
import requests.auth
import socket
import argparse
import subprocess


def get_ticket(
    local_hostname,
    icinga_host,
    username,
    password,
):
    response = requests.post(
        url='https://{icinga_host}:5665/v1/actions/generate-ticket'.format(
            icinga_host=icinga_host,
            hostname=local_hostname,
        ),
        json={
            'cn': local_hostname,
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
    ticket = response['results'][0]['ticket']

    print(
        'Ticket is {ticket}'.format(
            ticket=ticket,
        ),
    )
    return ticket


def parse_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        '-H',
        '--icinga-hostname',
        help='The hostname of the Icinga API instance',
        required=True,
    )
    arg_parser.add_argument(
        '-u',
        '--username',
        help='The API username for Icinga',
        required=True,
    )

    arg_parser.add_argument(
        '-p',
        '--password',
        help='The API password for Icinga',
        required=True,
    )

    arg_parser.add_argument(
        '-P',
        '--icinga-port',
        help='The API port for Icinga',
        default=5665,
    )

    return arg_parser.parse_args()


def main():
    args = parse_args()
    local_hostname = socket.getfqdn()

    ticket = get_ticket(
        local_hostname=local_hostname,
        icinga_host=args.icinga_hostname,
        username=args.username,
        password=args.password,
    )
    create_new_certificate(
        local_hostname=local_hostname,
    )

    save_icinga_master_certificate(
        icinga_hostname=args.icinga_hostname,
    )

    setup_local_node(
        local_hostname=local_hostname,
        icinga_hostname=args.icinga_hostname,
        icinga_port=args.icinga_port,
        ticket=ticket,
    )


def setup_local_node(
    icinga_hostname,
    icinga_port,
    local_hostname,
    ticket,
):
    print('Performing setup.')
    subprocess.check_call(
        [
            'icinga2',
            'node',
            'setup',
            '--ticket',
            ticket,
            '--endpoint',
            '{icinga_hostname},{icinga_hostname},{icinga_port}'.format(
                icinga_hostname=icinga_hostname,
                icinga_port=icinga_port,
            ),
            '--accept-config',
            '--accept-commands',
            '--zone',
            local_hostname,
            '--parent_host',
            icinga_hostname,
            '--parent_zone',
            'master',
            '--cn',
            local_hostname,
            '--trustedcert',
            '/etc/icinga2/pki/trusted-master.crt',
        ],
        stdout=sys.stdout,
    )


def save_icinga_master_certificate(
    icinga_hostname,
):
    print('Getting certificate from master node.')
    subprocess.check_call(
        [
            'icinga2',
            'pki',
            'save-cert',
            '--host',
            icinga_hostname,
            '--port',
            '5665',
            '--trustedcert',
            '/etc/icinga2/pki/trusted-master.crt',
        ],
        stdout=sys.stdout,
    )


def create_new_certificate(
    local_hostname,
):
    print('Creating new certificate.')
    subprocess.check_call(
        [
            'icinga2',
            'pki',
            'new-cert',
            '--key',
            '/etc/icinga2/pki/{hostname}.key'.format(
                hostname=local_hostname,
            ),

            '--cert',
            '/etc/icinga2/pki/{hostname}.crt'.format(
                hostname=local_hostname,
            ),
            '--cn',
            local_hostname,
        ],
        stdout=sys.stdout,
    )


if __name__ == '__main__':
    main()

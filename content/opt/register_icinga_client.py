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
    local_hostname = platform.node()
    create_new_certificate(
        local_hostname=local_hostname,
    )

    get_icinga_master_certificate(
        local_hostname=local_hostname,
        icinga_hostname=args.icinga_hostname,
    )

    create_login_ticket(
        local_hostname=local_hostname,
        icinga_hostname=args.icinga_hostname,
        ticket_salt=ticket_salt,
    )


def create_login_ticket(
    icinga_hostname,
    local_hostname,
    ticket_salt,
):
    subprocess.check_call(
        [
            'icinga2',
            'node',
            'setup',
            '--ticket',
            ticket_salt,
            '--endpoint',
            icinga_hostname,
            '--accept-config',
            '--accept-commands',
            '--zone',
            local_hostname,
            '--master_host',
            icinga_hostname,
            '--cn',
            local_hostname,
            '--trustedcert',
            '/etc/icinga2/pki/trusted-master.crt',
        ],
        stdout=sys.stdout,
    )


def get_icinga_master_certificate(
    local_hostname,
    icinga_hostname,
):
    subprocess.check_call(
        [
            'icinga2',
            'pki',
            'save-cert',
            '--host',
            icinga_hostname,
            '--port',
            '5665',
            '--key',
            '/etc/icinga2/pki/{hostname}.key'.format(
                hostname=local_hostname,
            ),
            '--cert',
            '/etc/icinga2/pki/{hostname}.crt'.format(
                hostname=local_hostname,
            ),
            '--trustedcert',
            '/etc/icinga2/pki/trusted-master.crt',
        ],
        stdout=sys.stdout,
    )


def create_new_certificate(
    local_hostname,
):
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
            '--trustedcert',
            '/etc/icinga2/pki/trusted-master.crt',
            '--cn',
            local_hostname,
        ],
        stdout=sys.stdout,
    )


if __name__ == '__main__':
    main()
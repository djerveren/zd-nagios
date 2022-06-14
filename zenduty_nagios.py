#!/usr/bin/python3
import sys, os
import argparse
import urllib3
import json

http = urllib3.PoolManager()

def build_arguments_parser(description):
    parser = argparse.ArgumentParser(description)

    parser.add_argument('-n', '--token',
                        dest="token",
                        required=True,
                        help="Zenduty unique token assigned to this service")
    parser.add_argument('-e', '--notification-source',
                        dest="notification_source",
                        required=True,
                        help="nagios notification source (host/service)",
                        choices=["service", "host"])
    parser.add_argument('-t', "--notification-type",
                        dest="notification_type",
                        required=True,
                        help='nagios notification-type ("PROBLEM", "RECOVERY", "FLAPPINGSTART", etc ...)')
    parser.add_argument('-f', '--additional-fields',
                        action="append",
                        dest="field",
                        help="additional fields/details to send")
    return parser


def get_fields(field_array):
    if field_array is None:
        return {}
    to_ret=dict(f.split("=", 1) for f in field_array)
    return to_ret
    

def main():
    try:
        description = "collect arguments for zenduty"
        parser = build_arguments_parser(description)
        args = parser.parse_args()
        data_to_send = {
            "token": args.token,
            "notification_type": args.notification_type,
            "notification_source": args.notification_source,
            "fields": get_fields(args.field)
        }
        url = "https://www.zenduty.com/api/integration/nagios/{0}/".format(args.token)
        data = json.dumps(data_to_send)
        req = http.request('POST', url, body=data, headers={'Content-Type': 'application/json'})
        exit(0)
    except Exception as e:
        print(str(e))
        exit(4)


main()

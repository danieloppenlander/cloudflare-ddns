#!/usr/bin/python

import requests
import os

def main():

    # Load environment variables
    ZONE_NAME = os.getenv("ZONE_NAME")
    NAME = os.getenv("NAME")
    IS_PROXIED = os.getenv("IS_PROXIED").lower() == 'true'
    EMAIL = os.getenv("API_EMAIL")
    API_KEY = os.getenv("API_KEY")

    auth_headers = {
        'X-Auth-Email': EMAIL,
        'X-Auth-Key': API_KEY,
    }

    # Get my IP
    public_ip = get_public_ip()

    # Get zone ID
    zone = get_first_zone_by_name(ZONE_NAME, auth_headers)

    # Get record ID
    record = get_first_record_by_name(zone['id'], NAME, auth_headers)

    # Check if IP has changed
    if record['content'] == public_ip:
        return

    # Create new record
    new_record = {
        'content': public_ip,
        'name': NAME,
        'proxied': IS_PROXIED,
        'type': 'A',
        'comment': 'Updated automatically.',
    }

    # Update record
    put_record(zone['id'], record['id'], new_record, auth_headers)

    print(f'Updated {NAME} to {public_ip}')

# Get public IP
def get_public_ip():
    public_ip_response = requests.get('https://checkip.amazonaws.com')

    if public_ip_response.status_code != 200:
        raise Exception(f'Could not get public IP: {public_ip_response.text}')

    return public_ip_response.text.strip()

# Get zone from a zone name
def get_first_zone_by_name(zone_name, headers):
    zone_id_response = requests.get(
        f'https://api.cloudflare.com/client/v4/zones?name={zone_name}&status=active',
        headers=headers
    )

    if zone_id_response.status_code != 200:
        raise Exception(f'Could not get zone ID: {zone_id_response.json()}')

    if len(zone_id_response.json()['result']) == 0:
        raise Exception(f'Zone not found: {zone_name}')

    return zone_id_response.json()['result'][0]

# Get record from a zone ID and record name
def get_first_record_by_name(zone_id, name, headers):
    record_id_response = requests.get(
        f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?type=A&name={name}',
        headers=headers
    )

    if record_id_response.status_code != 200:
        raise Exception(f'Could not get record ID: {record_id_response.json()}')

    if len(record_id_response.json()['result']) == 0:
        raise Exception(f'Record not found: {name}')

    return record_id_response.json()['result'][0]

# Udates the record with the new one specified
def put_record(zone_id, record_id, record, headers):
    update_response = requests.put(
        f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}',
        headers=headers,
        json=record
    )

    if update_response.status_code != 200:
        raise Exception(f'Could not update record: {update_response.json()}')


if __name__ == "__main__":
    main()
#!/usr/bin/env python3

import os
import json

import urllib.parse
import requests

#from google.cloud import storage
from google.oauth2 import service_account
from google.auth import impersonated_credentials
from google.auth.transport.requests import Request


class GoogleStorage:

    def __init__(self, host_mode=False):

        self.initialized = False
        self.base_url = 'https://storage.googleapis.com/storage/v1/'

        if host_mode:
            # make read-only temporary credentials
            target_scopes = ['https://www.googleapis.com/auth/devstorage.read_only']
            self.admin_credentials = service_account.Credentials.from_service_account_file(os.getenv('RD_STORAGE_GOOGLE_ACCOUNT'), scopes=target_scopes)

            self.reader_credentials = impersonated_credentials.Credentials(
                    source_credentials=self.admin_credentials,
                    target_principal=os.getenv('RD_STORAGE_GOOGLE_ACCOUNT_READONLY'),
                    target_scopes=target_scopes,
                    lifetime=3600)

            self.reader_credentials.refresh(Request())

            self.initialize(os.getenv('RD_STORAGE_GOOGLE_BUCKET'), self.reader_credentials.token)

        else:
            # guest mode
            pass

    def initialize(self, bucket, token):

        self.bucket = bucket
        self.token = token
        self.initialized = True


    def list(self):
        headers = {'Authorization': 'Bearer {}'.format(self.token)}
        response = requests.get(self.base_url + 'b/' + self.bucket + '/o', headers=headers)

        return [item['name'] for item in response.json()['items']]

    def get(self, object_name, location):
        headers = {'Authorization': 'Bearer {}'.format(self.token)}

        url = self.base_url + 'b/' + self.bucket + '/o/' + urllib.parse.quote(object_name, safe='') + '?alt=media'
        print(url)
        response = requests.get(url, headers=headers)

        with location.open('w') as f:
            json.dump(response.json(), f)


if __name__ == '__main__':
    s = GoogleStorage(host_mode=True)
    print(s.token)
    print(s.list())

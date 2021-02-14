# Copyright © 2019 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Centralized setup of logging for the service."""
import base64

import requests


def get_reminders(app, reminder_type: str = 'email'):
    """Return reminders for next day."""
    # Create a keycloak service account token to call the appointment api
    access_token = get_access_token(app)

    # Add this token as bearer token to invoke the reminders endpoint
    reminders_endpoint = app.config.get('REMINDER_ENDPOINT') + f'{reminder_type}/'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(reminders_endpoint, data=None, headers=headers)
    response.raise_for_status()
    return response


def get_access_token(app):
    token_url = app.config.get('OIDC_PROVIDER_TOKEN_URL')
    basic_auth_encoded = base64.b64encode(
        bytes(app.config.get('SERVICE_ACCOUNT_ID') + ':' + app.config.get('SERVICE_ACCOUNT_SECRET'), 'utf-8')).decode(
        'utf-8')
    data = 'grant_type=client_credentials'
    headers = {
        'Authorization': f'Basic {basic_auth_encoded}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    token_response = requests.post(token_url, data=data, headers=headers)
    access_token = token_response.json().get('access_token')
    return access_token

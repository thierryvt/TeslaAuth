import os
import uuid
import requests
from flask import Flask, request, render_template
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
DOMAIN = os.environ['DOMAIN']
AUDIENCE = os.environ['AUDIENCE']
SCOPES = 'openid offline_access vehicle_device_data vehicle_cmds vehicle_charging_cmds'

def auth():
    print('\n### Generate Partner Authentication Token ###')
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'scope': 'openid vehicle_device_data vehicle_cmds vehicle_charging_cmds',
        'audience': AUDIENCE
    }
    req = requests.post('https://auth.tesla.com/oauth2/v3/token', headers=headers, data=payload)
    req.raise_for_status()
    tesla_api_token = req.json()['access_token']

    print('\n### Registering Tesla account ###')
    headers = {
        'Authorization': 'Bearer ' + tesla_api_token,
        'Content-Type': 'application/json'
    }
    payload = '{"domain": "%s"}' % DOMAIN
    req = requests.post('https://fleet-api.prd.eu.vn.cloud.tesla.com/api/1/partner_accounts', headers=headers,
                        data=payload)
    print(req.text)
    req.raise_for_status()

@app.errorhandler(Exception)
def handle_exception(e):
    print(f'Exception caught: {e}')
    # pass through HTTP errors
    if isinstance(e, HTTPException):
        return e

    # now you're handling non-HTTP exceptions only
    return 'Unknown Error', 500

@app.route('/')
def index():
    print('rendering root')
    return render_template('index.html', domain=DOMAIN, client_id=CLIENT_ID, scopes=SCOPES, randomstate=uuid.uuid4().hex, randomnonce=uuid.uuid4().hex)

@app.route('/redirect')
def callback():
    print('redirect url called!')
    # Tesla servers POST here to complete authorization
    # sometimes I don't get a valid code, not sure why
    try:
        code = request.args['code']
    except KeyError:
        app.logger.error('args: %s' % request.args)
        return f'Invalid code!', 400

    print(f'Got code: {code}')

    # Exchange code for refresh_token
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'audience': AUDIENCE,
        'redirect_uri': f"https://{DOMAIN}/redirect"
    }
    req = requests.post('https://auth.tesla.com/oauth2/v3/token', headers=headers, data=payload)
    req.raise_for_status()
    app.logger.warning('Access token for Fleet API requests: %s' % req.json()['access_token'])

    return req.json()

if __name__ == '__main__':
    print('\n### Starting Flask server... ###')
    app.run(port=4200, debug=False, host='0.0.0.0')
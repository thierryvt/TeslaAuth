# TeslaAuth
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Simple web-app to handle the new Tesla Fleet API OAuth flow

## pre-requisites

an environment with docker, docker-compose, and python installed.

You have gone through the necessary steps to set up your app, see https://github.com/teslamotors/vehicle-command for more details.
This means, in short:

- you have created a public/private key-pair using the tesla-keygen utility included in the vehicle-command repo
- you are hosting the public key created in the previous step at `https://<your domain>/.well-known/appspecific/com.tesla.3p.public-key.pem`
- You have registered your app with Tesla, see https://developer.tesla.com/docs/fleet-api for more info. For this app to work your allowed redirect url should be `/redirect` and the allowed return should be `/exit` (note: this is also where you will find your client_id and client_secret)

## installing

- download or clone this repo
- create .env file in root of project folder for client_id, client_secret, domain, audience, and port
- run `docker-compose up -d` to start container

## Usage

When running for the first time you'll need to enroll the public key into your car's keychain, otherwise you will not be able to send commands. 
This should preferably be done from a phone that has the Tesla app installed and is already a key for the car you wish to enroll.

This will open the Tesla app and ask you if you wish to enroll your car.

When that's done you can generate the oauth tokens

## warning
this is uses a Flask server, best to not keep it running longer than necessary.

# S3 Backup

I use this to backup a Unity directory to s3 providers: cloudflare r2 and backblaze b2
Given a target Unity directory, it zips up the Assets and ProjectSettings directories and uploads them to the s3 API providers.

## Requires

- Python 3 (tested with 3.9)
- boto3 library

## Config

Uses a local .json config file, check "conf.json.example".

## Issues

Lots. This is for my personal use, if you want to use it youself I'd consider:

- Using env vars rather than a .json file for config
- Making a generic s3 config type so you can use any s3 API provider
- Allowing different bucket name per provider
- Using a temp file for the .zip so it's cleaned automagically on a script interuption
- Parrallel s3 uploads

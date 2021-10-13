# Backup Util

Used to backup large directories to cloud storage (i.e. S3, Google Drive. ect) and remote server filesystems.

Given a target directory, it zips it and backs it up to a remote server via rsync and to cloud storage via rclone.

I use this with a cronjob for nightly backups of large binary assets and whole directories that are not  suited to Git (because git-lfs is a hot mess).

## Requires

- Python 3 (tested with 3.9)
- rsync installation configured in PATH
- ssh access to rsync target
- rclone installation configured in PATH and with a remote set up

## Config

Uses a local json config file, check "conf.json.example".

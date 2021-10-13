import shutil
import subprocess
from datetime import datetime
from typing import NamedTuple
import json
import os

print('*** BACKUP UTIL')

class Conf(NamedTuple):
    target_dir: str
    rsync_remote_host: str
    rsync_ssh_key_path: str
    rclone_remote: str

def read_json_conf() -> Conf:
    f = open('conf.json', "r")
    data = json.loads(f.read())
    f.close()
    return Conf(
        target_dir=data['target_dir'],
        rsync_remote_host=data['rsync_remote_host'],
        rsync_ssh_key_path=data['rsync_ssh_key_path'],
        rclone_remote=data['rclone_remote'],
    )

conf = read_json_conf()

date_today = datetime.today().strftime('%Y-%m-%d')
zip_output_base_name = f'{os.path.basename(conf.target_dir)}_{date_today}'
zip_output_file_name = f'{zip_output_base_name}.zip'

print(f'{datetime.now().strftime("%H:%M:%S")} zipping target directory "{conf.target_dir}"')
# TODO: would be nice to use tempfile.TemporaryFile for the zip but WSL goes mad with tmp behavior
shutil.make_archive(zip_output_base_name, 'zip', conf.target_dir)

print(f'{datetime.now().strftime("%H:%M:%S")} running rsync to "{conf.rsync_remote_host}"')
rsync_result = subprocess.run(['rsync', zip_output_file_name, conf.rsync_remote_host])
rsync_success = rsync_result.returncode == 0

print(f'{datetime.now().strftime("%H:%M:%S")} running rclone to "{conf.rclone_remote}"')
rclone_result = subprocess.run(['rclone', 'copy', zip_output_file_name, conf.rclone_remote])
rclone_success = rclone_result.returncode == 0

print(f'{datetime.now().strftime("%H:%M:%S")} cleaning up local zip')
os.remove(zip_output_file_name)
print(f'{datetime.now().strftime("%H:%M:%S")} finished\n')

print(f'*** rsync upload: {"SUCCESS" if rsync_success else "FAILED"}')
print(f'*** rclone upload: {"SUCCESS" if rclone_success else "FAILED"}')

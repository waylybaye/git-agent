from __future__ import unicode_literals
from __future__ import print_function

import os
import time
import subprocess
from collections import defaultdict

import docker


MOUNT_ROOT = '/rootfs/'
PULL_INTERVAL_SECONDS = 60 * 5


def parse_env(envs):
    return dict(env.split('=', 1) for env in envs)


def main():
    """
    Docker ENVs

    GIT_VOLUME: the base git volume
    GIT_REMOTE: the git remote
    GIT_BRANCH: the git branch
    GIT_INTERVAL: interval seconds
    GIT_FORCE: force to pull
    """
    client = docker.from_env()
    ps_interval = 30

    last_updates = defaultdict(int)

    print("Started, watching container changes ...")

    while True:
        start_at = time.time()

        for container in client.containers.list():
            envs = parse_env(container.attrs['Config']['Env'])

            if 'GIT_VOLUME' not in envs or 'GIT_REMOTE' not in envs:
                continue

            interval = envs.get('GIT_INTERVAL', '')
            interval = int(interval) if interval.isdigit() else PULL_INTERVAL_SECONDS

            last_update = last_updates[container.id]
            if not last_update:
                print("New Container: ", container.name)

            if last_update and (time.time() - last_update) < interval:
                continue

            git_volume = envs['GIT_VOLUME']
            git_remote = envs['GIT_REMOTE']
            git_branch = envs['GIT_BRANCH'] or 'master'
            git_force = envs.get('GIT_FORCE', os.environ.get('GIT_FORCE', 'false'))
            git_force_flag = ' -f ' if git_force.lower() == 'true' else ''

            host_source = ''

            mounts = container.attrs.get('Mounts', [])

            print(container.name, " : check for update ...")
            if not mounts:
                print("ERROR: no mounts found")
                continue

            for mount in mounts:
                if mount['Destination'] == git_volume:
                    host_source = mount['Source']
                    break
            else:
                print("ERROR: volume not found")
                continue

            path = os.path.join(MOUNT_ROOT, host_source[1:])

            if not os.path.exists(os.path.join(path, '.git')):
                print("Clone ", git_remote)
                cmd = "git clone -b %s %s ." % (git_branch, git_remote)
                subprocess.Popen(cmd)

            else:
                cmd = "git checkout %s %s && git pull %s" % (
                    git_force_flag, git_branch, git_force_flag
                )
                subprocess.Popen(cmd)

        end_at = time.time()

        if end_at - start_at < ps_interval:
            time.sleep(ps_interval - (end_at - start_at))


if __name__ == '__main__':
    main()

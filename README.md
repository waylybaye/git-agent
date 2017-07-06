# git-agent
a docker image helps you pull all git volumes automatically


## Usage

1. Create a `git-agent` container

```sh
docker run -d -v /:/rootfs \
-v /var/run/docker.sock:/var/run/docker.sock:ro \
hyperapp/git-agent
```

You need to mount `/` to `/rootfs` to allow `git-agent` to update all other containers' volumes.


2. Start your container with `git-agent` ENV

```sh
docker run --rm -it -e GIT_VOLUME='/srv' \
-e GIT_REMOTE='https://github.com/waylybaye/git-agent.git' \
-v /srv s alpine sh
```

### git-agent docker envs

```
GIT_INTERVAL: pull interval, default to 300 (seconds)
GIT_FORCE: force to pull
```


### other container's docker envs

```
# required
GIT_VOLUME: the volume inside your container
GIT_REMOTE: remote git repo, NOTE ssh need interactive confirm when first clone

# optional
GIT_BRANCH: branch to work on, default to master
GIT_INTERVAL: check for update every GIT_INTERVAL seconds, default to 5*60
GIT_FORCE: force to pull, default to git-agent's GIT_FORCE
GIT_CHOWN: run chown -r $GIT_CHOWN after git updated
GIT_CHMOD: run chmod $GIT_CHMOD after git updated
```

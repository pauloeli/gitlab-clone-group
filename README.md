# gitlab-clone-group

> **Based on [adroste/gitlab-clone-group](https://github.com/adroste/gitlab-clone-group)**

Python script to clone all GitLab projects of a group keeping the tree structure. Tested with GitLab API v4.

I found problems in some structures, where list generated by groups don't show some projects (I don't know why). So, I
get all projects which user have permission and make a filter. It's not so performative, but I get all I want.

Python isn't my first language, so make comfortable to improve or submit changes.

## Usage

1. Download the gitlab-clone-group.py
2. Generate a private access token with *read_api* and *read_repository* rights
3. Specify the "root" name of group. (after `gitlab.com`)
4. Run the script

### Example:

```
python3 gitlab-clone-group.py --token glabc-XXX "personal/services" .
```

### Help:

```
usage: gitlab-clone-group.py [-h] [--token TOKEN] [--gitlab-domain GITLAB_DOMAIN] group_id directory

positional arguments:
  group                 group path (piece)
  directory             directory to clone repos into

options:
  -h, --help            show this help message and exit
  --token TOKEN         gitlab private access token with read_api and read_repository rights
  --gitlab-domain       domain of Gitlab instance to use, defaults to: gitlab.com
  --dump                if you want to dump all items in a text file list
  --dump-file           file location to dump items
```

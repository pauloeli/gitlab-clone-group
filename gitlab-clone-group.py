#!/usr/bin/env python3

import argparse
import json
import os
import posixpath

import requests
from git import Repo

MAX_ITENS_PER_PAGE = 100

parser = argparse.ArgumentParser('gitlab-clone-group.py')
parser.add_argument('group', help='group path (piece)', default='personal/services')
parser.add_argument('directory', help='directory to clone repos into')
parser.add_argument('--dump', help='if you want to dump all items in a text file list', type=bool, default=False)
parser.add_argument('--dump-file', help='file location to dump items', type=str)
parser.add_argument('--token', help='Gitlab private access token with read_api and read_repository rights')
parser.add_argument('--gitlab-domain', help='Domain of Gitlab instance to use, defaults to: gitlab.com', default='gitlab.com')

args = parser.parse_args()


def get_projects(page):
    api_url = 'https://{0}?private_token={1}&per_page={2}&page={3}'.format(
        posixpath.join(args.gitlab_domain, 'api/v4/projects'), args.token, MAX_ITENS_PER_PAGE, page)
    response = requests.get(api_url)
    return response, response.headers['X-Total']


def get_rel_path(path, base_ns):
    subpath = path[len(base_ns):]
    if subpath.startswith('/'):
        subpath = subpath[1:]
    return posixpath.join(args.directory, subpath)


response = get_projects(1)

cloned_projects = int(0)

for e in range(int(response[1]) // 100 + (int(response[1]) % 100 > 0)):
    page = (e + 1)

    if page > 1:
        response = get_projects(e)

    projects = response[0].json()
    print('Found %d projects in page: {0}'.format(page))

    if args.dump and not args.dump_file:
        with open('{0}.json'.format(args.dump_file), 'a') as f:
            json.dump(projects, f)

    for p in projects:
        path_with_namespace = p['path_with_namespace']
        if args.group not in path_with_namespace:
            continue

        base_ns = os.path.commonprefix([p['namespace']['full_path'] for p in projects])

        abs_dir = os.path.abspath(args.directory)
        os.makedirs(abs_dir, exist_ok=True)

        clone_dir = get_rel_path(p['namespace']['full_path'], base_ns)
        project_path = get_rel_path(p['path_with_namespace'], base_ns)
        print('Cloning project: %s' % project_path)
        if os.path.exists(project_path):
            print('\tProject folder already exists, skipping')
        else:
            print('\tGit url: %s' % p['ssh_url_to_repo'])
            os.makedirs(clone_dir, exist_ok=True)
            Repo.clone_from(p['ssh_url_to_repo'], project_path)
            cloned_projects += 1

print('\t{0} are cloned'.format(cloned_projects))

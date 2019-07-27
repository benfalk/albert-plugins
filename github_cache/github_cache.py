"""
GitHub Cache

This script is designed to build a lookup cache of repos
for orgs and users you want to have quick information access to.
"""
import http.client
import json
import re
from os import path
from base64 import encodestring

# Regex that when found has a two groups, the first being
# the path for the link to the github api, and the second
# is the text for the relationship
# IE: ('/user/2657901/repos?page=2', 'next')
link_regex = re.compile('api.github.com([^>]*)>; rel="([^"]*)"')
headers = {}
config = {'users':[], 'orgs':[]}

location = path.expanduser("~/.github_cache/token")
if path.exists(location):
    token_file = open(location, "r")
    token = json.load(token_file)
    token_file.close()
    auth_pair = "%s:%s" % (token['user'], token['token'])
    encoded_auth = encodestring(bytes(auth_pair, 'utf8')).decode().strip()
    headers.update({'Authorization': "Basic %s" % encoded_auth})

location = path.expanduser("~/.github_cache/config")
if path.exists(location):
    config_file = open(location, "r")
    config = json.load(config_file)
    config_file.close()

headers.update({'User-Agent': 'GitHub Cache'})

def get(api_endpoint):
    conn = http.client.HTTPSConnection("api.github.com")
    conn.request("GET", api_endpoint, "", headers)
    return conn.getresponse()

def links_from_resp(resp):
    if resp.headers['Link'] is None:
        return {}

    raw_links = resp.headers['Link'].split(",")
    groups = list(map(lambda link: re.search(link_regex, link).groups(), raw_links))
    return dict((k,v) for v,k in groups)

def all_items_for(link):
    items = []

    while True:
        resp = get(link)
        items = items + json.load(resp)
        link = links_from_resp(resp).get('next')
        if link is None:
            break

    return items

def user_repos(user):
    return all_items_for("/users/%s/repos?per_page=100" % user)

def org_repos(org):
    return all_items_for("/orgs/%s/repos?per_page=100" % org)


repos = []

for user in config['users']:
    print("Fetching User [%s] Repos..." % user)
    repos = repos + user_repos(user)

for org in config['orgs']:
    print("Fetching Org [%s] Repos..." % org)
    repos = repos + org_repos(org)

with open('all-data.json', 'w') as outfile:
    json.dump(repos, outfile, indent=4)
    print('all-data.json file generated')

with open('repo-names.txt', 'w') as outfile:
    full_names = list(map(lambda r: r.get('full_name'), repos))
    outfile.write('\n'.join(full_names))
    print('repo-names.txt file generated')

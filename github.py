#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
                             
"""
import urllib2
import urllib
import os
import ConfigParser
from urllib2 import HTTPError
try:
    import simplejson as json
except ImportError:
    import json


class CommandDict(dict):
    """An implementation of dictionary which adds commands to dictioanry by the
    use of decorators
    """
    def add(self, func):
        self[func.__name__] = func


USERNAME = PASSWORD = OWNER = None
ALLOWED_COMMANDS = CommandDict()



class GitHub(object):
    """Main github class.  Use an instantiated version of this class
    to make calls against the REST API."""

    base_url = 'https://api.github.com/'

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def call(self, url, data=None, as_json=True):
        auth = '%s:%s' % (self.username, self.password)
        auth = {'Authorization': 'Basic %s' % (auth.encode('base64').strip())}
        data = urllib.urlencode(data) if data else None
        real_url = url
        if 'http' != url[:4].lower():
            real_url = self.base_url + url
        request = urllib2.Request(real_url, data, auth)
        response = urllib2.urlopen(request)
        # look for next
        next_link = None
        if 'link' in response.info():
            links = response.info()['link'].split(',')
            for link in links:
                if link.find('rel="next"') != -1:
                    next_link = link[link.index('<')+1:link.index('>')]
                    break
            
        response_data = response.read()
        return ( (json.loads(response_data) if as_json else response_data), next_link)

    def get_issues(self, issue_filter=None):
        """Returns issues"""
        url = 'issues'
        if issue_filter:
            url = "%s?%s" % (url, urllib.urlencode(issue_filter, doseq=True))
        try:
            (issues, next_url) = self.call(url)
            while next_url:
                (next_issues, next_url) = self.call(next_url)
                issues.extend(next_issues)
        except HTTPError:
            issues = {}
        return issues

def set_authentication():
    """Extracts authentication according to above schema

    The auth through arguments when starting the program need not be handled 
    here since, the USERNAME and PASSWORD will be set automatically
    """
    if 'GITHUB_USERNAME' in os.environ and 'GITHUB_PASSWORD' in os.environ:
        (USERNAME, PASSWORD) = (os.environ['GITHUB_USERNAME'], os.environ['GITHUB_PASSWORD'])
        return

    config_file = os.path.join(os.environ['HOME'], '.github')
    if os.path.exists(config_file):
        config = ConfigParser.RawConfigParser()
        config.read(config_file)
        USERNAME = config.get('auth', 'username')
        PASSWORD = config.get('auth', 'password')

    raise Exception("No username and password given")

def get_authenticated_api():
    """Returns authenticated bit bucket API for the current user"""
    if USERNAME is None or PASSWORD is None:
        set_authentication()
    return GitHub(USERNAME, PASSWORD)

def get_repositories(user):
    """Return list of slugs of user's repositries"""
    return [repo['slug'] for repo in user.repositories()]

@ALLOWED_COMMANDS.add
def my_issues():
    """Displays all the issues assigned to you
    """
    api = get_authenticated_api()
    
    issues = api.get_issues()

    for issue in issues:
        print "#%s %s %s" %(issue['number'], issue['title'], issue['html_url'])

def execute_commands(commands):
    """Commands can be passed positional arguments using :
    For example

    github -u username -p password my_issues
    """
    for command in commands:
        if ':' in command:
            method_name, args = command.split(':', 1)
            pargs, kwargs = [], {}
            for arg in args.split(','):
                if '=' not in arg:
                    pargs.append(arg)
                else:
                    kwargs.update([arg.split('=')])
            ALLOWED_COMMANDS[method_name](*pargs, **kwargs)
        else:
            ALLOWED_COMMANDS[command]()


if __name__ == '__main__':
    from optparse import OptionParser
    usage = "usage: %prog [options] command"
    parser = OptionParser(usage=usage, description=__doc__)
    parser.add_option('-u', '--username', dest='username', default=None)
    parser.add_option('-p', '--password', dest='password', default=None)

    (options, args) = parser.parse_args()
    if len(args) == 0:
        parser.error("No command specified")

    USERNAME, PASSWORD = options.username, options.password

    execute_commands(args)

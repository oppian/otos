otos
====

Python scripts to list issues from github and bitbucket.

Original bitbucket script taken from https://gist.github.com/2828291 and some fixes applied.

bitbucket
---------

This script allows you to display all your bitbucket issues in one place and optionally filter it.

By default it will show all your open (which is new and open) issues.

### Usage

```
./bitbucket.py -<options> <command>:<command_options>
```

Options are:

-u, --username --- BitBucket username

-p, --password --- BitBucket password

-o, --owner --- BitBucket owner (for when issues are owned by another user, i.e. your organization, but assigned to you)

-i, --ignore_empty --- If set will not output projects with no issues

Commands are:

my_issues --- Display list of my issues

my_issues options are:

project --- Display issues from a specific project

status --- Display issues with a particular status, by default displays 'new' and 'open'

### Example

Display all my issues from my organization:

```
./bitbucket.py -u oppianmatt -p password -o owner -i my_issues
```

Display all my issues from my organization that is set to 'wontfix':

```
./bitbucket.py -u oppianmatt -p password -o owner -i my_issues:status=wontfix
```

### Auth

The username and password for this program can be set in multiple ways.        
                                                                             
1. Set environment variable                                                    
```
export BITBUCKET_USERNAME = <username>                                           
export BITBUCKET_PASSWORD = <password>                                           
export BITBUCKET_OWNER = <owner>                                                 
```
2. Create a file called .bitbucket in your home directory and set the following
```
[auth]                                                                  
username = <username>                                                   
password = <password>                                                   
owner = <owner>                                                         
```
3. Pass as command line arguments when calling this program


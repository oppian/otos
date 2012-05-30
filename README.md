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
                                                                             
Set environment variables:                                                    

```
	export BITBUCKET_USERNAME = <username>                                           
	export BITBUCKET_PASSWORD = <password>                                           
	export BITBUCKET_OWNER = <owner>                                                 
```

Create a file called .bitbucket in your home directory and set the following:

```
	[auth]                                                                  
	username = <username>                                                   
	password = <password>                                                   
	owner = <owner>                                                         
```

Pass as command line arguments when calling this program:

```
	./bitbucket.py --username <username> --password <password> --owner <owner>
```

github
------

This script allows you to display and filter your github issues.

By default it will show all your open issues.

### Usage

```
./github.py -<options> <command>:<command_options>
```

Options are:

-u, --username --- BitBucket username

-p, --password --- BitBucket password

Commands are:

my_issues --- Display list of my issues

my_issues options can be separated with a ',' and are:

repo --- Display issues from a specific repo

Other options can be used from http://developer.github.com/v3/issues/

### Example

Display all my issues

```
./bitbucket.py -u oppianmatt -p password my_issues
```

Display all my issues from a specific repo (oppian/oppian):

```
./bitbucket.py -u oppianmatt -p password my_issues:oppian/oppian
```

Display all my closed issues

```
./bitbucket.py -u oppianmatt -p password my_issues:state=closed
```

### Auth

The username and password for this program can be set in multiple ways.        
                                                                             
Set environment variables:                                                    

```
	export GITHUB_USERNAME = <username>                                           
	export GITHUB_PASSWORD = <password>                                           
	export GITHUB_OWNER = <owner>                                                 
```

Create a file called .github in your home directory and set the following:

```
	[auth]                                                                  
	username = <username>                                                   
	password = <password>                                                   
```

Pass as command line arguments when calling this program:

```
	./github.py --username <username> --password <password>
```


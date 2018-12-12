---
date: 2018-12-04
title: Discourse Helper
permalink: /helper-discourse
categories:
  - helpers
description: Using the Discourse helper
type: Document
tags: [helpers]
---

Discourse is a helpful client if you are a member of one or more 
[Discourse boards](https://www.discourse.org/). While it's easy enough to go to
a web interface, with the helpme client you can:

 - post your question from the command line
 - easily record and send an asciinema terminal recording
 - include relevant environment variables, if desired

Let's get started!

## Getting Started
If you need to test this first, see the [developer setup](#developer-setup)
instructions at the bottom of the page. If not, continue reading to interact
with an active discourse installation. If you haven't yet, install the 
dependencies for the discourse client, either just for discourse (or for all clients).

```bash
pip install discourse[uservoice]
pip install discourse[all]
```

Note that your system will need openssl libraries. If you get an error message,
see the [dependencies to install here](https://pgpy.readthedocs.io/en/latest/).

### Generate a Token

The ease of this step will depend on if you have an older version of discourse 
(one where an administrator needs to generate a token for you) OR a recent 
update that allows users to generate their own. 

#### User Generation of Tokens

If your discourse site will allow you to generate a token, you can export your
global `HELPME_DISCOURSE_TOKEN=`



#### Admin Generation of Tokens

**All Users Token**

You can generate a single global token (giving access to
all users) to authenticate with the API. This token would be more appropriate for
applications that must act on behalf of all users, and likely not recommended for
helpme. 

If you want this level of token and have admin status (such as with the container deployment above) if you 
click on your user icon in the top right and then Settings, you will see a button for "admin" in the
top right:

<a href="{{ site.baseurl }}/assets/img/helpers/discourse-admin-panel.png">
<img src="{{ site.baseurl }}/assets/img/helpers/discourse-admin-panel.png">
</a>

Then you can click on the API tag to generate your token!

<a href="{{ site.baseurl }}/assets/img/helpers/discourse-token.png">
<img src="{{ site.baseurl }}/assets/img/helpers/discourse-token.png">
</a>

**User Token**

Discourse [also supports](https://meta.discourse.org/t/discourse-api-authentication/25941) 
creating tokens on a per user basis. If you are a board user and don't have
admin, you should contact your board admin to ask for a token to be generated for you.
If you do have admin access, you can navigate to the Admin Settings --> Users
panel:

<img src="{{ site.baseurl }}/assets/img/helpers/discourse-admin-users.png">


Click on a user of interest, and navigate down to the "Permissions" section.

<a href="{{ site.baseurl }}/assets/img/helpers/discourse-user-permissions.png">
<img src="{{ site.baseurl }}/assets/img/helpers/discourse-user-permissions.png">
</a>

And then click "generate." It will show a token.


Whichever method you choose, export the token to the environment. It will be 
found by the client when you start helpme. 

```bash
export HELPME_DISCOURSE_TOKEN=xxxxxxxxxxxxxxxxxxxxx
```

Once you have exported your token, you can use the client.  The token will be 
found the first time you run the client, and cached in your `$HOME/helpme.cfg`
file. If you are interested in how this works, see the [developer](/helpme/docs-development) documentation.

## Setting Defaults

If you post to a single board or category often, you can set some defaults in your
configuration file (and won't be prompted by the client). These defaults
include the discourse board, your username, and the category to post to. If you don't set the board,
you will provide it as an argument like this:

```bash
$ helpme discourse neurostars.org
```

But let's say, for example, that we always are going to be using neurostars! 
We would export this environment variable to set it as default:

```bash
export HELPME_DISCOURSE_BOARD=neurostars.org
```

By default, all boards will be prefixed with https. If you need to use http
instead, then you need to specify this:

```bash
export HELPME_DISCOURSE_BOARD=http://neurostars.org
```

If you don't set the board via the environment or command line, it will prompt
you for it when you run the client.

Here is how to set the category. If it doesn't exist, it won't be used and will
give you a warning message.

```bash
export HELPME_DISCOURSE_CATEGORY=Uncategorized
```

Finally, you can also set your username.

```bash
export HELPME_DISCOURSE_USERNAME=dinosaur
```


## Ask for Help
The main `discourse` command will ask for help from a Discourse board, meaning posting to it. 
This means we will do the following:

 - Ask you for the discourse board identifier, if not provided via command line (1st) or environment (2nd)
 - Ask you to describe the issue that you are having
 - (optional) record an asciinema to show us what is going on

Let's walk through a few examples. We can first ask for help for general discourse,
and be prompted for the board and category. An example asciinema is [here](https://asciinema.org/a/nUA0DqasBsTfEEGH1aVEbCJPv)

### Quick Examples

You can provide optionally the discourse board url and the category (or none at all!) Any
of these three things work:

```bash
# Just have it prompt you for everything
$ helpme discourse

# Provide the board
$ helpme discourse http://127.0.0.1

# Provide the board and topic
$ helpme discourse http://127.0.0.1 Uncategorized
```

And don't forget you can set variables in the environment. The command line specifications
above override environment settings.

### Detailed Example

```bash
$ helpme discourse
[helpme|discourse]
Hello Friend! I'll help you ask a question to a discourse board today.
What is the URL of the board you want to post to? (e.g., https://neurostars.org): http://127.0.0.1
What category board do you want to post to? (e.g., Uncategorized): Uncategorized
Please provide a meaningful title for your question or issue: WHY AM I A DINOSAUR
Now please provide detail: It's just so distressing. Please help.
Would you like to send a terminal recording?
Please enter your choice [Y/N/y/n] : n
Environment  USER|TERM|SHELL|PATH|LD_LIBRARY_PATH|PWD|JAVA_HOME|LANG|HOME|DISPLAY
Is this list ok to share?
Please enter your choice [Y/N/y/n] : y
http://127.0.0.1/t/why-am-i-a-dinosaur/37
[submit=>discourse]
```

If I said yes to the asciinema recording, it would also show the path of it, and 
if I need to do it again (to some other helper) I can supply the asciinema on the command line.

```bash
$ helpme github --asciinema /tmp/helpme.5hcz3w6v.json vsoch/helpme 
```

And here is the post created above!

<a href="{{ site.baseurl }}/assets/img/helpers/discourse-post.png">
<img src="{{ site.baseurl }}/assets/img/helpers/discourse-post.png">
</a>


## Python API
You can also ask for help from within Python! Here is how you create the client:

```python
from helpme.main import get_helper
helper = get_helper('discourse')
```

If you exported the token, it will be found:

```python

helper._get_setting('HELPME_DISCOURSE_TOKEN')
xxxxxxxxxxxxxxxxxxx

```

If not, you would see an error message and you should export it first! Then you
run the client like this:

```python
helper.run()
```

This isn't the intended use of the client, but please [open an issue](https://www.github.com/vsoch/helpme)
if you want help doing this in Python (and more examples).

## Developer Setup

If you want to test this helper first, you can deploy Discourse via a container. If
not, skip this entire section.

```bash

$ mkdir -p /tmp/discourse
$ cd /tmp/discourse
$ curl -sSL https://raw.githubusercontent.com/bitnami/bitnami-docker-discourse/master/docker-compose.yml > docker-compose.yml
$ docker-compose up -d

```

You should be patient while the database migrates, you can check it's status like:

```bash
$ docker-compose logs discourse
discourse_1   | 
discourse_1   | Welcome to the Bitnami discourse container
discourse_1   | Subscribe to project updates by watching https://github.com/bitnami/bitnami-docker-discourse
discourse_1   | Submit issues and feature requests at https://github.com/bitnami/bitnami-docker-discourse/issues
discourse_1   | 
discourse_1   | nami    INFO  Initializing postgresql-client
discourse_1   | postgre INFO  Trying to connect to PostgreSQL server
discourse_1   | postgre INFO  Found PostgreSQL server listening at postgresql:5432
discourse_1   | postgre INFO  PostgreSQL server listening and working at postgresql:5432
discourse_1   | nami    INFO  postgresql-client successfully initialized
discourse_1   | nami    INFO  Initializing discourse
discourse_1   | discour INFO  Patching Discourse...
discourse_1   | postgre INFO  Trying to connect to PostgreSQL server
discourse_1   | postgre INFO  Found PostgreSQL server listening at postgresql:5432
discourse_1   | postgre INFO  PostgreSQL server listening and working at postgresql:5432
discourse_1   | discour INFO  Migrating database...
```

Until that's done, you are best to not restart the containers (it resulted in many
errors for me). When the migration is done (this is what you will see)

```bash
discourse_1   | Started GET "/manifest.webmanifest" for 172.18.0.1 at 2018-12-04 17:00:27 +0000
discourse_1   | Processing by MetadataController#manifest as */*
discourse_1   | Completed 200 OK in 15ms (Views: 0.3ms | ActiveRecord: 3.6ms)
```

The interface will be available at [http://127.0.0.1](http://127.0.0.1).
the username is `user` and the password is `bitnami123`. More details on this 
deployment can be found [here](https://github.com/bitnami/bitnami-docker-discourse#environment-variables).


## Support

If you have any issues with the Discourse helper, please [open an issue](https://www.github.com/vsoch/helpme). If
relevant or you are able, check the [Discourse API Documentation](https://docs.discourse.org/)
for any relevant notes or changes.

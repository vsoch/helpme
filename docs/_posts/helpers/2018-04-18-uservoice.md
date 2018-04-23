---
date: 2017-01-16
title: UserVoice Helper
permalink: /helper-uservoice
categories:
  - helpers
description: Using the UserVoice helper
type: Document
tags: [helpers]
---

<a href="https://www.uservoice.com/" target="_blank">UserVoice</a> is a support system that is commonly deployed
at large centers to accept user requests for help, typically via an email. On the user side of things, the user
can submit a tickete asking for help via email. On the agent (research computing) side, there is a web interface
to manage and respond to the tickets. 

## How is HelpMe useful?
It's very likely that a UserVoice ticket is coming from a user that is working on a command line. This means that in
order to submit a ticket, he or she needs to stop working in the terminal, open a browser to an email client,
and then write up the issue, sometimes copy pasting content from the terminal. While this works for many use cases,
arguably, the extra clicks and need to copy paste are un-needed extra steps. It also does not do well to show the
agent exactly what is going on, or to add extra detail from the environment. Helpme it better integrated because:

 - the user doesn't have to leave the command line where he/she is working
 - the entire experience can be recorded to show the issue directly
 - metadata about the environment is included with the request

## Install
UserVoice isn't one of the default clients provided by HelpMe, so you need to install
one extra dependency:

```bash
$ pip install helpme[uservoice]
```


## Usage

If you are installing helpme yourself, you will need to export a set of environment
variables the first time that you use HelpMe. Primarily you will need a HelpDesk
<a href="http://developer.uservoice.com/docs/api/getting-started/" target="_blank">Api token</a>, 
and to specify that it will not be in a trusted location. Note that @vsoch is waiting 
to hear back from UserVoice support about whether:

 - the user can get a personal access token OR
 - HelpMe can use a single (seen by all) token to grant user tokens

It likely is the case that we will be fine to use the untrusted location key and
secret, and then rely on authentication to the service via the user email. This
documentation will be updated when we know the answer to this.

For now, you can test by way of an untrusted api key and secret, and you will
need to export them to the environment (only once when you first use HelpMe
with UserVoice). For example:

```bash
export HELPME_USERVOICE_SUBDOMAIN=srcc
export HELPME_USERVOICE_API_KEY=xxxxx
export HELPME_USERVOICE_SECRET=xxxxxx
export HELPME_USERVOICE_EMAIL=myname@email.com
```

If you are an admin on a shared resource and want to provide this for your users,
then you can also define these variables in the global configuration in the 
uservoice section:

```bash
[uservoice]
helpme_uservoice_subdomain=srcc
helpme_uservoice_api_key=xxxxx
helpme_uservoice_secret=xxxxxx
```

And your users would be responsible for exporting the email environment variable still.

```bash
export HELPME_USERVOICE_EMAIL=myname@email.com
```

This means that if you are the user on the shared resource, you would only need
to export your email to the environment. If you *don't* have any of these 
variables defined, you will get an error message telling you which are missing:

```bash
ERROR export HELPME_USERVOICE_EMAIL environment or add to helpme.cfg
```

## Ask for Help
A request for help takes the following steps:

 - Ask you to describe the issue that you are having
 - (optional) record an asciinema to show us what is going on
 - (optional) you can choose to include a whitelisted set of environment variables

And then the ticket is submit! Here is what that looks like.

```bash
$ helpme uservoice
[helpme|uservoice]
Hello Friend! I'll help you post a UserVoice ticket today.
Please describe the issue you are having: Hello Research Computing! 
I am having so many problems, I am a very easily distracted user. 
Oh, and I looove Matlab, it's like, so great! Please do my science for 
me and solve the thing. Thanks!
Would you like to send a terminal recording?
Please enter your choice [Y/N/y/n] : Y
asciinema: recording asciicast to /tmp/helpme.bji8orya.json
asciinema: press <ctrl-d> or type "exit" when you're done
...
exit
asciinema: recording finished
asciinema: asciicast saved to /tmp/helpme.bji8orya.json
Asciinema  If you need to run helpme again you can give
           the path to this file with  --asciinema /tmp/helpme.bji8orya.json
Environment  USER|TERM|SHELL|PATH|LD_LIBRARY_PATH|PWD|JAVA_HOME|LANG|HOME|DISPLAY
Is this list ok to share?
Please enter your choice [Y/N/y/n] : Y
https://srcc.uservoice.com/admin/tickets/23818
[submit=>uservoice]
```

You can also use an asciinema that you already have:

```bash
$ helpme uservoice --asciinema /tmp/helpme.bji8orya.json
```

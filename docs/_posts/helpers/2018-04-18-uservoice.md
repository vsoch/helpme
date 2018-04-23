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
variables the first time that you use HelpMe. These include an API token and secret,
along with the subdomain for your UserVoice installation. For example:

```bash
export HELPME_USERVOICE_SUBDOMAIN=srcc
export HELPME_USERVOICE_ID=xxxxx
export HELPME_USERVOICE_SECRET=xxxxxx
```

If you are a user and are using an installation provided on your shared resource, 
your resource provider should have already done this for you.

## Ask for Help

*IN PROGRESS* need to hear back from uservoice about native client keys.

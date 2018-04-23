---
date: 2017-01-16
title: Helper Options
permalink: /docs-options
categories:
  - development
description: Options and configuration for a helper
type: Document
tags: [development]
---

If you are developing a custom helper (or if you have installed it and want to
edit the helpme.cfg file in the root of the install folder, given appropriate permissions)
you can choose from one or more custom options. Setting any custom option for a helper
will influence the data that is submit to the helper system. For example, let's take
a look at Github:


```
[DEFAULT]

[github]
user_message_welcome = Hello Friend! I'll help you post a Github issue today.
user_prompt_repo = What is the Github repository that you want to post to?
record_asciinema = True
record_environment = True
user_prompt_issue = Please describe the issue you are having
```

The helper is going to be called in the order specified there. For example, 
it will first greet the user with a welcome message, and prompt him or her for
the name of the repository if it wasn't provided as an argument at runtime.
It will then ask the user to record an asciinema to capture the issue, 
record a restricted set of environment variables, and then submit the issue 
per the Helper endpoints. Since giving information is at the discretion of the
user, regardless of the configuration setting, the user can say no to providing
any kind of recording or information.

# User Inputs

## user_message_<name>
The `user_message_<name>` value can be set to deliver a custom message to the
user. There is no collection or recording to save data to the helper.

## user_confirm_<name>
This will ask the user to confirm yes or no to a particular query, and return
a boolean to the calling function. For example, specifying this in the 
helpme.cfg:

```
user_confirm_colors = Would you like colors added to the request?
```

Will ask the user "Would you like colors added to the request? [y/n/Y/N]" and
then save the response in the helper data dictionary as:

```python
$ self.data['user_confirm_colors']
True
```

## user_prompt_<name>
The `user_prompt_<name>` value will again prompt the user, but free text is given
until the user presses enter. The data saved is then the user response. For example,
if I want to collect the name of a Github repository I might put this in the config:

```
user_prompt_repo = What is the Github repository that you want to post to?
```

and then if the user types "researchapps/helpme" [ENTER] we save the following
in data:

```python
$ self.data['user_prompt_repo']
'researchapps/helpme'
```

# Recorders
A recorder is a plugin that comes with HelpMe that is configured to perform
a particular kind of recording. This comes down to having a set of functions
under [helpme/action/record.py](../../helpme/action/record.py) that are then
called if the action is found in the configuration.

## record_asciinema
If set and found as True, and if the user approves, record an asciinema to file
that will be upload and submit to the helper's endpoint as a link. The flow of logic
goes as follows:

  1. The user confirms it is ok to record
  2. The record_asciinema setting is present and True in the config
  3. An asciinema file path has not been provided by the user

If the user has previously recorded an asciinema, it can be provided on the command
line of the request:

```bash
$ helpme github --asciinema /tmp/pancakes.json
```

## record_environment
If set and found as True, we look for a section of the same name and a list
of whitelisted variables to include. The user is shown the list to confirm, and
nothing is sent without the user's consent. For a complete list and description
of the environment recording, see [the environment docs](/helpme/docs-environment).

---
date: 2017-01-16
title: Contributing
permalik: /docs-contributing
categories:
  - contribute
description: Hot to contribute to HelpMe
type: Document
tags: [contribute]
---

It's so great that you want to contribute! There are several ways to do this.

 - [Contribute Code](https://www.github.com/vsoch/helpme) meaning these documentation pages, or helpme itself!
 - [Add A Helper](#add-a-helper) a module for a user to ask help from.
 - [Add A Recorder](#add-a-recorder) for a user to request help to an endpoint.
 - [Ask a question](https://www.github.com/vsoch/helpme/issues), anything on your mind.

# Add a Helper
You will first want to add the helper to the list in the helpme/defaults.py 
settings file:

```python
HELPME_HELPERS = ["github", "uservoice"]
```

And add a check for your helper under `helpme/main/__init__.py`

```python
if   HELPME_CLIENT == 'github': from .github import Helper
elif HELPME_CLIENT == 'uservoice': from .uservoice import Helper
elif HELPME_CLIENT == 'yourname': from .yourname import Helper
else: from .github import Helper
```
and this will logically import the Helper class from the submodule named `yourname`,
which you should customize for your helper. Specifically, you will want to pay close 
attention to the following functions:

 - `load_secrets`: is where you should use the various [settings functions](/helpme/docs-settings) to collect variables that you have told the user to export / provide in the environment, or load from the user configuration. You should exit on error if something is missing.
 - `_speak`: is where you should implement any custom _print_ message to the user at the onset of the help session. The user will by default see the name of your client with a small welcome message, and so this implementation is optional.
 - `_start`: is where you should implement any custom functions that need to be called after setup but before collection.
 - `_submit`: is where you should write code to take the self.data dictionary, finished at the end of `self.collect()` to parse and upload to your helper endpoint(s) of interest.

To make writing these functions easier, it's recommended to take one of the
helpers under `helpme/main/<helper>` and use it as a template. Next, decide what steps
you want your helper to take by writing the section in the helpme.cfg file. For information on
this file, [see the settings pages](/helpme/docs-settings).

Finally, write a page in the docs folder under `docs/_posts/helpers` to coincide with your helper.
You should write the page talking to the user and giving instruction on how to use your helper from
start to finish. You can again use another helper page as a guide.

# Add a Recorder
A recorder is a function in `helpme/action/record.py` that is imported as a check to the base
client and then run to collect some kind of recording to save to self.data. To add a recorder, you should:

## Name the record function
All recorders have functions and corresponding configuration names that begin with `record_`. You should follow this convention.

## Write the record function
First write this function! It can be in `helpme/action/record.py` and then imported into the `__init__.py` if desired
so it will be imported into `helpme/main/base/__init__.py` like:

```python
from helpme.action import record_thing
```

## Add a config check
The recorder will be specified for use by a client given that the `record_<name>` is found in the configuration. Thus, you should
add a check for this string in the collect() function of the HelperBase client:

```python
# Option 3: The step is to record an asciinema!
elif step == 'record_asciinema':
    self.record_asciinema()
```

Currently, the recorders are few in number, and thus provided as functions saved with the HelperBase. If the number increases or if its the case
we don't want to provide all by default, this organization can change to import the client recording functions in a more modular way.


---
date: 2017-01-16
title: Create a Helper
permalink: /docs-contribute-helper
categories:
  - contribute
description: How to create a helper
type: Document
---

This page provides more detail on contributing a helper, first described in the
[contributing](/helpme/docs-contributing) pages. As already described, if you are creating a helper, you should:

 - add a module folder under `helpme/main` named according to your helper. You can start with another one of the helpers as a template.
 - add the helper name to the defaults.py file in the `HELPME_HELPERS` list
 - add the helper to be imported if specified in the get_helper function in `helpme/main/__init__.py`
 - create an entry in the helpme/helpme.cfg config file

## What are you responsible for?

*Credentials and Settings*

At the instantiation of each helper, the subclass function `load_secrets` is called.
If your endpoint doesn't require any tokens / settings or other, you don't need to implement
this for your Helper class. If You need to load or check for something, you should write this
function for your class. You can take advantage of the many functions to

*Submission*

When the helper finishes, a data dictionary will be passed to your submit() function with
the recordings, environments, and prompts that were asked for in the config above in a key:value
dictionary. For example, given that we asked for `user_prompt_issue`, `record_asciinema`,
`record_environment`, we might get something that looks like this:

```python
$ self.data   ( -- self refers to the helper 
 {'record_prompt_issue': "Hi I can't get this command to run.",
  'record_asciinema': None,
  'record_environment': None }
```

It is up to you to parse the above into a well formualted API post to the helper endpoint
on behalf of the user. Regardless of the settings in the application helpme.cfg, the user
can choose to not record or collect extra metadata, and so your parsing of the functions should
not expect these fields to be defined or provided. We recommend that you take advantage of 
the dictionary "get" function to ask for a value, and return None if the key is not defined 
in `self.data`:

```python
$ value = self.data.get('record_prompt_issue')
```

*Error Catching*

You should generally take a conservative approach in handling your helper flow. For 
example, exit with the proper exit code if an environment variable that needs to be set
by the user is missing, and use try, catch statements with specific errors.

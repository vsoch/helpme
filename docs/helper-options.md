# Helper Options

If you are developing a custom helper (or if you have installed it and want to
edit the helpme.cfg file in the root of the install folder, given appropriate permissions)
you can choose from one or more custom options. Setting any custom option for a helper
will influence the data that is submit to the helper system. For example, let's take
a look at Github:


```
[DEFAULT]

[github]
user_prompt_issue
record_asciinema = True
record_environment = True
```

The helper is going to be called in the order specified there. For example, 
it will first greet the user (internally, this is the Helper module function start())
and prompt him or her to describe the issue. It will then ask the user to record 
an asciinema to capture the issue, record a restricted set of environment 
variables, and then submit the issue per the Helper endpoints.

# Creating a Helper
Thus, if you are creating a helper, you should:

 - add a module folder under `helpme/main` named according to your helper. You can start with another one of the helpers as a template.
 - add the helper name to the defaults.py file in the `HELPME_HELPERS` list
 - add the helper to be imported if specified in the get_helper function in `helpme/main/__init__.py`
 - create an entry in the helpme/helpme.cfg config file

## What are you responsible for?

*Credentials and Settings*

At the instantiation of each helper, the subclass function `load_secrets` is called.
If your endpoint doesn't require any tokens / settings or other, you don't need to implement
this for your Helper class. If You need to load or check for something, you should write this
function for your class.

*Submission*
When the helper finishes, a data structure will be passed to your submit() function with
the recordings, environments, and prompts that were asked for in the config above in a key:value
dictionary. For example, given that we asked for `user_prompt_issue`, `record_asciinema`,
`record_environment`, we might get something that looks like this:

```python
result
 {'record_prompt_issue': "Hi I can't get this command to run.",
  'record_asciinema': None,
  'record_environment': None }
```

It is up to you to parse the above into a well formualted API post to the helper endpoint
on behalf of the user.


*Error Catching*


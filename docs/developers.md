# Developer Usage

HelpMe is also accessible from within Python! In this documentation we will
show you how to initialize a helper, and then interact with settings and functions.

## Helper

Here is how to load the helper client, in the example we load github.

```python
from helpme.main import get_helper
helper = get_helper('github')
# [helper|github]
```

## Environment Variables and Configuration
There are two primary configuration files, both are called helpme.cfg, but helpme.cfg
lives with the application installation (at the root of the helpme module, meaning 
it might be editable by a system admin or owner but not the user) and the other lives
in the user's $HOME folder. The latter contains user-specific settings like tokens 
and preferences. Each helper has its own namespace in the configuration file. For
example, here we should how the helper "github" might store a variable from the
environment called `HELPME_GITHUB_TOKEN`:

```
[DEFAULT]
alias = rainbow-taco-0103

[github]
helpme_github_token = xxxxxxxx
```

The mapping works so that when the user exports an environment variable that an
application is looking for, if it finds the variable, it will save it to the user
configuration file for discovery next time. The flow looks like this:

 - user exports `HELPME_GITHUB_TOKEN`
 - github helper calls function to get and update a setting
 - the environment variable is found, saved to configuration file
 - next time, the variable is found in the configuration file.

More on the functions to interact with settings is discussed next.

## Helper Settings

The global settings for each helper broadly refer to what shared "HelpMe"
functions should be called per helper. For example, there is a general function
to prompt the user for an asciinema recording, or to collect some subset of 
the environment. We turn these settings on and off via adding sections to the
global helpme.cfg file in the root of the helpme module folder. Here is what
the section for Github might look like when we have turned on asciinema recording
and asked the user for two prompts:

```
```

For a complete list of options that can be given to a helper, see the [options](helper-options.md)
page.

## User Settings
Once the helper is loaded, we can use its various functions to inspect settings.
Here is how we would look for a setting defined in the environment (first priority),
then the config file (second priority) and if found, save it
to the config file for next time. If found, we return the value.

```python
$ helper._get_and_update_setting('HELPME_GITHUB_TOKEN')
12345xxxxxx
```

If you want to do the same, but the setting isn't found in the config *or* 
environment, this function would return None.

```python
$ helper._get_and_update_setting('HELPME_GITHUB_DOESNTEXIST')

```

It can be helpful in this case to give the function a default to return in the
case that nothing is set.


```python
$ helper._get_and_update_setting('HELPME_GITHUB_DOESNTEXIST', 'default')
'default'
```

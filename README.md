# HelpMe

A command line helper when you need it.

**under development**

## Docker

```bash
docker build -t vanessa/helpme .
```

### Interactive Development

```bash
docker run -it --entrypoint bash vanessa/helpme
```

# Overview
HelpMe is a general tool that can support the addition of helpers, or different
modules that have a set of metadata to collect for the user, and based on an internal
configuration file to define these metadata, and (if needed) an external config file
for user variables, we send help requests to the various helpers. For example:

 - `helpme github` posts an issue on a Github board
 - `helpme uservoice` creates a ticket on uservoice


# Usage

```bash

# Post an issue to a Github Repo.
$ helpme github singularityware/singularity

# Post a ticket to UserVoice
$ helpme uservoice
```


# Development

*What is a helper?*
A helper is a submodule in the [helpme/helpers](helpme/helpers) folder that has
a `helpme.cfg` file. Specifically, the configuration file should specify the following:

*How is the application configured?*
The core helpme software has a primary [helpme.cfg](helpme.cfg) that defines various
helper defaults. This file is stored with the installed modules, and not intended to keep
user credentials. However, it can be used to keep global API keys, etc. for a group
of users. For example, here we see a configuration file that holds an API key for 
uservoice, and a base for Github.

```
[DEFAULT]

[uservoice]
client_token 123456

[github]
api_url https://api.github.com/v3
```

*What about user configuration?*

The individual user will have a `helpme.cfg` file placed in his or her `$HOME`,
and this file will serve to hold runtime variables and user-specific customizations.

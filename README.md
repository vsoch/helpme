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

For more details, see our [documentation](https://vsoch.github.io/helpme) that is also under development.

## License

This code is licensed under the Affero GPL, version 3.0 or later [LICENSE](LICENSE).

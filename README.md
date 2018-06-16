# HelpMe

A command line helper when you need it.

![docs/assets/img/interface.png](docs/assets/img/interface.png)

# Overview

HelpMe is a general tool that can support the addition of helpers, or different
modules that have a set of metadata to collect for the user, and based on an internal
configuration file to define these metadata, and (if needed) an external config file
for user variables, we send help requests to the various helpers. For example:

 - `helpme github` posts an issue on a Github board
 - `helpme uservoice` creates a ticket on uservoice

Please [post issues](https://www.github.com/vsoch/helpme/issues)
with questions, feedback, or just to say hello, and see our [complete documentation here](https://vsoch.github.io/helpme).


# Background

Asking for help is a standard need for research software users, and needing to perform this function from a command line is common given the headless environments provided on shared cluster resources.  While interactive web interfaces are the main avenue to submit help tickets and issues to get help, they are many steps away from the original command line where the issue arose, meaning that the user must interrupt a workflow, navigate to another program, and perform several clicks before needing to try to manually capture the problem at hand. At best, the user might copy an error message and the support staff then needs to ask or use internal resources to collect more information. This reality is not ideal because the user often presents a limited summary of the issue, and valuable information about the system, environment, or even a recording of the actual issue are lost. Extra time is spent on further communication and effort to obtain this information. HelpMe resolves these issues by recording information about the issue directly from the source, and allowing users to ask for help without leaving the working environment.

HelpMe is a free to use, open source command line tool that serves one purpose: to connect a user on a command line to a a resource to get help. The software provides a general framework for developers to add "helpers," or different support endpoints to work with "recorders," each a specific way of capturing information like messages, terminal recordings (asciinema), and environment, to easily submit to the endpoint. Importantly, the complex interaction of various application programming interfaces (APIs) with the user's terminal is presented in a simple and intuitive way that puts the user in control of the interaction. By default, the software comes ready to use for interaction with Github and the UserVoice ticketing softwarecommonly used in Research Computing.  The HelpMe [documentation base](https://vsoch.github.io/helpme) is rendered from the same repository and open for contribution. It provides ample detail for developers to add new helpers, recorders, and for users to install the software.


# Installation

## Local

```bash
pip install helpme[all]
pip install helpme[github]
pip install helpme[uservoice]
```

## Docker

You can use the image built on Docker Hub directory

```bash
$ docker run -it --entrypoint bash vanessa/helpme
```

or you can build it from this repository!

```bash
$ docker build -t vanessa/helpme .
```

# Usage

```bash
# Post an issue to a Github Repo.
$ helpme github vsoch/helpme

# Post a ticket to UserVoice
$ helpme uservoice
```

This is a very brief summary of usage. For complete details, see our [documentation](https://vsoch.github.io/helpme).

## Contributing

If you'd like to contribute, we welcome pull requests, feature requests, and any form of help you
might offer! Please see our [contributing guidelines](.github/CONTRIBUTING.md) for more details. Do you
have a question, or did you find a bug? You can [submit an issue](https://www.github.com/vsoch/helpme/issues) and we will help you out.

## License

This code is licensed under the Affero GPL, version 3.0 or later [LICENSE](LICENSE).

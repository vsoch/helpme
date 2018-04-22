---
date: 2018-04-20
title: Environment Recorder
permalink: /record-environment
categories:
  - recorders
description: collector to record subset of environment
type: Document
---

HelpMe has a record_environment recorder that will collect a limited set of
environment variables to (optionally) pass to the helper and assist with
helping the user. Since the user environment can have very sensitive information,
we take a whitelist approach and allow only the subset of variables that are
defined in the `whitelist` variable of the `record_environment` section in
the application helpme.cfg file. Here is the default base, without any
additional edits.

```
[record_environment]
whitelist = user
            term
            shell
            path
            ld_library_path
            pwd
            java_home
            lang,home
            display
```

As another precaution, the user is shown the list at runtime, and asked to
approve (or deny) sending the list.

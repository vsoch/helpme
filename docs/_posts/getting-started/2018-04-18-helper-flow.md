---
date: 2018-04-19
title: The Helper Flow
permalink: /docs-flow
categories:
  - getting started
description: flow of events for a helper
type: Document
tags: [getting-started]
---

# Helper Flows

There are two kinds of helper interactions.

 - [Interactive Flow](#interactive-flow)
 - [Headless Flow](#headless-flow)

## Interactive Flow

The helper follows a logical flow of events, which sandwich a custom routine
between a start and stop procedure. We will review the basic flow here, and you
can read more about configuration of these events under [/helpme/docs-options](/helpme/docs-options/).
The events look like the following:

```
run --> start --> collect --> submit
```

And it all starts with "run," the function that tells the helper to start
execution of the flow.

### run
For each of the below, the base client has a "run" function that executes the
following events:

 - [start](#start)
 - [collect](#collect)
 - [submit](#submit)

Within each function above, the helper class can subclass an equivalently named
(but with an underscore) function that, if it exists, will be called to
extend behavior of the step.

### start
Start is primarily a step to call self.speak(), where the helper announces itself.
If the helper has implemented a self._speak() to add information to show the user
here, then this function is called too.

### collect
collect is the main guts of the collection and recording process. During this
time, the helper section defined in the application helpme.cfg is parsed over,
and each performs some collection or recording action. For more detail on these
actions, see the [documentation on helper options](/docs-options/).

### submit
On submit, the helper is expected to have a json data structure under `self.data`
that should be parsed to submit the help request to the helper's specific endpoint.
The fields that are specified for collection in the configuration file, typically

 - `user_prompt_<name>`
 - `record_asciinema`
 - `record_environment`

Will be provided in the dictionary under indices of the same name. For the asciinema
recording, the fullpath to the file is provided and not the asciinema json itself.

## Headless Flow

A headless flow can optionally be implemented for a helper, and it generally goes 
through the same steps as above, but with minimal user interaction. This means
that the calling function usually supplies needed arguments. This flow is most 
appropriate for integration with other python libraries that might want
to automatically submit issues. For an example, see [the GitHub headless]({{ site.baseurl }}/helper-github#headless) flow.

---
date: 2017-01-16
title: Contributing
permalik: /contributing
categories:
  - contributing
description: Hot to contribute to HelpMe
type: Document
---

# Adding a new helper

You will first want to add the helper to the list in the helpme/defaults.py 
settings file:

```python
HELPME_HELPERS = ["github", "uservoice"]
```

This will expose the helper to the command line client.

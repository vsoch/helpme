---
title: 'HelpMe Command Line Helper Utility'
tags:
  - Docker
  - github
  - uservoice
  - support
  - hpc
  - computing
authors:
 - name: Vanessa Sochat
   orcid: 0000-0002-4387-3819
   affiliation: 1
affiliations:
 - name: Stanford University Research Computing
   index: 1
date: 30 April 2018
bibliography: paper.bib
---

# Summary

Asking for help is a standard need for research software users, and needing to perform this function from a command line is common given the headless environments provided on shared cluster resources.  While interactive web interfaces are the main avenue to submit help tickets and issues to get help, they are many steps away from the original command line where the issue arose, meaning that the user must interrupt a workflow, navigate to another program, and perform several clicks before needing to try to manually capture the problem at hand. At best, the user might copy an error message and the support staff then needs to ask or use internal resources to collect more information. This reality is not ideal because the user often presents a limited summary of the issue, and valuable information about the system, environment, or even a recording of the actual issue are lost. Extra time is spent on further communication and effort to obtain this information. We can resolve these issues by way of developing not just a single tool for a resource, but a framework that records information about the issue directly from the source. Such a tool would allow users to ask for help without leaving the working environment.

HelpMe is a free to use, open source command line tool that serves one purpose: to connect a user on a command line to a a resource to get help. The software provides a general framework for developers to add "helpers," or different support endpoints to work with "recorders," each a specific way of capturing information like messages, terminal recordings [@asciinema], and environment, to easily submit to the endpoint. Importantly, the complex interaction of various application programming interfaces (APIs) with the user's terminal is presented in a simple and intuitive way that puts the user in control of the interaction. By default, the software comes ready to use for interaction with Github [@github] and the UserVoice ticketing software [@uservoice] commonly used in Research Computing.  The HelpMe documentation base [@helpme], shown below, is rendered from the same repository and open for contribution. It provides ample detail for developers to add new helpers, recorders, and for users to install the software. 

![img/helpme.png](img/helpme.png)

Dissemination of Research Computing support tools like HelpMe are essential to be developed in the open source community because of generally small staff in these departments that provide such support to academic researchers. The HelpMe software is open source and freely available on Github [@software], and contribution is highly encouraged to add additional helper endpoints of interest.

# References

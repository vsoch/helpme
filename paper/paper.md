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

HelpMe is a free to use, open source command line tool that serves one purpose: to connect a user on a command line to a a resource to get help. The software provides a general framework for developers to add "helpers," or different support endpoints to work with "recorders," each a specific way of capturing information like messages, terminal recordings [@asciinema], and environment, to easily submit to the endpoint. Importantly, the complex interaction of various application programming interfaces (APIs) with the user's terminal is presented in a simple and intuitive way that puts the user in control of the interaction. By default, the software comes ready to use for interaction with Github [@github] and the UserVoice ticketing software [@uservoice] commonly used in Research Computing.  The HelpMe documentation base [@helpme], shown below, is rendered from the same repository and open for contribution. It provides ample detail for developers to add new helpers, recorders, and for users to install the software. 

![img/helpme.png](img/helpme.png)

The software is open source and freely available on Github [@software], and contribution is highly encouraged to add additional helper endpoints of interest.


# References

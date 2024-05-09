# Pimp my jira

A simple and stupid python helper 
to create multiple jira issues at once

It uses [jira-cli-go](https://github.com/ankitpokhrel/jira-cli) under the hood.


## Usage

```bash
$ pmj --help

Usage: pmj [OPTIONS]

Options:
  -f, --ifile PATH  The input file to be processed
  -n, --dry-run     Dry run the command
  --help            Show this message and exit.
```

Use dry run first 

```bash

 pmj -f test.yaml -n
/Users/manuel.bovo/.nix-profile/bin/jira
(Version="1.5.1", GitCommit="v1.5.1", CommitDate="1970-01-01T00:00:00+00:00", GoVersion="go1.22.2", Compiler="gc", Platform="darwin/arm64")
Loaded 3 issues to process
Dry run, no commands executed
[
    'echo jira issue create -pDEVOPS -P"DEVOPS-13579" -t"Task" -s"Implement GitOps workflow with 
Flux" -b"Set up Flux CD to automate deployment and manage infrastructure configuration stored in 
Git repositories" -C"general"--no-input',
    'echo jira issue create -pDEVOPS -P"DEVOPS-24680" -t"Task" -s"Configure Argo CD for 
Kubernetes clusters" -b"Install and configure Argo CD to provide continuous delivery of 
applications running on Kubernetes clusters" -C"general"--no-input',
    'echo jira issue create -pDEVOPS -P"DEVOPS-36912" -t"Task" -s"Manage Infrastructure as Code 
with Terraform" -b"Develop Terraform modules to provision and manage cloud resources for 
infrastructure deployment and configuration" -C"general"--no-input'
]
```
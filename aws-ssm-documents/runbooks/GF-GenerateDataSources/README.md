# GF-GenerateDataSources

## What does this runbook do?

Generate Grafana data sources configuration file

## Input Parameters

- **AssumeRole**: (Required) IAM Role that runbook will assume to perform AWS call on your behalf
- **InstanceIds**: (Required) List of EC2 instances that runbook will be applied
- **RepositoryUrl**: (Required) HTTP URL of the repository. Including OAuth token in the URL. E.g. https://username:personal-access-token@github.com/username/repo.git
- **Env**: (Required) Which environment that runbook will be applied to. E.g. nonprod, prod

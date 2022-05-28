# GH-CloneRepository

## What does this document do?

Clone Github repository. If the repository is already cloned, repository will be pulled instead

## Input Parameters

- **RepositoryUrl**: (Required) HTTP URL of the repository. Including OAuth token in the URL. E.g. https://username:personal-access-token@github.com/username/repo.git
- **Branch**: Branch that will be checked out. Default `master`
- **WorkingDirectory**: Working directory that the give repository will be cloned into. Default `/opt`

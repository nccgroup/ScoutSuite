<p align="center">
  <img src="https://user-images.githubusercontent.com/4206926/49877604-10457580-fe26-11e8-92d7-cd876c4f6454.png" width=350/>
</p>

#

[![Workflow](https://github.com/nccgroup/ScoutSuite/workflows/CI%20Workflow/badge.svg)](https://github.com/nccgroup/ScoutSuite/actions)
[![CodeCov](https://codecov.io/gh/nccgroup/ScoutSuite/branch/master/graph/badge.svg)](https://codecov.io/gh/nccgroup/ScoutSuite)

[![PyPI version](https://badge.fury.io/py/ScoutSuite.svg)](https://badge.fury.io/py/ScoutSuite)
[![PyPI downloads](https://img.shields.io/pypi/dm/scoutsuite)](https://img.shields.io/pypi/dm/scoutsuite)
[![Docker Hub](https://img.shields.io/badge/Docker%20Hub-rossja%2Fncc--scoutsuite-blue)](https://hub.docker.com/r/rossja/ncc-scoutsuite/)
[![Docker Pulls](https://img.shields.io/docker/pulls/rossja/ncc-scoutsuite.svg?style=flat-square)](https://hub.docker.com/r/rossja/ncc-scoutsuite/)

## Description
This pull request introduces support for key AWS container services—ECR (Elastic Container Registry), EKS (Elastic Kubernetes Service), and ECS (Elastic Container Service) within ScoutSuite. The changes extend the tool's capabilities to comprehensively assess the security posture of AWS environments utilizing container services.

New Features:

AWS Container Service Support:
Integration for ECR, EKS, and ECS services has been implemented, allowing ScoutSuite to analyze and report on the security configuration of these AWS container services.

Sample Rules:
To jumpstart the assessment process, several sample rules have been incorporated to evaluate the vulnerability and compliance status of the AWS container services. These rules cover key security considerations in line with best practices.

HTML Report Validation:
The HTML reports generated by the modified code have been reviewed to confirm that they accurately represent the security posture of AWS container services.

Issue Resolution:
This pull request addresses the concerns raised in GitHub issue #1491, providing the requested support for AWS container services and delivering a comprehensive solution for security assessment within these environments.



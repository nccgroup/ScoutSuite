# DockerScoutSuiteRunner.ps1

PowerShell script for running ScoutSuite security scans in an existing Docker container.

## Prerequisites

1. PowerShell 5.1+
2. Existing ScoutSuite Docker container
3. AWS CLI configured with profiles

## Script Deployment

1. Copy script to container:
   ```powershell
   # Copy script to container
   docker cp DockerScoutSuiteRunner.ps1 scoutsuite-runner:/scout/
   
   # Copy AWS credentials (if needed)
   docker cp "$env:USERPROFILE\.aws" "scoutsuite-runner:/root/.aws"
   ```

2. Set results directory:
   ```powershell
   # Local directory must match container mount point
   $localResultsDirectory = "/scout/results"
   ```

3. Run script in container:
   ```powershell
   docker exec scoutsuite-runner pwsh /scout/DockerScoutSuiteRunner.ps1
   ```

## Output Location
```
/scout/results/
    profile1/
        yyyy-MM-dd_HH-mm-ss/
            scoutsuite-report.html
```

## Troubleshooting

Test container access:
```powershell
docker exec scoutsuite-runner pwd  # Should show /scout
docker exec scoutsuite-runner ls /root/.aws  # Check AWS credentials
```

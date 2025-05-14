# RunScoutSuiteAWSAudit.ps1

A PowerShell script that automates ScoutSuite security audits against multiple AWS accounts. This script runs ScoutSuite scans locally and saves results to your local filesystem.

## Prerequisites

- PowerShell 5.1 or higher
- Python installed and in PATH
- ScoutSuite installed
- AWS CLI configured with profiles
- AWS credentials file (.aws folder)
- Network access to AWS services

## Required AWS Permissions

Minimum IAM permissions needed for the script:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "sts:GetCallerIdentity"
            ],
            "Resource": "*"
        }
    ]
}
```

## Configuration

The script uses these main variables:
```powershell
[string[]]$awsProfiles = @('', '', '', '')  # AWS profile names to audit
$localResultsDirectory = ""                  # Local directory to save results
$scoutExecutable = "ScoutSuite\scout.py"    # Path to ScoutSuite executable
```

## Usage

1. Edit the script to set your AWS profiles:
   ```powershell
   $awsProfiles = @('profile1', 'profile2', 'profile3')
   ```

2. Set your local results directory:
   ```powershell
   $localResultsDirectory = "C:\ScoutSuite-Results"
   ```

3. Run the script:
   ```powershell
   .\RunScoutSuiteAWSAudit.ps1
   ```

## Output

The script creates timestamped directories for each profile:
```
LocalResultsDirectory/
├── profile1/
│   └── yyyy-MM-dd_HH-mm-ss/
│       └── scoutsuite-results/
├── profile2/
│   └── yyyy-MM-dd_HH-mm-ss/
│       └── scoutsuite-results/
```

## Process Flow

1. Iterates through configured AWS profiles
2. Creates timestamped directory for each profile
3. Runs ScoutSuite against each profile
4. Saves results locally with timestamp

## Error Handling

The script includes basic error handling for:
- Directory creation
- ScoutSuite execution

## Helper Commands

Test your setup with these commands:

```powershell
# Test AWS credentials
aws sts get-caller-identity --profile your-profile-name

# Test directory permissions
Test-Path -Path $localResultsDirectory -IsValid

# Test ScoutSuite installation
python -m scout --help
```

## Tips

1. Use full paths for reliability
2. Ensure write permissions on results directory
3. Test AWS profiles before running bulk scan
4. Monitor disk space for large multi-account scans

# AutomateAWSAudit.ps1

A PowerShell script that runs ScoutSuite security audits against multiple AWS accounts using AWS profiles.

## Prerequisites

- PowerShell 5.1 or higher
- AWS CLI with configured profiles
- Python 3.7+ with ScoutSuite installed
- AWS PowerShell modules:
  ```powershell
  Install-Module -Name AWS.Tools.Common
  ```

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
   .\AutomateAWSAudit.ps1
   ```

## Output

The script creates timestamped directories for each profile:
```
LocalResultsDirectory/
├── profile1/
│   └── yyyy-MM-dd_HH-mm-ss/
│       └── scoutsuite-results
├── profile2/
│   └── yyyy-MM-dd_HH-mm-ss/
│       └── scoutsuite-results
```

## Process Flow

1. Iterates through configured AWS profiles
2. Creates temporary directory for each profile
3. Runs ScoutSuite against each profile
4. Saves results locally with timestamp
5. Cleans up temporary files

## Error Handling

The script includes basic error handling for:
- Directory creation
- ScoutSuite execution
- File cleanup

## Helper Functions

The script includes these useful commands:

```powershell
# Test AWS credentials
aws sts get-caller-identity --profile your-profile-name

# Test ScoutSuite installation
python -m scout --help
```

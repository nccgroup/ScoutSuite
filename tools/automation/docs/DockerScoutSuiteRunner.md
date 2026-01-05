# DockerScoutSuiteRunner.py

A Python script that runs ScoutSuite security audits against multiple AWS accounts using Docker containerization. This script provides a containerized environment for consistent and isolated AWS security assessments across different profiles.

## Prerequisites

- Docker Desktop installed and running
- AWS CLI configured with profiles
- AWS credentials file (.aws folder)
- S3 bucket created for storing reports
- Network access to:
  - AWS services
  - Docker Hub
  - Python pip repositories

## Required AWS Permissions

Minimum IAM permissions needed for the script:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "sts:GetCallerIdentity",
                "s3:PutObject",
                "s3:ListBucket",
                "s3:GetObject"
            ],
            "Resource": "*"
        }
    ]
}
```

## Configuration

The script uses these main variables:
```python
# List of AWS profiles to audit
aws_profiles = ["", "", "", ""]  

# Directory within container for temporary results
temp_results_directory = "/root/ScoutSuite/scoutsuite-results"

# Path to ScoutSuite executable
scout_executable = "/root/ScoutSuite/scout.py"

# S3 bucket for storing reports
s3_bucket_name = ""
```

## Usage

1. Edit the script to set your AWS profiles and S3 bucket:
   ```python
   aws_profiles = ["profile1", "profile2", "profile3"]
   s3_bucket_name = "your-bucket-name"
   ```

2. Set your local results directory:
   ```powershell
   $localResultsDirectory = "C:\ScoutSuite-Results"
   ```

3. Copy script to container:
   ```powershell
   # Copy script to container
   docker cp DockerScoutSuiteRunner.py <container-name>:/ScoutSuite/
   
   # Copy AWS credentials (if needed)
   docker cp "$env:USERPROFILE\.aws" "<container-name>:/root/.aws"
   ```

5. Run script in container:
   ```powershell
   # Start the container if it's stopped
   docker start <container-name>

   # Enter container in interactive mode
   docker exec -it <container-name> /bin/bash

   # Navigate to ScoutSuite directory
   cd /ScoutSuite

   # Run the script
   python DockerScoutSuiteRunner.py

   # Exit container when done
   exit
   ```

## Output

The script generates two types of output:

1. Temporary local results in the container:
   ```
   /root/ScoutSuite/scoutsuite-results/
   ├── profile1/
   │   └── scoutsuite-results/
   ├── profile2/
   │   └── scoutsuite-results/
   └── index.html
   ```

2. Permanent results in S3:
   ```
   your-s3-bucket/
   ├── index.html                # Main dashboard
   └── accounts/
       ├── profile1/
       │   ├── latest/          # Most recent scan
       │   │   └── aws-profile1.html
       │   └── yyyy-MM-dd_HH-mm-ss/
       │       └── aws-profile1.html
       └── profile2/
           ├── latest/
           └── yyyy-MM-dd_HH-mm-ss/
   ```

## Process Flow

1. Iterates through configured AWS profiles
2. For each profile:
   - Creates temporary directory in container
   - Runs ScoutSuite scan
   - Uploads results to S3 with timestamp
   - Creates/updates "latest" folder in S3
   - Cleans up temporary files
3. Generates and uploads index.html dashboard

## Error Handling

The script includes basic error handling for:
- Directory operations
- ScoutSuite execution
- S3 uploads
- File cleanup

## Helper Functions

Test your setup with these commands:

```bash
# Test AWS credentials
aws sts get-caller-identity --profile your-profile-name

# Test S3 bucket access
aws s3 ls s3://your-bucket-name --profile sandbox

# Test ScoutSuite installation
python -m scout --help
```

Note: The script uses the "sandbox" profile for S3 operations. Ensure this profile has the necessary S3 permissions.

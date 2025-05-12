# Define AWS account profiles
[string[]]$awsProfiles = @('', '','','') #Replace with the accounts you want to audit.

# Define the local directory for saving results
$localResultsDirectory = ""  # Replace with your desired local directory

# Path to ScoutSuite executable
$scoutExecutable = "ScoutSuite\scout.py"

# Get the current date
$currentDatetime = Get-Date -Format 'yyyy-MM-dd_HH-mm-ss'

# Iterate through each AWS profile and run ScoutSuite
foreach ($profile in $awsProfiles) {
    
    # Create a temporary directory for the current profile and date
    $tempDirectory = Join-Path -Path $localResultsDirectory -ChildPath "$profile\$currentDatetime"
    if (-Not (Test-Path $tempDirectory)) {
        New-Item -Path $tempDirectory -ItemType Directory -Force
    }

    # Run ScoutSuite for the current profile
    Write-Host "Running ScoutSuite for profile: $profile"
    $scoutSuiteCommand = "python $scoutExecutable aws --profile $profile --report-dir $tempDirectory"
    Invoke-Expression $scoutSuiteCommand

    Write-Host "Report saved to: $tempDirectory"
}

Write-Host "ScoutSuite audit completed and results saved locally for all profiles."

# Define AWS account profiles
[string[]]$awsProfiles = @('management-account','corporate-applications','public-sites','tii-data-lake')

# Define the base directory for saving results
$resultsBaseDirectory = "C:\ScoutSuiteAudits"

# Path to ScoutSuite executable
$scoutExecutable = "C:\Users\ashika.sreerambushan\source\repos\ScoutSuite\scout.py"

# Get the current date
$currentDatetime = Get-Date -Format 'yyyy-MM-dd_HH-mm-ss'


# Iterate through each AWS profile and run ScoutSuite
foreach ($profile in $awsProfiles) {
    
    # Create a directory for the current profile and date
    $profileDirectory = Join-Path -Path $resultsBaseDirectory -ChildPath $profile
    if (-Not (Test-Path $profileDirectory)) {
        New-Item -Path $profileDirectory -ItemType Directory
    }
    
    $dateTimeDirectory = Join-Path -Path $profileDirectory -ChildPath $currentDatetime 
    if (-Not (Test-Path $dateTimeDirectory)) {
        New-Item -Path $dateTimeDirectory -ItemType Directory
    }

    # Run ScoutSuite for the current profile
    Write-Host "Running ScoutSuite for profile: $profile"
    $scoutSuiteCommand = "python $scoutExecutable aws --profile $profile --report-dir $dateTimeDirectory"
    Invoke-Expression $scoutSuiteCommand

}

Write-Host "ScoutSuite audit completed for all profiles."

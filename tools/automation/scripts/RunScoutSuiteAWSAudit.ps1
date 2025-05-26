# Define AWS account profiles
[string[]]$awsProfiles = @('management')
#, 'publicsites', 'corporateapplications', 'tiidatalake') # Replace with the accounts you want to audit.

# Define directories
$tempResultsDirectory = "C:\Users\ashika.sreerambushan\source\repos\ScoutSuite\scoutsuite_reports"
$scoutExecutable = "C:\Users\ashika.sreerambushan\source\repos\ScoutSuite\scout.py"
$s3BucketName = "" # Replace with your S3 bucket name

# Get current date
$currentDatetime = Get-Date -Format 'yyyy-MM-dd_HH-mm-ss'

# Set your CloudFront Distribution ID here
$distributionId = ""   # <-- Replace with your actual Distribution ID
# Define a list to hold CloudFront invalidation paths
$cloudfrontInvalidationPaths = @("/index.html")

function Create-IndexHtml {
    # Create the HTML index file content
    $indexHtml = @"
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ScoutSuite Reports</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { color: #333; }
        table { border-collapse: collapse; width: 100%; }
        th, td { padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }
        a { color: #0066cc; }
    </style>
</head>
<body>

<h1>ScoutSuite Security Reports</h1>
<p>Last updated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')</p>
<table>
    <tr>
        <th>Account</th>
        <th>Link</th>
    </tr>
"@

    foreach ($profile in $awsProfiles) {
        $indexHtml += @"
        <tr>
            <td>$profile</td>
            <td><a href="accounts/$profile/latest/aws-$profile.html">View Report</a></td>
        </tr>
"@
    }

    $indexHtml += @"
    </table>
</body>
</html>
"@

    # Write index.html to temp file
    $indexPath = Join-Path -Path $tempResultsDirectory "index.html"
    New-Item -Path (Split-Path $indexPath) -ItemType Directory -Force | Out-Null
    Set-Content -Path $indexPath -Value $indexHtml

    Write-Host "Uploading index.html to S3 with cache-control headers"
    aws s3 cp $indexPath "s3://$s3BucketName/index.html" `
        --cache-control "no-cache, no-store, must-revalidate" `
        --profile "sandbox1-admin"
    Write-Host "Index.html uploaded successfully"
}

# Run ScoutSuite for each profile
foreach ($profile in $awsProfiles) {
    # Create temporary directory for this run
    $tempDirectory = Join-Path $tempResultsDirectory $profile
    New-Item -Path $tempDirectory -ItemType Directory -Force | Out-Null

    Write-Host "Running ScoutSuite for profile: $profile"
    python $scoutExecutable aws --profile $profile --report-dir $tempDirectory --no-browser
    Write-Host "Results saved in: $tempDirectory"

    # Upload to dated directory with cache-control
    $datedDir = "accounts/$profile/$currentDatetime"
    Write-Host "Uploading report for profile $profile to $datedDir"
    aws s3 cp $tempDirectory "s3://$s3BucketName/$datedDir/" --recursive `
        --cache-control "no-cache, no-store, must-revalidate" `
        --profile "sandbox1-admin"
    Write-Host "Uploaded: $tempDirectory to s3://$s3BucketName/$datedDir/"

    # Update latest directory with cache-control
    Write-Host "Updating 'latest' directory for profile $profile"
    aws s3 sync $tempDirectory "s3://$s3BucketName/accounts/$profile/latest/" `
        --delete `
        --cache-control "no-cache, no-store, must-revalidate" `
        --profile "sandbox1-admin"
    Write-Host "Updated 'latest' directory for profile $profile"

    # Add the path of the main HTML report to the invalidation list
    $mainReportPath = "/accounts/$profile/latest/aws-$profile.html"
    $cloudfrontInvalidationPaths += $mainReportPath

    # Remove the temporary directory
    Remove-Item -Path $tempDirectory -Recurse -Force
}

# Create and upload the index.html after all profiles are processed
Create-IndexHtml

# Invalidate CloudFront cache for all changed files
if ($distributionId -ne "<YOUR_CLOUDFRONT_DISTRIBUTION_ID>") {
    $pathsString = $cloudfrontInvalidationPaths | ForEach-Object { "`"$_`"" } | Join-String " "
    Write-Host "Invalidating CloudFront cache for: $($cloudfrontInvalidationPaths -join ', ')"
    aws cloudfront create-invalidation `
        --distribution-id $distributionId `
        --paths $cloudfrontInvalidationPaths `
        --profile "sandbox1-admin"
    Write-Host "CloudFront invalidation requested for updated files."
} else {
    Write-Host "CloudFront Distribution ID not set! Skipping invalidation."
}

Write-Host "ScoutSuite audit completed and results saved for all profiles."

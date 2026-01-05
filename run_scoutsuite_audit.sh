#!/bin/bash

# Define AWS account profiles
aws_profiles=("management-account" "corporate-applications" "public-sites" "tii-data-lake")
sandbox_profile="sandbox1-admin"

# Path to ScoutSuite executable
scout_executable="scout.py"

# Get the current date
current_datetime=$(date '+%Y-%m-%d_%H-%M-%S')

# Base directory for storing results
results_base_directory="./results"

# Define the S3 bucket path for the sandbox account
s3_bucket="s3://awsconfigauditscoutreport"

# Create the base directory
mkdir -p "$results_base_directory" || { echo "Error creating base directory: $results_base_directory"; exit 1; }

# Iterate through each AWS profile and run ScoutSuite
for profile in "${aws_profiles[@]}"; do
    # Create a directory for the current profile and date
    profile_directory="$results_base_directory/$profile/$current_datetime"
    mkdir -p "$profile_directory" || { echo "Error creating directory: $profile_directory"; continue; }

    # Run ScoutSuite for the current profile
    echo "Running ScoutSuite for profile: $profile"
    if ! python "$scout_executable" aws --profile "$profile" --report-dir "$profile_directory"; then
        echo "Error: ScoutSuite failed for profile: $profile"
        continue
    fi

    # Upload the ScoutSuite report to the S3 bucket in the sandbox account
    echo "Uploading report to S3 bucket in sandbox account: $s3_bucket/$profile/$current_datetime"
    if ! aws s3 cp "$profile_directory/" "$s3_bucket/$profile/$current_datetime/" --recursive --profile "$sandbox_profile"; then
        echo "Error: Failed to upload report for profile: $profile to S3"
    fi
done

# Create or overwrite the index.html file
index_file="$results_base_directory/index.html"
echo "<!DOCTYPE html>" > "$index_file" || { echo "Error writing to index.html"; exit 1; }
echo "<html>" >> "$index_file" || { echo "Error writing to index.html"; exit 1; }
echo "<head><title>ScoutSuite Audit Reports</title></head>" >> "$index_file" || { echo "Error writing to index.html"; exit 1; }
echo "<body><h1>ScoutSuite Audit Reports</h1><ul>" >> "$index_file" || { echo "Error writing to index.html"; exit 1; }

# Iterate through each AWS profile to build the index.html file
for profile in "${aws_profiles[@]}"; do
    # Create a directory for the current profile and date
    profile_directory="$results_base_directory/$profile/$current_datetime"
    
    # Append the link to the index.html file
    echo "<li><a href=\"$profile/$current_datetime/report.html\">$profile Report</a></li>" >> "$index_file" || { echo "Error writing to index.html"; exit 1; }
done

echo "</ul></body></html>" >> "$index_file" || { echo "Error writing to index.html"; exit 1; }

# Check if the index.html file was created successfully
if [ -f "$index_file" ]; then
    echo "Index file created: $index_file"
else
    echo "Error: Index file not created"
fi

echo "ScoutSuite audit completed and uploaded to the sandbox account for all profiles."
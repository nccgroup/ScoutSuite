import os
import subprocess
from datetime import datetime

# List of AWS profiles
aws_profiles = ["", "", "", ""]  #Replace with the accounts you want to audit.

# Temporary directory within the container to save the reports
temp_results_directory = "/root/ScoutSuite/scoutsuite-results"

# Path to ScoutSuite executable
scout_executable = "/root/ScoutSuite/scout.py"

# S3 bucket to send the reports
s3_bucket_name = "" # Replace with the name of your S3 bucket

# Get the current date
current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Create and upload index.html
def create_and_upload_index_html():
    index_html = """<!DOCTYPE html>
    <html>
    <head>
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
        <p>Last updated: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
        <table>
            <tr>
                <th>Account</th>
                <th>Link</th>
            </tr>
    """

    # Add a row for each profile
    for profile in aws_profiles:
        index_html += f"""
            <tr>
                <td>{profile}</td>
                <td><a href="accounts/{profile}/latest/aws-{profile}.html">View Report</a></td>
            </tr>
        """

    # Close the HTML
    index_html += """
        </table>
    </body>
    </html>
    """

    # Write index.html to a temporary file
    index_path = os.path.join(temp_results_directory, "index.html")
    os.makedirs(os.path.dirname(index_path), exist_ok=True)
    with open(index_path, "w") as f:
        f.write(index_html)

    # Upload index.html to the root of the bucket
    subprocess.run([
        "aws", "s3", "cp", 
        index_path, 
        f"s3://{s3_bucket_name}/index.html", 
        "--profile", "sandbox"
    ], check=True)
    
    print("Index.html file uploaded successfully")

# Run ScoutSuite for each profile
for profile in aws_profiles:
    # Create temporary directory for this run
    temp_directory = os.path.join(temp_results_directory, profile)
    os.makedirs(temp_directory, exist_ok=True)

    print(f"Running ScoutSuite for profile: {profile}")
    
    # Run ScoutSuite
    subprocess.run(["python", scout_executable, "aws", "--profile", profile, "--report-dir", temp_directory, "--no-browser"], check=True)
    
    print(f"Results saved in: {temp_directory}")

    # Upload to dated directory
    dated_dir = f"accounts/{profile}/{current_datetime}"
    
    print(f"Uploading report for profile {profile} to {dated_dir}")
    
    # Upload everything in the directory
    subprocess.run([
        "aws", "s3", "cp", 
        temp_directory, 
        f"s3://{s3_bucket_name}/{dated_dir}/", 
        "--profile", "sandbox", "--recursive"
    ], check=True)
    
    print(f"Uploaded: {temp_directory} to s3://{s3_bucket_name}/{dated_dir}/")
    
    # Also copy to a "latest" folder for easy access
    print(f"Updating 'latest' directory for profile {profile}")
    
    # Sync the dated directory to the latest directory
    subprocess.run([
        "aws", "s3", "sync", 
        f"s3://{s3_bucket_name}/{dated_dir}/", 
        f"s3://{s3_bucket_name}/accounts/{profile}/latest/",
        "--profile", "sandbox"
    ], check=True)
    
    print(f"Updated 'latest' directory for profile {profile}")

    # Remove the temporary directory
    subprocess.run(["rm", "-rf", temp_directory], check=True)

# Create and upload the index.html after all profiles are processed
create_and_upload_index_html()

print("ScoutSuite audit completed and results saved for all profiles.")
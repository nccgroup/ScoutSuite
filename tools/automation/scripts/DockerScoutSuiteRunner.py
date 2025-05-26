import os
import subprocess
from datetime import datetime

# --- CONFIGURATION ---
aws_profiles = ["profile1", "profile2"]  # Replace with your AWS profiles
temp_results_directory = "/root/ScoutSuite/scoutsuite-results"
scout_executable = "/root/ScoutSuite/scout.py"
s3_bucket_name = "your-s3-bucket" # Replace with your S3 bucket name
cloudfront_distribution_id = "YOUR_DIST_ID" # Replace with your CloudFront distribution ID

current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

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
    for profile in aws_profiles:
        index_html += f"""
            <tr>
                <td>{profile}</td>
                <td><a href="accounts/{profile}/latest/aws-{profile}.html">View Report</a></td>
            </tr>
        """
    index_html += """
        </table>
    </body>
    </html>
    """

    index_path = os.path.join(temp_results_directory, "index.html")
    os.makedirs(os.path.dirname(index_path), exist_ok=True)
    with open(index_path, "w") as f:
        f.write(index_html)

    # Upload index.html with no-cache headers
    subprocess.run([
        "aws", "s3", "cp", 
        index_path, 
        f"s3://{s3_bucket_name}/index.html", 
        "--profile", "sandbox",
        "--cache-control", "no-cache, no-store, must-revalidate"
    ], check=True)
    print("Index.html file uploaded successfully")

    # Invalidate CloudFront cache for index.html
    subprocess.run([
        "aws", "cloudfront", "create-invalidation",
        "--distribution-id", cloudfront_distribution_id,
        "--paths", "/index.html"
    ], check=True)
    print("CloudFront invalidation for index.html triggered.")

for profile in aws_profiles:
    temp_directory = os.path.join(temp_results_directory, profile)
    os.makedirs(temp_directory, exist_ok=True)

    print(f"Running ScoutSuite for profile: {profile}")
    subprocess.run([
        "python", scout_executable, "aws", "--profile", profile, "--report-dir", temp_directory, "--no-browser"
    ], check=True)
    print(f"Results saved in: {temp_directory}")

    dated_dir = f"accounts/{profile}/{current_datetime}"
    print(f"Uploading report for profile {profile} to {dated_dir}")

    # Upload reports with no-cache headers
    subprocess.run([
        "aws", "s3", "cp", 
        temp_directory, 
        f"s3://{s3_bucket_name}/{dated_dir}/", 
        "--profile", "sandbox", "--recursive",
        "--cache-control", "no-cache, no-store, must-revalidate"
    ], check=True)
    print(f"Uploaded: {temp_directory} to s3://{s3_bucket_name}/{dated_dir}/")

    print(f"Updating 'latest' directory for profile {profile}")

    # Sync to latest with no-cache headers
    subprocess.run([
        "aws", "s3", "sync", 
        f"s3://{s3_bucket_name}/{dated_dir}/", 
        f"s3://{s3_bucket_name}/accounts/{profile}/latest/",
        "--profile", "sandbox",
        "--cache-control", "no-cache, no-store, must-revalidate"
    ], check=True)
    print(f"Updated 'latest' directory for profile {profile}")

    # Invalidate CloudFront cache for this profile's latest reports
    subprocess.run([
        "aws", "cloudfront", "create-invalidation",
        "--distribution-id", cloudfront_distribution_id,
        "--paths", f"/accounts/{profile}/latest/*"
    ], check=True)
    print(f"CloudFront invalidation for /accounts/{profile}/latest/* triggered.")

    # Remove temporary directory
    subprocess.run(["rm", "-rf", temp_directory], check=True)

    # Update index.html after each account
    create_and_upload_index_html()

print("ScoutSuite audit completed and results saved for all profiles.")

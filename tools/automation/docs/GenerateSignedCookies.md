# CloudFront Signed Cookie Generator

A Python script for generating signed cookies for AWS CloudFront private content access.

## Overview

This script generates CloudFront signed cookies that allow authenticated access to private content distributed through Amazon CloudFront. It creates the necessary policy, signs it with your private key, and provides easy-to-use browser console commands for setting the cookies.

## Prerequisites

- Python 3.x
- Required Python packages:
  - cryptography
- AWS CloudFront distribution set up with private content
- CloudFront key pair (public and private keys)

## Key Generation and CloudFront Setup

1. **Generate RSA Key Pair**
   ```bash
   # Generate private key
   openssl genrsa -out private_key.pem 2048

   # Generate public key from private key
   openssl rsa -pubout -in private_key.pem -out public_key.pem
   ```

2. **Upload Public Key to CloudFront**
   - Go to AWS Console → CloudFront
   - Navigate to "Key Management" → "Public Keys"
   - Click "Create Public Key"
   - Enter a name for your key
   - Open public_key.pem and paste the contents
   - Click "Create"

3. **Create Key Group**
   - In CloudFront, go to "Key Management" → "Key Groups"
   - Click "Create Key Group"
   - Enter a name for your key group
   - Select the public key you just created
   - Click "Create"

4. **Configure CloudFront Distribution**
   - Select your distribution
   - Go to "Behaviors"
   - Edit the behavior you want to restrict
   - Under "Restrict Viewer Access", select "Yes"
   - Choose your key group
   - Click "Save Changes"

5. **Get Key Pair ID**
   - Go back to "Public Keys"
   - Note the "Key ID" - this is your KEY_PAIR_ID for the script

## Configuration

Before running the script, configure the following variables in the script:

```python
CLOUDFRONT_DOMAIN = ""  # Your CloudFront domain (e.g., "https://d123456abcdef8.cloudfront.net")
KEY_PAIR_ID = ""       # Your CloudFront key pair ID (e.g., "K2ABCDEFGHIJKL")
PRIVATE_KEY_PATH = r"" # Path to your private key file (e.g., "C:\path\to\private_key.pem")
COOKIE_EXPIRATION = 12 # Cookie expiration time in hours
```

## Features

- Generates CloudFront signed cookies with configurable expiration
- Provides browser console commands for easy cookie setup
- Includes colored output for better readability
- Comprehensive error handling for common issues
- Step-by-step instructions for implementing the cookies

## Usage Instructions

1. **Configuration Setup**
   - Update the configuration variables in the script with your CloudFront details
   - Ensure your private key file is accessible

2. **Running the Script**
   - Execute the script using Python
   - The script will generate the necessary signed cookies

3. **Implementing the Cookies**
   - Open your browser and navigate to your CloudFront domain
   - Open Developer Tools (F12)
   - Copy and paste the provided console commands
   - Verify cookie installation in the Application tab

## Cookie Implementation Steps

1. Open your browser and navigate to any page on your CloudFront domain
2. Open Developer Tools (F12)
3. Click on the Console tab
4. Copy and paste each provided command
5. Verify cookies in Application → Cookies → Your Domain

## Important Deployment Considerations

### Key Rotation Process
When updating or rotating keys:
1. Generate and upload the new public key to CloudFront
2. Update the key groups to include the new public key
3. **Important**: Wait for the CloudFront distribution to fully deploy
   - Distribution status will show "In Progress"
   - Deployment typically takes 1-2 minutes
   - Access using old keys remains valid until deployment completes
   - New signed cookies will only work after deployment finishes

## Troubleshooting

Common issues and solutions:

1. **Private Key Not Found**
   - Verify the path to your private key file
   - Check file permissions

2. **Access Denied After Setting Cookies**
   - Verify cookie domain matches CloudFront domain
   - Check cookie expiration time
   - Ensure CloudFront distribution is properly configured

3. **Invalid Signature Errors**: May occur immediately after key updates
  - Wait for distribution deployment to complete
  - Verify key group contains the correct public key
  - Ensure distribution behavior uses the updated key group

4. **Access Denied After Key Update**:
  - Check distribution deployment status
  - Clear old cookies and set new ones
  - Verify the new KEY_PAIR_ID matches the uploaded public key

## Security Considerations

- Keep your private key secure
- Set appropriate cookie expiration times
- Use HTTPS for all CloudFront distributions
- Regularly rotate CloudFront key pairs

## Technical Details

The script generates three required cookies:
- CloudFront-Policy
- CloudFront-Signature
- CloudFront-Key-Pair-Id

These cookies are domain-specific and secure-only (HTTPS).

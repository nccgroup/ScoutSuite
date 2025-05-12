import time
import json
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from datetime import datetime, timedelta
import os

# ANSI color codes for colored terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
# CloudFront configuration
CLOUDFRONT_DOMAIN = ""  # Replace with your CloudFront domain, e.g. "https://d123456abcdef8.cloudfront.net"
KEY_PAIR_ID = ""  # Replace with your CloudFront key pair ID, e.g. "K2ABCDEFGHIJKL"
PRIVATE_KEY_PATH = r""  # Path to your private key file, e.g. r"C:\path\to\your\private_key.pem"
COOKIE_EXPIRATION = 12  # Hours


def load_private_key():
    """Load the private key file."""
    try:
        with open(PRIVATE_KEY_PATH, 'rb') as key_file:  # Changed to 'rb' for binary read
            private_key = load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )
        return private_key
    except FileNotFoundError:
        print(f"{Colors.RED}ERROR: Private key file not found at '{PRIVATE_KEY_PATH}'{Colors.ENDC}")
        exit(1)
    except Exception as e:
        print(f"{Colors.RED}ERROR: Failed to load private key: {str(e)}{Colors.ENDC}")
        exit(1)
        
def generate_signed_cookies():
    """Generate CloudFront signed cookies."""
    # Check if configuration is set
    if not CLOUDFRONT_DOMAIN or not KEY_PAIR_ID or not PRIVATE_KEY_PATH:
        print(f"{Colors.RED}ERROR: Please configure CLOUDFRONT_DOMAIN, KEY_PAIR_ID and PRIVATE_KEY_PATH in the script.{Colors.ENDC}")
        exit(1)
    
    private_key = load_private_key()
    
    # Set expiration time
    expiration_date = datetime.now() + timedelta(hours=COOKIE_EXPIRATION)
    expiration_timestamp = int(time.mktime(expiration_date.timetuple()))
    
    # Create policy
    policy = {
        "Statement": [
            {
                "Resource": f"{CLOUDFRONT_DOMAIN}/*",
                "Condition": {
                    "DateLessThan": {
                        "AWS:EpochTime": expiration_timestamp
                    }
                }
            }
        ]
    }
    
    # Convert policy to JSON string
    policy_json = json.dumps(policy).replace(" ", "")
    
    # Create policy signature
    policy_bytes = policy_json.encode('utf-8')
    signature = private_key.sign(
        policy_bytes,
        padding.PKCS1v15(),
        hashes.SHA1()
    )
    
    # Encode policy and signature
    policy_b64 = base64.b64encode(policy_bytes).decode('utf-8')
    signature_b64 = base64.b64encode(signature).decode('utf-8')
    
    # Extract domain without https://
    domain = CLOUDFRONT_DOMAIN.replace("https://", "")
    
    # Create cookies dict
    cookies = {
        "CloudFront-Policy": policy_b64,
        "CloudFront-Signature": signature_b64,
        "CloudFront-Key-Pair-Id": KEY_PAIR_ID
    }
    
    # Print cookie information
    print(f"\n{Colors.BLUE}{Colors.BOLD}COOKIE INFORMATION{Colors.ENDC}")
    print(f"{Colors.YELLOW}Domain:{Colors.ENDC} {domain}")
    print(f"{Colors.YELLOW}Expiration:{Colors.ENDC} {expiration_date.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Print commands for browser console
    print(f"\n{Colors.GREEN}{Colors.BOLD}BROWSER CONSOLE COMMANDS:{Colors.ENDC}")
    print(f"{Colors.YELLOW}Copy and paste each of these commands into your browser console:{Colors.ENDC}")
    
    for name, value in cookies.items():
        console_command = f"document.cookie = \"{name}={value}; domain={domain}; path=/; secure\";"
        print(f"{Colors.GREEN}{console_command}{Colors.ENDC}")
    
    return cookies

def print_instructions():
    """Print usage instructions with color formatting."""
    print(f"\n{Colors.BLUE}{Colors.BOLD}HOW TO SET COOKIES IN YOUR BROWSER:{Colors.ENDC}")
    print(f"{Colors.BOLD}Step 1:{Colors.ENDC} Open your browser and navigate to any page on your CloudFront domain")
    print(f"{Colors.BOLD}Step 2:{Colors.ENDC} Open Developer Tools by pressing {Colors.YELLOW}F12{Colors.ENDC} or right-click and select {Colors.YELLOW}Inspect{Colors.ENDC}")
    print(f"{Colors.BOLD}Step 3:{Colors.ENDC} Click on the {Colors.YELLOW}Console{Colors.ENDC} tab")
    print(f"{Colors.BOLD}Step 4:{Colors.ENDC} Copy and paste {Colors.YELLOW}each{Colors.ENDC} command from above, one at a time, and press Enter after each")
    print(f"{Colors.BOLD}Step 5:{Colors.ENDC} Verify cookies are set by:")
    print(f"         - Click on the {Colors.YELLOW}Application{Colors.ENDC} tab in Developer Tools")
    print(f"         - Select {Colors.YELLOW}Cookies{Colors.ENDC} from the left sidebar")
    print(f"         - Click on your domain under Cookies")
    print(f"         - Look for the three CloudFront cookies in the list")
    print(f"\n{Colors.BLUE}{Colors.BOLD}TESTING ACCESS:{Colors.ENDC}")
    print(f"{Colors.BOLD}Step 6:{Colors.ENDC} Navigate to your protected CloudFront content")
    print(f"         - You should now have access to the protected content")
    print(f"         - If you see an access denied error, check troubleshooting in the documentation")

if __name__ == "__main__":
    # Clear screen for better readability
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}           CLOUDFRONT SIGNED COOKIE GENERATOR{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.ENDC}")
    
    # Generate cookies
    print(f"\n{Colors.BLUE}{Colors.BOLD}Generating signed cookies...{Colors.ENDC}")
    generate_signed_cookies()
    
    # Print instructions
    print_instructions()
    
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.ENDC}")
import datetime

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from botocore.signers import CloudFrontSigner

# Define a function to sign the message using the private key
def rsa_signer(message):
    # Load the private key from a file
    with open("C:\\Users\\ashika.sreerambushan\\private_key.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    # Sign the message using the private key
    return private_key.sign(message, padding.PKCS1v15(), hashes.SHA1())

# Set the Key ID and Distribution domain name
key_id = "KCZ21FGS965K8"  # Key ID on the Public Keys Screen
url = "https://d58zunix20d2g.cloudfront.net"  # Distribution domain name

# Calculate the expiry date as one hour from the current time
expire_date = datetime.datetime.utcnow() + datetime.timedelta(hours=1)

# Create a CloudFrontSigner object using the key ID and RSA signer function
cloudfront_signer = CloudFrontSigner(key_id, rsa_signer)

# Create a signed URL that will be valid for one hour from now
signed_url = cloudfront_signer.generate_presigned_url(
    url, date_less_than=expire_date)

# Print the signed URL
print(signed_url)

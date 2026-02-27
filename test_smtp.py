import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Load environment
load_dotenv(project_root / '.env')

# Test credentials
email_user = os.getenv('EMAIL_HOST_USER')
email_pass = os.getenv('EMAIL_HOST_PASSWORD')

print(f"Email User: {email_user}")
print(f"Password Length: {len(email_pass) if email_pass else 0}")
print(f"Password (first 4 chars): {email_pass[:4] if email_pass else 'None'}")
print(f"Password (last 4 chars): {email_pass[-4:] if email_pass else 'None'}")
print(f"Password has spaces: {' ' in email_pass if email_pass else False}")

# Test SMTP connection
import smtplib

print("\n--- Testing SMTP Connection ---")
try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.set_debuglevel(1)
    server.ehlo()
    server.starttls()
    server.ehlo()
    print(f"\nAttempting login with user: {email_user}")
    server.login(email_user, email_pass)
    print("\n✓ SMTP Authentication SUCCESSFUL!")
    server.quit()
except smtplib.SMTPAuthenticationError as e:
    print(f"\n✗ SMTP Authentication FAILED: {e}")
except Exception as e:
    print(f"\n✗ Connection error: {e}")

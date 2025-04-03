#!/usr/bin/env python3
from mastodon import Mastodon
import os
import sys
from src.settings import settings

def check_instance(instance_url, client_id, client_secret, access_token):
    """Test authentication against a specific Mastodon instance"""
    print(f"\nTrying instance: {instance_url}")
    try:
        # Create client
        mastodon = Mastodon(
            client_id=client_id,
            client_secret=client_secret,
            access_token=access_token,
            api_base_url=instance_url
        )
        
        # Test connection
        account = mastodon.account_verify_credentials()
        print(f"✅ SUCCESS: Connected to {instance_url} as @{account.username}")
        print(f"Account ID: {account.id}")
        print(f"Display name: {account.display_name}")
        return True
    except Exception as e:
        print(f"❌ FAILED: {instance_url} - {e}")
        return False

def main():
    """Check authentication against various Mastodon instances"""
    # Get credentials from settings
    client_id = settings.credentials.client_id.get_secret_value()
    client_secret = settings.credentials.client_secret.get_secret_value()
    access_token = settings.credentials.access_token.get_secret_value()
    
    print("=== Mastodon Authentication Checker ===")
    print(f"Using Client ID: {client_id[:8]}...")
    print(f"Using Client Secret: {client_secret[:8]}...")
    print(f"Using Access Token: {access_token[:8]}...")
    
    # Get instances from settings
    instances = [settings.mastodon.instance_url] + settings.mastodon.alt_instances
    
    # Try each instance
    success = False
    for instance in instances:
        if check_instance(instance, client_id, client_secret, access_token):
            success = True
    
    if not success:
        print("\n⚠️ Authentication failed on all tested instances.")
        print("Possible issues:")
        print("1. The access token may be invalid or expired")
        print("2. The app may be registered on a different instance")
        print("3. The credentials may be incorrect")
        print("\nTry updating your credentials in the .env file.")
        sys.exit(1)
    else:
        print("\n✅ Authentication successful on at least one instance.")

if __name__ == "__main__":
    main()

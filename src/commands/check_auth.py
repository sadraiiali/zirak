import os
import sys
from cleo.commands.command import Command
from cleo.helpers import option

class CheckAuthCommand(Command):
    name = "check-auth"
    description = "Check authentication against configured Mastodon instances"
    options = [
        option(
            "verbose",
            "v",
            description="Increase the verbosity of messages",
            flag=True
        )
    ]
    
    def handle(self):
        """Check authentication against various Mastodon instances"""
        # Import here to avoid loading dependencies when just showing help
        from mastodon import Mastodon
        from src.settings import settings
        
        # Get credentials from settings
        client_id = settings.credentials.client_id.get_secret_value()
        client_secret = settings.credentials.client_secret.get_secret_value()
        access_token = settings.credentials.access_token.get_secret_value()
        
        self.line("<info>=== Mastodon Authentication Checker ===</info>")
        self.line(f"Using Client ID: {client_id[:8]}...")
        self.line(f"Using Client Secret: {client_secret[:8]}...")
        self.line(f"Using Access Token: {access_token[:8]}...")
        
        # Get instances from settings
        instances = [settings.mastodon.instance_url] + settings.mastodon.alt_instances
        
        # Try each instance
        success = False
        for instance in instances:
            if self.check_instance(instance, client_id, client_secret, access_token):
                success = True
        
        if not success:
            self.line("\n<error>⚠️ Authentication failed on all tested instances.</error>")
            self.line("<comment>Possible issues:</comment>")
            self.line("1. The access token may be invalid or expired")
            self.line("2. The app may be registered on a different instance")
            self.line("3. The credentials may be incorrect")
            self.line("\n<comment>Try updating your credentials in the .env file.</comment>")
            return 1
        else:
            self.line("\n<info>✅ Authentication successful on at least one instance.</info>")
            return 0

    def check_instance(self, instance_url, client_id, client_secret, access_token):
        """Test authentication against a specific Mastodon instance"""
        # Import here to avoid loading dependencies when just showing help
        from mastodon import Mastodon
        
        self.line(f"\n<question>Trying instance: {instance_url}</question>")
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
            self.line(f"<info>✅ SUCCESS: Connected to {instance_url} as @{account.username}</info>")
            
            if self.option('verbose'):
                self.line(f"Account ID: {account.id}")
                self.line(f"Display name: {account.display_name}")
            
            return True
        except Exception as e:
            self.line(f"<error>❌ FAILED: {instance_url} - {e}</error>")
            return False

# Standalone execution for backward compatibility
def main():
    command = CheckAuthCommand()
    return command.run([])

if __name__ == "__main__":
    sys.exit(main())

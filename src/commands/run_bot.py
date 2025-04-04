import sys
import asyncio
from cleo.commands.command import Command
from cleo.helpers import option

class RunBotCommand(Command):
    name = "run-bot"
    description = "Start the Zirak bot with notification polling"
    options = [
        option(
            "verbose",
            "v",
            description="Increase the verbosity of messages",
            flag=True
        ),
    ]
    
    def handle(self):
        """Start the bot with notification polling"""
        self.line("<info>Starting Zirak bot...</info>")
        try:
            # Import run_bot function here to avoid loading dependencies
            # until the command is actually executed
            from zirak import run_bot
            asyncio.run(run_bot())
            return 0
        except Exception as e:
            self.line(f"<error>Error: {e}</error>")
            return 1

# For backward compatibility
def main():
    command = RunBotCommand()
    return command.run([])

if __name__ == "__main__":
    sys.exit(main())

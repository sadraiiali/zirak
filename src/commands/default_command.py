from cleo.commands.command import Command

class DefaultCommand(Command):
    name = "default"
    description = "The default command executed when no command is provided"
    hidden = True
    
    def handle(self):
        """Display help information when no command is provided"""
        # Simply call the help command
        return self.call("help")

import sys
from cleo.commands.command import Command
from cleo.helpers import argument

class RunCommand(Command):
    name = "run"
    description = "Run a specific task or command"
    arguments = [
        argument(
            "task",
            description="The task to run (e.g., list, check-auth, etc.)",
            optional=True
        )
    ]
    
    def handle(self):
        """Run a specific task or display available tasks"""
        task = self.argument("task")
        
        if not task:
            self.line("<comment>Please specify a task to run.</comment>")
            self.line("Available tasks:")
            
            # Get all registered commands except this one
            commands = []
            for name, cmd in self.application.all().items():
                # Skip the 'run' command itself
                if name == "run":
                    continue
                # Skip hidden commands if they have the is_hidden attribute and it's True
                if hasattr(cmd, "is_hidden") and cmd.is_hidden():
                    continue
                commands.append(cmd)
            
            for command in sorted(commands, key=lambda x: x.name):
                self.line(f"  <info>{command.name}</info>: {command.description}")
            
            return 1
        
        # Special handling for "list" to show all available commands
        if task == "list":
            self.line("<info>Available commands:</info>")
            
            # Get all commands except hidden ones
            commands = []
            for name, cmd in self.application.all().items():
                # Skip hidden commands if they have the is_hidden attribute and it's True
                if hasattr(cmd, "is_hidden") and cmd.is_hidden():
                    continue
                commands.append(cmd)
            
            for command in sorted(commands, key=lambda x: x.name):
                self.line(f"  <info>{command.name}</info>: {command.description}")
            
            return 0
        
        # For any other task, try to run it as a command
        try:
            # Don't pass any arguments - let Cleo handle them natively
            # This avoids double-parsing of options which causes the 
            # "option already exists" error
            return self.call(task)
        except Exception as e:
            self.line(f"<error>Error: {e}</error>")
            return 1

# For standalone execution (backward compatibility)
def main():
    command = RunCommand()
    return command.run([])

if __name__ == "__main__":
    sys.exit(main())

import asyncio
import sys
import importlib
import inspect


async def main():
    # get the function name from the argument and call it
    module_name = sys.argv[1]
    module_name = 'test.' + module_name
    
    module = importlib.import_module(module_name)
    
    if hasattr(module, 'main'):
        # Check if the function is async and call it accordingly
        if inspect.iscoroutinefunction(module.main):
            await module.main()
        else:
            module.main()
    else:
        print(f"No function 'main' in module {module_name}")
    

if __name__ == "__main__":
    asyncio.run(main())

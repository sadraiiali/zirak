import os

def generate_prompt():
    # Define paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(current_dir, 'templates', 'react')
    output_file = os.path.join(current_dir, 'prompt.txt')
    
    # Check if template directory exists
    if not os.path.exists(template_dir):
        print(f"Error: Template directory not found at {template_dir}")
        return False
    
    # Define template files
    index_html_path = os.path.join(template_dir, 'index.html')
    main_js_path = os.path.join(template_dir, 'main.js')
    
    # Check if template files exist
    if not os.path.exists(index_html_path):
        print(f"Error: index.html not found at {index_html_path}")
        return False
    if not os.path.exists(main_js_path):
        print(f"Error: main.js not found at {main_js_path}")
        return False
    
    try:
        # Read template files
        with open(index_html_path, 'r') as f:
            index_html_content = f.read()
        
        with open(main_js_path, 'r') as f:
            main_js_content = f.read()
        
        # Create formatted prompt
        prompt = (
            f"index.html \n"
            f"```\n"
            f"{index_html_content}\n"
            f"```\n\n"
            f"main.js \n"
            f"```\n"
            f"{main_js_content}\n"
            f"```\n"
        )
        
        # Write prompt to file
        with open(output_file, 'w') as f:
            f.write(prompt)
        
        print(f"Prompt generated successfully at {output_file}")
        return True
    
    except Exception as e:
        print(f"Error generating prompt: {str(e)}")
        return False

if __name__ == "__main__":
    generate_prompt()

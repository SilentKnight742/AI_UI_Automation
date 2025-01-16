# from openai import OpenAI
import subprocess
import os
from transformers import T5ForConditionalGeneration, RobertaTokenizer

# api_key = os.getenv("OPENAI_API_KEY")
# client = OpenAI(api_key=api_key)

model_name = "Salesforce/codet5-base"
tokenizer = RobertaTokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

def generate_playwright_script(user_input):
#     response = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": f"Write a Playwright script in JavaScript to perform the following task: {user_input}. Ensure the script is functional, simple, and opens Google.com to complete the task."}
#     ]
# )
#     script_code = response.choices[0].text.strip()
    prompt = f"""
    You are a developer who is using Playwright to automate browsing. 
    Based on the user input, you will generate a JavaScript Playwright script that:
    1. Opens a browser.
    2. Goes to google.com.
    3. Searches for the query specified by the user.
    4. Takes a screenshot of the results page.
    The user input is: {user_input}
    The generated Playwright script should be valid JavaScript code that performs the above actions.
    """
    input_ids = tokenizer.encode("translate English to Python: " + prompt, return_tensors="pt")
    outputs = model.generate(input_ids)
    script_code = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return script_code

def execute_script(script_code, filename="generated_script.js"):
    """
    Saves the generated script to a file and executes it using Node.js.
    """
    # Save the generated script to a file
    with open(filename, "w") as script_file:
        script_file.write(script_code)
    
    try:
        # Run the generated script using Node.js
        result = subprocess.run(["node", filename], capture_output=True, text=True)
        
        # Output the results of the script execution
        print("Execution Output:\n", result.stdout)
        print("Execution Errors (if any):\n", result.stderr)
    except Exception as e:
        print(f"Error executing the script: {e}")

if __name__ == "__main__":
    # Input the task in plain English
    user_input = "search for 'adani share price' on Google"
    
    # Generate the Playwright script
    script_code = generate_playwright_script(user_input)
    print("Generated Playwright Script:\n", script_code)
    
    # Execute the generated script
    execute_script(script_code)

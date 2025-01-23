import subprocess
import ollama

def generate_playwright_script(user_input, url):
    """
    Generate a Playwright script based on the user input.

    Args:
    user_input (str): The task to be performed in plain English.
    url (str): The URL where the task will be performed.

    Returns:
    str: The generated Playwright script.
    """
# Initialize the OLLama client
    client = ollama.Client()

# Define the model and the input prompt
    model = "llama3.2"
    f_prompt = f""" this is the user input for the UI task that needs to be carried out: {user_input} on {url}. break it down into proper steps that will be used to write python code that uses playwright.
    """

# Send the query to the model
    steps = client.generate(model=model, prompt=f_prompt)

    prompt = f"""
    You are now a master at UI test coding in python using playwright. I need t do the following UI task: {user_input} on {url}. Here are the steps to do the same: {steps.response}. I want you to return to me the code for this. bear in mind that you must return only the code and the entire code, absolutely no other text before and after or in between the code. I want JUST the code, because your entire response is going to be written to a file, which will be executed. Any additional text will cause errors.
    """

    response = client.generate(model=model, prompt=prompt)

# Return the generated script
    return response.response


def execute_script(script_code, filename="generated_script.py"):
    """
    Saves the generated script to a file and executes it

    Args:
        script_code (str): The generated Playwright script.
        filename (str, optional): The filename to save the script. Defaults to "generated_script.py".
    """
    # Save the generated script to a file
    with open(filename, "w") as script_file:
        script_file.write(script_code)

    try:
        # Run the generated script using Python
        result = subprocess.run(["python", filename], capture_output=True, text=True)

        # Output the results of the script execution
        print("Execution Output:\n", result.stdout)
        print("Execution Errors (if any):\n", result.stderr)
    except Exception as e:
        print(f"Error executing the script: {e}")


if __name__ == "__main__":
# Input the task in plain English
    user_input = "search for 'adani share price' on Google and click a screenshot of the results page, and save that screenshot."
    url = "https://www.google.com"
    # Generate the Playwright script
    script_code = generate_playwright_script(user_input, url)
    print("Generated Playwright Script:\n", script_code)

    # Execute the generated script
    execute_script(script_code)
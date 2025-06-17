import subprocess

def load_prompt_template():
   with open(r"P:\My_project\LLM\prompt\fix_prompt.txt", "r", encoding="utf-8") as f:

        return f.read()

def generate_fixed_code(vulnerable_code: str) -> str:
    # Load the prompt template and insert the vulnerable code
    prompt_template = load_prompt_template()
    full_prompt = prompt_template.replace("{{code}}", vulnerable_code.strip())

    # Run the prompt using CodeLLaMA
    process = subprocess.Popen(
        ["ollama", "run", "codellama:7b"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8"
    )
    output, error = process.communicate(full_prompt)

    # Optionally extract just the part between //BEGIN and //END
    if "//BEGIN" in output and "//END" in output:
        fixed_code = output.split("//BEGIN")[1].split("//END")[0].strip()
        return fixed_code
    else:
        return output.strip()  # fallback if markers not found

# Example usage for testing:
if __name__ == "__main__":
    test_code = """
#include <stdio.h>

int main() {
    char *ptr;
    printf("%s", ptr);
    return 0;
}
"""
    result = generate_fixed_code(test_code)
    print("fixed Code")
    print(result)

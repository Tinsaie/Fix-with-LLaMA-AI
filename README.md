# FIX_WITH_LLMA AI

A simple AI-powered code fixer using a local LLM (like CodeLlama). This app allows users to input code and receive suggested fixes or improvements via a GUI.

## Features

- Tkinter-based graphical user interface (GUI)
- Input and fix prompts for code
- Integration with local LLMs via `ollama`
---
## Project Structure in folder
```
FIX_WITH_LLMA AI/
│
├── app.py                # GUI using tkinter
├── main.py               # Logic to send prompt and get response from AI
├── prompt/
│   └── fix_prompt.txt    # Template for the AI prompt
├── requirements.txt      # Python libraries needed
└── README.md             # This file
```

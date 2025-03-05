## Demo
[Link](https://www.loom.com/share/17f1ca0c70d44952a69823292ff23017?sid=5a48a226-86e7-47a5-aaab-3de9a6671f1e)

Link to frontend repo: https://github.com/shivamrawat1/tiptap

# Interactive Code Learning Platform
Implemented custom extensions for the TipTap editor.

## Prerequisites

- Node.js (v18.x.x)
- Python (3.11.0)
- pip (Python package manager)
- npm

## Getting Started

### Backend Setup

1. Navigate to the backend directory

```bash
cd tiptap-backend
```
2. Create and Activate a virtual environment

-On Mac/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

-On Windows

```bash
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the backend server

```bash
python run.py
```

## Features

### 1. CodeBlock Extension (with LLMs based Hints)
The CodeBlock extension transforms the editor into an interactive coding environment. Users can write, execute, and debug Python code directly within the document. Each code block comes with an AI-powered hint system that leverages Large Language Models to provide contextual assistance when students are stuck. The extension includes features like real-time code execution, syntax highlighting through Monaco Editor, and the ability to create custom test cases for validation. 

### 2. CommandsMenu Extension (Add Nodes with / Commands)
The CommandsMenu extension provides a slash-command interface (triggered by typing '/') that enables quick insertion of various content blocks. Users can efficiently add code blocks, MCQs, headings, and lists without leaving the keyboard. The menu features fuzzy search capabilities, keyboard navigation, and custom command suggestions based on the current context, making document structuring fast and intuitive.

### 3. BubbleMenu Extension (Inline Toolbar)
The BubbleMenu extension offers a context-sensitive formatting toolbar that appears when text is selected. This floating menu provides quick access to common text formatting options (Marks in TipTap) like bold, italic, and strike-through. The menu is position-aware, ensuring it remains within viewport bounds, and includes subtle animations for a polished user experience. It's designed to minimize mouse movement while maintaining full formatting capabilities.

## Design decisions / Tradeoffs you made

1. **Synchronous vs Asynchronous Hint Generation**: Implemented synchronous hint generation with loading states rather than streaming responses, favoring simplicity over real-time feedback.

2. **Client-Side State Management**: Opted for local state management using React's useState/useEffect instead of global state management, keeping the implementation simpler for the current scope but potentially limiting scalability.

3. **Python Code Execution**: Chose server-side execution with safety constraints over WebAssembly alternatives, prioritizing security and control over offline capabilities.

4. **View/Edit Mode Toggle**: Implemented a global edit/view mode instead of per-component toggles, simplifying the UI but reducing granular control. The view and edit mode act as the student and author/teacher mode respectively - as required by the project.

# CodeConverse

CodeConverse is a dynamic tool designed to facilitate seamless interaction with your GitHub repositories. Utilizing the power of OpenAI's GPT-3 language model, CodeConverse enables you to explore, interact with, and generate detailed responses based on the contents of a GitHub repository. 

## Prerequisites

To use CodeConverse, you need:

- Python 3.6+
- OpenAI API key

## Branches

- **main**: This is the primary branch that allows you to interact with the GitHub repository using OpenAI's GPT-3 language model.
- **Confluence Integration**: This branch is a working version that further includes the ability to send documentation to a Confluence project directly. Refer to the README in this branch for more details.

## Getting Started

1. **Set OpenAI API key:** Set the OpenAI API key as an environment variable `OPENAI_API_KEY`.

   ```
   OPENAI_API_KEY=your-api-key
   ```
   Replace `your-api-key` with your actual OpenAI API key.

2. **Run the Script:** Run the `app.py` Python script.

3. **Enter the GitHub URL:** When prompted, enter the GitHub URL of the repository you want to explore.

4. **Interact with the Language Model:** You can now ask questions or interact with the language model. Type `exit()` to quit.

5. **Generate Documentation:** CodeConverse generates detailed responses about your code to assist with documentation.

## Key Features

- **Repository Cloning & Indexing:** CodeConverse clones and indexes the contents of a GitHub repository for efficient exploration.
- **Multi-format Support:** Supports various file types, including code, text, and Jupyter Notebook files.
- **Detailed Responses:** Utilizes OpenAI's GPT-3 language model to generate detailed answers to user queries based on the repository's contents.
- **Interactive Conversation:** Enables an interactive conversation with the language model, allowing for dynamic responses based on the context of the discussion.
- **Relevant Documents:** Presents the top relevant documents for each question, making it easier to find precise information.

**Note:** The 'Confluence Integration' branch of this repository provides a working version of CodeConverse that allows for direct transmission of generated documentation to a Confluence project. Refer to the README in the 'Confluence Integration' branch for more details. In the future both of them will be merged into one project that works in sync. 

## Contributions

Your contributions are always welcome! Feel free to submit a pull request, create an issue, or reach out directly if you have something you'd like to add or modify. 

Happy coding with CodeConverse!

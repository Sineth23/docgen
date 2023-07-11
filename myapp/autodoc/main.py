#main.py
import os
import tempfile
from dotenv import load_dotenv
from langchain import PromptTemplate, LLMChain
from langchain.llms import OpenAI
from config import WHITE, GREEN, RESET_COLOR, model_name
from utils import format_user_question
from file_processing import clone_github_repo, load_and_index_files, generate_documentation
from questions import ask_question, QuestionContext
import re

from langchain.document_loaders import DirectoryLoader, NotebookLoader
from utils import clean_and_tokenize
#load_dotenv()
#OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")





def generate_documentation(repo_path, llm_chain, model_name, repo_name, github_url, file_type_counts, filenames):
    #extensions = ['txt', 'md', 'markdown', 'rst', 'py', 'js', 'java', 'c', 'cpp', 'cs', 'go', 'rb', 'php', 'scala', 'html', 'htm', 'xml', 'json', 'yaml', 'yml', 'ini', 'toml', 'cfg', 'conf', 'sh', 'bash', 'css', 'scss', 'sql', 'gitignore', 'dockerignore', 'editorconfig', 'ipynb']
    extensions = ['txt','markdown', 'rst', 'py', 'js', 'java', 'c', 'cpp', 'cs', 'go', 'rb', 'php', 'scala', 'html', 'htm', 'xml', 'json', 'yaml', 'yml', 'ini', 'toml', 'cfg', 'conf', 'sh', 'bash', 'css', 'scss', 'sql', 'gitignore', 'dockerignore', 'editorconfig', 'ipynb']

    for ext in extensions:
        glob_pattern = f'**/*.{ext}'
        try:
            loader = None
            if ext == 'ipynb':
                loader = NotebookLoader(str(repo_path), include_outputs=True, max_output_length=20, remove_newline=True)
            else:
                loader = DirectoryLoader(repo_path, glob=glob_pattern)

            loaded_documents = loader.load() if callable(loader.load) else []
            if loaded_documents:
                for doc in loaded_documents:
                    file_path = doc.metadata['source']
                    relative_path = os.path.relpath(file_path, repo_path)
                    # Don't generate documentation for existing README files
                    if relative_path.lower() == 'readme.md':
                        continue
                    doc_text = clean_and_tokenize(doc.page_content)
                    markdown_filename = os.path.basename(relative_path) + '.md'
                    with open(os.path.join(repo_name, markdown_filename), 'w') as md_file:
                        # Generate documentation using the language model
                        doc_content = llm_chain.run(
                            model=model_name,
                            question="Explain this code, and the purpose of each function in the file",
                            context=doc_text,
                            repo_name=repo_name,
                            github_url=github_url,
                            conversation_history="",
                            numbered_documents="",
                            file_type_counts=file_type_counts,
                            filenames=filenames
                        )
                        md_file.write(doc_content)
        except Exception as e:
            print(f"Error loading files with pattern '{glob_pattern}': {e}")
            continue


def count_tokens(text):
    return len(text.split())

def autodoc(github_url):
    #github_url = input("Enter the GitHub URL of the repository: ")
    repo_name = github_url.split("/")[-1]
    print("Cloning the repository...")
    with tempfile.TemporaryDirectory() as local_path:
        if clone_github_repo(github_url, local_path):
            index, documents, file_type_counts, filenames = load_and_index_files(local_path)
            if index is None:
                print("No documents were found to index. Exiting.")
                exit()

            print("Repository cloned. Indexing files...")
            llm = OpenAI(api_key=OPENAI_API_KEY, temperature=0.2)

            # Create a new directory to store the markdown files
            os.makedirs(repo_name, exist_ok=True)

            template = """
            Repo: {repo_name} ({github_url}) | Conv: {conversation_history} | Docs: {numbered_documents} | Q: {question} | FileCount: {file_type_counts} | FileNames: {filenames}

            Instr:
            1. Answer based on context/docs.
            2. Focus on repo/code.
            3. Consider:
                a. Purpose/features - describe.
                b. Functions/code - provide details/samples.
                c. Setup/usage - give instructions with code for setting it up such that anyone can just replicate those exact steps and set it up.
            4. Unsure? Say "I am not sure".

            Answer:
            """

            prompt = PromptTemplate(
                template=template,
                input_variables=["repo_name", "github_url", "conversation_history", "question", "numbered_documents", "file_type_counts", "filenames"]
            )

            llm_chain = LLMChain(prompt=prompt, llm=llm)

            conversation_history = ""
            question_context = QuestionContext(index, documents, llm_chain, model_name, repo_name, github_url, conversation_history, file_type_counts, filenames)

            total_input_tokens = 0
            total_output_tokens = 0
            
            for filename in filenames:
                try:
                    print(f'\nGenerating documentation for {filename}...')
                    question = f"Describe the functionality and usage of the file '{filename}'"
                    question = format_user_question(question)

                    total_input_tokens += count_tokens(question)  # add input tokens

                    answer = ask_question(question, question_context)
                    
                    total_output_tokens += count_tokens(answer)  # add output tokens

                    print(GREEN + '\nDOCUMENTATION\n' + answer + RESET_COLOR + '\n')
                    conversation_history += f"Question: {question}\nAnswer: {answer}\n"
                    
                    # Remove special characters and extensions from filename for the markdown file
                    markdown_filename = re.sub(r'\W+', '_', filename.rsplit('.', 1)[0]) + ".md"
                    
                    # Save the generated documentation in the new directory
                    with open(os.path.join(repo_name, markdown_filename), 'w') as md_file:
                        md_file.write("# Documentation for " + filename + "\n\n" + answer)
                    print(f"{markdown_filename} file saved in the {repo_name} directory.")
                except Exception as e:
                    print(f"An error occurred: {e}")
            
            # assuming a hypothetical token cost (e.g., 0.05 USD)
            token_cost = 0.05

            total_cost = (total_input_tokens + total_output_tokens) * token_cost
            print(f"Total input tokens: {total_input_tokens}")
            print(f"Total output tokens: {total_output_tokens}")
            print(f"Estimated cost: ${total_cost}")
            
        else:
            print("Failed to clone the repository.")

def main5():
    load_dotenv()

    # Define the model and the prompt template
    llm_chain = LLMChain(
        llm=[
            OpenAI(api_key=os.getenv("OPENAI_API_KEY")),
        ],
        prompt_template=PromptTemplate(gpt_code_completion=gpt_code_completion_prompt)
    )

    github_url = input("Enter a GitHub repository URL to clone: ")
    repo_name = github_url.split('/')[-1]

    # Create a temporary directory and clone the repository there
    with tempfile.TemporaryDirectory() as temp_dir:
        local_path = os.path.join(temp_dir, repo_name)
        if not clone_github_repo(github_url, local_path):
            return

        # Load and index files
        documents, index, file_type_counts, filenames = load_and_index_files(local_path)

    # Remove ".git" from the end of the repository name
    repo_name_clean = repo_name.rstrip(".git")
    repo_dir = os.path.join(os.getcwd(), repo_name_clean)
    if not os.path.exists(repo_dir):
        os.makedirs(repo_dir)

    generate_documentation(local_path, llm_chain, model_name, repo_dir, github_url, file_type_counts, filenames)

    # After generating the documentations, check if README.md exists
   # readme_path = os.path.join(repo_dir, 'README.md')
   # if not os.path.exists(readme_path):
   #     # If README.md doesn't exist, create it
   #     with open(readme_path, 'w') as readme_file:
   #         readme_content = "This is the generated README for this repository."
   #         readme_file.write(readme_content)

    # Ask the user questions and search the index
    while True:
        # Get user's question and convert it to the model's input format
        user_question = input("Enter a question to ask the codebase: ")
        if user_question.lower() == 'quit':
            break

        question_context = QuestionContext(
            model=model_name,
            question=user_question,
            context="",
            repo_name=repo_name_clean,
            github_url=github_url,
            conversation_history="",
            numbered_documents="",
            file_type_counts=file_type_counts,
            filenames=filenames
        )

        formatted_question = format_user_question(question_context)

        # Get answers to the question
        answers = ask_question(
            llm_chain=llm_chain,
            documents=documents,
            index=index,
            question=formatted_question,
            num_results=5,
            match_threshold=0.1
        )

        # Display the answers and append them to the README.md file
        with open(readme_path, 'a') as readme_file:
            for i, answer in enumerate(answers):
                print(f"\nAnswer {i+1}: {answer['text']}")
                print(f"Match score: {answer['score']}")
                print(f"File path: {answer['metadata']['source']}")
                readme_file.write(f"\nQuestion: {user_question}")
                readme_file.write(f"\nAnswer {i+1}: {answer['text']}")
                readme_file.write(f"\nMatch score: {answer['score']}")
                readme_file.write(f"\nFile path: {answer['metadata']['source']}\n")


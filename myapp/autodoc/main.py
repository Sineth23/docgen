#main.py
import os
import tempfile
from dotenv import load_dotenv
from langchain import PromptTemplate, LLMChain
from langchain.llms import OpenAI
from config import WHITE, GREEN, RESET_COLOR, model_name
from utils import format_user_question
from file_processing import clone_github_repo, load_and_index_files
from questions import ask_question, QuestionContext
import re

#load_dotenv()
#OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def main():
    github_url = input("Enter the GitHub URL of the repository: ")
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
            while True:
                try:
                    user_question = input("\n" + WHITE + "Ask a question about the repository (type 'exit()' to quit): " + RESET_COLOR)
                    if user_question.lower() == "exit()":
                        break
                    print('Thinking...')
                    user_question = format_user_question(user_question)

                    answer = ask_question(user_question, question_context)
                    print(GREEN + '\nANSWER\n' + answer + RESET_COLOR + '\n')
                    conversation_history += f"Question: {user_question}\nAnswer: {answer}\n"
                except Exception as e:
                    print(f"An error occurred: {e}")
                    break

        else:
            print("Failed to clone the repository.")




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

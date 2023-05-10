import os
import uuid
import click
from os import path, makedirs, getenv
import openai
from rich.progress import Console
import json
from file_utils import file_utils

console = Console()


def configure_proxy():
    os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
    os.environ['HTTPS_PROXY'] = 'https://127.0.0.1:7890'
    proxies = {'http': "http://127.0.0.1:7890",
               'https': "http://127.0.0.1:7890"}
    openai.proxy = proxies


def configure_openai():
    config_file = path.expanduser("~/.openai/config.json")
    if not path.exists(config_file):
        makedirs(path.dirname(config_file), exist_ok=True)
        api_key = input("🔑 Enter your OpenAI API key: ")
        with open(config_file, "w", encoding="UTF-8") as f:
            f.write(f'{{"api_key": "{api_key}"}}')
    else:
        with open(config_file, "r", encoding="UTF-8") as f:
            api_key = json.load(f).get("api_key")
        if not api_key:
            api_key = input("🔑 Enter your OpenAI API key: ")
            with open(config_file, "w", encoding="UTF-8") as f:
                f.write(f'{{"api_key": "{api_key}"}}')
    openai.api_key = api_key or getenv("OPENAI_API_KEY")


@click.group(invoke_without_command=True)
@click.version_option(version="1.0.0")
@click.option("--model", default="gpt-3.5-turbo", help="The OpenAI model type.")
@click.option("--code_path", help="The code path which need to be tested.")
@click.option("--proxy", is_flag=False, default=False, help="Weather use proxy.")
def run(model, code_path, proxy):
    configure_openai()
    if proxy:
        configure_proxy()
    try:
        if code_path==None:
            return
        code = file_utils.read_file(code_path)
    except Exception as e:
        print("Error reading file")
        return

    filename = os.path.basename(code_path)
    unique_id = uuid.uuid4().hex[:6]  # Generate a random 6-character string
    new_filename = f"{filename}_{unique_id}"  # Append the random string to the filename

    """Intention"""
    Intention_message = [{"role": "system",
                          "content": "You are a coding tutor bot to help user summary code."},
                         {"role": "user", "content": "What the intention of this program: " + code}]
    intention = ask_gpt(model, Intention_message, "intention")
    if intention == None:
        return
    file_utils.write_file('Results/' + new_filename + "/Intention/", filename, intention)
    """Codes"""
    Code_message = [{"role": "system",
                     "content": "You are a coding tutor bot to help user write and optimize  code."},
                    {"role": "user",
                     "content": "Generate two programs which achieve this intention:" + intention}]
    generate_codes = ask_gpt(model, Code_message, "codes")
    if generate_codes == None:
        return
    file_utils.write_file('Results/' + new_filename + "/Codes/", filename, generate_codes)
    file_utils.clean_codes('Results/' + new_filename + "/Codes/" + filename)
    """Test cases"""
    case_message = [{"role": "system",
                     "content": "You are a test input generator. You need generate available test input base the codes"},
                    {"role": "user",
                     "content": "Generate diverse test inputs for this program:" + code}]
    test_cases = ask_gpt(model, case_message, "test pool")
    if test_cases == None:
        return
    file_utils.write_file('Results/' + new_filename + "/Cases/", filename, test_cases)

    print("Done and save the results in :" + 'Results/' + new_filename)


def ask_gpt(model, message, status):
    try:
        with console.status("Generate " + status + "\n" + "Waiting for chatgpt...", spinner="dots8Bit"):
            completion = openai.ChatCompletion.create(
                model=model, messages=message
            )
            print(completion["choices"][0]["message"]["content"])
            print("")
        results = ''
        for choice in completion.choices:
            results += choice.message.content
        return results
    except openai.error.AuthenticationError():
        print("🔒 Authentication Failed. Try with a fresh API key.")
        return None
    except Exception:
        print(
            "❌ Failed to get reply from chatGPT. Please try again with a different prompt or check your api key quota."
        )
        return None


@run.command("update")
def update_key():
    """Update the OpenAI API key."""
    config_file = path.expanduser("~/.openai/config.json")
    if not path.exists(config_file):
        makedirs(path.dirname(config_file), exist_ok=True)

    api_key = input("Enter your OpenAI API key: ")
    with open(config_file, "w", encoding="UTF-8") as f:
        f.write(f'{{"api_key": "{api_key}"}}')
    print("API key updated successfully!")


if __name__ == '__main__':
 run()
# import requests
import sys
import subprocess
import openai
import json
openai.api_type = "azure"
openai.api_base = "https://inferenceendpointeastus.openai.azure.com/"
openai.api_version = "2022-06-01-preview"

# API Key set here

# Prints the help commands
def help():
    print("Welcome to CodeHelp! \n Available Commands: Quit (q), Debug (d), Explain (e), Optimize (o), History (h), Help (?)")

# Collects user input
def request_input():
    user_input = input("Pick a Command\n").lower()
    return user_input

# Requests content from the api.
# @Param prompt: prompt to feed to the api
# @Param tokens: max number of tokens to generate
def api_request(prompt="", tokens=400):

    # collects the api response
    api_response = openai.Completion.create(
            engine="athena-text-davinci-002",
            prompt=prompt,
            temperature=0.3,
            max_tokens=tokens,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None)

    # jsonifies response
    json_response = json.dumps(api_response)
    json_obj = json.loads(json_response)

    # collects the text component of the json response
    response = json_obj['choices'][0]['text']

    # prints response as text
    print(response)

    # returns response as text
    return response

# Heart of repl format
# @param file_contents: contents of the file as a string
# @param errlogs: contents of the file's error logs as a string
def replRunner(file_contents, errlogs):

    # initial introduction
    help()

    # initiates variables
    initFileErrLogs = "" + file_contents + errlogs
    history = ""

    while (True):

        # collects user input
        user_input = request_input()

        if user_input == "q":
            print("Exiting CodeHelp")
            break
        elif user_input == "d":
            prompt = 'Explain the issue with the following code, given the file contents and the error output' + initFileErrLogs
            response = api_request(prompt)
            history += response
        elif user_input == "e":
            prompt = "provide an explanation of the following code as if explaining to a novice programmer" + file_contents
            response = api_request(prompt)
            history += response
        elif user_input == "o":
            prompt = "Write an optimized version of the code provided" + file_contents
            response = api_request(prompt)
            history += response
        elif user_input == "h":
            print(history)
        elif user_input == "?":
            help()


def main(file_name):
    try:
        # Read the contents of the file into a string
        with open(file_name, 'r') as f:
            file_contents = f.read()

        # Print the contents of the file
        # print(file_contents)

        # Run the file and get its stderr logs
        process = subprocess.Popen(['python', file_name], stderr=subprocess.PIPE)
        stderr = process.communicate()[1].decode('utf-8')

        # Print the stderr logs of the file
        # print(stderr)

        # initiates the general repl running system
        replRunner(file_contents, stderr)

    except Exception as e:
        print("An error occurred while reading the file or running the file:", e)


if __name__ == "__main__":
    # Get the file name from the command line argument
    file_name = sys.argv[1]
    main(file_name)

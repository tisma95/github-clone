#################################################################
#               Author: Ismael Maurice                          #
#               Language: Python                                #
#               Projet: Github Clone                            #
#               Version: V1                                     #
#               File: main.py                                   #
#################################################################

"""
    The main package which will load the env variable to clone the gihub repositories.
"""

try:
    # Import the env
    from dotenv import dotenv_values

    config = dotenv_values(".env")

    # Define the list of expected .env variable
    expectedKeys = ["DOMAIN", "TOKEN", "FOLDER", "PROTOCOL"]

    # Verify if the contains of env
    if len(config) == 0:
        print("\nThe .env file is empty or not found\n")
        exit(0)

    # Verify that each expected keys are present
    for key in expectedKeys:
        if key not in config:
            print(f"\nThe key/value of {key} is required inside .env\n")
            exit(0)
        elif len(config[key]) < 1:
            print(f"\nThe {key} inside .env is empty\n")
            exit(0)

    # Create the folder for clone
    import os
    resultPath = config["FOLDER"]
    isNewFolder = False
    if not os.path.exists(resultPath):
        # Create the folder
        print(f"\nThe result folder {resultPath} not exists it will be created !\n")
        os.makedirs(resultPath)
        isNewFolder = True

    # Get the env variable and build the request to call
    DOMAIN_URL = config['DOMAIN']
    DOMAIN_PROTOCOL = config["PROTOCOL"]
    DOMAIN_API = f"{DOMAIN_PROTOCOL}://api.{DOMAIN_URL}"
    TOKEN = config['TOKEN']
    # Get the profile of user
    import requests
    headers = {'Authorization': f'Bearer {TOKEN}'}
    response = requests.get(DOMAIN_API + "/user", headers=headers)
    if response.status_code != 200:
        print("\nRequest to Github connexion failed !\n")
        print(response.text)
        exit(0)
    # Convert the response to json
    responseData = response.json()
    USERNAME = responseData["login"]
    print(f"\nThe connexion is successfully we will clone the repositories of {USERNAME}\n")

    # Get the list of repositories
    page = 0
    isContinue = True
    while isContinue:
        page += 1
        responseRepo = requests.get(f"{DOMAIN_API}/user/repos?page={page}", headers=headers)
        if responseRepo.status_code != 200:
            print(f"\nRequest to Github to fetch repository of user {USERNAME} failed !\n")
            print(responseRepo.text)
            exit(0)
        else:
            # Convert the response of repository list
            responseRepoData = responseRepo.json()
            if len(responseRepoData) > 0:
                for repo in responseRepoData:
                    repoName = repo["name"]
                    RESULT_FOLDER = resultPath + "/" + repoName
                    if isNewFolder or not os.path.exists(RESULT_FOLDER):
                        os.mkdir(RESULT_FOLDER)
                        print(f"\nStarting cloning of repository {repoName} inside {RESULT_FOLDER}\n")
                        cloneCommand = f"git clone {DOMAIN_PROTOCOL}://{USERNAME}:{TOKEN}@{DOMAIN_URL}/{USERNAME}/{repoName}.git {RESULT_FOLDER}"
                        os.system(cloneCommand)
                    # Change the folder location
                    os.chdir(RESULT_FOLDER)
                    # Pull all code in all branch
                    os.system("git pull --all")
            else:
                # Stopped it
                isContinue = False

except Exception as err:
    print(f"\nUnexpected {err}, {type(err)}\n")
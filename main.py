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

# Import the modules
import pyfiglet
import os
from helpers import *

# Display the application logo
ASCII_art_1 = pyfiglet.figlet_format("Github Clone", justify="center")
print(ASCII_art_1)

try:
    # Import the env
    from dotenv import dotenv_values

    config = dotenv_values(".env")

    # Verification of config
    verificationCnfig(config=config)

    # Create the folder for clone
    resultPath = config["FOLDER"]
    isNewFolder = createFolder(path=resultPath)

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

    # Get the list of repositories and clone each after each
    page = 0
    isContinue = True
    metric = {
        "success": 0,
        "failed": 0,
        "update": 0,
        "new": 0
    }
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
                    try:
                        repoName = repo["name"]
                        RESULT_FOLDER = resultPath + "/" + repoName
                        if isNewFolder or not os.path.exists(RESULT_FOLDER):
                            os.mkdir(RESULT_FOLDER)
                            print(f"\nStarting cloning of repository {repoName} inside {RESULT_FOLDER}\n")
                            cloneCommand = f"git clone {DOMAIN_PROTOCOL}://{USERNAME}:{TOKEN}@{DOMAIN_URL}/{USERNAME}/{repoName}.git {RESULT_FOLDER}"
                            os.system(cloneCommand)
                            # Increment the number of new repository which has clone
                            metric["new"] += 1
                        else:
                            # Increment the number of new repository which should be updated
                            metric["update"] += 1
                        # Change the folder location
                        os.chdir(RESULT_FOLDER)
                        # Now ge the branch of repository
                        pageBranch = 0
                        isContinueBranch = True
                        while isContinueBranch:
                            pageBranch += 1
                            branchUrl = f"{DOMAIN_API}/repos/{USERNAME}/{repoName}/branches?page={pageBranch}"
                            responseBranch = requests.get(branchUrl, headers=headers)
                            if responseBranch.status_code != 200:
                                print(f"\nRequest to Github to fetch repository {repoName} branchs failed !\n")
                                print(responseBranch.text)
                                exit(0)
                            else:
                                responseBranchData = responseBranch.json()
                                if len(responseBranchData) > 0:
                                    # Loop to checkout all branchs
                                    for branch in responseBranchData:
                                        # Checkout branch
                                        checkoutCommand = f"git fetch origin {branch['name']} && git checkout {branch['name']}"
                                        os.system(checkoutCommand)
                                else:
                                    # Stop fetch the branch
                                    isContinueBranch = False
                        # Pull all code in all branch
                        os.system("git pull --all")
                        # Increment here the number of success
                        metric["success"] += 1
                    except Exception as err:
                        print(f"\nUnexpected {err}, {type(err)}\n")
                        # Increment here the number of failed
                        metric["failed"] += 1
            else:
                # Stopped it
                isContinue = False
    # Display the result of metric
    print("\nThe summary of actions are:\n")
    print(f"Number of new deposit clones: {metric['new']}")
    print(f"Number of repository updates: {metric['update']}")
    print(f"Number of failures: {metric['failed']}")
    print(f"Number of successes: {metric['success']}")

except Exception as err:
    print(f"\nUnexpected {err}, {type(err)}\n")
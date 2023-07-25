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
import constants

# Display the application logo
ASCII_art = pyfiglet.figlet_format(constants.APP_NAME, justify="center")
print(ASCII_art)

try:
    # Import the env
    from dotenv import dotenv_values

    config = dotenv_values(".env")

    # Verification of config
    verificationCnfig(config=config)

    # Create the folder for clone
    resultPath = config["FOLDER"]
    isNewFolder = createFolder(path=resultPath)

    # Get the domain API url
    DOMAIN_API = getUrl(config=config, urlTYpe=constants.API_URL_TYPE)
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

    # Add the username in config
    config["USERNAME"] = USERNAME

    # Get the list of repositories and clone each after each
    metric = {
        "success": 0,
        "failed": 0,
        "update": 0,
        "new": 0
    }
    # Define the list of repo list which has failed to be cloned
    repoListFailed = []
    # Deine the list of repo list which branches have failed to be cloned
    repoListPartial = []
    repoData = getRepositoryData(config=config)
    for repo in repoData:
        try:
            # Get the repo name
            repoName = repo["name"]
            # Specify if the repo is clone or not
            isCloneRepo = False
            # Build the folder and clone the repository if necessary
            RESULT_FOLDER = resultPath + "/" + repoName
            if isNewFolder or not os.path.exists(RESULT_FOLDER):
                createFolder(RESULT_FOLDER)
                print(f"\nStarting cloning of repository {repoName} inside {RESULT_FOLDER}\n")
                # Call the function to clone the repository
                isCloneRepo = cloneRepository(config=config, repoName=repoName, location=RESULT_FOLDER)
                if isCloneRepo:
                    metric["new"] += 1
                else:
                    metric["failed"] += 1
                    # Add in failded list
                    repoListFailed.append(repoName)
            else:
                # Set true it is already clone
                isCloneRepo = True
                # Increment the number of new repository which should be updated
                metric["update"] += 1

            # Checkout and update the branch if repo is clone successfully
            if isCloneRepo:
                # Get the list of branches
                listOfBranchs = getRepositoryBranchesNames(config=config, repoName=repoName)
                if len(listOfBranchs) > 0:
                    # Clone each branch
                    isBranchClone = cloneRepoBranches(location=RESULT_FOLDER, listOfBranch=listOfBranchs)
                    if isBranchClone:
                        # Increment here the number of success
                        metric["success"] += 1
                    else:
                        # Increment the number of failed
                        metric["failed"] += 1
                        # Add in branch failed list
                        repoListPartial.append(repoName)
                else:
                    # Increment the number of failed
                    metric["failed"] += 1
                    # Add in branch failed list
                    repoListPartial.append(repoName)
        except Exception as err:
            print(f"\nUnexpected {err}, {type(err)}\n")
            # Increment here the number of failed
            metric["failed"] += 1

    # Display the result of metric
    print("\nThe summary of actions are:\n")
    print(f"Number of new deposit clones: {metric['new']}")
    print(f"Number of repository updates: {metric['update']}")
    print(f"Number of failures: {metric['failed']}")
    print(f"Number of successes: {metric['success']}")
    if len(repoListFailed) > 0:
        print(f"\nThe list of {len(repoListFailed)} {'repository which' if len(repoListFailed) < 2 else 'repositories which are failed'} failed to be cloned:\n")
        for repo in repoListFailed:
            print(repo)
        print("\n")
    if len(repoListPartial) > 0:
        print(f"\nThe list of {len(repoListPartial)} {'repository' if len(repoListPartial) < 2 else 'repositories'} which failed to be updated:\n")
        for repo in repoListPartial:
            print(repo)
        print("\n")
except Exception as err:
    print(f"\nUnexpected {err}, {type(err)}\n")
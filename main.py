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
import logging

# Init the date
import datetime
now = datetime.datetime.now()
displayDate = now.strftime("%Y-%m-%d")
# Configure the logging
if not os.path.exists('logs') or not os.path.isdir('logs'):
    os.makedirs('logs')
logging.basicConfig(filename=f'logs/{displayDate}.log', format='%(levelname)s:%(message)s', filemode='w', level=logging.DEBUG)

# Display the application logo
ASCII_art = pyfiglet.figlet_format(constants.APP_NAME + f'\n{displayDate}', justify="center")
print(ASCII_art)
message = constants.APP_NAME + f' - {now.strftime("%Y-%m-%d")}'
logging.debug(message)

# Init start time
import time
startTime = time.time()

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
        message = "Request to Github connexion failed !"
        logMessage(message=message, logType="error")
        logMessage(message=response.text, logType="error", addSeparator=False)
        exit(0)
    # Convert the response to json
    responseData = response.json()
    USERNAME = responseData["login"]
    message = f"The connexion is successfully we will clone the repositories of {USERNAME}"
    logMessage(message=message, logType="info")

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
    # Define the list of repo list which branches have failed to be cloned
    repoListPartial = []
    # Define the list of failed update forked
    repoForkFailed = []
    repoData = getRepositoryData(config=config)
    # Display the repository list
    message = f"{len(repoData)} repositories found for user {USERNAME}"
    logMessage(message=message, logType="info")
    for repo in repoData:
        message = f"{repo['name']} ({repo['owner']})"
        logMessage(message=message, logType="info", addSeparator=False)
    for repo in repoData:
        try:
            # Get the repo name and default branch
            repoName = repo["name"]
            defaulBranch = repo["defaultBranch"]
            # Specify the right user of repository because the owner of repository can be another user not login user
            config["USERNAME"] = repo["owner"]
            # If the repository is fork repository run the update of fork before any actions
            if repo["isFork"] == True:
                message = f"Starting synchronization of fork repository {repoName}"
                logMessage(message=message, logType="info")
                isSync = updateFork(config=config, repoName=repoName, branch=defaulBranch)
                if not isSync:
                    repoForkFailed.append(repoName)
            # Specify if the repo is clone or not
            isCloneRepo = False
            # Build the folder and clone the repository if necessary
            RESULT_FOLDER = resultPath + "/" + repoName
            if isNewFolder or not os.path.exists(RESULT_FOLDER):
                createFolder(RESULT_FOLDER)
                message = f"Starting cloning of repository {repoName} inside {RESULT_FOLDER}"
                logMessage(message=message, logType="info")
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
                # Display the repository list
                message = f"{len(listOfBranchs)} branch(es) found on repository {repoName}"
                logMessage(message=message, logType="info")
                for branch in listOfBranchs:
                    logMessage(message=branch, logType="info", addSeparator=False)
                if len(listOfBranchs) > 0:
                    message = f"Starting updating of repository {repoName} branches inside {RESULT_FOLDER}"
                    logMessage(message=message, logType="info")
                    # Clone each branch
                    isBranchClone = cloneRepoBranches(location=RESULT_FOLDER, listOfBranch=listOfBranchs, defaultBranch=defaulBranch)
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
            message = f"Unexpected {err}, {type(err)}"
            logMessage(message=message, logType="error")
            # Increment here the number of failed
            metric["failed"] += 1

    # Display the result of metric
    message = f"The summary of actions are:"
    logMessage(message=message, logType="info")
    message = f"Number of new deposit clones: {metric['new']}"
    logMessage(message=message, logType="info", addSeparator=False)
    message = f"Number of repository updates: {metric['update']}"
    logMessage(message=message, logType="info", addSeparator=False)
    message = f"Number of failures: {metric['failed']}"
    logMessage(message=message, logType="info", addSeparator=False)
    message = f"Number of successes: {metric['success']}"
    logMessage(message=message, logType="info", addSeparator=False)
    if len(repoForkFailed) > 0:
        message = f"The list of {len(repoForkFailed)} fork {'repository' if len(repoForkFailed) < 2 else 'repositories'} which failed to be synchronized:"
        logMessage(message=message, logType="info")
        for repo in repoForkFailed:
            logMessage(message=repo, logType="info", addSeparator=False)
        logMessage(message="\n", logType="info", addSeparator=False)
    if len(repoListFailed) > 0:
        message = f"The list of {len(repoListFailed)} {'repository which' if len(repoListFailed) < 2 else 'repositories which are failed'} failed to be cloned:"
        logMessage(message=message, logType="info")
        for repo in repoListFailed:
            logMessage(message=repo, logType="info", addSeparator=False)
        logMessage(message="\n", logType="info", addSeparator=False)
    if len(repoListPartial) > 0:
        message = f"The list of {len(repoListPartial)} {'repository' if len(repoListPartial) < 2 else 'repositories'} which failed to be updated:"
        logMessage(message=message, logType="info")
        for repo in repoListPartial:
            logMessage(message=repo, logType="info", addSeparator=False)
        logMessage(message="\n", logType="info", addSeparator=False)
except Exception as err:
    message = f"Unexpected {err}, {type(err)}"
    logMessage(message=message, logType="error")

finally:
    # Show analyse time
    endTime = time.time()
    message = f"This programme takes: {getSecondsConvertion(endTime-startTime)}"
    logMessage(message=message, logType="info")
#################################################################
#               Author: Ismael Maurice                          #
#               Language: Python                                #
#               Projet: Github Clone                            #
#               Version: V1                                     #
#               File: helpers.py                                #
#################################################################

"""
    The helper functions which will be used inside the main file.
"""

def getSecondsConvertion(seconds):
    """
        Name
        ----
        getSecondsConvertion

        Description
        -----------
        Return the conversion of seconds to years, months, days, hours, minutes and seconds

        Parameters
        ----------
        :param seconds (required number): the number of seconds which will be converted.

        Response
        --------
        :return string

        Examples
        -------
        getSecondsConvertion(10000) => Return '0 year(s) and 0 month(s) and 0 day(s) and 2 hour(s) and 46 minute(s) and 40 second(s)'
        getSecondsConvertion(100000000) => Return '3 year(s) and 2 month(s) and 17 day(s) and 9 hour(s) and 46 minute(s) and 40 second(s)'
    """
    functionName = "getSecondsConvertion"
    import logging

    # Verify the parameter
    if seconds < 0:
        message = f"\n{functionName}::The parameter 'seconds' must be a positive number\n"
        logMessage(message=message, logType="error")
        exit(0)

    # Defines constantes
    oneMinuteSeconds = 60 #=> 1 minute = 60 seconds
    oneHourMinutes = 60 #=> 1 hour = 60 minutes
    oneDayHours = 24 #=> 1 day = 24 hours
    oneMonthDays = 30 #=> 1 month = 30 days generally
    oneYearMonths = 12 #=> 1 year = 12 months
    # Get the seconds to user entry
    howManySeconds = seconds
    # Convert to int
    try:
        # Calculate the number of year, month, days, hours, minutes and seconds
        minutes, seconds = howManySeconds // oneMinuteSeconds, howManySeconds % oneMinuteSeconds
        hours, minutes = minutes // oneHourMinutes, minutes % oneHourMinutes
        days, hours = hours // oneDayHours, hours % oneDayHours
        months, days = days // oneMonthDays, days % oneMonthDays
        years, months = months // oneYearMonths, months % oneYearMonths
        return f"{int(years)} year(s) and {int(months)} month(s) and {int(days)} day(s) and {int(hours)} hour(s) and {int(minutes)} minute(s) and {int(seconds)} second(s)"

    except AssertionError:
        message = f"{functionName}::You must give a positive number for second(s) !"
        logMessage(message=message, logType="error")
        exit(0)
    except ValueError:
        message = f"{functionName}::You must give a number for second(s) !"
        logMessage(message=message, logType="error")
        exit(0)
    except:
        message = f"{functionName}::Error has met!"
        logMessage(message=message, logType="error")
        exit(0)

def updateFork(config, repoName, branch):
    """
        Name
        -----
        updateFork

        Description
        ------------
        Helper function to update the fork repository.

        Parameters
        -----------
        :param config(required dict): the configuration environment variables
        :param repoName(required str): the name of repository which branchs should be clone
        :param branch(required str): the name of branch to clone

        Response
        ---------
        Return True if the repository has been updated else False

        Example
        --------
        updateFork(config, 'test') => will update the fork repository 'test'
    """
    functionName = "updateFork"
    import logging
    try:
        import requests
        import constants
        # Get the API url
        apiUrl = getUrl(config=config, urlTYpe=constants.API_URL_TYPE)
        url = f"{apiUrl}/repos/{config['USERNAME']}/{repoName}/merge-upstream"
        # Update the fork
        url = f"https://api.github.com/repos/{config['USERNAME']}/{repoName}/merge-upstream"
        payload = {"branch": branch}
        headers = {
            "Authorization": f"Bearer {config['TOKEN']}",
            "Content-Type": "application/json"
        }
        responseSync = requests.post(url, json=payload, headers=headers)
        if responseSync.status_code != 200:
            message = f"{functionName}::Request to Github to synchronize fork repository {repoName} failed !"
            logMessage(message=message, logType="error")
            logMessage(message=responseSync.text, logType="error", addSeparator=False)
            return False
        return True
    except Exception as err:
        message = f"{functionName}::Unexpected {err}, {type(err)}"
        logMessage(message=message, logType="error")
        return False


def updateCommitAndLFS():
    """
        Name
        -----
        updateCommitAndLFS

        Description
        ------------
        Helper function to execute the defense push and update the lfs file.
    """
    import os
    # Fetch git lfs files if exists
    os.system("git lfs ls-files")
    os.system("git lfs fetch --all")
    os.system("git lfs pull")
    # Add defense push if some changes
    os.system("git add .")
    os.system("git commit -m 'Synchro by Github Clone Script'")
    os.system("git push")

def cloneRepoBranches(location, listOfBranch, defaultBranch):
    """
        Name
        -----
        cloneRepoBranches

        Description
        ------------
        Helper function to clone each branch of repository in specific location.

        Parameters
        -----------
        :param location (required str): the location of folder where the repository is located
        :param listOfBranch (required array of str): the list of repository branch
        :param defaultBranch (required str): the default branch of repository to clone

        Response
        ---------
        Will checkout the branch of repository and return True if successfull else False

        Example
        --------
        cloneRepoBranches("/home/test/repo/test", ['main', 'test'], "main") => will checkout the branch of repository each branch 'main' and 'test'
    """
    import os
    import logging
    functionName = "cloneRepoBranches"
    try:
        if not os.path.exists(location):
            message = f"{functionName}::Not found folder in location {location} !"
            logMessage(message=message, logType="error")
            return False
        elif not os.path.isdir(location):
            message = f"{functionName}::Location {location} is not a folder we cannot clone the branches there !"
            logMessage(message=message, logType="error")
            return False
        else:
            # Change the folder location
            os.chdir(location)
            for branchName in listOfBranch:
                if branchName != defaultBranch:
                    # Checkout branch
                    checkoutCommand = f"git fetch origin {branchName} && git checkout {branchName}"
                    os.system(checkoutCommand)
                    # Pull all code in branch
                    os.system("git pull")
                    # Apply defense
                    updateCommitAndLFS()
            # Move to default branch
            os.system(f"git checkout {defaultBranch}")
            # Pull all code in branch
            os.system("git pull")
            # Apply defense
            updateCommitAndLFS()
            return True
    except Exception as err:
        message = f"{functionName}::Unexpected {err}, {type(err)}"
        logMessage(message=message, logType="error")
        return False

def getRepositoryBranchesNames(config, repoName):
    """
        Name
        -----
        getRepositoryBranchesNames

        Description
        ------------
        Helper function to return the list of branches of specific repository of connected user.

        Parameters
        -----------
        :param config(required dict): the configuration environment variables
        :param repoName(required str): the name of repository which branchs should be clone

        Response
        ---------
        Will return the list of user repository branches names
    """
    functionName = "getRepositoryBranchesNames"
    import requests
    import constants
    import logging
    response = []
    try:
        # Now fetch the branch of repository
        page = 0
        isContinueBranch = True
        headers = headers = {'Authorization': f'Bearer {config["TOKEN"]}'}
        while isContinueBranch:
            page += 1
            # Add the repository name in config to get the url to fetch the branch list
            config["REPOSITORY"] = repoName
            branchListUrl = getUrl(config=config, urlTYpe=constants.BRANCH_LIST_URL_TYPE)
            # Fetch the branch
            responseBranch = requests.get(f"{branchListUrl}?page={page}", headers=headers)
            if responseBranch.status_code != 200:
                message = f"{functionName}::Request to Github to fetch repository {repoName} branchs failed !"
                logMessage(message=message, logType="error")
                logMessage(message=responseBranch.text, logType="error", addSeparator=False)
                return response
            else:
                responseBranchData = responseBranch.json()
                if len(responseBranchData) > 0:
                    # Loop to add the name of all branchs
                    for branch in responseBranchData:
                        response.append(branch['name'])
                else:
                    # Stop fetch the branch
                    isContinueBranch = False
        return response
    except Exception as err:
        message = f"{functionName}::Unexpected {err}, {type(err)}"
        logMessage(message=message, logType="error")
        return response

def cloneRepository(config, repoName, location):
    """
        Name
        -----
        cloneRepository

        Description
        ------------
        Helper function to clone the repository in specific location.

        Parameters
        -----------
        :param config(required dict): the dictionary of configuration
        :param repoName(required str): the name of repository which should be clone
        :param location (required str): the location of folder where to clone will not clone if not found the folder

        Response
        ---------
        Will return True if the clone is successfull else False

        Example
        --------
        cloneRepository(config, 'test', '/home/test/repo') => will clone the repository test in folder /home/test/repo
    """
    import constants
    import os
    import logging
    functionName = "cloneRepository"
    try:
        if not os.path.exists(location):
            message = f"{functionName}::Not found folder in location {location} !"
            logMessage(message=message, logType="error")
            return False
        elif not os.path.isdir(location):
            message = f"{functionName}::Location {location} is not a folder we cannot clone the repo {repoName} there !"
            logMessage(message=message, logType="error")
            return False
        else:
            # Get the repo branch should be clone only if one branch found for this repository
            repoBranch = getRepositoryBranchesNames(config=config, repoName=repoName)
            if len(repoBranch) > 0:
                # Add the repo name in config to build the right url to use
                config["REPOSITORY"] = repoName
                repoCloneUrl = getUrl(config=config, urlTYpe=constants.REPOSITORY_CLONE_URL_TYPE)
                cloneCommand = f"git clone {repoCloneUrl} {location}"
                os.system(cloneCommand)
                return True
            else:
                return False
    except Exception as err:
        message = f"{functionName}::Unexpected {err}, {type(err)}"
        logMessage(message=message, logType="error")
        return False

def getUrl(config, urlTYpe):
    """
        Name
        -----
        getUrl

        Description
        ------------
        Helper function to get the right url to call for API.

        Parameters
        -----------
        :param config(required dict): the dictionary of configuration
        :param urlTYpe(required string): the type of url to get between API, USER, REPOSITORY, BRANCH
            + API: to return the url of host API
            + USER: to return the url to use to fetch the user
            + REPOSITORY: to return the url to use to fetch the repository of user
            + BRANCH: to return the url to use to fetch the branches of specific repository

        Response
        ---------
        Will return the url to use to call API

        Example
        --------
        getUrl(config, 'USER') => will response like https://api.github.com
    """
    import constants
    import logging
    functionName = "getUrl"
    try:
        DOMAIN_URL = config['DOMAIN']
        DOMAIN_PROTOCOL = config["PROTOCOL"]
        DOMAIN_API = f"{DOMAIN_PROTOCOL}://api.{DOMAIN_URL}"
        if urlTYpe.upper() == constants.API_URL_TYPE:
            return DOMAIN_API
        elif urlTYpe.upper() == constants.REPOSITORY_CLONE_URL_TYPE:
            USERNAME = config["USERNAME"]
            TOKEN = config["TOKEN"]
            REPOSITORY_NAME = config["REPOSITORY"]
            return f"{DOMAIN_PROTOCOL}://{USERNAME}:{TOKEN}@{DOMAIN_URL}/{USERNAME}/{REPOSITORY_NAME}.git"
        elif urlTYpe.upper() == constants.REPOSITORY_LIST_URL_TYPE:
            return f"{DOMAIN_API}/user/repos"
        elif urlTYpe.upper() == constants.BRANCH_LIST_URL_TYPE:
            USERNAME = config["USERNAME"]
            REPOSITORY_NAME = config["REPOSITORY"]
            return f"{DOMAIN_API}/repos/{USERNAME}/{REPOSITORY_NAME}/branches"
        else:
            message = f"{functionName}::Unknown url type {urlTYpe}"
            logMessage(message=message, logType="error")
            exit(0)
    except Exception as err:
        message = f"{functionName}::Unexpected {err}, {type(err)}"
        logMessage(message=message, logType="error")
        exit(0)

def getRepositoryData(config):
    """
        Name
        -----
        getRepositoryData

        Description
        ------------
        Helper function to return the list of repositories names for connected user.

        Parameters
        -----------
        :param config(required dict): the configuration environment variables

        Response
        ---------
        Will return the list of user repository data, the response will be an array of dict with description for each item:
        + name: the name of repository
        + url: the clone url of repository
        + isFork: the boolean to specify if the repository is cloning repository or not
    """
    functionName = "getRepositoryData"
    import requests
    import constants
    try:
        # Prepare the requests need
        page = 0
        isContinue = True
        headers = headers = {'Authorization': f'Bearer {config["TOKEN"]}'}
        username = config["USERNAME"]
        response = []
        while isContinue:
            page += 1
            # BUild the repo list url before clone
            repoListUrl = getUrl(config=config, urlTYpe=constants.REPOSITORY_LIST_URL_TYPE)
            # Call the API to fetch the list of repositories
            responseRepo = requests.get(f"{repoListUrl}?page={page}", headers=headers)
            if responseRepo.status_code != 200:
                message = f"{functionName}::Request to Github to fetch repository of user {username} failed !"
                logMessage(message=message, logType="error")
                logMessage(message=responseRepo.text, logType="error", addSeparator=False)
                exit(0)
            else:
                # Convert the response of repository list
                responseRepoData = responseRepo.json()
                if len(responseRepoData) > 0:
                    for repo in responseRepoData:
                        # Add the repo name in list
                        response.append({
                            "name": repo["name"],
                            "url": repo["clone_url"] if repo["clone_url"] else "",
                            "isFork": True if repo["fork"] else False,
                            "owner": repo["owner"]["login"],
                            "defaultBranch": repo["default_branch"]
                        })
                else:
                    # All repositories has been fetched
                    isContinue = False
        return response
    except Exception as err:
        message = f"{functionName}::Unexpected {err}, {type(err)}"
        logMessage(message=message, logType="error")
        exit(0)

def createFolder(path):
    """
        Name
        -----
        createFolder

        Description
        ------------
        Helper function to create the folder inside the location folder and all parents folder if not created.

        Parameters
        -----------
        :param path(required str): the location path of folder to create example /home/toto/test

        Response
        ---------
        Will return True if new folder has been created else False
    """
    functionName = "createFolder"
    try:
        # Create the folders if not exists
        import os
        isNewFolder = False
        if not os.path.exists(path):
            # Create the folder
            message = f"The result folder {path} not exists it will be created !"
            logMessage(message=message, logType="info")
            os.makedirs(path)
            isNewFolder = True
        return isNewFolder
    except Exception as err:
        message = f"{functionName}::Unexpected {err}, {type(err)}"
        logMessage(message=message, logType="error")
        exit(0)

def verificationCnfig(config):
    """
        Name
        -----
        verificationCnfig

        Description
        ------------
        Helper function which will verify that the configuration file for dotenv is correct and contains the expected values.

        The function will stop the program if incorrect config file.

        Parameters
        -----------
        :param config(required dict): the dictionary which contains the environment variables.

        Response
        ---------
        None
    """
    functionName = "verificationCnfig"
    try:
        # Define the list of expected .env variable
        expectedKeys = ["DOMAIN", "TOKEN", "FOLDER", "PROTOCOL"]

        # Verify if the contains of env
        if not config or len(config) == 0:
            message = "The .env file is empty or not found"
            logMessage(message=message, logType="error")
            exit(0)
        elif not isinstance(config, dict):
            message = "The .env file is not dictionary"
            logMessage(message=message, logType="error")
            exit(0)
        # Verify that each expected keys are present
        for key in expectedKeys:
            if key not in config:
                message = f"The key/value of {key} is required inside .env"
                logMessage(message=message, logType="error")
                exit(0)
            elif len(config[key]) < 1:
                message = f"The {key} inside .env is empty"
                logMessage(message=message, logType="error")
                exit(0)
    except Exception as err:
        message = f"{functionName}::Unexpected {err}, {type(err)}"
        logMessage(message=message, logType="error")
        exit(0)

def logMessage(message, logType, addSeparator=True):
    """
        Name
        -----
        logMesaage

        Description
        ------------
        Helper function use to display the message in terminal and in log.

        Parameters
        -----------
        :param message(required str): the log message to display.
        :param logType (requied str): the log type between error, warning, info
        :param addSeparator (required boolean): define if for terminal the seperator should be done

        Response
        ---------
        None
    """
    import logging
    # Display the log in terminal
    if addSeparator:
        print(f"\n{message}\n")
    else:
        print(message)
    # Display the log in log file according to message type
    if logType and logType.lower() == "info":
        logging.info(message)
    elif logType and logType.lower() == "error":
        logging.error(message)
    elif logType and logType.lower() == "warning":
        logging.warning(message)

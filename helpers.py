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
                print(f"\n{functionName}::Request to Github to fetch repository {repoName} branchs failed !\n")
                print(responseBranch.text)
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
        print(f"\n{functionName}::Unexpected {err}, {type(err)}\n")
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
    functionName = "cloneRepository"
    try:
        if not os.path.exists(location):
            print(f"\n{functionName}::Not found folder in location {location} !\n")
            return False
        elif not os.path.isdir(location):
            print(f"\n{functionName}::Location {location} is not a folder we cannot clone the repo {repoName} there !\n")
            return False
        else:
            # Add the repo name in config to build the right url to use
            config["REPOSITORY"] = repoName
            repoCloneUrl = getUrl(config=config, urlTYpe=constants.REPOSITORY_CLONE_URL_TYPE)
            cloneCommand = f"git clone {repoCloneUrl} {location}"
            os.system(cloneCommand)
            return True
    except Exception as err:
        print(f"\n{functionName}::Unexpected {err}, {type(err)}\n")
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
            print(f"\n{functionName}::Unknown url type {urlTYpe}\n")
            exit(0)
    except Exception as err:
        print(f"\n{functionName}::Unexpected {err}, {type(err)}\n")
        exit(0)

def getRepositoryNames(config):
    """
        Name
        -----
        getRepositoryNames

        Description
        ------------
        Helper function to return the list of repositories names for connected user.

        Parameters
        -----------
        :param config(required dict): the configuration environment variables

        Response
        ---------
        Will return the list of user repository name
    """
    functionName = "getRepositoryNames"
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
                print(f"\n{functionName}::Request to Github to fetch repository of user {username} failed !\n")
                print(responseRepo.text)
                exit(0)
            else:
                # Convert the response of repository list
                responseRepoData = responseRepo.json()
                if len(responseRepoData) > 0:
                    for repo in responseRepoData:
                        # Add the repo name in list
                        response.append(repo["name"])
                else:
                    # All repositories has been fetched
                    isContinue = False
        return response
    except Exception as err:
        print(f"\n{functionName}::Unexpected {err}, {type(err)}\n")
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
            print(f"\nThe result folder {path} not exists it will be created !\n")
            os.makedirs(path)
            isNewFolder = True
        return isNewFolder
    except Exception as err:
        print(f"\n{functionName}::Unexpected {err}, {type(err)}\n")
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
            print("\nThe .env file is empty or not found\n")
            exit(0)
        elif not isinstance(config, dict):
            print("\nThe .env file is not dictionary\n")
            exit(0)
        # Verify that each expected keys are present
        for key in expectedKeys:
            if key not in config:
                print(f"\nThe key/value of {key} is required inside .env\n")
                exit(0)
            elif len(config[key]) < 1:
                print(f"\nThe {key} inside .env is empty\n")
                exit(0)
    except Exception as err:
        print(f"\n{functionName}::Unexpected {err}, {type(err)}\n")
        exit(0)

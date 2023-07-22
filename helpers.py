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
        else:
            print(f"\n{functionName}::Unknown url type {urlTYpe}\n")
            exit(0)
    except Exception as err:
        print(f"\n{functionName}::Unexpected {err}, {type(err)}\n")
        exit(0)

def getRepositoryNames():
    """
        Name
        -----
        createFolder

        Description
        ------------
        Helper function to return the list of repositories names for connected user.

        Parameters
        -----------
        # TODO: to be complete
        :param path(required str): the location path of folder to create example /home/toto/test

        Response
        ---------
        # TODO: to be completed
        Will return True if new folder has been created else False
    """
    functionName = "getRepositoryNames"
    try:
       # TODO: code here
       pass
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

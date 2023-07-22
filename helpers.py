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

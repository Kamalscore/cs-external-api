import sys
from pathlib import Path

from config.ConfigManager import ConfigManager
from utils.HelperUtils import isNotNone



def __validateConfigFilePathParam(configFilePath):
    try:
        if not Path(configFilePath).is_file():
            print("Provided config file path is invalid: " + configFilePath)
        else:
            ConfigManager(configFilePath)
            return True
    except Exception as e:
        print("Error while parsing the config file: {0}, cause: {1}".format(configFilePath, e))
    return False


def __validateInputs(configFilePath):
    valid = True
    if isNotNone(configFilePath):
        valid = __validateConfigFilePathParam(configFilePath)
    else:
        valid = False
    if not valid:
        #print("USAGE: DSLTranslator.py config_file_path, sourcePlatform, sourceType, sourceFormat, destinationPlatform, destinationType, destinationFormat, inputTemplate")
        sys.exit(2)


def _processTemplate(argv):
    if argv.__len__() > 0:
        __validateInputs(argv[0])
    else:
        print("USAGE: Main.py config_file_path")
        sys.exit(2)

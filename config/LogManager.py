import logging

from utils.Constants import *
from config.ConfigManager import getProperty

"""
####
###
### Purpose: Define a function to manage the logging framework.
###
####
"""


class LogManager(object):

    def __init__(self, filepath='/tmp/dsl_translator.log', fileLogLevel=logging.DEBUG, consoleLogLevel=logging.DEBUG, format='[%(asctime) s] [%(name) s] [%(levelname) s]: %(message)s'):
        self.__filepath = filepath
        self.__fileLogLevel = fileLogLevel
        self.__format = format
        self.__consoleLogLevel = consoleLogLevel
        self.__prepare()

    def __prepare(self):
        # set up logging to a file
        logging.basicConfig(level=self.__fileLogLevel,
                            format=self.__format,
                            #datefmt='%d-%m-%Y %H:%M:%S,%f',
                            filename=self.__filepath,
                            filemode='w')

        # define a Handler which writes INFO messages or higher to the sys.stderr
        console = logging.StreamHandler()
        console.setLevel(self.__consoleLogLevel)

        # set  a format which is simpler for console use
        formatter = logging.Formatter('[%(asctime) s] [%(name) s] [%(levelname) s]: %(message)s')

        # tell the handler to use this format
        console.setFormatter(formatter)

        # add the handler to the root Logger
        logging.getLogger('').addHandler(console)


def initLogManager():
    logFilePath = getProperty(LOG_CONFIG_SECTION, LOG_FILE_PATH_PROPERTY_NAME, LOG_FILE_NAME_PROPERTY_DEFAULT_VALUE)
    logFileLevel = getProperty(LOG_CONFIG_SECTION, LOG_FILE_LEVEL_PROPERTY_NAME, logging.DEBUG)
    logConsoleLevel = getProperty(LOG_CONFIG_SECTION, LOG_CONSOLE_LEVEL_PROPERTY_NAME, logging.DEBUG)
    return LogManager(filepath=logFilePath, fileLogLevel=logFileLevel, consoleLogLevel=logConsoleLevel)
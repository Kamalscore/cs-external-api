import configparser

import logging
from utils.HelperUtils import getClassName
from utils.Constants import *


class Singleton(object):
    _instances = {}

    def __new__(class_, *args, **kwargs):
        if class_ not in class_._instances:
            class_._instances[class_] = super(Singleton, class_).__new__(class_, *args, **kwargs)
        return class_._instances[class_]


class ConfigHolder(Singleton):

    def getConfig(self):
        return self.__config

    def setConfig(self, config):
        self.__config = config


class ConfigNotLoadedException(Exception):
    pass


class ConfigManager:
    def __init__(self, configFilePath):
        self.logger = logging.getLogger(getClassName(ConfigManager))
        ConfigHolder().setConfig(configparser.RawConfigParser())
        self.logger.debug("Provided config file path is: " + configFilePath)
        ConfigHolder().getConfig().read(configFilePath)


def getProperty(section, propertyName, defaultValue=None):
    if ConfigHolder().getConfig() is None:
        raise ConfigNotLoadedException(
            "Config file is not loaded properly, make sure to invoke ConfigManger before calling this.")

    return str(ConfigHolder().getConfig().get(section, propertyName, fallback=defaultValue))
    # return str(ConfigHolder().getConfig().get(section, propertyName, fallback=defaultValue)).encode(UTF_8)
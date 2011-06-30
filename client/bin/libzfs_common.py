import logging
from autotest_lib.client.bin import  utils, configzfs
from autotest_lib.client.common_lib import error
from configzfs import *


def load_zfs_modules():
    zfs_modules = ["spl","zfs","lzfs"]
    for module in zfs_modules:
        if utils.load_module(module) == False:
           logging.info(module + " module has already been loaded..")
        else:
           logging.info(module + " module loaded successfully..")
    return SUCCESS

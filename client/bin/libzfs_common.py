import logging
from autotest_lib.client.bin import  utils, configzfs
from autotest_lib.client.common_lib import error
from configzfs import *


def load_zfs_modules():
    if utils.load_module("zfs") == False:
        logging.info(zfs_module + " module has already been loaded..")
    else:
        logging.info(zfs_module + " module loaded successfully..")
    return SUCCESS

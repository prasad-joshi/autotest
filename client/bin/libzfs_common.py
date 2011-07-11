import logging, fsdev_disks
from autotest_lib.client.bin import  utils, configzfs
from autotest_lib.client.common_lib import error
from configzfs import *


def load_zfs_modules():
    if utils.load_module("zfs") == False:
        logging.info("zfs module has already been loaded..")
    else:
        logging.info("zfs module loaded successfully..")
    return SUCCESS

def unload_zfs_modules():
    if utils.unload_module("zfs") == False:
        logging.info("zfs cannot unload module..")
    else:
        logging.info("zfs module unloaded successfully..")
    return SUCCESS

def get_free_disks():
    disks = fsdev_disks.get_disk_list(get_all_disks=True)
    free_disks = []
    for i in disks:
        if i['mountpt'] == None:
            free_disks.append(i['device'])
    return free_disks

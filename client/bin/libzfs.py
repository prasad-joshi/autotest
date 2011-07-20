import logging
from autotest_lib.client.bin import  utils, configzfs
from autotest_lib.client.common_lib import error
from configzfs import *

def is_mounted(pool, fs):
    if pool == "":
       raise error.TestFail("Missing pool name..")
    if fs == "":
       raise error.TestFail("Missing file system name..")
    status = utils.system("zfs mount | awk '{print $1}' | grep -w " + pool + "/" + fs, ignore_status = True)
    return status

def create(pool, fs):
    if pool == "":
       raise error.TestFail("cannot create file system : Missing pool name..")
    if fs == "":
       raise error.TestFail("cannot create file system : Missing file system name..")
    utils.system("zfs create " + pool + "/" + fs)
    return SUCCESS

def mount(pool, fs):
    if pool == "":
       raise error.TestFail("cannot mount file system : Missing pool name..")
    if fs == "":
       raise error.TestFail("cannot mount file system : Missing file system name..")
    utils.system("zfs mount " + pool + "/" + fs)
    return SUCCESS

def unmount(pool, fs):
    if pool == "":
       raise error.TestFail("cannot unmount file system : Missing pool name..")
    if fs == "":
       raise error.TestFail("cannot unmount file system : Missing file system name..")
    utils.system("zfs unmount " + pool + "/" + fs)
    return SUCCESS

def destroy(pool, fs):
    if pool == "":
       raise error.TestFail("cannot destroy file system : Missing pool name..")
    if fs == "":
       raise error.TestFail("cannot destroy file system : Missing file system name..")
    status = utils.system("zfs destroy " + pool + "/" + fs, ignore_status = True)
    return status

def create_zvol(pool, size, zvol):
    if pool == "":
       raise error.TestFail("pool is not provided..")
    if size == "":
       raise error.TestFaile("size is not provided..")
    if zvol == "":
       raise error.TestFaile("zvol name not provided..")
    utils.system("zfs create -V " + size + " " + pool + "/" + zvol)
    return SUCCESS

def dataset_exists(dataset):
    if dataset == "":
       raise error.TestFail("dataset name not provided..")
    utils.system("zfs list -H -t filesystem,snapshot,volume " + dataset + " > /dev/null")
    return SUCCESS

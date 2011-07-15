import logging
from autotest_lib.client.bin import  utils, configzfs
from autotest_lib.client.common_lib import error
from configzfs import *

def is_mounted(fs):
    status = SUCCESS
    try:
       if fs[0] == '/':
          utils.system("zfs mount | awk '{print $2}' | grep -w " + fs)
       else:
           utils.system("zfs mount | awk '{print $1}' | grep -w " + fs)
    except:
          status = FAIL
    return status

def create(fs):
    if fs == "":
       raise error.TestFail("cannot create file system : Missing file system name..")
    utils.system("zfs create " + fs)
    return SUCCESS

def set_mount_point(dir, fs):
    if dir == "":
       raise error.TestFail("cannot set mount point : Missing directory name..")
    if fs == "":
       raise error.TestFail("cannot set mount point : Missing file system name..")
    utils.system("zfs set mountpoint=" + dir + " " + fs)
    return SUCCESS

def mount(fs):
    if fs == "":
       raise error.TestFail("cannot mount file system : Missing file system name..")
    utils.system("zfs mount " + fs)
    return SUCCESS

def unmount(fs):
    if fs == "":
       raise error.TestFail("cannot unmount file system : Missing file system name..")
    utils.system("zfs unmount " + fs)
    return SUCCESS

def destroy(fs):
    if fs == "":
       raise error.TestFail("cannot destroy file system : Missing file system name..")
    utils.system("zfs destroy " + fs)
    return SUCCESS

#type is on or off.
def set_compression(type, fs):
    if type == "":
       raise error.TestFail("Compression type may have been omitted..")
    if fs == "":
       raise error.TestFail("File system name may have been omitted..")
    utils.system("zfs set compression=" + type + " " + fs)
    return SUCCESS

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

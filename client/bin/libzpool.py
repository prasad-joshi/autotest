import logging, re
from autotest_lib.client.bin import  utils, configzfs
from autotest_lib.client.common_lib import error
from configzfs import *

def create(pool, disks, version = 0):
    if pool == "":
       raise error.TestFail("cannot create pool :  Missing pool name..")
    if disks == "":
       raise error.TestFail("cannot create pool : Missing disk list..")
    if pool_exists(pool) == SUCCESS:
       raise error.TestFail("cannot create '" + pool + "': " + pool + " already
		       exists")
    try:
       status = SUCCESS
       if version == 0:
          utils.system_output("zpool create " + pool + " " + disks)
       else:
          utils.system("zpool create -o version=" + version + " " + pool + " " +
                        disks)
    except:
       status = FAIL
    return SUCCESS

def pool_exists(pool):
    if pool == "":
       raise error.TestFail("Missing pool name..")
    try:
       status = SUCCESS
       utils.system_output("zpool list -H " + pool)
    except:
       status = FAIL
    return status

def destroy(pool):
    if pool == "":
       raise error.TestFail("cannot destroy pool : Missing pool name..")
    if pool_exists(pool) == SUCCESS:
       utils.system("zpool destroy " + pool)
    return SUCCESS

def add_disks(pool, disks):
    if pool == "":
       raise error.TestFail("cannot add disks : Missing pool name..")
    if disk == "":
       raise error.TestFail("cannot add disks : Missing disk name..")
    utils.system("zpool add -f " + pool + " " + disks)
    return SUCCESS

def set_version(pool, version):
    if pool == "":
       raise error.TestFail("cannot set version : Missing pool name..")
    if version == "":
       raise error.TestFail("cannot set version : Missing version number..")
    try:
       status = SUCCESS
       utils.system_output("zpool set version=" + str(version) + " " + pool)
    except:
       status = FAIL
    return status

def get_version(pool):
    if pool == "":
       raise.error.TestFail("cannot get version : Missing pool name..")
    version = utils.system_output("zpool get version "+ pool + "| grep version |
		    awk '{print $3}'")
    version = re.sub('\n',"",version)
    return version

import logging
from autotest_lib.client.bin import  utils, configzfs
from autotest_lib.client.common_lib import error
from configzfs import *

def create(pool, disks):
    if pool == "":
       raise error.TestFail("cannot create pool :  Missing pool name..")
    if disks == "":
       raise error.TestFail("cannot create pool : Missing disk list..")
    if pool_exists(pool) == SUCCESS:
       raise error.TestFail("cannot create '" + pool + "': " + pool + " already exists")
    utils.system("zpool create " + pool + " " + disks)
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

def add(pool, disk):
    if pool == "":
       raise error.TestFail("cannot add disk : Missing pool name..")
    if disk == "":
       raise error.TestFail("cannot add disk : Missing disk name..")
    utils.system("zpool add -f " + pool + " " + disk)
    return SUCCESS

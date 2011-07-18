import logging, re
from autotest_lib.client.bin import  utils, configzfs
from autotest_lib.client.common_lib import error
from configzfs import *

def create(pool, disks, version = "", cachefile = "", altroot = ""):
    if pool == "":
       raise error.TestFail("cannot create pool :  Missing pool name..")
    if disks == "":
       raise error.TestFail("cannot create pool : Missing disk list..")
    if pool_exists(pool) == SUCCESS:
       raise error.TestFail("cannot create '" + pool + "': " + pool + " already exists.")
    options = ""
    if(version):
       options = " -o version=" + version
    if(cachefile):
       options += " -o cachefile=" + cachefile
    if(altroot):
       options += " -o altroot=" + altroot
    try:
       status = SUCCESS
       if(options):
            utils.system_output("zpool create" + options + " " + pool + " " + disks)
       else:
	    utils.system_output("zpool create "  + pool + " " + disks)
    except:
       status = FAIL
    return status

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

def set_property(pool, pr, val):
    if pool == "":
       raise error.TestFail("cannot set property : Missing pool name..")
    if pr == "":
       raise error.TestFail("cannot set property : Missing property name..")
    if val == "":
       raise error.TestFail("cannot set property : Missing property value..")
    try:
       status = SUCCESS
       utils.system_output("zpool set " + pr + "=" + val + " " + pool)
    except:
       status = FAIL
    return status

def get_property(pool, pr):
    if pool == "":
       raise error.TestFail("cannot get property : Missing pool name..")
    if pr == "":
       raise error.TestFail("cannot get property : Missing property name..")
    val = utils.system_output("zpool get " + pr + " " + pool + " | awk '/" + pr +
		               "/{print $3}'")
    val = re.sub('\n',"", val)
    return val

def export_pool(pool):
    if pool == "":
       raise error.TestFail("cannot export pool : Missing pool name..")
    utils.system("zpool export " + pool)

def import_pool(pool, cachefile = ""):
    if pool == "":
       raise error.TestFail("cannot export pool : Missing pool name..")
    if(cachefile):
       utils.system("zpool import -o cachefile=" + cachefile + " " + pool)
    else:
       utils.system("zpool import " + pool)

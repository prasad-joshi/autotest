################################################################################
#
# ID: nestedfs
#
# DESCRIPTION:
# The test verifies that a parent file system
# should not be destroy if it has children.

# STRATEGY:
# 1.Create a zpool.
# 2.Create two file systems on zpool.
#   tank/fs ==> mounted at /tank/fs
#   tank/fs1 ==> mounted at /tank/fs/fs1
# 3.Destroying file system fs should not be allowed.
##############################################################################

import os, logging
from autotest_lib.client.bin import test, utils, libzfs, libzpool, configzfs, libzfs_common
from configzfs import *
from autotest_lib.client.common_lib import error

fs1 = TESTFS
fs2 = TESTFS + "/" + TESTFS1

class nestedfs(test.test):
        version = 2
	def setup(self):
            logging.info("In setup function..")

	    if libzfs_common.load_zfs_modules() != SUCCESS:
               raise error.TestFail("Failed to load zfs modules..")
            return SUCCESS

        def run_once(self):
            logging.info("In run_once function.. ")

            logging.info("Here we will create the pool..")
            disks = libzfs_common.get_free_disks()

            status = libzpool.create(TESTPOOL, disks[0])
            if status != SUCCESS:
	       raise error.TestFail("zpool create failed..")

            logging.info("Create a file system and set its mount point....")

            utils.system("mkdir -p " + TESTDIR)
            libzfs.create(TESTPOOL, fs1)
            libzfs.set_property(TESTPOOL, fs1, "mountpoint", TESTDIR)

            logging.info("Create nested file system..")
            libzfs.create(TESTPOOL, fs2)

            status = libzfs.destroy(TESTPOOL, fs1)
            if status == SUCCESS:
               raise error.TestFail("Parent file system destroyed..")

	    logging.info("The nestedfs test passed successfully..")
            return SUCCESS


        def cleanup(self):
            logging.info("In cleanup function.. ")

            for fs in [fs2, fs1]:
	        status = libzfs.is_mounted(TESTPOOL, fs)
                if status == SUCCESS :
                   libzfs.unmount(TESTPOOL, fs)
                   libzfs.destroy(TESTPOOL, fs)

            status = os.path.exists(TESTDIR)
            if status == True:
               utils.system("rm -r " + TESTDIR)

            status = libzpool.pool_exists(TESTPOOL)
            if status == SUCCESS:
               libzpool.destroy(TESTPOOL)

            logging.info("Cleanup done successfully...")
            return SUCCESS

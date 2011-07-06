################################################################################
#
# ID: mount test
#
# DESCRIPTION:
# zfs mount and unmount commands should mount and unmount existing
# file system.
#
# STRATEGY:
# 1. Call zfs mount command
# 2. Make sure the file system was mounted
# 3. Call zfs unmount command
# 4. Make sure the file system was unmounted
#
##############################################################################

import os, logging
from autotest_lib.client.bin import test, utils, libzfs, libzpool, configzfs, libzfs_common
from configzfs import *
from autotest_lib.client.common_lib import error

class mount(test.test):
        version = 2
	def setup(self):
            logging.info("In setup function..")
            if libzfs_common.load_zfs_modules() != SUCCESS:
               raise error.TestFail("Failed to load zfs modules..")
            return SUCCESS

        def run_once(self):
            logging.info("In run_once function.. ")

            logging.info("Here we will create the pool..")
            disks = "/dev/sda1"
            libzpool.create(TESTPOOL, disks)

            logging.info("Create a file system with mount point, so it will mount automatically..")
            utils.system("mkdir -p " + TESTDIR)
            fs = TESTPOOL + "/" + TESTFS
            libzfs.create(fs)
            libzfs.set_mount_point(TESTDIR,fs)

            status = libzfs.is_mounted(fs)
            if status != SUCCESS :
               raise error.TestFail("File system " + TESTFS +" is not mounted..")

            logging.info("Unmount the file system..")
            libzfs.unmount(fs)

            logging.info("Make sure file system " + fs + " is unmounted..")
            status = libzfs.is_mounted(fs)
            if status == SUCCESS :
               raise error.TestFail("File system " + fs +" is mounted..")

            logging.info("File system " + fs +" is unmounted..")

            logging.info("Here we will mount the file system..")
            fs = TESTPOOL + "/" + TESTFS
            libzfs.mount(fs)

            logging.info("Make sure the file system is mounted..")
            status = libzfs.is_mounted(fs)
            if status != SUCCESS :
               raise error.TestFail("File system " + TESTFS +" is not mounted..")

            logging.info("Unmount the file system..")
            libzfs.unmount(fs)

            logging.info("Make sure the file system is unmounted..")
            status = libzfs.is_mounted(fs)
            if status == SUCCESS :
               raise error.TestFail("File system " + TESTFS +" is  mounted..")

            logging.info("Mount test passed successfully..")
            return SUCCESS


        def cleanup(self):
            logging.info("In cleanup function.. ")

            fs = TESTPOOL + "/" + TESTFS
            status = libzfs.is_mounted(fs)
            if status == SUCCESS :
               libzfs.unmount(fs)
               libzfs.destroy(fs)

            status = os.path.exists(TESTDIR)
            if status == True:
               utils.system("rm -r " + TESTDIR)

            status = libzpool.pool_exists(TESTPOOL)
            if status == SUCCESS:
               libzpool.destroy(TESTPOOL)

            logging.info("Cleanup done successfully...")
            return SUCCESS

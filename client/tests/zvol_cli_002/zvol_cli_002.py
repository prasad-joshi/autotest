###############################################################################
#
# __stc_assertion_start
#
# ID: zvol_cli_002_pos
#
# DESCRIPTION:
# Creating a volume with a 50 letter name should work.
#
# STRATEGY:
# 1. Using a very long name, create a zvol
# 2. Verify volume exists
#
###############################################################################

import os,logging
from autotest_lib.client.bin import test, utils
from autotest_lib.client.bin import libzfs, libzpool, configzfs, libzfs_common
from configzfs import *
from autotest_lib.client.common_lib import error

class zvol_cli_002(test.test):
      version = 2

      def setup(self):
          logging.info("In setup function..")
          if libzfs_common.load_zfs_modules() != SUCCESS:
             raise error.TestFail("Failed to load zfs modules..")
          return SUCCESS

      def run_once(self):
          logging.info("In run_once function.. ")
          logging.info("create pool of version 1.. ")
          disks = libzfs_common.get_free_disks()
          version = "1"
          status = libzpool.create(TESTPOOL, disks[0])
          if status != SUCCESS:
             raise error.TestFail("zpool create failed.. ")

          logging.info("Creating a volume a 50 letter name should work..")
          status = libzfs.create_zvol(TESTPOOL, "2G", LONGVOLNAME)
          if status != SUCCESS:
             raise error.TestFail("failed to create zvol..")

          status = libzfs.dataset_exists(TESTPOOL + "/" + LONGVOLNAME)
          if status != SUCCESS:
             raise error.TestFail("Couldn't find long volume name")

          logging.info("Created a 50-letter zvol volume name")

      def cleanup(self):
          logging.info("In cleanup function..")
          status = libzpool.pool_exists(TESTPOOL)
          if status == SUCCESS:
             libzpool.destroy(TESTPOOL)
          logging.info("Cleanup done successfully")
          return SUCCESS

###############################################################################
#
# __stc_assertion_start
#
# ID: zvol_cli_003_neg
#
# DESCRIPTION:
# Try each ZFS volume sub-command without parameters to make sure
# it returns an error.
#
# STRATEGY:
# 1. Create an array of parameters
# 2. For each parameter in the array, execute the sub-command
# 3. Verify an error is returned.
#
##############################################################################

import os,logging
from autotest_lib.client.bin import test, utils
from autotest_lib.client.bin import libzfs, libzpool, configzfs, libzfs_common
from configzfs import *
from autotest_lib.client.common_lib import error

class zvol_cli_003(test.test):
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

          logging.info("create zvol on pool..")
          status = libzfs.create_zvol(TESTPOOL, "2G", TESTVOL)
          if status != SUCCESS:
             raise error.TestFail("cannot create zvol..")

          list_args = ["", "create -V", "create -V " + TESTPOOL,
                       "create -V " + TESTPOOL + "/" + TESTVOL + "@",
                       "create -V blah", "destroy"]

          logging.info("Try each ZFS volume sub-command without parameters to\
make sure it returns an error.")
          for i in list_args:
             try:
                status = SUCCESS
                utils.system_output("zfs " + i)
             except:
                status = FAIL
             if status == FAIL:
                logging.info("Badly formed ZFS volume sub-commands fail as expected.")
             else:
                raise error.TestFail("ZFS volume sub-commands succeeded unexpectedly.")

      def cleanup(self):
          logging.info("In cleanup function..")
          status = libzpool.pool_exists(TESTPOOL)
          if status == SUCCESS:
             libzpool.destroy(TESTPOOL)
          logging.info("Cleanup done successfully")
          return SUCCESS

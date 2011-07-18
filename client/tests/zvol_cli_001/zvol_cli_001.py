###############################################################################
#
# __stc_assertion_start
#
# ID: zvol_cli_001_pos
#
# DESCRIPTION:
# Executing well-formed 'zfs list' commands should return success
#
# STRATEGY:
# 1. Create an array of valid options.
# 2. Execute each element in the array.
# 3. Verify success is returned.
#
###############################################################################

import os,logging
from autotest_lib.client.bin import test, utils
from autotest_lib.client.bin import libzfs, libzpool, configzfs, libzfs_common
from configzfs import *
from autotest_lib.client.common_lib import error

class zvol_cli_001(test.test):
      version = 2

      def setup(self):
          logging.info("In setup function..")
          if libzfs_common.load_zfs_modules() != SUCCESS:
             raise error.TestFail("Failed to load zfs modules..")
          return SUCCESS

      def run_once(self):
          logging.info("In run_once function.. ")
          logging.info("create pool..")
          disks = libzfs_common.get_free_disks()
          version = "1"
          status = libzpool.create(TESTPOOL, disks[0])
          if status != SUCCESS:
             raise error.TestFail("zpool create failed.. ")

          logging.info("create zvol on pool..")
          status = libzfs.create_zvol(TESTPOOL, "2G", TESTVOL)
          if status != SUCCESS:
             raise error.TestFail("cannot create zvol..")

          list_args = ["list", "list -r", "list "+TESTPOOL+"/"+TESTVOL,
                       "list -r "+TESTPOOL+"/"+TESTVOL,
                       "list -H "+TESTPOOL+"/"+TESTVOL,
                       "list -Hr "+TESTPOOL+"/"+TESTVOL,
                       "list -rH "+TESTPOOL+"/"+TESTVOL,
                       "list -o name "+TESTPOOL+"/"+TESTVOL,
                       "list -r -o name "+TESTPOOL+"/"+TESTVOL,
                       "list -H -o name "+TESTPOOL+"/"+TESTVOL,
                       "list -rH -o name "+TESTPOOL+"/"+TESTVOL]

          logging.info("Executing well-formed 'zfs list' commands")
          for i in list_args:
             utils.system("zfs " + i + " > /dev/null")

          logging.info("Executing zfs list on volume works as expected")

      def cleanup(self):
          logging.info("In cleanup function..")
          status = libzpool.pool_exists(TESTPOOL)
          if status == SUCCESS:
             libzpool.destroy(TESTPOOL)
          logging.info("Cleanup done successfully")
          return SUCCESS

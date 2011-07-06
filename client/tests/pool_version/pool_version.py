#############################################################################
# ID: pool version
#
# DESCRIPTION:

# zpool set version can only increment pool version or upgrade the pool.
# It should not downgrade the pool version.

# STRATEGY:
# 1. Taking a version 1 pool.
# 2. For all known versions(i.e. from 1 to 28), set the version of the pool
#     using zpool set.
# 3. Verify that pools versions.
# 4. Attempt to set prior versions.
# 5. Verify zpool should not downgrade the pool version.
##############################################################################

import os, logging
from autotest_lib.client.bin import test, utils
from autotest_lib.client.bin import libzfs, libzpool, configzfs, libzfs_common
from configzfs import *
from autotest_lib.client.common_lib import error

class pool_version(test.test):
      version = 2
      def setup(self):
          logging.info("In setup function.. ")
          if libzfs_common.load_zfs_modules() != SUCCESS:
             raise error.TestFail("Failed to load zfs modules..")
          return SUCCESS

      def run_once(self):
          logging.info("In run_once function.. ")

          logging.info("create zpool of version 1..")
          disks = "/dev/sda1"
          version = "1"
          status = libzpool.create(TESTPOOL, disks, version)
          if status != SUCCESS:
             raise error.TestFail("zpool create failed..")

          logging.info("Verify zpool set version can upgrade a pool..")
          for version in range(1, 29):
              status = libzpool.set_version(TESTPOOL, version)
              if status != SUCCESS:
                 raise error.TestFail("Version not set to expected version..")

              ret_val = libzpool.get_version(TESTPOOL)
              if ret_val != str(version):
                 raise error.TestFail("Version not set to expected version..")

          logging.info("Verify zpool set version should not downgrade the version..")

          for version in range(27, 0, -1):
              status = libzpool.set_version(TESTPOOL, version)
              if status == SUCCESS:
                 raise error.TestFail("version should not downgrade..")

              ret_val = libzpool.get_version(TESTPOOL)
              if ret_val != "28":
                 raise error.TestFail("version should not downgrade..")

          logging.info("Upgrading and downgrading pool version passed..")

      def cleanup(self):
          logging.info("In cleanup function.. ")

          status = libzpool.pool_exists(TESTPOOL)
          if status == SUCCESS:
             libzpool.destroy(TESTPOOL)

          logging.info("Cleanup done successfully...")
          return SUCCESS



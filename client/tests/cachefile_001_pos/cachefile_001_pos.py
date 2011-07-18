#############################################################################
# ID: cachefile_001_pos
#
# DESCRIPTION:
#
# Creating a pool with cachefile property and verifying the property
#
# STRATEGY:
# 1. Create a pool with the cachefile property
# 2. Verify the cachefile property is set
#
# TESTABILITY: explicit
#
# TEST_AUTOMATION_LEVEL: automated
#
# CODING_STATUS: COMPLETED (2007-09-05)
#
##############################################################################

import os, logging
from autotest_lib.client.bin import test, utils
from autotest_lib.client.bin import libzfs, libzpool, configzfs, libzfs_common
from configzfs import *
from autotest_lib.client.common_lib import error

CPATH = "/etc/zfs/zpool.cache"
CPATH1 = "/var/tmp/cachefile"

class cachefile_001_pos(test.test):
      version = 2
      def setup(self):
	  logging.info("In setup function.. ")

	  if libzfs_common.load_zfs_modules() != SUCCESS:
             raise error.TestFail("Failed to load zfs modules..")
          return SUCCESS

      def run_once(self):
          logging.info("In run_once function.. ")

	  disks = libzfs_common.get_free_disks()

          opts = ["none", "false", "none", CPATH, "true", "-", CPATH1, "true", CPATH1]
	  for i in range(0, 8, 3):
              logging.info("create a zpool with cachefile property..")

	      status = libzpool.create(TESTPOOL, disks[0], cachefile = opts[i])
              if status != SUCCESS:
                 raise error.TestFail("zpool create failed..")

	      # checking for the pool name in the strings output of
	      # the given cachefile, default is /etc/zfs/zpool.cache
	      if opts[i + 1] == "false":
	         tmp = "strings " + CPATH + " | grep -w " + TESTPOOL
	      else:
	         tmp = "strings " + opts[i] + " | grep -w " + TESTPOOL
	      try:
		 status = SUCCESS
                 utils.system_output(tmp)
              except:
	         status = FAIL

              if status == SUCCESS:
	         if opts[i + 1] != "true":
		    raise error.TestFail("pool was not in cache..")
              else:
		 if opts[i + 1] != "false":
		    raise error.TestFail("pool was in cache..")

              prop_val = libzpool.get_property(TESTPOOL, "cachefile")
              if prop_val != opts[i + 2]:
	         raise error.TestFail("cachefile property not set as expected..")

              libzpool.destroy(TESTPOOL)

	  logging.info("cachefile_001_pos test passed successfully..")

      def cleanup(self):
          logging.info("In cleanup function.. ")

          status = libzpool.pool_exists(TESTPOOL)
          if status == SUCCESS:
             libzpool.destroy(TESTPOOL)

          for file in [CPATH, CPATH1]:
              if os.path.isfile(file):
		 utils.system("rm " + file)

          logging.info("Cleanup done successfully...")
          return SUCCESS

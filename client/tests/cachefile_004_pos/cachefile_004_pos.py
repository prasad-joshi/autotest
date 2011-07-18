#############################################################################
# ID: cachefile_004_pos
#
# DESCRIPTION:
#
# Setting altroot=<path> and cachefile=$CPATH for zpool create is succeed
#
# STRATEGY:
# 1. Attempt to create a pool with -o altroot=<path> -o cachefile=<value>
# 2. Verify the command succeed
#
# TESTABILITY: explicit
#
# TEST_AUTOMATION_LEVEL: automated
#
# CODING_STATUS: COMPLETED (2011-07-14)
##############################################################################

import os, logging
from autotest_lib.client.bin import test, utils
from autotest_lib.client.bin import libzfs, libzpool, configzfs, libzfs_common
from configzfs import *
from autotest_lib.client.common_lib import error

pid = os.getpid()
TESTDIR = "/altdir." + str(pid)
CPATH = "/etc/zfs/zpool.cache"
CPATH1 = "/var/tmp/cachefile"

# checking for the pool name in the strings output of
# the given cachefile, default is /etc/zfs/zpool.cache
def pool_in_cache(pool, file):
    try:
       status = SUCCESS
       utils.system_output("strings " + file + " | grep -w " + pool)
    except:
       status = FAIL
    return status

class cachefile_004_pos(test.test):
      version = 2
      def setup(self):
	  logging.info("In setup function.. ")

	  if libzfs_common.load_zfs_modules() != SUCCESS:
             raise error.TestFail("Failed to load zfs modules..")
          return SUCCESS

      def run_once(self):
          logging.info("In run_once function.. ")

	  disks = libzfs_common.get_free_disks()

          opts = ["none", "none", CPATH, "-", CPATH1, CPATH1]
	  for i in range(0, 5, 2):
              logging.info("create a zpool with cachefile and altroot property..")
	      status = libzpool.create(TESTPOOL, disks[0], cachefile = opts[i],
			               altroot = TESTDIR)
              if status != SUCCESS:
                 raise error.TestFail("zpool create failed..")

	      if opts[i] == "none":
                 status = pool_in_cache(TESTPOOL, CPATH)
                 if status == SUCCESS:
	            raise error.TestFail("pool was in cache..")
              else:
	          status = pool_in_cache(TESTPOOL, opts[i])
                  if status != SUCCESS:
		     raise error.TestFail("pool was not in cache..")

              prop_val = libzpool.get_property(TESTPOOL, "cachefile")
              if prop_val != opts[i + 1]:
	         raise error.TestFail("cachefile property not set as expected..")

              libzpool.destroy(TESTPOOL)

	  logging.info("cachefile_004_pos test passed successfully..")

      def cleanup(self):
          logging.info("In cleanup function.. ")

          status = libzpool.pool_exists(TESTPOOL)
          if status == SUCCESS:
             libzpool.destroy(TESTPOOL)

          for file in [CPATH, CPATH1]:
              if os.path.isfile(file):
		 utils.system("rm " + file)

          if os.path.exists(TESTDIR):
             utils.system("rm -r " + TESTDIR)

	  logging.info("Cleanup done successfully...")
          return SUCCESS

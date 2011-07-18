#############################################################################
# ID: cachefile_002_pos
#
# DESCRIPTION:
#
# Importing a pool with cachefile property and verifying it
#
# STRATEGY:
# 1. Create a pool with the none cachefile property
# 2. Verify the pool doesn't have an entry in zpool.cache
# 3. Export the pool
# 4. Import the pool
# 5. Verify the pool does have an entry in zpool.cache
# 6. Export the pool
# 7. Import the pool with cacahefile
# 8. Verify the pool does have an entry in cachefile
#
# TESTABILITY: explicit
#
# TEST_AUTOMATION_LEVEL: automated
#
# CODING_STATUS: COMPLETED (2011-07-13)

##############################################################################

import os, logging
from autotest_lib.client.bin import test, utils
from autotest_lib.client.bin import libzfs, libzpool, configzfs, libzfs_common
from configzfs import *
from autotest_lib.client.common_lib import error

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

class cachefile_002_pos(test.test):
      version = 2
      def setup(self):
          logging.info("In setup function.. ")

	  if libzfs_common.load_zfs_modules() != SUCCESS:
             raise error.TestFail("Failed to load zfs modules..")
          return SUCCESS

      def run_once(self):
          logging.info("In run_once function.. ")

	  disks = libzfs_common.get_free_disks()

	  logging.info("create a zpool with cachefile property..")
	  status = libzpool.create(TESTPOOL, disks[0], cachefile = "none")
          if status != SUCCESS:
	     raise error.TestFail("zpool create failed..")

          status = pool_in_cache(TESTPOOL, CPATH)
	  if status == SUCCESS:
	     raise error.TestFail("pool was in cache..")

	  libzpool.export_pool(TESTPOOL)
          libzpool.import_pool(TESTPOOL)

          status = pool_in_cache(TESTPOOL, CPATH)
          if status != SUCCESS:
             raise error.TestFail("pool was not in cache..")

          libzpool.export_pool(TESTPOOL)
	  libzpool.import_pool(TESTPOOL, cachefile="none")

	  status = pool_in_cache(TESTPOOL, CPATH)
	  if status == SUCCESS:
	     raise error.TestFail("pool was not in cache..")

          libzpool.export_pool(TESTPOOL)
          libzpool.import_pool(TESTPOOL, cachefile = CPATH1)

	  status = pool_in_cache(TESTPOOL, CPATH1)
	  if status != SUCCESS:
	     raise error.TestFail("pool was not in cache..")

	  logging.info("cachefile_002_pos test passed successfully..")

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

#############################################################################
# ID: cachefile_003_pos
#
# DESCRIPTION:
#       Verify set, export and destroy when cachefile is set on pool.
#
# STRATEGY:
#       1. Create two pools with same cahcefile1.
#       2. Set cachefile of the two pools to another same cachefile2.
#       3. Verify cachefile1 not exist.
#       4. Export the two pools.
#       5. Verify cachefile2 not exist.
#       6. Import the two pools and set cachefile to cachefile2.
#       7. Destroy the two pools.
#       8. Verify cachefile2 not exist.
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
CPATH1 = "/var/tmp/cachefile." + str(pid)
CPATH2 = "/cachefile." + str(pid)

# checking for the pool name in the strings output of
# the given cachefile, default is /etc/zfs/zpool.cache
def pool_in_cache(pool, file):
    try:
       status = SUCCESS
       utils.system_output("strings " + file + " | grep -w " + pool)
    except:
       status = FAIL
    return status

class cachefile_003_pos(test.test):
      version = 2
      def setup(self):
          logging.info("In setup function.. ")

	  if libzfs_common.load_zfs_modules() != SUCCESS:
             raise error.TestFail("Failed to load zfs modules..")
          return SUCCESS

      def run_once(self):
          logging.info("In run_once function.. ")

	  logging.info("Verify set, export and destroy when cachefile is set on pool.")
          disks = libzfs_common.get_free_disks()

          logging.info("create a zpool with cachefile property..")
          status = libzpool.create(TESTPOOL, disks[0], cachefile = CPATH1)
          if status != SUCCESS:
	     raise error.TestFail("zpool create failed..")

	  status = pool_in_cache(TESTPOOL, CPATH1)
	  if status != SUCCESS:
	     raise error.TestFail("pool was not in cache..")

	  status = libzpool.create(TESTPOOL1, disks[3], cachefile = CPATH1)
	  if status != SUCCESS:
	     raise error.TestFail("zpool create failed..")

          status = pool_in_cache(TESTPOOL1, CPATH1)
	  if status != SUCCESS:
	     raise error.TestFail("pool was not in cache..")

	  status = libzpool.set_property(TESTPOOL, "cachefile", CPATH2)
	  if status != SUCCESS:
	     raise error.TestFail("zpool set property failed..")

          status = pool_in_cache(TESTPOOL, CPATH2)
	  if status != SUCCESS:
	     raise error.TestFail("pool was not in cache..")

	  status = libzpool.set_property(TESTPOOL1, "cachefile", CPATH2)
          if status != SUCCESS:
	     raise error.TestFail("zpool set property failed..")

          status = pool_in_cache(TESTPOOL1, CPATH2)
	  if status != SUCCESS:
	     raise error.TestFail("pool was not in cache..")

	  if os.path.isfile(CPATH1) :
	     raise error.TestFail(CPATH1 + " file still exist..")

	  libzpool.export_pool(TESTPOOL)
	  libzpool.export_pool(TESTPOOL1)

          if os.path.isfile(CPATH2) :
	     raise error.TestFail(CPATH2 + " file still exist..")

	  libzpool.import_pool(TESTPOOL)

          status = libzpool.set_property(TESTPOOL, "cachefile", CPATH2)
	  if status != SUCCESS:
	     raise error.TestFail("zpool set property failed..")

          status = pool_in_cache(TESTPOOL, CPATH2)
	  if status != SUCCESS:
             raise error.TestFail("pool was not in cache..")

          libzpool.import_pool(TESTPOOL1)

          status = libzpool.set_property(TESTPOOL1, "cachefile", CPATH2)
	  if status != SUCCESS:
	     raise error.TestFail("zpool set property failed..")

	  status = pool_in_cache(TESTPOOL1, CPATH2)
          if status != SUCCESS:
             raise error.TestFail("pool was not in cache..")

          libzpool.destroy(TESTPOOL)
          libzpool.destroy(TESTPOOL1)

	  if os.path.isfile(CPATH2):
	     raise error.TestFail(CPATH2 + " file still exist..")

	  logging.info("cachefile_003_pos test passed successfully..")

      def cleanup(self):
          logging.info("In cleanup function.. ")

          status = libzpool.pool_exists(TESTPOOL)
          if status == SUCCESS:
             libzpool.destroy(TESTPOOL)

          status = libzpool.pool_exists(TESTPOOL1)
	  if status == SUCCESS:
	     libzpool.destroy(TESTPOOL1)

          for file in [CPATH1, CPATH2]:
              if os.path.isfile(file):
		 utils.system("rm " + file)

          logging.info("Cleanup done successfully...")
          return SUCCESS

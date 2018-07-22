"""
Copyright (c) 2018 VMware, Inc.  All rights reserved.
-- VMware Confidential
"""

import sys
import getopt
from helper.connector import ElevatorConnector
from helper.loadgenerator import WorkLoadGenerator

usage = """Load dummy workload and verify specified elevator service

Usage: testclient.py [options]

Options:
    -h / --help
        Print this message and exit.

    -S servicename
    --servicename=servicename
        The endpoint of elevator service (required field)

"""

def Usage():
    print(usage)

def main():
   try:
      opts, args = getopt.getopt(sys.argv[1:],"hS:",["help","servicename="])
   except getopt.error, msg:
       # print help information and return:
       Usage()
       return(1)
   service = None
   for opt, arg in opts:
      if opt in ("-h","--help"):
         Usage()
         return(0)

      if opt in ("-S","--servicename"):
         service = arg

   if service is None:
      Usage()
      return(1)

   loadGenerator = WorkLoadGenerator()
   if not service.startswith("http://"):
      service = "http://%s" % service
   conn = ElevatorConnector(service)
   worldClock = 0
   while(not loadGenerator.IsDone()):
      try:
         if worldClock == 0:
            newState = conn.ResetElevator()
            continue
         workloads = loadGenerator.GenNext(worldClock, newState)
         newState = conn.RequestElevator(workloads)
      finally:
         worldClock += 1

if __name__ == '__main__':
   main()

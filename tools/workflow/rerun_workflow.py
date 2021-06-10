#!/usr/bin/env python3

import argparse
import time
import sys
from ghapi.all import GhApi

timeout = 3*60*60 # wait for max 3 hours
interval = 5*60 # wait for 5 minutes between query status

parser = argparse.ArgumentParser(description="Re-run failed GitHub workflow")
parser.add_argument("owner", type=str, help="owner")
parser.add_argument("repo", type=str, help="repository")
parser.add_argument("run", type=str, help="run id")
args = parser.parse_args()

api = GhApi(args.owner, args.repo)
run_id = args.run

start = int(time.time())
while (int(time.time()) - start < timeout):
    status = api.actions.get_workflow_run(run_id).status
    print("Workflow Status:", status)
    if status == "completed":
        result = api.actions.get_workflow_run(run_id).conclusion
        print("Workflow Result:", result)
        if result != "success" and result != "cancelled":
            api.actions.re_run_workflow(run_id)
            print("Re-run workflow")
            sys.exit(0)
        else:
            print("Needn't re-run if it is sucess or cancelled")
            sys.exit(0)
    else:
        time.sleep(interval)
        print("Sleep %d seconds" % interval)
print("Time out!!!")
sys.exit(1)




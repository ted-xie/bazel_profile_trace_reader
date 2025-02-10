#!/usr/bin/env python3
"""Dump the critical path events from a bazel profile"""

import argparse
import gzip
import json
import os

from common import JsonToDict

def ValidateArgs(cml_args):
  # TODO(tedx): Same as extract_totle_time_per_mnemonic#ValidateArgs, maybe move to common?
  if not os.path.exists(cml_args.profile_json):
    raise FileNotFoundError(f"Profile JSON '{cml_args.profile_json}' not found.")

def DumpCriticalPath(profile_json: str):
  profile_dict = JsonToDict(profile_json)
  # TODO(tedx): Break down critical path by mnemonic
  for event in profile_dict["traceEvents"]:
    if event["cat"] == "critical path component":
      out_buffer = event["name"]
      if "args" in event and "mnemonic" in event["args"]:
        out_buffer = f"{event['args']['mnemonic']}: {event['name']}"
      print(out_buffer)

def DumpCriticalPathMain():
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument("profile_json", help="Path to Bazel profile json")
  args = parser.parse_args()

  ValidateArgs(args)

  DumpCriticalPath(args.profile_json)

if __name__ == "__main__":
  DumpCriticalPathMain()

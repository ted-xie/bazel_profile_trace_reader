#!/usr/bin/env python3
"""Extract the total time per mnemonic from a bazel profile"""

import argparse
import gzip
import json
import os

from common import JsonToDict

def ValidateArgs(cml_args):
  if not os.path.exists(cml_args.profile_json):
    raise FileNotFoundError(f"Profile JSON '{cml_args.profile_json}' not found.")

def ExtractTotalTimePerMnemonic(profile_json, mnemonic):
  sum = 0
  num_actions = 0

  profile_dict = JsonToDict(profile_json)

  for event in profile_dict["traceEvents"]:
    arg_mnemonic = ""
    if "args" in event and "mnemonic" in event["args"]:
      arg_mnemonic = event["args"]["mnemonic"]
    if mnemonic in event["name"] or mnemonic in arg_mnemonic:
      num_actions += 1
      # Duration in microseconds is the "dur" field
      sum += event["dur"]

  ret_dict = {"num_actions": num_actions, "total_cpu_time": sum}
  return ret_dict

def ExtractTotalTimePerMnemonicMain():
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument("profile_json", help="Path to Bazel profile json")
  parser.add_argument("--mnemonic", help="Mnemonic to search for, "
                      "for example 'Dexing'", required=True)
  args = parser.parse_args()

  ValidateArgs(args)

  ret_dict = ExtractTotalTimePerMnemonic(args.profile_json, args.mnemonic)
  total_actions = ret_dict["num_actions"]
  total_time_us = ret_dict["total_cpu_time"]
  print(f"Total number of actions for {args.mnemonic} was {total_actions}.")
  print(f"Total time for {args.mnemonic} was {total_time_us} microseconds.")

if __name__ == "__main__":
  ExtractTotalTimePerMnemonicMain()

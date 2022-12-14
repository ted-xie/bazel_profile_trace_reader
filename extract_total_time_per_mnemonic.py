#!/usr/bin/env python3
"""Extract the total time per mnemonic from a bazel profile"""

import argparse
import gzip
import json
import os

def ValidateArgs(cml_args):
  if not os.path.exists(cml_args.profile_json):
    raise FileNotFoundError(f"Profile JSON '{cml_args.profile_json}' not found.")

def ExtractTotalTimePerMnemonic(profile_json, mnemonic):
  json_raw = ""
  sum = 0
  num_actions = 0

  if profile_json.endswith(".gz"):
    with gzip.open(profile_json, "r") as f:
      json_raw = f.read()
  else:
    with open(profile_json, "r") as f:
      json_raw = f.read()

  # TODO(tedx): Loads the entire thing at once. Consider using streaming API for
  # larger json files.
  profile_dict = json.loads(json_raw)
  for event in profile_dict["traceEvents"]:
    if mnemonic in event["name"]:
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

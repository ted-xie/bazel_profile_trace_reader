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
  total_wall_time = 0
  num_actions = 0

  profile_dict = JsonToDict(profile_json)

  durations = []

  for event in profile_dict["traceEvents"]:
    arg_mnemonic = ""
    if "args" in event and "mnemonic" in event["args"]:
      arg_mnemonic = event["args"]["mnemonic"]
    if mnemonic in event["name"] or mnemonic in arg_mnemonic:
      num_actions += 1
      # Duration in microseconds is the "dur" field
      sum += event["dur"]
      durations.append(event["dur"])
    total_wall_time += event["dur"] if "dur" in event else 0

  # Calculate p25, p50, p90 durations
  num_events = len(durations)
  durations = sorted(durations)
  p25 = durations[int(num_events / 4)]
  p50 = durations[int(num_events / 2)]
  p90 = durations[int(num_events * 0.90)]
  p95 = durations[int(num_events * 0.95)]
  p99 = durations[int(num_events * 0.99)]

  ret_dict = {
          "total_actions": len(profile_dict["traceEvents"]),
          "num_actions": num_actions,
          "total_cpu_time": sum,
          "total_wall_time": total_wall_time,
          "p25_time": p25,
          "p50_time": p50,
          "p90_time": p90,
          "p95_time": p95,
          "p99_time": p99
          }
  return ret_dict

def ExtractTotalTimePerMnemonicMain():
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument("profile_json", help="Path to Bazel profile json")
  parser.add_argument("--mnemonic", help="Mnemonic to search for, "
                      "for example 'Dexing'", required=True)
  args = parser.parse_args()

  ValidateArgs(args)

  ret_dict = ExtractTotalTimePerMnemonic(args.profile_json, args.mnemonic)
  bazel_total_actions = ret_dict["total_actions"]
  total_mnemonic_actions = ret_dict["num_actions"]
  total_time_us = ret_dict["total_cpu_time"]
  total_wall_time = ret_dict["total_wall_time"]
  print(f"Total wall time: {total_wall_time} microseconds.")
  print(f"Total number of Bazel actions was {bazel_total_actions}")
  print(f"Total number of actions for {args.mnemonic} was {total_mnemonic_actions}.")
  print(f"Total time for {args.mnemonic} was {total_time_us} microseconds.")
  print(f"P25 time for {args.mnemonic} was {ret_dict['p25_time']} microseconds.")
  print(f"P50 time for {args.mnemonic} was {ret_dict['p50_time']} microseconds.")
  print(f"P90 time for {args.mnemonic} was {ret_dict['p90_time']} microseconds.")
  print(f"P95 time for {args.mnemonic} was {ret_dict['p95_time']} microseconds.")
  print(f"P99 time for {args.mnemonic} was {ret_dict['p99_time']} microseconds.")

if __name__ == "__main__":
  ExtractTotalTimePerMnemonicMain()

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

def NormalizeSpecialCases(s: str) -> str:
  # Some special case scenarios
  SPECIAL_STARTS = set([
    "Merging Kotlin output jar",
    "Extracting interface for jar",
    "Symlinking virtual headers",
    "Linking"
    "Generating Descriptor Set",
    "ProtoCompile",
    "KotlinCompile",
  ])

  for special in SPECIAL_STARTS:
    if s.startswith(special):
      return special
  return s

def ExtractMessage(s: str) -> str:
  # Critical path names are formatted like so:
  # action 'Something something /path/to/file'
  # The action message is everything except the last word, omitting the apostrophe
  # Regular action processing messages are formatted like so:
  # "Something something /path/to/file"
  # This function must handle both cases.

  sc = NormalizeSpecialCases(s)
  if sc != s:
    return sc

  info_and_message = " ".join(s.split(" ")[:-1])
  start_idx = 0
  if "'" in info_and_message:
    start_idx = info_and_message.index("'") + 1
  return info_and_message[start_idx:]

def DumpCriticalPath(profile_json: str):
  profile_dict = JsonToDict(profile_json)

  # A dictionary corresponding message to mnemonics
  messages_to_mnemonics = dict()
  # A list of (message, name) tuples
  crit_path_events = []
  for event in profile_dict["traceEvents"]:
    if "cat" not in event:
      continue
    if event["cat"] == "critical path component":
      name = event["name"]
      message = ""
      if name.startswith("action '"):
        message = ExtractMessage(name)
      crit_path_events.append((message, name))
    elif event["cat"] == "action processing":
      # Correlate the message to the mnemonic, if possible
      if "args" in event and "mnemonic" in event["args"]:
        messages_to_mnemonics[ExtractMessage(event["name"])] = event["args"]["mnemonic"]

  # Print out the critical path event list with messages substituted for their appropriate mnemonics
  for event in crit_path_events:
    # By default, use tuple[0] (the message) as the mnemonic. The mnemonic may not be known by the dict.
    mnemonic = event[0]
    mnemonic_candidate = NormalizeSpecialCases(event[0])
    if mnemonic_candidate in messages_to_mnemonics:
        mnemonic = messages_to_mnemonics[mnemonic_candidate]
    elif event[0].startswith(NormalizeSpecialCases(event[0])):
        mnemonic = mnemonic_candidate
    else:
        print(f"WARN: Could not find '{mnemonic_candidate}' in messages_to_mnemonics")
    print(f"{mnemonic}: {event[1]}")

def DumpCriticalPathMain():
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument("profile_json", help="Path to Bazel profile json")
  args = parser.parse_args()

  ValidateArgs(args)

  DumpCriticalPath(args.profile_json)

if __name__ == "__main__":
  DumpCriticalPathMain()

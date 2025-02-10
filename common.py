#!/usr/bin/env python3
"""Common utilities"""

import gzip
import json
import os

def JsonToDict(profile_json: str) -> dict:
  json_raw = ""
  if profile_json.endswith(".gz"):
    with gzip.open(profile_json, "r") as f:
      json_raw = f.read()
  else:
    with open(profile_json, "r") as f:
      json_raw = f.read()

  # TODO(tedx): Loads the entire thing at once. Consider using streaming API for
  # larger json files.
  profile_dict = json.loads(json_raw)

  return profile_dict

load("@rules_python//python:py_binary.bzl", "py_binary")
load("@rules_python//python:py_library.bzl", "py_library")

py_library(
  name = "common",
  srcs = ["common.py"],
)

py_binary(
  name = "extract_total_time_per_mnemonic",
  srcs = ["extract_total_time_per_mnemonic.py"],
  deps = [":common"],
)

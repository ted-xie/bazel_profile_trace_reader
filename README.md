# Bazel profile reader

Bazel provides a handy flag (`--profile`) to extract the amount of time taken
per action in a build. This profile trace can be loaded into `chrome://tracing`,
or the critical path can be analyzed using `bazel analyze-profile`. See
https://bazel.build/rules/performance for more information.

This tool is a simple command-line utility that reads the trace and extracts
total CPU time per mnemonic. It is much lighter-weight than both Bazel and
Chrome, doesn't require a graphical session, and is easily hackable.

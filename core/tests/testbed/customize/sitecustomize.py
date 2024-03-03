import os

# Only set up the app processes for coverage *if* coverage is running.
# Otherwise, just importing coverage will force running coverage.
# The COVERAGE_RUN environment variable is set by coverage.py itself.
if os.environ.get("COVERAGE_RUN"):
    import coverage

    coverage.process_startup()

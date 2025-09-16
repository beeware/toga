This repository is dedicated to development, testing, and proof-of-concept work related to issue [3545](https://github.com/beeware/toga/issues/3545), which focuses on implementing testing for the web platform.

## How We Run this Test Suite
1. Open this directory.
2. Create a Python 3.12 virtual environment and install test requirements:
   - `python3.12 -m venv venv`
   - `source venv/bin/activate`
   - `pip install -U pip`
   - `pip install --group test`
   - `playwright install chromium`
3. Run your Toga app as a web app.
   - `briefcase run web`
4. In a separate terminal, run the test suite:
   - `source venv/bin/activate`
   - `pytest tests`

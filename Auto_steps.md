======================= Installation ===============================

1. Install VS Code
2. Install Python through MS Store
3. mkdir playwright-python
   cd playwright-python
and also crate "tests" folder

In "playwright-python" folder create environment
4. For Environment
  --------> python -m venv venv

5. To Activate
  --------> 
venv\Scripts\activate
cd pages

6. pytest installation
  --------> python -m pip install pytest

7. Version
  --------> python -m pytest --version

8. Playwright Installation
  --------> python -m pip install playwright

9. playwright Browsers Installation
  --------> python -m playwright install

10. Install Pytest Playwright Plugin
  --------> python -m pip install pytest-playwright

11. For Excel readable
  --------> python -m pip install openpyxl

12. Run Command
  -------->
python -m pytest -s test_cv.py
pytest -s test_mc.py
python -m pytest -s test_uat_pc.py
python -m pytest -s test_pa.py

13. For Traces
 -------->
python -m playwright show-trace traces/test_cv.zip
python -m playwright show-trace traces/test_pa.zip


Code Generation
  --------> playwright codegen https://tune.sit.indigit.io/#/home#Apps
  --------> playwright codegen --browser=firefox https://tune.sit.indigit.io/#/home#Agent%20Dashboard
  --------> playwright codegen --browser=firefox https://agent-uat.tuneinsurance.com/#/home#QMS%20Agent
  --------> python -m playwright codegen --browser=firefox https://tus4appsit.tuneprotect.com:44300/sap/bc/ui2/flp#Shell-home
  --------> python -m playwright codegen --browser=firefox https://tus4appuat.tuneprotect.com:44303/sap/bc/ui2/flp#Shell-home
  --------> python -m playwright codegen --browser=firefox https://tupqmdbsit.tuneprotect.com:10002/sap/bc/ui2/flp#Shell-home
  























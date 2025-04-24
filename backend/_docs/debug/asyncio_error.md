bug Summary: pytest [trio] Error Despite Forcing asyncio
Objective
Run async FastAPI tests using only the asyncio backend, avoiding errors about missing trio.

Steps Taken
1. Test File Marking
Added at the top of test_rate_limit_and_headers.py:
python
CopyInsert
pytestmark = pytest.mark.anyio("asyncio")
Goal: Only run tests with the asyncio backend.
2. Project & Global Config
Added to pytest.ini:
CopyInsert
[pytest]
anyio_backend = asyncio
Added to pyproject.toml:
toml
CopyInsert
[
tool.pytest.ini_options
]
anyio_backend = "asyncio"
Goal: Ensure all pytest runs use only asyncio for async tests.
3. Cache & Bytecode Cleanup
Ran pytest --cache-clear and deleted __pycache__ folders. Goal: Remove any old config or bytecode that could interfere.
4. Forced Backend via CLI
Tried running:
CopyInsert
pytest --anyio-backend=asyncio app/tests/api/test_rate_limit_and_headers.py --maxfail=1 --disable-warnings -v
Result: --anyio-backend not recognized (old pytest-anyio version).
5. Dependency Upgrades
Recommended:
CopyInsert
pip install --upgrade pytest pytest-anyio anyio
Goal: Ensure latest versions that respect config and CLI flags.
6. Checked for Rogue Parameterization
Searched for pytest.mark.anyio and anyio_backend in all test and conftest.py files. Goal: Ensure no test or fixture is forcing both backends.
Persistent Error
Despite all the above, the following error persists:

CopyInsert
app/tests/api/test_rate_limit_and_headers.py::test_rate_limit_exceeded[trio] ERROR
ModuleNotFoundError: No module named 'trio'
Meaning: pytest is still parameterizing tests for both asyncio and trio, even though all configs and markers restrict to asyncio.
Symptoms: Tests pass for [asyncio] but fail for [trio] due to missing trio package.
Root Cause Hypotheses
Outdated or broken pytest/pytest-anyio/anyio install: CLI flags and config are not respected.
Hidden parameterization: A conftest.py or plugin somewhere is still requesting both backends.
Multiple pytest installs or wrong environment: pytest is run from a different environment than where dependencies are installed.
Next Recommendations
Upgrade all test dependencies in your active virtual environment.
Check for and remove any pytest.mark.anyio without arguments in all test and conftest files.
Check for multiple pytest installations (where pytest on Windows).
If you need to unblock immediately:
Install trio with pip install trio (not a real fix, but will silence the error).
Summary Table
| Step | Action Taken | Result / Error | |-----------------------------|----------------------------------------|---------------------------------------| | Test file marker | pytestmark = pytest.mark.anyio("asyncio") | [trio] test still runs | | pytest.ini/pyproject.toml | anyio_backend = asyncio | [trio] test still runs | | Cache clear | pytest --cache-clear | [trio] test still runs | | CLI flag | --anyio-backend=asyncio | Flag not recognized | | Dependency upgrade | (recommended) | Unknown (please confirm if done) | | Search for parameterization | (recommended) | Unknown (please confirm if done) |

If you want to fully resolve this, please confirm:

The output of pip show pytest-anyio
That you have no stray pytest.mark.anyio or parameterization for both backends in your codebase
That you are running pytest from the correct environment
`make test` runs the project's test suite with pytest.

**The command** (`Makefile:19-20`):
```make
test: ## Palaiž testus
	python -m pytest -q
```
`-q` is quiet mode: you get a line of dots and a short summary instead of one line per test. The Makefile also exports `OMD_API_TOKEN=macibu-tokens-tikai-imitacijai`, a token meant only for the mock, so tests run with that variable set.

**Configuration** (`pyproject.toml`, `[tool.pytest.ini_options]`):
- `testpaths = ["tests"]`: pytest only looks for tests in `tests/`.
- `pythonpath = ["."]`: the repo root is added to the import path, so `from app...` works.
- One known httpx/Starlette `TestClient` deprecation warning is hidden.

**Fixtures** (`tests/conftest.py`):
- `client`: clears the in-memory SQLite storage with no seed data (`storage.reset(seed=False)`). It replaces the real OMD registry client with `FakeOmd`, then gives back a FastAPI `TestClient`. Tests don't make real HTTP calls, so you don't need `make mock` running.
- `fake_omd`: a stand-in for the registry. Personal code `32000000001` returns `ACTIVE`, every other code returns `NOT_ACTIVATED`, and it records each lookup in `calls`.
- `valid_payload`: a synthetic, valid submission body.

**What's tested** (17 tests):
- `tests/test_submissions.py` (10 tests), the API:
  - the health endpoint
  - creating a submission (201) and fetching it
  - 404 for an unknown ID
  - 400 errors for a missing field or an unknown topic
  - using the e-address when OMD reports it active
  - seed data existing
  - `/ui` being served
- `tests/test_working_days.py` (7 tests), the working-day calendar:
  - weekends and public holidays (Proclamation Day, Līgo/Jāņi) are skipped
  - adding N working days
  - a year outside the calendar is rejected

I read the configuration but didn't run the suite, so I can't say whether the tests currently pass.

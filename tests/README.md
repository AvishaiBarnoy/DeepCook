# DeepCook Test Suite

This directory contains automated tests for the DeepCook meal suggestion engine.

## Test Structure

### `test_auxillary.py`
Tests for the core meal selection logic (`scripts/auxillary.py`):

- **TestChooseRandom**: 8 tests covering the main `choose_random()` function
  - Basic random selection
  - Recently-made filtering (`last_made` parameter)  
  - Take-away filtering (`TA` parameter)
  - Combined filters
  - Edge cases (fallback when all filtered)

- **TestIsTooLateToCook**: 3 tests for time-based filtering
  - Before cutoff time
  - After cutoff time
  - Midnight cooking (now FIXED - correctly returns True for 0-4 AM)

- **TestMakeThisMeal**: 3 tests for meal logging
  - User confirms meal (yes)
  - User rejects meal (no)
  - Invalid input handling

- **TestEdgeCases**: 2 tests for edge cases
  - Empty database handling
  - Single meal database

### `test_filters.py`
Tests for kosher and diet filtering (`scripts/auxillary.py`):

- **TestFilterKosher**: 4 tests for kosher filtering
  - Nonkosher shows all meals
  - Parve excludes meat and dairy
  - Milchik excludes meat
  - Fleisch excludes dairy

- **TestFilterDiet**: 6 tests for diet filtering
  - Any diet shows all
  - Vegan-only filtering
  - Vegetarian includes vegan
  - Gluten-free filtering
  - Keto filtering
  - Missing column handling

- **TestFilterCombination**: 3 tests for combined filters
  - Vegan and parve together
  - Vegetarian and milchik together
  - Fleisch with dietary preferences

### `test_iodata.py`
Tests for data I/O operations (`scripts/iodata.py`):

- **TestAddMeal**: 3 tests for adding meals to database
  - Add single meal
  - Preserve existing meals
  - Add multiple meals

- **TestSaveData**: 2 tests for saving data
  - Creating CSV files
  - Overwriting existing files

- **TestWriteToLog**: 3 tests for meal logging
  - Creating log entries
  - Appending to existing log
  - Log format validation

- **TestEdgeCasesIO**: 2 tests for I/O edge cases
  - Empty database
  - Empty dataframe

## Running Tests

### Run all tests
```bash
pytest tests/
```

### Run specific test file
```bash
pytest tests/test_auxillary.py
pytest tests/test_iodata.py
pytest tests/test_filters.py
```

### Run with verbose output
```bash
pytest tests/ -v
```

### Run specific test class or function
```bash
pytest tests/test_auxillary.py::TestChooseRandom
pytest tests/test_auxillary.py::TestChooseRandom::test_last_made_filter_excludes_recent
pytest tests/test_filters.py::TestFilterKosher::test_filter_parve_excludes_meat_dairy
```

### Generate coverage report (if pytest-cov installed)
```bash
pytest tests/ --cov=scripts --cov-report=html
```

## Test Results

**Current Status**: ✅ All 39 tests passing

```
tests/test_auxillary.py::TestChooseRandom (8 tests) ............. PASSED
tests/test_auxillary.py::TestIsTooLateToCook (3 tests) .......... PASSED
tests/test_auxillary.py::TestMakeThisMeal (3 tests) ............. PASSED
tests/test_auxillary.py::TestEdgeCases (2 tests) ................ PASSED
tests/test_filters.py::TestFilterKosher (4 tests) ............... PASSED
tests/test_filters.py::TestFilterDiet (6 tests) ................. PASSED
tests/test_filters.py::TestFilterCombination (3 tests) .......... PASSED
tests/test_iodata.py::TestAddMeal (3 tests) ..................... PASSED
tests/test_iodata.py::TestSaveData (2 tests) .................... PASSED
tests/test_iodata.py::TestWriteToLog (3 tests) .................. PASSED
tests/test_iodata.py::TestEdgeCasesIO (2 tests) ................. PASSED

======================== 39 passed in 0.80s ========================
```

## Dependencies

Tests require:
- `pytest >= 7.4.3`
- `pytest-mock >= 3.12.0`

Install with:
```bash
pip install -r requirements.txt
```

## Test Fixtures

Tests use pytest fixtures to create sample data:
- `sample_meals_db`: Complete meal database with all required columns
- `meals_with_kosher`: Database with kosher type information
- `meals_with_diet`: Database with dietary information
- `meals_with_both`: Database with both kosher and diet info
- `sample_meals_for_logging`: Minimal database for logging tests
- Temporary files/directories for I/O tests

## Known Issues

### Fixed Bugs ✅
- **Midnight cooking logic**: FIXED in 2026-02-16 - `is_too_late_to_cook()` now correctly checks early morning hours (0-4 AM) before cutoff time

### Warnings
- **FutureWarning**: pandas `replace()` downcasting behavior (pre-existing)
- **FutureWarning**: Timestamp dtype compatibility (pre-existing)

These warnings don't affect functionality but should be addressed in future updates.

## Contributing

When adding new features:
1. Write tests first (TDD approach)
2. Ensure all existing tests still pass
3. Add new test files for new modules
4. Update this README with new test descriptions

## Test Coverage

Current test coverage focuses on:
- ✅ Core meal selection logic
- ✅ Filtering functionality (recently-made, take-away, time-based, kosher, diet)
- ✅ Data I/O operations
- ✅ Edge cases and error handling
- ✅ User interaction (mocked input)
- ✅ Filter combinations

Not yet covered:
- ⚠️ Web app (`streamlit_app.py`)
- ⚠️ Image loading (`image_loader.py`)
- ⚠️ Integration tests with real CSV files

---

**Last Updated**: 2026-02-16  
**Test Framework**: pytest 7.4.3  
**Test Count**: 39 tests (all passing)

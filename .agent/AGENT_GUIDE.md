# DeepCook Agent Guide

This guide provides essential information for AI agents working on the DeepCook meal suggestion engine.

## Project Overview

**DeepCook** is a Python meal suggestion engine that helps users decide what to make for dinner. It features:
- **CLI interface** (via Typer) for command-line meal suggestions
- **Web interface** (via Streamlit) for browser-based meal suggestions
- **Meal database** with tracking, logging, and filtering capabilities
- **Smart filtering** based on time, preferences, and meal attributes

**Author**: Avishai Barnoy (computational chemist/theoretical biophysicist)  
**License**: MIT  
**Development Philosophy**: Practical utility over formal engineering; acknowledged technical debt

## Core Architecture

### Entry Points

1. **CLI**: `main.py` 
   - Uses Typer for argument parsing
   - Calls `scripts.auxillary.choose_random()` for meal selection
   - Handles user prompts via `scripts.iodata.make_this_meal()`

2. **Web App**: `streamlit_app.py`
   - Single-page app with random meal button
   - Integrates Pexels API for food images
   - Tracks usage with counter

### Key Modules

#### `scripts/auxillary.py`
**Purpose**: Core meal selection logic

Key functions:
- `choose_random(meals, rank, times, last_made, TA, k)`: Main selection algorithm with filtering
- `is_too_late_to_cook(cutoff)`: Time-based filtering (after 8 PM, exclude long prep meals)
- `make_this_meal(meals, choice)`: User prompt for logging meals
- `filter_kosher(meal_list, kosher)`: Kosher filtering (placeholder, not implemented)

**Important Notes**:
- Returns tuple: `(meals, chosen_name, chosen_idx)`
- Modifies DataFrame in-place for timestamps
- Uses `pd.sample()` with optional weights from "Rank" column

#### `scripts/iodata.py`
**Purpose**: Data persistence and I/O operations

Key functions:
- `save_data(meals_db, path)`: Save meal database to CSV
- `write_to_log(meal_name)`: Log meal choices to `meal.log`
- `meal_questions(meals_db)`: Interactive prompts for adding new meals
- `add_meal(meals_db, new_meal)`: Insert new meal into database

#### `classes/classes.py`
**Purpose**: Type definitions

Currently defines:
- `KosherType(Enum)`: parve, milchik, fleisch, nonkosher

### Data Schema

**Primary Database**: `data/meal_list.csv`

| Column | Type | Description |
|--------|------|-------------|
| Name | str | English meal name |
| Name_he | str | Hebrew meal name |
| Rank | int | Personal preference (1-10) |
| Kosher | str | Kosher type |
| Prep_Time | str | short/medium/long |
| Cook_Time | str | short/medium/long |
| TA | int | Take-away flag (0/1) |
| Timestamp | date | Last prepared date |
| times_made | int | Preparation counter |
| recipe_suggestion | str | URL to recipe |
| ... | ... | Additional columns |

**Additional Databases** (in `data/`):
- `soups.csv`, `salads.csv`, `sandwiches.csv`, `sidedishes.csv`, `maincourses.csv`, `ta_list.csv`
- `muchtar_list.csv`: Alternative meal database
- `gerev_combinations.csv`, `cova_gerev.csv`: Combination data

## Development Guidelines

### Code Style
- **Minimal testing**: Currently NO unit tests (acknowledged by author)
- **Interactive testing**: Uses `--mock` flag for non-logging test runs
- **Import handling**: Try/except blocks for relative vs absolute imports
- **Path handling**: Uses `pathlib.Path` for cross-platform compatibility

### Common Patterns

#### Loading Data
```python
from pathlib import Path
import pandas as pd

MEAL_LIST = "data/meal_list.csv"
absolute_path = Path(__file__).parent / MEAL_LIST
meals_db = pd.read_csv(absolute_path, index_col=0)
```

#### Adding CLI Options (Typer)
```python
import typer

def main(
    new_flag: bool = typer.Option(False, help="Description here")
):
    # implementation
    pass

if __name__ == "__main__":
    typer.run(main)
```

#### Filtering Meals
```python
# Time-based filtering
if is_too_late_to_cook():
    meals_copy = meals_copy[meals_copy["Prep_Time"] < 2]

# Take-away filtering
if TA == False:
    meals_copy = meals_copy[meals_copy["TA"] == 0]
elif TA == True:
    meals_copy = meals_copy[meals_copy["TA"] == 1]
```

### Important Caveats

1. **In-place modifications**: Many functions modify DataFrames in-place
2. **No validation**: Input validation is minimal/absent
3. **Magic numbers**: Time cutoffs, rank values are hardcoded
4. **Incomplete features**: Several functions are stubs (e.g., `filter_kosher`)
5. **Deprecated code**: Look for comments like "DEPRECATED" or "NOT IMPLEMENTED YET"

## Feature Flags & CLI Options

Current CLI options (via `main.py --help`):

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--data` | str | `meal_list.csv` | CSV file with meal data |
| `--rank` | bool | False | Weight selection by rank |
| `--ta/--no-ta` | bool | None | Include/exclude take-away |
| `--inp` | bool | False | Add new meal interactively |
| `--kosher` | enum | fleisch | Kosher type (not implemented) |
| `--mock` | bool | False | Test mode (no logging) |

## Working with the Codebase

### Adding New Features

1. **New CLI option**: Add parameter to `main()` in `main.py`
2. **New filtering**: Add logic to `choose_random()` in `scripts/auxillary.py`
3. **New meal attribute**: Add column to `meal_list.csv` and update `meal_questions()`
4. **New page**: Add to `pages/` directory (Streamlit multi-page convention)

### Testing Strategy

Since there are no automated tests:
1. Use `--mock` flag to avoid polluting data
2. Run `scripts/reboot_timestamps.py` to reset test data
3. Test with small dataset changes first
4. Verify `meal.log` and timestamp updates manually

### Deployment

Web app deployment:
- Uses `deploy.sh` script
- Streamlit configuration in `.streamlit/` directory
- Counter tracked in `data/counter.txt`

## Known Issues & Technical Debt

From `TODO.md` and code comments:

### High Priority
- [ ] No automated tests
- [ ] Kosher filtering not implemented
- [ ] Diet-based filtering not implemented
- [ ] No prevention of recently-made meal suggestions
- [ ] Input validation missing

### Medium Priority
- [ ] Restructure web app pages
- [ ] Move to standardized column naming (snake_case vs camelCase)
- [ ] Extract magic numbers to configuration
- [ ] Add meal scaling factors

### Low Priority
- [ ] Hebrew translation
- [ ] Enhanced recipe suggestion integration
- [ ] Weekly meal planner
- [ ] Take-away category suggestions

## Dependencies

Key dependencies (see `requirements.txt`):
- **pandas** (2.2.2): Data manipulation
- **typer**: CLI framework
- **streamlit** (1.37.1): Web framework
- **pexels-api-py**: Food photography API
- **pillow**: Image handling
- **python-dotenv**: Environment configuration

## File Structure Reference

```
DeepCook/
├── main.py                      # CLI entry point
├── streamlit_app.py             # Web app entry point
├── image_loader.py              # Pexels API integration
├── requirements.txt             # Dependencies
├── deploy.sh                    # Deployment script
├── README.md                    # User documentation
├── TODO.md                      # Feature roadmap
├── CHANGELOG.txt                # Development history
├── METADATA.md                  # Data schema documentation
├── LICENSE.md                   # MIT license
├── classes/
│   ├── __init__.py
│   ├── classes.py               # Enum definitions
│   └── README.txt
├── scripts/
│   ├── __init__.py
│   ├── auxillary.py             # Core selection logic
│   ├── auxillary_new.py         # Experimental version
│   ├── iodata.py                # Data I/O operations
│   ├── reboot_timestamps.py     # Reset utility
│   ├── new_structure.py         # Refactoring experiments
│   └── idea_from_gptchat.py     # External contributions
├── data/
│   ├── meal_list.csv            # ⭐ Main meal database
│   ├── muchtar_list.csv         # Alternative database
│   ├── soups.csv, salads.csv, sandwiches.csv
│   ├── sidedishes.csv, maincourses.csv
│   ├── ta_list.csv              # Take-away options
│   ├── gerev_combinations.csv   # Meal combinations
│   ├── counter.txt              # Web app usage counter
│   └── duplicates.py            # Utility script
├── pages/
│   ├── 0_muchtar.py             # Streamlit page
│   ├── 2_suggest.py             # Streamlit page
│   └── 3_about.py               # Streamlit page
├── tests/
│   └── __init__.py              # (Empty test directory)
├── backup_and_templates/        # Backup files
├── full_meal_rnd/              # Experimental directory
├── .streamlit/                 # Streamlit config
└── .agent/
    └── AGENT_GUIDE.md          # This file
```

## Quick Start for Agents

### 1. Understanding User Intent
When users ask for features, check:
- Is this already partially implemented? (check `TODO.md`)
- Does it involve the CLI or web app?
- Does it require database schema changes?

### 2. Making Changes

**IMPORTANT: Use Feature Branches for New Development**

Always create a new branch for feature development:

```bash
# 1. Create and checkout a feature branch
git checkout -b feature/descriptive-name

# Examples:
# git checkout -b feature/kosher-filtering
# git checkout -b fix/midnight-cooking-bug
# git checkout -b docs/update-readme
```

Standard workflow:
1. **Create feature branch** from main
2. Load and explore relevant code files
3. Check `CHANGELOG.txt` for historical context
4. Make focused, incremental commits
5. Test with `--mock` flag and/or pytest
6. Update `TODO.md` if completing tasks
7. Update `CHANGELOG.txt` with changes
8. **Commit with descriptive messages**
9. **Push branch and create Pull Request**
10. **After merge, delete the feature branch**

### 3. Git Workflow Details

#### Branch Naming Conventions

Use descriptive, kebab-case branch names with prefixes:

- `feature/` - New features (e.g., `feature/diet-filtering`)
- `fix/` - Bug fixes (e.g., `fix/midnight-cooking-logic`)
- `refactor/` - Code refactoring (e.g., `refactor/extract-filters`)
- `docs/` - Documentation only (e.g., `docs/add-api-guide`)
- `test/` - Test additions (e.g., `test/add-filter-tests`)

#### Commit Message Guidelines

Write clear, descriptive commit messages:

```bash
# Good commit messages:
git commit -m "Add kosher filtering with parve/milchik/fleisch support"
git commit -m "Fix midnight cooking bug in is_too_late_to_cook()"
git commit -m "Add comprehensive test suite with 39 tests"

# Include details in multi-line commits:
git commit -m "Implement diet filtering system

- Added DietType enum (vegan, vegetarian, glutenfree, keto)
- Created filter_diet() function with graceful fallback
- Wired up --diet CLI option
- Added 6 tests for diet filtering
All tests passing"
```

#### Pull Request Workflow

After completing work on a feature branch:

```bash
# 1. Ensure all tests pass
pytest tests/ -v

# 2. Commit all changes
git add .
git commit -m "Descriptive message"

# 3. Push feature branch to remote
git push -u origin feature/your-feature-name

# 4. Create Pull Request on GitHub
# - Add descriptive title and description
# - Reference any related issues
# - Request review if needed

# 5. After PR is merged, delete the branch
git checkout main
git pull origin main
git branch -d feature/your-feature-name        # Delete local
git push origin --delete feature/your-feature-name  # Delete remote
```

#### Clean Up Old Branches

Periodically clean up merged branches:

```bash
# List all branches
git branch -a

# Delete local branches that are merged
git branch --merged main | grep -v "^\* main" | xargs -n 1 git branch -d

# Prune remote-tracking branches
git fetch --prune

# Delete specific remote branch
git push origin --delete feature/old-branch-name
```

#### Emergency Hotfixes

For critical bugs in production:

```bash
# Create hotfix branch from main
git checkout main
git checkout -b hotfix/critical-bug-description

# Make fix and test
# ... edits ...
pytest tests/

# Fast-track merge
git checkout main
git merge hotfix/critical-bug-description
git push origin main

# Clean up
git branch -d hotfix/critical-bug-description
```

### 4. Common Tasks

**Adding a new meal attribute**:
1. Add column to `data/meal_list.csv`
2. Update `meal_questions()` in `scripts/iodata.py`
3. Update `METADATA.md` documentation

**Adding CLI filtering**:
1. Add parameter to `main()` in `main.py`
2. Add filtering logic to `choose_random()` in `scripts/auxillary.py`
3. Update README with new flag

**Adding web app feature**:
1. Modify `streamlit_app.py` or add page to `pages/`
2. Test locally with `streamlit run streamlit_app.py`

## Contact & Contribution

- **Author**: [@avishai231](https://twitter.com/avishai231)
- **Repository**: AvishaiBarnoy/DeepCook
- **Contribution Style**: Informal, practical, PR-friendly
- **Documentation**: Update `CHANGELOG.txt` and `TODO.md` with changes

---

**Last Updated**: 2026-02-16  
**Guide Version**: 2.0


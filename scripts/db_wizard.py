import pandas as pd
from pathlib import Path
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.iodata import maintenance_wizard

def main():
    DATA_DIR = Path(__file__).parent.parent / "data"
    MEAL_LIST = DATA_DIR / "meal_list.csv"
    
    if not MEAL_LIST.exists():
        print(f"Error: {MEAL_LIST} not found.")
        return

    print("Loading database...")
    df = pd.read_csv(MEAL_LIST, index_col=0)
    
    # Run the wizard
    maintenance_wizard(df, file_path=MEAL_LIST)
    
    print("\nWizard finished. Goodbye!")

if __name__ == "__main__":
    main()

import streamlit as st
from pathlib import Path

st.title("ℹ️ About DeepCook")

st.markdown("""
## What is DeepCook?

DeepCook is a meal suggestion engine designed to help you decide what to 
cook for dinner. No more endless browsing or decision fatigue!

### Features

- 🎲 **Random Meal Suggestions** - Get instant meal ideas
- 🔍 **Smart Filtering** - Filter by kosher type, diet, and more
- 📊 **Personal Database** - Track your favorite meals
- 🕒 **Time-Aware** - Suggests quick meals when it's late
- 🆕 **Recently-Made Filter** - Avoid repeating recent meals

### How It Works

1. **Maintain your meal database** - Add meals you like to cook
2. **Set your preferences** - Choose filters (kosher, diet, etc.)
3. **Get suggestions** - Click the button and get a random meal
4. **Track history** - See what you've made and when

###Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python, Pandas
- **Images**: Pexels API
- **Testing**: pytest (39 tests)

### Project Info

- **Author**: Avishai Barnoy
- **GitHub**: [AvishaiBarnoy/DeepCook](https://github.com/AvishaiBarnoy/DeepCook)
- **License**: MIT
- **Version**: 2.0

### Credits

- Food photography from [Pexels](https://www.pexels.com/)
- Built with [Streamlit](https://streamlit.io/)
- Inspired by the eternal question: "What's for dinner?"

---

Made with ❤️ by someone who loves cooking but hates deciding
""")

# Optional: Add usage statistics
if st.checkbox("Show Usage Statistics"):
    counter_file = Path(__file__).parent.parent / "data/counter.txt"
    try:
        with open(counter_file, "r") as f:
            counter = f.readline()
            counter = 0 if counter == "" else int(counter)
        
        st.metric("Total Button Clicks", counter)
        st.caption("Number of times the random meal button has been clicked")
    except FileNotFoundError:
        st.info("Counter file not found")

import streamlit as st
from pathlib import Path

# Language State
if 'lang' not in st.session_state:
    st.session_state.lang = 'EN'
l = st.session_state.lang

TRANS = {
    'title': {'EN': "ℹ️ About DeepCook", 'HE': "ℹ️ אודות DeepCook"},
    'what_is': {'EN': "What is DeepCook?", 'HE': "מה זה DeepCook?"},
    'description': {
        'EN': "DeepCook is a meal suggestion engine designed to help you decide what to cook for dinner. No more endless browsing or decision fatigue!",
        'HE': "DeepCook הוא מנוע הצעות לארוחות שנועד לעזור לכם להחליט מה לבשל לארוחת ערב. לא עוד גלישה אינסופית או עייפות מהחלטות!"
    },
    'features': {'EN': "Features", 'HE': "תכונות"},
    'f1': {'EN': "🎲 **Random Meal Suggestions** - Get instant meal ideas", 'HE': "🎲 **הצעות ארוחה אקראיות** - קבלו רעיונות מיידיים"},
    'f2': {'EN': "🔍 **Smart Filtering** - Filter by kosher type, diet, and more", 'HE': "🔍 **סינון חכם** - סינון לפי כשרות, דיאטה ועוד"},
    'f3': {'EN': "📊 **Personal Database** - Track your favorite meals", 'HE': "📊 **מאגר אישי** - מעקב אחר הארוחות האהובות עליכם"},
    'f4': {'EN': "🕒 **Time-Aware** - Suggests quick meals when it's late", 'HE': "🕒 **מודע לזמן** - מציע ארוחות מהירות כשמאוחר"},
    'f5': {'EN': "🆕 **Recently-Made Filter** - Avoid repeating recent meals", 'HE': "🆕 **סינון ארוחות אחרונות** - הימנעו מחזרה על ארוחות מהזמן האחרון"},
    'how_it_works': {'EN': "How It Works", 'HE': "איך זה עובד"},
    'step1': {'EN': "1. **Maintain your meal database** - Add meals you like to cook", 'HE': "1. **תחזקו את המאגר** - הוסיפו ארוחות שאתם אוהבים לבשל"},
    'step2': {'EN': "2. **Set your preferences** - Choose filters (kosher, diet, etc.)", 'HE': "2. **הגדירו העדפות** - בחרו מסננים (כשרות, דיאטה וכו')"},
    'step3': {'EN': "3. **Get suggestions** - Click the button and get a random meal", 'HE': "3. **קבלו הצעות** - לחצו על הכפתור וקבלו ארוחה אקראית"},
    'step4': {'EN': "4. **Track history** - See what you've made and when", 'HE': "4. **עקבו אחר ההיסטוריה** - ראו מה הכנתם ומתי"},
    'tech_stack': {'EN': "Technology Stack", 'HE': "טכנולוגיות"},
    'project_info': {'EN': "Project Info", 'HE': "מידע על הפרויקט"},
    'author': {'EN': "Author", 'HE': "מחבר"},
    'credits': {'EN': "Credits", 'HE': "קרדיטים"},
    'made_with': {'EN': "Made with ❤️ by someone who loves cooking but hates deciding", 'HE': "נוצר באהבה ❤️ על ידי מישהו שאוהב לבשל אבל שונא להחליט"},
    'show_stats': {'EN': "Show Usage Statistics", 'HE': "הצג סטטיסטיקות שימוש"},
    'total_clicks': {'EN': "Total Button Clicks", 'HE': "סה''כ לחיצות על הכפתור"},
    'counter_desc': {'EN': "Number of times the random meal button has been clicked", 'HE': "מספר הפעמים שלחצו על כפתור הארוחה האקראית"},
    'no_counter': {'EN': "Counter file not found", 'HE': "קובץ המונה לא נמצא"}
}

st.title(TRANS['title'][l])

st.markdown(f"""
## {TRANS['what_is'][l]}

{TRANS['description'][l]}

### {TRANS['features'][l]}

- {TRANS['f1'][l]}
- {TRANS['f2'][l]}
- {TRANS['f3'][l]}
- {TRANS['f4'][l]}
- {TRANS['f5'][l]}

### {TRANS['how_it_works'][l]}

{TRANS['step1'][l]}
{TRANS['step2'][l]}
{TRANS['step3'][l]}
{TRANS['step4'][l]}

### {TRANS['tech_stack'][l]}

- **Frontend**: Streamlit
- **Backend**: Python, Pandas
- **Images**: Pexels API
- **Testing**: pytest (41 tests)

### {TRANS['project_info'][l]}

- **{TRANS['author'][l]}**: Avishai Barnoy
- **GitHub**: [AvishaiBarnoy/DeepCook](https://github.com/AvishaiBarnoy/DeepCook)
- **License**: MIT
- **Version**: 2.1

### {TRANS['credits'][l]}

- Food photography from [Pexels](https://www.pexels.com/)
- Built with [Streamlit](https://streamlit.io/)
- Inspired by the eternal question: "What's for dinner?"

---

{TRANS['made_with'][l]}
""")

# Optional: Add usage statistics
if st.checkbox(TRANS['show_stats'][l]):
    counter_file = Path(__file__).parent.parent / "data/counter.txt"
    try:
        with open(counter_file, "r") as f:
            counter = f.readline()
            counter = 0 if counter == "" else int(counter)
        
        st.metric(TRANS['total_clicks'][l], counter)
        st.caption(TRANS['counter_desc'][l])
    except FileNotFoundError:
        st.info(TRANS['no_counter'][l])

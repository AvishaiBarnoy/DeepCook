import streamlit as st
from pexels_api import API
import sys

# Try to mock st.secrets for a standalone test if needed, 
# but I'll try to run it in a way that access secrets if possible, 
# or just use the string directly for a quick test.

api_key = "IImtt4ExDm421E2kBzDTwhPf4ecrSvgXkQxEVaewU8jj9BlXemJM5ZeX"
api = API(api_key)
prompt = "Pasta"
api.search(prompt, page=1, results_per_page=1)
photos = api.get_entries()

print(f"Photos found: {len(photos)}")
for photo in photos:
    print(f"URL: {photo.medium}")
    print(f"Photographer: {photo.photographer}")

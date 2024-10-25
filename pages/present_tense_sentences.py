import streamlit as st

from display_page import display_sentences_page
from conf_data import page_conf

page_data = page_conf['present_tense_sentences']
display_sentences_page(page_data)

st.markdown('''
### Grammar Notes
"**Tu es**" is for informal or familiar situations, used with friends, family, or people of similar age.

"**Vous êtes**" can be formal (for one person you don't know well or in professional contexts) or plural.

"**On est**" is an informal way to say "**We are**" and is commonly used in spoken French instead of "**Nous sommes**."
''')

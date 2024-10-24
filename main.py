import streamlit as st
from conf_data import page_conf

## Display the main page
st.set_page_config(page_title="French Direct", page_icon="./img/french_direct_icon.png")

st.logo(
    "img/french_direct_logo.png",
    icon_image="img/french_direct_icon.png",
    size='large'
)

pages = [
    st.Page('pages/basic_dialogs.py', title=page_conf['basic_dialogs']['title']),
    st.Page('pages/in_restaurant.py', title=page_conf['in_restaurant']['title']),
    st.Page('pages/fussy_client.py', title=page_conf['fussy_client']['title']),
    st.Page('pages/calendar_numbers.py', title=page_conf['cal_nums']['title']),
]

pg = st.navigation(pages)
pg.run()

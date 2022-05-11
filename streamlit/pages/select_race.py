import streamlit as st
import time
import base64
from datetime import timedelta
import pandas as pd 
import numpy as np
import qrcode
from PIL import Image
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

from  .session import fetch_post, fetch_put, fetch_get
from .singletons import settings, logger

def app():

    if st.button("Back to Main Menue"):
        st.session_state.nextpage = "main_page"
        st.experimental_rerun()

    game_id = None


    if 'game_id' not in st.session_state:
        with st.form("my_form"):
            result = fetch_post(f"{settings.driftapi_path}/manage_game/find/", {})
            if result:
                result = [r["game_id"] for r in result if ("game_id" in r.keys())]
                game_id = st.selectbox(label="Choose Game", options=result)
                if st.form_submit_button("Show"):
                    st.session_state.game_id = game_id
                    st.session_state.nextpage = "racedisplay"
                    st.experimental_rerun()
    else:
        st.session_state.nextpage = "racedisplay"
        st.experimental_rerun()
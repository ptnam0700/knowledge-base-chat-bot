#!/usr/bin/env python3
"""
Main entry point for ROAD TO 8M Streamlit multi-page application.
"""

import streamlit as st
from src.interface.utils.prompt_text import t
from src.utils.settings_manager import get_settings

def _get_lang() -> str:
    try:
        import streamlit as st  # local import to avoid issues when not running in Streamlit
        lang = st.session_state.get('language')
        if not lang and 'app_settings' in st.session_state:
            lang = (st.session_state.app_settings or {}).get('language')
        if not lang:
            lang = get_settings().get('language', 'vi')
        st.session_state['language'] = lang
        return lang
    except Exception:
        return 'vi'


def main():
    st.set_page_config(
        page_title="ROAD TO 8M Notebooks",
        page_icon="📓",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    lang = _get_lang()
    st.title(t("app_home_title", lang))
    st.markdown(t("app_home_welcome", lang))
    
    with st.expander(t("expander_app_intro", lang), expanded=True):
        # Features table
        cols = st.columns([2, 4, 4])
        with cols[0]:
            st.markdown(f"**{t('features_table_header_feature', lang)}**")
        with cols[1]:
            st.markdown(f"**{t('features_table_header_desc', lang)}**")
        with cols[2]:
            st.markdown(f"**{t('features_table_header_tech', lang)}**")

        rows = [
            ("feat_notebooks", "feat_notebooks_desc"),
            ("feat_filter_sort", "feat_filter_sort_desc"),
            ("feat_ingest", "feat_ingest_desc"),
            ("feat_youtube", "feat_youtube_desc"),
            ("feat_chunk_search", "feat_chunk_search_desc"),
            ("feat_mindmap", "feat_mindmap_desc"),
            ("feat_i18n", "feat_i18n_desc"),
            ("feat_settings", "feat_settings_desc"),
        ]
        for key_feat, key_desc in rows:
            c1, c2, c3 = st.columns([2, 4, 4])
            c1.write(t(key_feat, lang))
            c2.write(t(key_desc, lang))
            c3.write(t("feat_tech_stack", lang))

        st.markdown("---")

if __name__ == "__main__":
    main()

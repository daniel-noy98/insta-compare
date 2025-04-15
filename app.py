
import streamlit as st
from bs4 import BeautifulSoup
import pandas as pd
import re

st.set_page_config(page_title="ניתוח עוקבים", layout="centered")

# Custom CSS styling
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@400;700&display=swap');
        body, .stApp {
            font-family: 'Assistant', sans-serif;
            color: black;
            text-align: center;
        }
        .title {
            font-size: 16pt;
            font-weight: bold;
            text-decoration: underline;
            margin-bottom: 20px;
        }
        section[data-testid="stFileUploader"] {
            background-color: #fde4ec;
            border: 1px solid #f5c8d4;
            padding: 12px;
            border-radius: 10px;
            font-weight: bold;
            color: black;
        }
        section[data-testid="stFileUploader"] label {
            color: black !important;
        }
        thead tr th {
            background-color: #fde4ec !important;
            color: black;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">ניתוח עוקבים</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    followers_file = st.file_uploader("העלאת קובץ followers_1", type="html")
with col2:
    following_file = st.file_uploader("העלאת קובץ following", type="html")

def extract_usernames(html_file):
    soup = BeautifulSoup(html_file, "html.parser")
    links = soup.find_all("a", href=True)
    usernames = []
    for link in links:
        match = re.match(r"^https://www.instagram.com/([^/]+)/$", link["href"])
        if match:
            usernames.append(match.group(1))
        else:
            usernames.append(link.text.strip())
    return sorted(list(set(usernames)))

if followers_file and following_file:
    followers = extract_usernames(followers_file)
    following = extract_usernames(following_file)

    followers_set = set(followers)
    following_set = set(following)

    mutual = sorted(followers_set & following_set)
    you_only = sorted(following_set - followers_set)
    they_only = sorted(followers_set - following_set)

    max_len = max(len(mutual), len(you_only), len(they_only))
    df = pd.DataFrame({
        "עוקבים הדדיים": mutual + [""] * (max_len - len(mutual)),
        "במעקב על ידך בלבד": you_only + [""] * (max_len - len(you_only)),
        "במעקב על ידם בלבד": they_only + [""] * (max_len - len(they_only)),
    })

    st.markdown("---")
    st.dataframe(df, use_container_width=True, height=400)

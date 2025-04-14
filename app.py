
import streamlit as st
from bs4 import BeautifulSoup
import re

st.set_page_config(page_title="השוואת עוקבים באינסטגרם", layout="centered")
st.title("📊 השוואת עוקבים ונעקבים מהורדת HTML של אינסטגרם")

st.markdown("העלאת קבצי `followers_1.html` ו־`following.html` כפי שהורדו מאינסטגרם")

followers_file = st.file_uploader("העלה את הקובץ followers_1.html", type="html")
following_file = st.file_uploader("העלה את הקובץ following.html", type="html")

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
    return list(set(usernames))

if followers_file and following_file:
    with st.spinner("מנתח את הנתונים..."):
        followers = extract_usernames(followers_file)
        following = extract_usernames(following_file)

        followers_set = set(followers)
        following_set = set(following)

        not_following_back = following_set - followers_set
        fans = followers_set - following_set
        mutual = followers_set & following_set

        st.success("✅ הניתוח הושלם!")

        st.subheader("👥 עוקבים הדדיים:")
        st.write(sorted(mutual))

        st.subheader("🚫 את עוקבת – הם לא עוקבים חזרה:")
        st.write(sorted(not_following_back))

        st.subheader("🙋‍♀️ הם עוקבים – ואת לא:")
        st.write(sorted(fans))

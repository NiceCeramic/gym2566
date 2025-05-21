import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import plotly.express as px

# Firebase 인증
cred = credentials.Certificate('path/to/your/serviceAccountKey.json')
firebase_admin.initialize_app(cred)

# Firestore 데이터베이스 참조
db = firestore.client()

# 데이터를 읽어오는 함수
def fetch_data():
    docs = db.collection('your_collection_name').stream()
    data = []
    for doc in docs:
        data.append(doc.to_dict())
    return data

# Streamlit 앱에 표시
st.title("Firebase 데이터")
st.write("Firestore에서 데이터를 가져옵니다.")

data = fetch_data()

# Pandas DataFrame으로 변환
df = pd.DataFrame(data)

# 예시로 'value'라는 열을 기준으로 막대 그래프를 그려봄
fig = px.bar(df, x='name', y='value', title="Value별 그래프")
st.plotly_chart(fig)

# 데이터 입력 폼
st.title("데이터 추가하기")
name = st.text_input("이름")
value = st.number_input("값", min_value=0)

if st.button("데이터 저장"):
    # Firestore에 새로운 데이터 추가
    db.collection('your_collection_name').add({
        'name': name,
        'value': value
    })
    st.success("데이터가 성공적으로 저장되었습니다!")

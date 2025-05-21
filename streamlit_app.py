import streamlit as st
import datetime

st.set_page_config(page_title="운동 친구", layout="wide")

st.title("🏃‍♂️ 운동 친구")
st.caption("턱걸이 & 매달리기 기록하고, 목표를 달성하세요!")

# -------------------------------
# 운동 기록 저장용 세션 상태 초기화
# -------------------------------
if "records" not in st.session_state:
    st.session_state.records = []

# -------------------------------
# 사용자 별 집계
# -------------------------------
from collections import defaultdict

user_summary = defaultdict(lambda: {"days": set(), "pullup": 0})
for r in st.session_state.records:
    user_summary[r["name"]]["days"].add(r["date"])
    if r["type"] == "턱걸이":
        user_summary[r["name"]]["pullup"] += int(r["value"].replace("회", "").strip())

# -------------------------------
# 상단 배지
# -------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("⭐ 최고 성실맨 (지난 30일)")
    if user_summary:
        best_person = max(user_summary.items(), key=lambda x: len(x[1]["days"]))
        st.markdown(f"**{best_person[0]}**")
        st.caption(f"{len(best_person[1]['days'])}일 운동 기록")
    else:
        st.write("기록 없음")

with col2:
    st.subheader("🏅 최고 기록맨 (지난 30일)")
    if user_summary:
        best_pullup = max(user_summary.items(), key=lambda x: x[1]["pullup"])
        st.markdown(f"**{best_pullup[0]}**")
        st.caption(f"{best_pullup[1]['pullup']} 회 (턱걸이)")
    else:
        st.write("기록 없음")

st.markdown("---")

# -------------------------------
# 운동 기록 입력 폼
# -------------------------------
with st.expander("📋 운동 기록 입력", expanded=True):
    with st.form("entry_form"):
        name = st.selectbox("이름", ["Person 1", "Person 2", "Person 3"], index=1)
        exercise_type = st.selectbox("운동 종류", ["턱걸이", "매달리기"])
        date = st.date_input("날짜", datetime.date.today())
        value = st.text_input("기록", placeholder="예: 1회 또는 10초")

        submitted = st.form_submit_button("➕ 운동 추가")
        if submitted and name and value:
            st.session_state.records.append({
                "date": date.strftime("%b %d, %Y"),
                "name": name,
                "type": exercise_type,
                "value": value,
            })
            st.success("운동 기록이 추가되었습니다!")

st.markdown("---")

# -------------------------------
# 운동 내역 표시 및 삭제
# -------------------------------
st.subheader("📅 운동 내역")
if st.session_state.records:
    for i, record in enumerate(reversed(st.session_state.records)):
        cols = st.columns([2, 2, 2, 2, 1])
        cols[0].write(record["date"])
        cols[1].write(record["name"])
        cols[2].write(record["type"])
        cols[3].write(record["value"])
        if cols[4].button("🗑️", key=f"del_{i}"):
            index_to_delete = len(st.session_state.records) - 1 - i
            st.session_state.records.pop(index_to_delete)
            st.experimental_rerun()
else:
    st.write("기록이 없습니다.")



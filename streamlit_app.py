# app.py
import streamlit as st
import datetime
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="운동 친구", layout="wide")

# 세션 상태 초기화
if "records" not in st.session_state:
    st.session_state.records = []

# 사이드바 페이지 선택
page = st.sidebar.selectbox("페이지를 선택하세요", ["🏠 홈", "📊 운동 통계"])

# ---------------------------------------------------------------------
# 🏠 홈 페이지: 운동 기록 입력 및 내역 확인
# ---------------------------------------------------------------------
if page == "🏠 홈":
    st.title("🏃‍♂️ 운동 친구")
    st.caption("턱걸이 & 매달리기 기록하고, 목표를 달성하세요!")

    # 운동 기록 입력 폼
    with st.expander("📋 운동 기록 입력", expanded=True):
        with st.form("entry_form"):
            name = st.selectbox("이름", ["Person 1", "Person 2", "Person 3"], index=1)
            exercise_type = st.selectbox("운동 종류", ["턱걸이", "매달리기"])
            date = st.date_input("날짜", datetime.date.today())
            value = st.text_input("기록", placeholder="예: 1회 또는 10초")

            submitted = st.form_submit_button("➕ 운동 추가")
            if submitted and name and value:
                st.session_state.records.append({
                    "date": date.strftime("%Y-%m-%d"),
                    "name": name,
                    "type": exercise_type,
                    "value": value,
                })
                st.success("운동 기록이 추가되었습니다!")

    st.markdown("---")
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

# ---------------------------------------------------------------------
# 📊 운동 통계 페이지: 날짜별 집계 그래프
# ---------------------------------------------------------------------
elif page == "📊 운동 통계":
    st.title("📈 운동 통계")
    st.caption("사용자들의 운동 데이터를 날짜별로 시각화합니다.")

    if not st.session_state.records:
        st.warning("운동 기록이 없습니다.")
    else:
        # 데이터프레임 변환
        df = pd.DataFrame(st.session_state.records)
        df["date"] = pd.to_datetime(df["date"])

        # 턱걸이
        df_pullup = df[df["type"] == "턱걸이"].copy()
        df_pullup["reps"] = df_pullup["value"].str.extract("(\d+)").astype(float)
        pullup_sum = df_pullup.groupby("date")["reps"].sum().reset_index()

        # 매달리기
        df_hang = df[df["type"] == "매달리기"].copy()
        df_hang["seconds"] = df_hang["value"].str.extract("(\d+)").astype(float)
        hang_sum = df_hang.groupby("date")["seconds"].sum().reset_index()

        # 시각화
        if not pullup_sum.empty:
            st.subheader("Pull-up Progress (All Users)")
            fig1 = px.line(pullup_sum, x="date", y="reps", markers=True, labels={"reps": "Reps"})
            st.plotly_chart(fig1, use_container_width=True)

        if not hang_sum.empty:
            st.subheader("Hang Progress (All Users)")
            fig2 = px.line(hang_sum, x="date", y="seconds", markers=True, labels={"seconds": "Duration (s)"})
            st.plotly_chart(fig2, use_container_width=True)



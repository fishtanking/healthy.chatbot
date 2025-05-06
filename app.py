import streamlit as st
import time

# 페이지 설정
st.set_page_config(page_title="튼튼이 건강 상담 챗봇", page_icon="🩺")

# 챗봇 이름 및 아이콘
chatbot_name = "튼튼이"
chatbot_icon = "🩺"

# CSS로 꾸미기
st.markdown("""
    <style>
    .chat-message {
        padding: 1rem;
        margin-bottom: 1rem;
        border-radius: 10px;
        max-width: 80%;
    }
    .user {
        background-color: #DCF8C6;
        align-self: flex-end;
        margin-left: auto;
    }
    .bot {
        background-color: #F1F0F0;
        align-self: flex-start;
        margin-right: auto;
    }
    .chat-container {
        display: flex;
        flex-direction: column;
    }
    .icon {
        font-weight: bold;
        margin-right: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# 제목
st.title("🩺 튼튼이 건강 상담 챗봇")
st.caption("GPT 없이 작동하는 로컬 시뮬레이션 챗봇입니다.")

# 사용자 정보 입력
with st.sidebar:
    st.header("👤 사용자 정보")
    name = st.text_input("이름")
    age = st.number_input("나이", min_value=1, max_value=120, step=1)
    height = st.number_input("키 (cm)", min_value=100, max_value=220)
    weight = st.number_input("몸무게 (kg)", min_value=30, max_value=200)
    if height > 0:
        bmi = round(weight / ((height / 100) ** 2), 2)
    else:
        bmi = None

# 대화 흐름
st.subheader("💬 상담 시작")

if name and age and bmi:
    st.success(f"{name}님의 BMI는 {bmi}입니다.")

    question = st.selectbox(
        "상담을 원하는 건강 항목을 선택하세요:",
        ["수면", "영양", "운동", "정신건강", "BMI 관련 조언"]
    )

    if st.button("상담하기"):
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        st.markdown(
            f'<div class="chat-message user"><span class="icon">🙋‍♂️</span>{question}에 대해 알고 싶어요.</div>',
            unsafe_allow_html=True,
        )
        time.sleep(0.7)

        response = {
            "수면": "수면은 하루 평균 7~8시간이 권장되며, 일정한 수면 패턴이 건강에 매우 중요합니다.",
            "영양": "균형 잡힌 식사는 탄수화물, 단백질, 지방, 비타민, 무기질의 적절한 섭취가 포함되어야 합니다.",
            "운동": "일주일에 최소 150분의 유산소 운동과 주 2회의 근력 운동이 필요합니다.",
            "정신건강": "스트레스를 관리하고 충분한 휴식을 취하는 것은 정신건강을 유지하는 핵심 요소입니다.",
            "BMI 관련 조언": f"현재 BMI는 {bmi}이며, 정상 범위(18.5~24.9)에 비해 {'낮습니다' if bmi < 18.5 else '높습니다' if bmi >= 25 else '정상입니다'}. 체중 조절을 고려해보세요."
        }

        st.markdown(
            f'<div class="chat-message bot"><span class="icon">{chatbot_icon}</span>{response[question]}</div>',
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.warning("👈 왼쪽에서 사용자 정보를 먼저 입력해주세요.")

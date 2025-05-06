import streamlit as st
import time

st.set_page_config(page_title="튼튼이 건강 상담 챗봇", page_icon="🩺")

# 챗봇 이름 및 말풍선 CSS
chatbot_name = "튼튼이"
chatbot_icon = "🩺"

st.markdown("""
    <style>
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        margin-bottom: 1rem;
    }
    .chat-message {
        padding: 0.75rem 1rem;
        border-radius: 18px;
        max-width: 80%;
        width: fit-content;
        font-size: 0.95rem;
        line-height: 1.4;
        box-shadow: 1px 1px 4px rgba(0,0,0,0.1);
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
    .icon {
        font-weight: bold;
        margin-right: 6px;
    }
    .question-button {
        display: inline-block;
        padding: 0.3rem 0.7rem;
        margin: 0.2rem;
        background-color: #e1e1f0;
        border-radius: 12px;
        font-size: 0.88rem;
        cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)

# 질문 항목과 질문-답변 쌍 정의
questions_db = {
    "정신건강": {
        "스트레스를 줄이는 방법은?": "스트레스를 줄이기 위해 규칙적인 생활, 충분한 수면, 가벼운 운동, 그리고 취미 활동을 추천합니다.",
        "불안감이 심할 때 어떻게 해야 하나요?": "호흡 조절, 명상, 주변 사람과의 대화, 상담센터 활용 등이 도움이 됩니다.",
        "우울한 감정이 자주 드는데 어떻게 할까요?": "감정을 억누르지 말고 표현하고, 필요 시 정신건강 전문기관 상담을 권장합니다.",
        "공부나 일이 손에 잡히지 않을 땐?": "뇌 휴식을 위한 산책, 운동, 잠깐의 전환 활동을 추천합니다.",
        "마음이 지칠 때 쉴 수 있는 방법은?": "자연 속 산책, 디지털 디톡스, 따뜻한 차 한 잔 등이 효과적입니다.",
        "명상이나 호흡 훈련이 정말 효과가 있나요?": "네, 과학적으로 입증된 스트레스 완화 방법 중 하나입니다.",
        "상담센터는 누구나 이용할 수 있나요?": "네, 대부분의 상담센터는 지역 주민 또는 학생 누구나 무료로 이용할 수 있습니다.",
        "가끔씩 아무 이유 없이 불안해지는데 괜찮을까요?": "자주 반복된다면 전문가와의 상담을 권장합니다."
    }
}

# 사용자 정보
st.sidebar.title("👤 사용자 정보")
name = st.sidebar.text_input("이름")
age = st.sidebar.number_input("나이", min_value=1, max_value=100, step=1)

if name and age:
    st.title("🩺 튼튼이 건강 상담 챗봇")
    st.caption("마음이 힘들 땐 언제든지 튼튼이를 찾아주세요.")

    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="chat-message bot"><span class="icon">{chatbot_icon}</span>{name}님, 정신건강 관련하여 아래 질문 중 궁금한 점을 선택해주세요.</div>',
        unsafe_allow_html=True,
    )

    # 질문 리스트 버튼
    selected_question = st.radio("💬 아래 중 하나를 골라주세요:", list(questions_db["정신건강"].keys()))

    if st.button("질문하기"):
        st.markdown(
            f'<div class="chat-message user"><span class="icon">🙋‍♂️</span>{selected_question}</div>',
            unsafe_allow_html=True,
        )
        time.sleep(0.6)
        st.markdown(
            f'<div class="chat-message bot"><span class="icon">{chatbot_icon}</span>{questions_db["정신건강"][selected_question]}</div>',
            unsafe_allow_html=True,
        )

        # 추가 질문 유도
        time.sleep(0.5)
        st.markdown(
            f'<div class="chat-message bot"><span class="icon">{chatbot_icon}</span>혹시 더 궁금한 것이 있나요? 다른 질문도 선택해보세요!</div>',
            unsafe_allow_html=True,
        )

    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.warning("👈 먼저 왼쪽 사이드바에서 사용자 정보를 입력해주세요.")
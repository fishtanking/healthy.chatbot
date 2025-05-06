
import streamlit as st
import time

# 기본 설정
st.set_page_config(page_title="튼튼이 건강 상담 챗봇", page_icon="🩺")

# 챗봇 이름 및 스타일
chatbot_icon = "🩺"
chatbot_name = "튼튼이"

# CSS 스타일 삽입
st.markdown("""
<style>
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 1.2rem;
    margin-bottom: 1rem;
}
.chat-message {
    padding: 0.9rem 1.2rem;
    border-radius: 18px;
    max-width: 80%;
    width: fit-content;
    font-size: 0.96rem;
    line-height: 1.5;
    box-shadow: 1px 1px 5px rgba(0,0,0,0.1);
    animation: fadeIn 0.4s ease-in;
}
@keyframes fadeIn {
    0% { opacity: 0; transform: translateY(10px); }
    100% { opacity: 1; transform: translateY(0); }
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
</style>
""", unsafe_allow_html=True)

# 단계 흐름 상태 관리
def init_state():
    if 'step' not in st.session_state:
        st.session_state.step = 'info'
    if 'user_info' not in st.session_state:
        st.session_state.user_info = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

init_state()

# 1단계: 사용자 정보 입력
if st.session_state.step == 'info':
    st.title("👤 사용자 정보 입력")
    with st.form("info_form"):
        name = st.text_input("이름")
        age = st.number_input("나이", min_value=1, max_value=100)
        region = st.selectbox("소속 지역", ["서울", "경기", "부산", "대구", "인천", "기타"])
        height = st.number_input("키 (cm)", min_value=100, max_value=220)
        weight = st.number_input("몸무게 (kg)", min_value=30, max_value=200)
        submitted = st.form_submit_button("정보 등록")

    if submitted and name and height and weight:
        bmi = round(weight / ((height / 100) ** 2), 2)
        st.session_state.user_info = {
            "name": name, "age": age, "region": region,
            "height": height, "weight": weight, "bmi": bmi
        }
        st.success(f"✅ 정보가 등록되었습니다. BMI는 {bmi}입니다.")
        st.session_state.step = 'category'
        st.experimental_rerun()

# 2단계: 상담 분야 선택
elif st.session_state.step == 'category':
    st.title(f"🩺 {chatbot_name} 건강 상담 챗봇")
    st.caption(f"📍 지역: {st.session_state.user_info['region']} / BMI: {st.session_state.user_info['bmi']}")

    category = st.selectbox("💡 상담받고 싶은 분야를 선택하세요:", [
        "건강검진", "정신건강", "BMI", "영양", "운동", "예방접종", "지역복지"
    ])
    st.session_state.category = category
    if st.button("➡️ 질문 보기"):
        st.session_state.step = 'chat'
        st.experimental_rerun()

# 3단계: 질문 선택 및 대화
elif st.session_state.step == 'chat':
    user = st.session_state.user_info
    category = st.session_state.category

    question_db = {
        "건강검진": {
            "건강검진은 몇 년마다 받아야 하나요?": "성인은 2년에 한 번씩 국가 건강검진 대상입니다.",
            "검진 항목은 어떤 게 포함되나요?": "혈압, 혈액, 시력, 청력, 간 기능 등 기본 검사가 포함됩니다."
        },
        "정신건강": {
            "스트레스를 줄이는 방법은?": "충분한 수면, 운동, 명상 등이 스트레스 완화에 효과적입니다.",
            "불안감이 심할 때 어떻게 해야 하나요?": "호흡 조절, 친구와 대화, 상담센터 이용을 권장합니다."
        },
        "BMI": {
            "내 BMI가 정상인가요?": f"BMI {user['bmi']}는 {'정상 범위입니다.' if 18.5 <= user['bmi'] <= 24.9 else '정상 범위를 벗어났습니다.'}"
        },
        "영양": {
            "균형 잡힌 식단이란 무엇인가요?": "탄수화물, 단백질, 지방, 비타민, 무기질이 조화된 식단입니다.",
            "아침 식사가 중요한 이유는?": "에너지 공급과 뇌 활성화에 도움이 되기 때문입니다."
        },
        "운동": {
            "하루에 얼마만큼 운동해야 하나요?": "성인은 주 3~5회, 하루 30분 이상 운동이 권장됩니다.",
            "걷기 운동도 효과가 있나요?": "네, 꾸준한 걷기는 심혈관 건강에 매우 효과적입니다."
        },
        "예방접종": {
            "독감 예방접종은 언제 받아야 하나요?": "가을철, 보통 10~11월이 가장 적기입니다.",
            "청소년 예방접종 항목은 무엇이 있나요?": "일반적으로 A형간염, B형간염, HPV 백신이 포함됩니다."
        },
        "지역복지": {
            "복지관에서 받을 수 있는 건강 서비스는?": "건강 상담, 운동 프로그램, 예방 교육 등이 있습니다.",
            "노인 대상 프로그램은 어떤 것이 있나요?": "낙상 예방, 치매 예방, 건강 체조 등이 있습니다."
        }
    }

    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for msg in st.session_state.chat_history:
        who, content = msg
        role = "user" if who == "user" else "bot"
        icon = "🙋‍♂️" if who == "user" else chatbot_icon
        st.markdown(f'<div class="chat-message {role}"><span class="icon">{icon}</span>{content}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    question = st.radio("🤔 어떤 질문이 궁금한가요?", list(question_db[category].keys()))

    if st.button("🗨️ 질문하기"):
        st.session_state.chat_history.append(("user", question))
        answer = question_db[category][question]
        st.session_state.chat_history.append(("bot", answer))
        st.experimental_rerun()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔙 분야 선택으로 돌아가기"):
            st.session_state.step = 'category'
            st.experimental_rerun()
    with col2:
        if st.button("❌ 대화 종료하기"):
            st.session_state.chat_history.clear()
            st.session_state.step = 'info'
            st.session_state.user_info = None
            st.success("상담을 종료했습니다. 언제든 다시 찾아주세요!")
            st.experimental_rerun()

st.sidebar.markdown("""
### 🏛️ 튼튼이 추천 서비스
- 국가 건강검진 대상 확인
- 연령별 예방접종 확인
- 지역 복지관 건강 프로그램 안내
- 건강보험공단 민원 연결 안내
""")


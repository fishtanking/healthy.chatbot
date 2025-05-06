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

# 사용자 정보 세션 초기화
if 'user_info' not in st.session_state:
    st.session_state.user_info = None

# 사용자 정보 입력
if st.session_state.user_info is None:
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
        st.experimental_rerun()

# 사용자 정보 등록 후 챗봇 실행
if st.session_state.user_info:
    user = st.session_state.user_info
    st.title(f"🩺 {chatbot_name} 건강 상담 챗봇")
    st.caption(f"📍 지역: {user['region']} / BMI: {user['bmi']}")

    # 분야별 질문 정의
    question_db = {
        "건강검진": {
            "건강검진은 몇 년마다 받아야 하나요?": "성인은 2년에 한 번씩 국가 건강검진 대상입니다.",
            "검진 항목은 어떤 게 포함되나요?": "혈압, 혈액, 시력, 청력, 간 기능 등 기본 검사가 포함됩니다.",
            "청소년도 건강검진 대상인가요?": "청소년은 학교 건강검진 외 필요시 추가 검진이 가능합니다.",
            "검진받을 병원은 어디서 확인하나요?": "건강보험공단 홈페이지나 앱에서 확인 가능합니다.",
            "검진 전 주의사항은 무엇인가요?": "검진 전 8시간 금식 등 주의사항이 있습니다.",
            "직장인 건강검진도 국가 검진인가요?": "네, 직장가입자도 건강보험공단 검진 대상입니다.",
            "무료로 받을 수 있나요?": "일정 연령 및 직장가입자 등은 무료로 검진이 가능합니다.",
            "검진결과는 어디서 확인하나요?": "검진 병원 또는 건강iN 사이트에서 확인 가능합니다."
        },
        "정신건강": {
            "스트레스를 줄이는 방법은?": "충분한 수면, 운동, 명상 등이 스트레스 완화에 효과적입니다.",
            "불안감이 심할 때 어떻게 해야 하나요?": "호흡 조절, 친구와 대화, 상담센터 이용을 권장합니다.",
            "우울한 감정이 자주 드는데 어떻게 할까요?": "반복된다면 정신건강 전문가와 상담해보세요.",
            "공부나 일이 손에 잡히지 않을 땐?": "짧은 산책이나 잠깐의 전환 활동이 도움이 됩니다.",
            "마음이 지칠 때 쉴 수 있는 방법은?": "음악 듣기, 산책, 따뜻한 차 한 잔 추천합니다.",
            "명상이나 호흡 훈련이 정말 효과가 있나요?": "네, 많은 연구에서 과학적으로 입증됐습니다.",
            "상담센터는 누구나 이용할 수 있나요?": "지역 정신건강복지센터는 대부분 무료로 이용 가능합니다.",
            "가끔씩 아무 이유 없이 불안해지는데 괜찮을까요?": "자주 반복된다면 전문가 상담이 필요합니다."
        },
        "BMI": {
            "내 BMI가 정상인가요?": f"BMI {user['bmi']}는 {'정상 범위입니다.' if 18.5 <= user['bmi'] <= 24.9 else '정상 범위를 벗어났습니다.'}",
            "BMI 수치가 높으면 건강에 안 좋은가요?": "비만은 심혈관 질환, 당뇨 등과 관련 있습니다.",
            "체중 감량을 하려면 무엇부터 해야 하나요?": "식습관 조절과 운동 병행이 중요합니다.",
            "BMI만으로 비만 여부를 판단할 수 있나요?": "아니요. 체지방률, 복부둘레 등도 참고해야 합니다.",
            "청소년 BMI 기준은 어떻게 다른가요?": "성장 곡선을 기준으로 합니다.",
            "살을 빼면 BMI도 바로 줄어드나요?": "체중이 줄면 BMI도 줄어듭니다.",
            "정상 체중이어도 운동은 필요한가요?": "건강 유지를 위해 운동은 필수입니다.",
            "BMI가 낮아도 문제인가요?": "너무 낮으면 면역력 저하, 빈혈 위험이 있습니다."
        }
    }

    # 분야 선택
    category = st.selectbox("💡 상담받고 싶은 분야를 선택하세요:", list(question_db.keys()))
    question = st.radio("🤔 어떤 질문이 궁금한가요?", list(question_db[category].keys()))

    if st.button("🗨️ 질문하기"):
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        st.markdown(
            f'<div class="chat-message user"><span class="icon">🙋‍♂️</span>{question}</div>',
            unsafe_allow_html=True,
        )
        time.sleep(0.6)
        st.markdown(
            f'<div class="chat-message bot"><span class="icon">{chatbot_icon}</span>{question_db[category][question]}</div>',
            unsafe_allow_html=True,
        )
        time.sleep(0.5)
        again = st.radio("🔁 다른 질문이 있으신가요?", ["예, 다시 선택할게요", "아니요, 종료할게요"])
        if again == "예, 다시 선택할게요":
            st.experimental_rerun()
        else:
            st.success("상담을 종료했습니다. 언제든지 다시 찾아주세요!")
        st.markdown('</div>', unsafe_allow_html=True)

# 사이드바 기능 추천
st.sidebar.markdown("""
### 🏛️ 튼튼이 추천 서비스
- 국가 건강검진 대상 확인
- 연령별 예방접종 확인
- 지역 복지관 건강 프로그램 안내
- 건강보험공단 민원 연결 안내
""")

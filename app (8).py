import streamlit as st
import time

st.set_page_config(page_title="튼튼이 건강 상담 챗봇", page_icon="🩺")

# 사용자 정보 세션 관리
if 'user_info' not in st.session_state:
    st.session_state.user_info = None

# 챗봇 캐릭터 및 스타일
chatbot_name = "튼튼이"
chatbot_icon = "🩺"

# CSS 스타일
st.markdown("""
    <style>
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    .chat-message {
        padding: 0.75rem 1rem;
        border-radius: 18px;
        max-width: 80%;
        width: fit-content;
        font-size: 0.95rem;
        line-height: 1.5;
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
    </style>
""", unsafe_allow_html=True)

# 사용자 정보 입력
if st.session_state.user_info is None:
    with st.form("user_info_form"):
        st.title("👤 사용자 정보 등록")
        name = st.text_input("이름")
        age = st.number_input("나이", min_value=1, max_value=120)
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
            st.success("✅ 사용자 정보가 등록되었습니다. 상담을 시작합니다.")
            st.experimental_rerun()

# 사용자 정보 등록 후 챗봇 실행
if st.session_state.user_info:
    user = st.session_state.user_info
    st.title(f"🩺 {chatbot_name}와의 건강 상담")
    st.caption(f"📍 지역: {user['region']} | BMI: {user['bmi']}")

    # 분야별 질문 데이터
    question_categories = {
        "건강검진": {
            "건강검진은 몇 년마다 받아야 하나요?": "성인은 일반적으로 2년에 한 번 국가 건강검진 대상입니다.",
            "검진 항목은 어떤 게 포함되나요?": "기본검진, 혈압, 혈액, 시력, 청력, 구강검진 등이 포함됩니다.",
            "청소년도 건강검진 대상인가요?": "청소년은 학교 건강검진이 우선 시행되며 추가 검진은 별도입니다.",
            "검진받을 병원은 어디서 확인하나요?": "국민건강보험공단 홈페이지 또는 앱에서 확인할 수 있습니다.",
            "검진 전 주의사항은 무엇인가요?": "금식 여부, 약 복용 여부 등은 병원 안내를 꼭 따르세요.",
            "직장인 건강검진도 국가 검진인가요?": "네, 사업장 제공 검진도 국가에서 관리합니다.",
            "무료로 받을 수 있나요?": "국가 건강검진은 연령별, 직장가입자 등에 따라 무료 제공됩니다.",
            "검진결과는 어디서 확인하나요?": "병원 또는 건강검진 사이트에서 로그인 후 확인 가능합니다."
        },
        "정신건강": {
            "스트레스를 줄이는 방법은?": "규칙적인 수면, 운동, 명상 등이 도움이 됩니다.",
            "불안감이 심할 때 어떻게 해야 하나요?": "호흡 조절, 대화, 상담센터 이용을 권장합니다.",
            "우울한 감정이 자주 드는데 어떻게 할까요?": "전문가와의 상담을 권장합니다.",
            "공부나 일이 손에 잡히지 않을 땐?": "잠시 쉬는 시간과 환경 변화가 도움이 됩니다.",
            "마음이 지칠 때 쉴 수 있는 방법은?": "산책, 음악 듣기, 따뜻한 차 한 잔도 좋아요.",
            "명상이나 호흡 훈련이 정말 효과가 있나요?": "과학적으로도 효과가 입증된 방법입니다.",
            "상담센터는 누구나 이용할 수 있나요?": "대부분의 지역센터는 무료로 운영됩니다.",
            "가끔씩 아무 이유 없이 불안해지는데 괜찮을까요?": "반복되면 전문가 상담이 필요합니다."
        },
        "BMI": {
            "내 BMI가 정상인가요?": f"BMI {user['bmi']}은(는) {'정상 범위입니다.' if 18.5 <= user['bmi'] <= 24.9 else '정상 범위를 벗어났습니다.'}",
            "BMI 수치가 높으면 건강에 안 좋은가요?": "고혈압, 당뇨 등 만성질환과 연관이 있습니다.",
            "체중 감량을 하려면 무엇부터 해야 하나요?": "식습관 개선과 꾸준한 운동이 필요합니다.",
            "BMI만으로 비만 여부를 판단할 수 있나요?": "체지방률, 허리둘레 등 다른 지표도 함께 봐야 합니다.",
            "청소년 BMI 기준은 어떻게 다른가요?": "성장 곡선을 기준으로 평가합니다.",
            "살을 빼면 BMI도 바로 줄어드나요?": "체중이 줄면 BMI도 감소합니다.",
            "정상 체중이어도 운동은 필요한가요?": "물론입니다. 건강 유지를 위해 필요합니다.",
            "BMI가 낮아도 문제인가요?": "너무 낮은 경우도 빈혈, 면역력 저하 위험이 있습니다."
        }
    }

    category = st.selectbox("📚 상담 분야를 선택하세요:", list(question_categories.keys()))
    selected_question = st.radio("💬 아래 질문 중 궁금한 항목을 선택하세요:", list(question_categories[category].keys()))

    if st.button("🗨️ 튼튼이에게 물어보기"):
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        st.markdown(
            f'<div class="chat-message user"><span class="icon">🙋‍♀️</span>{selected_question}</div>',
            unsafe_allow_html=True,
        )
        time.sleep(0.7)
        st.markdown(
            f'<div class="chat-message bot"><span class="icon">{chatbot_icon}</span>{question_categories[category][selected_question]}</div>',
            unsafe_allow_html=True,
        )
        time.sleep(0.7)
        again = st.radio("🧐 다른 질문이 있으신가요?", ["네! 다른 질문 선택하기", "아니요, 종료할게요"])
        st.markdown('</div>', unsafe_allow_html=True)
        if again == "네! 다른 질문 선택하기":
            st.experimental_rerun()
        else:
            st.success("💡 상담을 종료했습니다. 언제든 다시 찾아주세요.")

# 사이드바 추천 기능
st.sidebar.markdown("""
### 📌 튼튼이 추천 기능
- 💉 국가 건강검진 시기 알림
- 🗓️ 연령별 필수 예방접종 확인
- 📍 지역 복지관 운동 프로그램 안내
- 📞 건강보험공단 민원 간편 연결
""")

import streamlit as st
import openai

# GPT 최신 클라이언트 사용
client = openai.OpenAI()
openai.api_key = "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"

st.set_page_config(page_title="튼튼이 건강 상담 챗봇", page_icon="🩺")

st.image("https://i.ibb.co/vdc34V9/character.png", width=80)
st.title("튼튼이 건강상담 챗봇")

# 사용자 정보 초기화
if "user_registered" not in st.session_state:
    st.session_state.user_registered = False
    st.session_state.user_info = {}

# 1단계: 사용자 정보 등록
if not st.session_state.user_registered:
    with st.form("user_info_form"):
        st.subheader("👤 먼저 사용자 정보를 입력해주세요")
        name = st.text_input("이름")
        age = st.number_input("나이", min_value=0, max_value=120, value=18)
        gender = st.selectbox("성별", ["남성", "여성", "기타"])
        height = st.number_input("키(cm)", min_value=100, max_value=250, value=170)
        weight = st.number_input("체중(kg)", min_value=20, max_value=200, value=60)
        region = st.selectbox("거주 지역", ["서울", "경기", "부산", "대구", "광주", "기타"])

        submitted = st.form_submit_button("등록하기")
        if submitted:
            st.session_state.user_info = {
                "name": name, "age": age, "gender": gender,
                "height": height, "weight": weight, "region": region
            }
            st.session_state.user_registered = True
            st.success(f"{name}님, 환영합니다! 아래에서 궁금한 항목을 선택해주세요.")

# 2단계: 기능 선택 및 실행
if st.session_state.user_registered:
    user = st.session_state.user_info

    st.sidebar.title("🗂️ 이용 가능한 기능")
    choice = st.sidebar.radio("궁금한 항목을 선택하세요", [
        "BMI 계산기", "국가 건강검진 안내", "예방접종 정보", "정신건강 지원 서비스", "학생 영양 식단", "기타 건강 상담"
    ])

    if choice == "BMI 계산기":
        st.subheader("🧮 BMI 계산기")
        height_m = user["height"] / 100
        bmi = round(user["weight"] / (height_m ** 2), 1)

        if bmi < 18.5:
            category = "저체중"
        elif 18.5 <= bmi < 23:
            category = "정상 체중"
        elif 23 <= bmi < 25:
            category = "과체중"
        else:
            category = "비만"

        st.success(f"{user['name']}님의 BMI는 **{bmi}**로, '{category}' 범주에 해당합니다.")

    else:
        st.subheader("💬 튼튼이 챗봇에게 물어보세요")

        if "chat_history" not in st.session_state:
            system_msg = f"""
            당신은 대한민국 보건복지부 산하 건강정책 상담 챗봇 '튼튼이'입니다.
            항상 공손하고 정확한 공공기관 말투를 사용하며, 사용자의 연령({user["age"]}세), 성별({user["gender"]}), 지역({user["region"]})을 고려해 
            건강검진, 예방접종, 정신건강, 영양 서비스, 민원 등과 관련된 정보를 전문적으로 안내합니다.
            필요시 정부기관 또는 건강보험공단, 보건소 등의 실명 기관을 언급하여 신뢰감을 줍니다.
            """
            st.session_state.chat_history = [{"role": "system", "content": system_msg}]

        user_input = st.text_input("궁금한 내용을 입력해주세요")

        if st.button("💬 상담하기") and user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.chat_history
            )
            reply = response.choices[0].message.content
            st.session_state.chat_history.append({"role": "assistant", "content": reply})

        for msg in st.session_state.chat_history[1:]:
            if msg["role"] == "user":
                st.markdown(f"**👤 {user['name']}**: {msg['content']}")
            else:
                col1, col2 = st.columns([1, 10])
                with col1:
                    st.image("https://i.ibb.co/vdc34V9/character.png", width=40)
                with col2:
                    st.markdown(f"**🩺 튼튼이**: {msg['content']}")

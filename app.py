
import streamlit as st
import openai

# API 키 (보안을 위해 배포 전에는 st.secrets["OPENAI_API_KEY"] 방식으로 전환할 것)
openai.api_key = "여기에_너의_API_키_입력"

st.set_page_config(page_title="튼튼이 건강 상담 챗봇", page_icon="🩺")
st.title("🩺 공공기관 건강상담 챗봇 - 튼튼이")

# 캐릭터 이미지 (임시 예시 URL)
st.image("https://i.ibb.co/vdc34V9/character.png", width=100)

# 사용자 정보 입력
with st.sidebar:
    st.header("👤 사용자 정보")
    user_name = st.text_input("이름", "홍길동")
    user_age = st.number_input("나이", min_value=0, max_value=120, value=18)
    user_region = st.selectbox("거주 지역", ["서울", "경기", "부산", "대구", "광주", "기타"])
    selected_topic = st.radio("궁금한 건강 분야를 선택하세요", ["건강검진", "예방접종", "정신건강지원", "운동 및 영양", "기타"])

# 기본 시스템 역할 설명
system_prompt = f"""
당신은 대한민국의 건강정책을 안내하는 공공기관 건강상담 챗봇 '튼튼이'입니다.
항상 공손하고 친절하게 답하며, 사용자의 연령({user_age}세), 지역({user_region}) 정보를 고려해 
국가 건강검진, 예방접종, 정신건강 복지, 운동·영양 서비스 등을 안내해 주세요.
정확한 진단은 의료 전문가에게 받도록 부드럽게 안내합니다.
"""

# 대화 히스토리 초기화
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "system", "content": system_prompt}]

# 질문 예시
faq_examples = {
    "건강검진": "제가 받을 수 있는 건강검진에는 어떤 것이 있나요?",
    "예방접종": "요즘 맞아야 할 예방접종이 있을까요?",
    "정신건강지원": "청소년 정신건강 상담은 어디서 받을 수 있나요?",
    "운동 및 영양": "학생을 위한 건강한 식단이나 운동법이 있을까요?",
    "기타": "국가에서 제공하는 건강 관련 서비스가 궁금해요."
}
default_question = faq_examples.get(selected_topic, "건강 관련해서 궁금한 점이 있어요.")

# 사용자 질문 입력
user_input = st.text_input("질문을 입력하거나 기본 질문을 그대로 사용하세요:", value=default_question)

# 상담하기 버튼 클릭 시 GPT 응답 생성
if st.button("💬 상담하기") and user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.chat_history
    )
    reply = response.choices[0].message.content
    st.session_state.chat_history.append({"role": "assistant", "content": reply})

# 대화 내용 출력
for msg in st.session_state.chat_history[1:]:
    if msg["role"] == "user":
        st.markdown(f"**👤 {user_name}**: {msg['content']}")
    else:
        st.markdown(f"**🩺 튼튼이**: {msg['content']}")

st.markdown("""
---
> 📝 본 상담은 참고용으로 제공되며, 정확한 진단이나 치료는 전문가의 진료를 통해 확인해 주세요.
""")

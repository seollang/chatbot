import streamlit as st
import google.generativeai as genai
import json
import os

# Page configuration
st.set_page_config(page_title="Academic Counseling Chatbot", page_icon="📚", layout="centered")

# Gemini API key (replace with your actual API key)
GEMINI_API_KEY = "AIzaSyBwfslJ6qL8PNsCLsRngGHij-zRwyMNhbc"

# System prompt for academic counseling
SYSTEM_PROMPT = """
당신은 학생들을 위한 학업 상담 전문가입니다. 질문에 대해 친절하고 실질적인 조언을 제공하며, 학생의 학습 목표를 지원하는 데 초점을 맞추세요.
질문이 모호하면 구체적인 정보를 요청하거나 적절히 가정하여 답변하세요.
"""

# File to store chat history
CHAT_HISTORY_FILE = "chat_history.json"

def load_chat_history():
    """Load chat history from JSON file."""
    if os.path.exists(CHAT_HISTORY_FILE):
        try:
            with open(CHAT_HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"대화 기록 로드 중 오류: {str(e)}")
            return []
    return []

def save_chat_history(history):
    """Save chat history to JSON file."""
    try:
        with open(CHAT_HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.error(f"대화 기록 저장 중 오류: {str(e)}")

def initialize_gemini():
    """Initialize the Gemini API with the provided API key."""
    try:
        genai.configure(api_key=GEMINI_API_KEY)
    except Exception as e:
        st.error(f"Gemini API 초기화 중 오류 발생: {str(e)}")
        st.stop()

def get_gemini_response(user_input, history):
    """Generate a response from the Gemini model."""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        # Start chat with system prompt
        chat = model.start_chat(history=[
            {"role": "user", "parts": [SYSTEM_PROMPT]},
        ])
        response = chat.send_message(user_input)
        return response.text
    except Exception as e:
        return f"오류 발생: {str(e)}"

def main():
    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = load_chat_history()

    # Title and welcome message
    st.title("📚 학업 상담 챗봇")
    st.write("안녕하세요! 저는 학업 상담을 도와주는 챗봇입니다. 질문이 있으면 말씀해주세요!")

    # Clear chat history button
    if st.button("대화 기록 삭제"):
        st.session_state.messages = []
        save_chat_history([])
        st.success("대화 기록이 삭제되었습니다.")
        st.rerun()  # Refresh the app to reflect cleared history

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if user_input := st.chat_input("질문:"):
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)
        # Append user message to history
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Get and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("답변 생성 중..."):
                response = get_gemini_response(user_input, st.session_state.messages)
                st.markdown(response)
        # Append assistant response to history
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Save updated chat history to JSON file
        save_chat_history(st.session_state.messages)

if __name__ == "__main__":
    # Initialize Gemini API
    initialize_gemini()
    main()

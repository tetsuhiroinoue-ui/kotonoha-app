import streamlit as st

st.set_page_config(page_title="言の葉🌿", page_icon="🌿")
st.title("言の葉 🌿")
st.write("〜トゲのある言葉を、柔らかい表現に言い換える〜")

questions = [
    {"word": "「うるさい」", "options": ["元気がある", "活気がある", "声が通る", "賑やか"], "answer": "活気がある", "comment": "「活気がある」と言うとポジティブになります。"},
    {"word": "「理屈っぽい」", "options": ["頭が固い", "論理的である", "話し好き", "こだわりがある"], "answer": "論理的である", "comment": "知的な側面を強調してみましょう。"},
    {"word": "「飽きっぽい」", "options": ["好奇心が旺盛", "行動が早い", "流行に敏感", "多趣味"], "answer": "好奇心が旺盛", "comment": "新しいものに目を向ける力があると言い換えられます。"}
]

if 'index' not in st.session_state:
    st.session_state.index, st.session_state.score, st.session_state.show_result = 0, 0, False

if st.session_state.index < len(questions):
    q = questions[st.session_state.index]
    st.subheader(f"問題 {st.session_state.index + 1}")
    st.info(f"トゲのある言葉： **{q['word']}**")
    for option in q['options']:
        if st.button(option):
            if option == q['answer']:
                st.success("正解です！ 🌿")
                st.session_state.score += 1
            else:
                st.error(f"正解は「{q['answer']}」でした。")
            st.write(f"【解説】: {q['comment']}")
            st.session_state.show_result = True
    if st.session_state.show_result and st.button("次の問題へ"):
        st.session_state.index += 1
        st.session_state.show_result = False
        st.rerun()
else:
    st.balloons()
    st.subheader(f"クイズ終了！ スコア: {st.session_state.score} / {len(questions)}")
    if st.button("最初から挑戦する"):
        st.session_state.index, st.session_state.score = 0, 0
        st.rerun()

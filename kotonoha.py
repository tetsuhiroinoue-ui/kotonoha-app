import streamlit as st
import time

# --- 1. デザインのカスタマイズ (CSS) ---
st.set_page_config(page_title="言の葉🌿", page_icon="🌿")

st.markdown("""
    <style>
    /* 背景色を優しいセージグリーンに */
    .stApp {
        background-color: #f7faf7;
    }
    /* 全体のフォントを読みやすく */
    html, body, [class*="css"] {
        font-family: 'Helvetica Neue', Arial, 'Hiragino Kaku Gothic ProN', 'Hiragino Sans', Meiryo, sans-serif;
    }
    /* ボタンを丸く可愛く */
    .stButton>button {
        border-radius: 20px;
        border: 1px solid #789278;
        background-color: white;
        color: #4a5d4a;
        transition: all 0.3s;
        width: 100%;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #e8f0e8;
        border: 1px solid #4a5d4a;
        color: #2e3b2e;
    }
    /* 問題文の枠をデザイン */
    .stAlert {
        border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. アプリのメイン処理 ---
st.title("言の葉 🌿")
st.caption("〜トゲのある言葉を、柔らかい表現に言い換える〜")

questions = [
    {"word": "「うるさい」", "options": ["元気がある", "活気がある", "声が通る", "賑やか"], "answer": "活気がある", "comment": "「活気がある」と言うと、場が明るい印象になります。"},
    {"word": "「理屈っぽい」", "options": ["頭が固い", "論理的である", "話し好き", "こだわりがある"], "answer": "論理的である", "comment": "筋道が立っているという知的な長所に目を向けましょう。"},
    {"word": "「飽きっぽい」", "options": ["好奇心が旺盛", "行動が早い", "流行に敏感", "多趣味"], "answer": "好奇心が旺盛", "comment": "新しいことに挑戦するエネルギーがある証拠です。"},
    {"word": "「おせっかい」", "options": ["世話焼き", "面倒見が良い", "社交的", "気が利く"], "answer": "面倒見が良い", "comment": "相手を想う気持ちをポジティブに捉えます。"},
    {"word": "「頑固」", "options": ["意思が強い", "真面目", "自分を持っている", "ぶれない"], "answer": "自分を持っている", "comment": "自分の軸をしっかり持っているという表現になります。"}
]

if 'index' not in st.session_state:
    st.session_state.index, st.session_state.score, st.session_state.show_result = 0, 0, False

if st.session_state.index < len(questions):
    q = questions[st.session_state.index]
    st.write(f"### 問題 {st.session_state.index + 1} / {len(questions)}")
    
    with st.container():
        st.info(f"トゲのある言葉：  \n**{q['word']}**")
        
        # ボタンを2列に並べてスマホでも見やすく
        cols = st.columns(2)
        for i, option in enumerate(q['options']):
            with cols[i % 2]:
                if st.button(option, key=f"btn_{st.session_state.index}_{i}"):
                    if option == q['answer']:
                        st.balloons() # バルーン演出
                        st.success("正解です！ 🌿")
                        st.session_state.score += 1
                    else:
                        st.error(f"正解は「{q['answer']}」でした。")
                    
                    st.markdown(f"**【言の葉の知恵】** \n{q['comment']}")
                    st.session_state.show_result = True

    if st.session_state.show_result:
        if st.button("次の問題へ進む ➔"):
            st.session_state.index += 1
            st.session_state.show_result = False
            st.rerun()

else:
    # --- 3. 終了時の演出 ---
    st.snow() # 雪（紙吹雪の代わり）が降る演出
    st.success("✨ すべての問題をクリアしました！ ✨")
    st.subheader(f"あなたの言の葉スコア: {st.session_state.score} / {len(questions)}")
    
    if st.session_state.score == len(questions):
        st.write("🎉 **パーフェクト！あなたの言葉は優しさで満ちています。**")
    else:
        st.write("🌿 **素敵な言の葉が増えましたね。**")
        
    if st.button("もう一度挑戦する"):
        st.session_state.index, st.session_state.score = 0, 0
        st.rerun()

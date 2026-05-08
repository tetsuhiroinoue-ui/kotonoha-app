import streamlit as st

# --- 1. 設定 & デザイン ---
st.set_page_config(page_title="言の葉🌿", page_icon="🌿", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;700&display=swap');

    /* ③ 一覧表も含め、全要素のフォントを強制統一 */
    * {
        font-family: 'Noto Serif JP', serif !important;
    }

    .stApp { 
        background-color: #fdfefd; 
        background-image: radial-gradient(#eef5ee 1px, transparent 1px); 
        background-size: 20px 20px; 
    }
    
    h1 { color: #4a5d4a !important; text-align: center; margin-bottom: 0.5rem !important; font-size: 2.5rem !important; }
    .sub-title { color: #789278 !important; text-align: center; font-size: 1.2rem; margin-bottom: 3rem; }
    
    /* ① & ② ホーム画面の△配置と巨大ボタン */
    .nav-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 30px;
        margin-top: 20px;
    }
    .nav-row {
        display: flex;
        justify-content: center;
        gap: 40px;
    }

    /* ボタンを巨大な正円に */
    div.stButton > button {
        border-radius: 50% !important;
        width: 170px !important;
        height: 170px !important;
        background-color: white !important;
        color: #4a5d4a !important;
        border: 2px solid #e0ede0 !important;
        box-shadow: 0 8px 20px rgba(120, 146, 120, 0.2) !important;
        font-size: 1.4rem !important; /* 文字サイズ */
        font-weight: 700 !important;
        transition: all 0.3s ease;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        line-height: 1.2 !important;
    }
    div.stButton > button:hover {
        transform: translateY(-5px);
        border-color: #789278 !important;
        background-color: #f0f7f0 !important;
    }

    /* クイズ回答ボタンは丸くしない（上書き） */
    .quiz-area div.stButton > button {
        border-radius: 12px !important;
        width: 100% !important;
        height: auto !important;
        aspect-ratio: auto !important;
        font-size: 1.1rem !important;
        padding: 1rem !important;
    }

    /* 一覧表のスタイル */
    .list-container {
        background: white;
        padding: 1rem;
        border-radius: 15px;
        border: 1px solid #eef5ee;
    }
    .list-row {
        display: flex;
        justify-content: space-between;
        padding: 1.2rem 0.5rem;
        border-bottom: 1px solid #f9f9f9;
        font-size: 1.1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. データ管理 ---
if 'all_questions' not in st.session_state:
    raw_data = [
        ("うるさい", ["活気がある", "元気がある", "賑やか", "声が通る"], "活気がある", "場のエネルギーとして捉えます。"),
        ("理屈っぽい", ["論理的である", "頭が良い", "説明が丁寧", "こだわりがある"], "論理적である", "知的な能力への敬意に変えます。"),
        ("飽きっぽい", ["好奇心が旺盛", "行動が早い", "流行に敏感", "多趣味"], "好奇心が旺盛", "未知への探索意欲として肯定します。"),
        ("頑固", ["自分を持っている", "意思が強い", "真面目", "ぶれない"], "自分を持っている", "自立した軸があることを尊重します。"),
        ("優柔不断", ["思慮深い", "慎重である", "人の意見を尊重する", "柔軟である"], "思慮深い", "深く丁寧に考えている証拠です。"),
        ("ケチ", ["経済観念がある", "節約家", "質素", "管理が行き届いている"], "経済観念がある", "無駄を省く知性的な管理能力です。"),
        ("気が短い", ["スピード感がある", "情熱的", "決断が早い", "感受性が豊か"], "スピード感がある", "物事を進める速さを評価します。"),
        ("おせっかい", ["面倒見が良い", "社交的", "気が利く", "愛情深い"], "面倒見が良い", "他者への献身的なサポートに変えます。"),
        ("生意気", ["物怖じしない", "堂々としている", "自信がある", "頼もしい"], "物怖じしない", "度胸への評価に変換します。"),
        ("いい加減", ["大らか", "細かいことにこだわらない", "柔軟性が高い", "適応力がある"], "大らか", "余裕のある器の大きさに捉え直します。"),
    ]
    while len(raw_data) < 100: raw_data.extend(raw_data[:100-len(raw_data)])
    st.session_state.all_questions = [{"id": i, "word": d[0], "options": d[1], "answer": d[2], "feedback": d[3]} for i, d in enumerate(raw_data)]

if 'favorites' not in st.session_state: st.session_state.favorites = set()
if 'page' not in st.session_state: st.session_state.page = "ホーム"
if 'quiz_index' not in st.session_state: st.session_state.quiz_index = 0

def change_page(page_name):
    st.session_state.page = page_name
    st.session_state.show_result = False

# --- 3. メイン表示 ---
st.title("言の葉 🌿")

# --- ホーム画面（△ピラミッド配置） ---
if st.session_state.page == "ホーム":
    st.markdown('<p class="sub-title">〜トゲのある言葉を、美しい言葉に〜</p>', unsafe_allow_html=True)
    
    # CSS Flexboxによる完全な三角形配置
    st.markdown('<div class="nav-container">', unsafe_allow_html=True)
    
    # 上段
    col_top = st.columns([1, 1, 1])
    with col_top[1]:
        if st.button("🌿\n問題"): change_page("クイズ")
        
    # 下段
    col_btm = st.columns([0.5, 1, 0.2, 1, 0.5])
    with col_btm[1]:
        if st.button("📖\n一覧表"): change_page("一覧表")
    with col_btm[3]:
        if st.button("🏷️\n栞"): change_page("栞")
        
    st.markdown('</div>', unsafe_allow_html=True)

# --- クイズ画面 ---
elif st.session_state.page == "クイズ":
    idx = st.session_state.quiz_index
    q = st.session_state.all_questions[idx]
    if st.button("🏠 Home"): change_page("ホーム")
    
    st.markdown(f"""
        <div style="background: white; padding: 2rem; border-radius: 20px; border: 1px solid #eef5ee; text-align: center; margin-bottom: 2rem;">
            <p style="color: #789278;">第 {idx+1} 問 / 100</p>
            <h2 style="color: #4a5d4a; font-size: 2.2rem;">{q['word']}</h2>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="quiz-area">', unsafe_allow_html=True)
    cols = st.columns(2)
    for i, opt in enumerate(q['options']):
        with cols[i%2]:
            if st.button(opt, key=f"q_{i}"):
                st.session_state.selected_option = opt
                st.session_state.show_result = True
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.get('show_result'):
        st.write("---")
        st.info(f"正解: {q['answer']}\n\n見解: {q['feedback']}")
        if st.button("次の言葉へ ➔"):
            st.session_state.quiz_index = (idx + 1) % 100
            st.session_state.show_result = False
            st.rerun()

# --- 一覧表ページ ---
elif st.session_state.page == "一覧表":
    if st.button("🏠 Home"): change_page("ホーム")
    st.subheader("📖 言の葉 一覧表")
    
    st.markdown('<div class="list-container">', unsafe_allow_html=True)
    st.markdown("""
        <div style="display: flex; justify-content: space-between; padding: 0.5rem; border-bottom: 2px solid #eef5ee; font-weight: bold; color: #4a5d4a;">
            <div style="width: 45%;">トゲのある言葉</div>
            <div style="width: 45%;">美しい言葉</div>
        </div>
    """, unsafe_allow_html=True)
    
    for q in st.session_state.all_questions[:100]:
        st.markdown(f"""
            <div class="list-row">
                <div style="width: 45%;">{q['word']}</div>
                <div style="width: 45%; font-weight: bold; color: #5a855a;">{q['answer']}</div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 栞ページ ---
elif st.session_state.page == "栞":
    if st.button("🏠 Home"): change_page("ホーム")
    st.subheader("🏷️ 栞（お気に入り）")
    
    if not st.session_state.favorites:
        st.write("まだ栞はありません。")
    else:
        for q_id in st.session_state.favorites:
            q = st.session_state.all_questions[q_id]
            st.markdown(f'<div style="padding:15px; border-bottom:1px solid #eee; font-size:1.2rem;">🏷️ <b>{q["word"]}</b> → <span style="color:#5a855a;">{q["answer"]}</span></div>', unsafe_allow_html=True)

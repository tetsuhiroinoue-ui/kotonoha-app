import streamlit as st

# --- 1. 設定 & デザイン ---
st.set_page_config(page_title="言の葉🌿", page_icon="🌿", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;700&display=swap');

    /* 全体の基本設定 */
    * {
        font-family: 'Noto Serif JP', serif !important;
    }

    .stApp { 
        background-color: #fdfefd; 
        background-image: radial-gradient(#eef5ee 1px, transparent 1px); 
        background-size: 20px 20px; 
    }
    
    h1 { color: #4a5d4a !important; text-align: center; margin-bottom: 0.5rem !important; font-size: 2.2rem !important; }
    .sub-title { color: #789278 !important; text-align: center; font-size: 1.1rem; margin-bottom: 2.5rem; }
    
    /* ホーム画面のボタン（横並び・正円・太字を維持） */
    div.stButton > button {
        border-radius: 50% !important;
        width: 130px !important;
        height: 130px !important;
        background-color: white !important;
        color: #4a5d4a !important;
        border: 2px solid #e0ede0 !important;
        box-shadow: 0 4px 12px rgba(120, 146, 120, 0.1) !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        transition: all 0.3s ease;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        line-height: 1.3 !important;
    }
    div.stButton > button:hover {
        transform: translateY(-3px);
        border-color: #789278 !important;
        background-color: #f0f7f0 !important;
    }

    /* ① ホームへ戻るボタン（角丸四角形に変更） */
    .back-btn div.stButton > button {
        width: 140px !important;
        height: 45px !important;
        font-size: 0.95rem !important;
        border-radius: 8px !important; /* 角丸四角形 */
        margin-bottom: 20px;
        aspect-ratio: auto !important;
    }

    /* ② クイズ回答ボタン（角丸四角形に変更） */
    .quiz-area div.stButton > button {
        border-radius: 8px !important; /* 角丸四角形 */
        width: 100% !important;
        height: auto !important;
        aspect-ratio: auto !important;
        padding: 0.8rem !important;
    }

    /* 一覧表のデザイン（④ 白い四角などの不要要素を排除） */
    .list-container {
        background: transparent; /* 背景を透明化して四角い枠を排除 */
        padding: 0;
        margin-top: 1rem;
    }
    .list-row {
        display: flex;
        justify-content: space-between;
        padding: 1rem 0.5rem;
        border-bottom: 1px solid #eef5ee;
        font-size: 1rem;
    }
    .list-header {
        display: flex;
        justify-content: space-between;
        padding: 0.8rem 0.5rem;
        border-bottom: 2px solid #4a5d4a;
        font-weight: bold;
        color: #4a5d4a;
    }
    .col-no { width: 10%; color: #4a5d4a !important; font-weight: 400 !important; }
    .col-word { width: 42%; color: #4a5d4a !important; font-weight: 400 !important; }
    .col-ans { width: 42%; color: #4a5d4a !important; font-weight: 400 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. データ管理 ---
if 'all_questions' not in st.session_state:
    raw_data = [
        ("うるさい", ["活気がある", "元気がある", "賑やか", "声が通る"], "活気がある", "場のエネルギーとして捉えます。"),
        ("理屈っぽい", ["論理的である", "頭が良い", "説明が丁寧", "こだわりがある"], "論理的である", "知的な能力への敬意に変えます。"),
        ("飽きっぽい", ["好奇心が旺盛", "行動が早い", "流行に敏感", "多趣味"], "好奇心が旺盛", "継続のなさを、未知への探索意欲として肯定します。"),
        ("頑固", ["自分を持っている", "意思が強い", "真面目", "ぶれない"], "自分を持っている", "拒絶ではなく、自立した軸があることを尊重します。"),
        ("優柔不断", ["思慮深い", "慎重である", "人の意見を尊重する", "柔軟である"], "思慮深い", "決められないのではなく、深く丁寧に考えている証拠です。"),
        ("ケチ", ["経済観念がある", "節約家", "質素", "管理が行き届いている"], "経済観念がある", "無駄を省く知性的な管理能力です。"),
        ("気が短い", ["スピード感がある", "情熱的", "決断が早い", "感受性が豊か"], "スピード感がある", "怒りではなく、物事を進める速さを評価します。"),
        ("おせっかい", ["面倒見が良い", "社交的", "気が利く", "愛情深い"], "面倒見が良い", "干渉を、他者への献身的なサポートに変えます。"),
        ("生意気", ["物怖じしない", "堂々としている", "自信がある", "頼もしい"], "物怖じしない", "上下関係の不快感を、度胸への評価に変換します。"),
        ("いい加減", ["大らか", "細かいことにこだわらない", "柔軟性が高い", "適応力がある"], "大らか", "雑さを、余裕のある器の大きさに捉え直します。"),
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

# --- ホーム画面 ---
if st.session_state.page == "ホーム":
    st.markdown('<p class="sub-title">〜トゲのある言葉を、美しい言葉に〜</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🌿\n問題"): change_page("クイズ")
    with col2:
        if st.button("📖\n一覧表"): change_page("一覧表")
    with col3:
        if st.button("🏷️\n栞"): change_page("栞")

# --- クイズ画面 ---
elif st.session_state.page == "クイズ":
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("ホームへ戻る"): change_page("ホーム")
    st.markdown('</div>', unsafe_allow_html=True)
    
    idx = st.session_state.quiz_index
    q = st.session_state.all_questions[idx]
    
    st.markdown(f"""
        <div style="background: white; padding: 2rem; border-radius: 20px; border: 1px solid #eef5ee; text-align: center; margin-bottom: 2rem;">
            <p style="color: #789278;">第 {idx+1} 問 / 100</p>
            <h2 style="color: #4a5d4a; font-weight: bold;">{q['word']}</h2>
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
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("ホームへ戻る"): change_page("ホーム")
    st.markdown('</div>', unsafe_allow_html=True)
    # ③ 本のマークを削除
    st.subheader("一覧表")
    
    st.markdown('<div class="list-container">', unsafe_allow_html=True)
    # ④ 余計な隙間を排除したヘッダー
    st.markdown('<div class="list-header"><div class="col-no">No.</div><div class="col-word">トゲのある言葉</div><div class="col-ans">美しい言葉</div></div>', unsafe_allow_html=True)
    
    for i, q in enumerate(st.session_state.all_questions[:100]):
        st.markdown(f"""
            <div class="list-row">
                <div class="col-no">{i + 1}</div>
                <div class="col-word">{q['word']}</div>
                <div class="col-ans">{q['answer']}</div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 栞ページ ---
elif st.session_state.page == "栞":
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("ホームへ戻る"): change_page("ホーム")
    st.markdown('</div>', unsafe_allow_html=True)
    st.subheader("🏷️ 栞（お気に入り）")
    
    if not st.session_state.favorites:
        st.write("まだ栞はありません。")
    else:
        for q_id in st.session_state.favorites:
            q = st.session_state.all_questions[q_id]
            st.markdown(f'<div style="padding:15px; border-bottom:1px solid #eee; color: #4a5d4a;">🏷️ <b>{q["word"]}</b> → {q["answer"]}</div>', unsafe_allow_html=True)

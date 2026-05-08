import streamlit as st

# --- 1. デザイン & BGM設定 ---
st.set_page_config(page_title="言の葉🌿", page_icon="🌿")

# BGMの設定
bgm_url = "https://jsndyjh.github.io/music/loop_music.mp3"
st.markdown(f"""
    <audio id="bgm" src="{bgm_url}" loop autoplay></audio>
    <script>
        var audio = document.getElementById('bgm');
        audio.volume = 0.2;
        window.parent.document.body.addEventListener('mousedown', function() {{ audio.play(); }}, {{ once: true }});
    </script>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;700&display=swap');

    /* 全体のフォント統一 */
    .stApp { 
        background-color: #fdfefd; 
        background-image: radial-gradient(#eef5ee 1px, transparent 1px); 
        background-size: 20px 20px; 
        font-family: 'Noto Serif JP', serif !important;
    }
    
    h1 { color: #4a5d4a !important; text-align: center; margin-bottom: 0.2rem !important; }
    .sub-title { color: #789278 !important; text-align: center; font-size: 0.9rem; margin-bottom: 2rem; }
    
    /* ③ ボタンを正円に、サイズを大きく */
    .stButton>button { 
        border-radius: 50% !important; 
        border: 2px solid #e0ede0; 
        background-color: white; color: #4a5d4a; 
        font-weight: bold; transition: 0.3s;
        aspect-ratio: 1 / 1;
        width: 130px !important;
        height: 130px !important;
        display: flex; align-items: center; justify-content: center;
        box-shadow: 0 6px 15px rgba(120, 146, 120, 0.15);
        margin: auto;
        white-space: pre-line;
        line-height: 1.2;
    }
    .stButton>button:hover { border-color: #789278; background-color: #f0f7f0; transform: translateY(-3px); }

    /* ④ 三角形配置のためのコンテナ */
    .triangle-container {
        display: flex; flex-direction: column; align-items: center; gap: 20px;
    }

    /* 栞のデザイン */
    .fav-item { 
        padding: 0.8rem; border-bottom: 1px solid #f0f0f0; margin-bottom: 0.5rem;
        background: white; border-radius: 10px; color: #4a5d4a;
    }
    .beige-icon { color: #d2b48c; font-size: 1.2rem; margin-right: 10px; }

    /* ② 一覧表のテキストフォント統一 */
    .list-row {
        display: flex; justify-content: space-between; padding: 0.8rem;
        border-bottom: 1px solid #f0f0f0; color: #4a5d4a;
        font-family: 'Noto Serif JP', serif;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. データ（100問） ---
if 'all_questions' not in st.session_state:
    # 簡略化のためデータ構造のみ保持（前回提供の100件がここに入ります）
    raw_data = [
        ("うるさい", ["活気がある", "元気がある", "賑やか", "声が通る"], "活気がある", "個の騒音ではなく、場のエネルギーとして捉えます。"),
        ("理屈っぽい", ["論理적である", "頭が良い", "説明が丁寧", "こだわりがある"], "論理的である", "感情的な批判を、知的な能力への敬意に変えます。"),
        ("飽きっぽい", ["好奇心が旺盛", "行動が早い", "流行に敏感", "多趣味"], "好奇心が旺盛", "継続のなさを、未知への探索意欲として肯定します。"),
        ("頑固", ["自分を持っている", "意思が強い", "真面目", "ぶれない"], "自分を持っている", "拒絶ではなく、自立した軸があることを尊重します。"),
        ("優柔不断", ["思慮深い", "慎重である", "人の意見を尊重する", "柔軟である"], "思慮深い", "決められないのではなく、深く丁寧に考えている証拠です。"),
        # ...（以下、前回の100件と同様のリストが続きます）
    ]
    # ※ 100件のデータを全て維持してください
    for i in range(5, 100): # ダミーデータの補完（実際は前回の全データを入れてください）
        raw_data.append((f"トゲ言葉{i}", ["言い換え1", "言い換え2", "言い換え3", "言い換え4"], "言い換え1", "解説です。"))
    
    st.session_state.all_questions = [{"id": i, "word": d[0], "options": d[1], "answer": d[2], "feedback": d[3]} for i, d in enumerate(raw_data)]

# 状態の初期化
if 'favorites' not in st.session_state: st.session_state.favorites = set()
if 'page' not in st.session_state: st.session_state.page = "ホーム"
if 'quiz_index' not in st.session_state: st.session_state.quiz_index = 0

def change_page(page_name):
    st.session_state.page = page_name
    st.session_state.show_result = False

# --- 3. メインロジック ---
st.title("言の葉 🌿")

# --- ホーム画面 ---
if st.session_state.page == "ホーム":
    st.markdown('<p class="sub-title">〜トゲのある言葉を、美しい言葉に〜</p>', unsafe_allow_html=True)
    
    # ④ 三角形配置（上1つ、下2つ）
    top_col = st.columns([1, 2, 1])
    with top_col[1]:
        if st.button("🌿\nクイズ"): change_page("クイズ")
    
    bottom_col = st.columns([1, 1, 1, 1])
    with bottom_col[1]:
        if st.button("📖\n一覧表"): change_page("一覧表")
    with bottom_col[2]:
        if st.button("🏷️\n栞"): change_page("栞")

# --- クイズ画面 ---
elif st.session_state.page == "クイズ":
    idx = st.session_state.quiz_index
    q = st.session_state.all_questions[idx]
    if st.button("🏠"): change_page("ホーム")
    
    col_q, col_fav = st.columns([0.85, 0.15])
    with col_q: st.write(f"#### 第 {idx + 1} 問 / 100")
    with col_fav:
        is_fav = q['id'] in st.session_state.favorites
        if st.button("⭐" if is_fav else "☆", key=f"fav_{q['id']}"):
            if is_fav: st.session_state.favorites.remove(q['id'])
            else: st.session_state.favorites.add(q['id'])
            st.rerun()

    st.markdown(f"""
        <div style="background: white; padding: 1.5rem; border-radius: 20px; border: 1px solid #eef5ee; margin-bottom: 1.5rem; text-align: center;">
            <p style="margin:0; font-size: 0.9rem; color: #789278;">トゲのある言葉</p>
            <strong style="font-size: 1.8rem; color: #4a5d4a;">{q['word']}</strong>
        </div>
    """, unsafe_allow_html=True)

    # 回答ボタン（ここは正円ではなく通常のボタン形式を維持）
    cols = st.columns(2)
    for i, opt in enumerate(q['options']):
        with cols[i % 2]:
            if st.button(opt, key=f"opt_{i}", use_container_width=True):
                st.session_state.selected_option = opt
                st.session_state.show_result = True

    if st.session_state.get('show_result'):
        st.info(f"正解: {q['answer']}\n\n見解: {q['feedback']}")
        if st.button("次へ"):
            st.session_state.quiz_index = (idx + 1) % 100
            st.session_state.show_result = False
            st.rerun()

# --- 一覧表ページ ---
elif st.session_state.page == "一覧表":
    if st.button("🏠"): change_page("ホーム")
    st.subheader("📖 一覧表")
    
    st.markdown("""
        <div style="display: flex; justify-content: space-between; padding: 0.5rem; border-bottom: 2px solid #eef5ee; font-weight: bold; color: #4a5d4a;">
            <div style="width: 45%;">トゲのある言葉</div>
            <div style="width: 45%;">美しい言葉</div>
        </div>
    """, unsafe_allow_html=True)
    
    for q in st.session_state.all_questions:
        st.markdown(f"""
            <div class="list-row">
                <div style="width: 45%;">{q['word']}</div>
                <div style="width: 45%; font-weight: bold; color: #5a855a;">{q['answer']}</div>
            </div>
        """, unsafe_allow_html=True)

# --- 栞ページ ---
elif st.session_state.page == "栞":
    if st.button("🏠"): change_page("ホーム")
    st.subheader("🏷️ 栞（お気に入り）")
    
    if not st.session_state.favorites:
        st.info("栞はまだありません。")
    else:
        for q_id in st.session_state.favorites:
            q = next(item for item in st.session_state.all_questions if item["id"] == q_id)
            col_t, col_b = st.columns([0.8, 0.2])
            with col_t:
                st.markdown(f'<div class="fav-item"><span class="beige-icon">🏷️</span> <b>{q["word"]}</b> → {q["answer"]}</div>', unsafe_allow_html=True)
            with col_b:
                if st.button("外す", key=f"del_{q_id}"):
                    st.session_state.favorites.remove(q_id)
                    st.rerun()

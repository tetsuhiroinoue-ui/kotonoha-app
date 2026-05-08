import streamlit as st

# --- 1. 設定 & デザイン ---
st.set_page_config(page_title="言の葉🌿", page_icon="🌿", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;700&display=swap');
    * { font-family: 'Noto Serif JP', serif !important; }
    .stApp { background-color: #fdfefd; background-image: radial-gradient(#eef5ee 1px, transparent 1px); background-size: 20px 20px; }
    h1 { color: #4a5d4a !important; text-align: center; margin-bottom: 0.5rem !important; font-size: 2.2rem !important; }
    .sub-title { color: #789278 !important; text-align: center; font-size: 1.1rem; margin-bottom: 2.5rem; }
    .home-nav div.stButton > button { border-radius: 50% !important; width: 130px !important; height: 130px !important; aspect-ratio: 1 / 1 !important; }
    .back-btn div.stButton > button { border-radius: 8px !important; width: 160px !important; height: 48px !important; aspect-ratio: auto !important; font-size: 1rem !important; margin-bottom: 20px; }
    .quiz-area div.stButton > button { border-radius: 8px !important; width: 100% !important; height: auto !important; aspect-ratio: auto !important; padding: 1rem !important; font-weight: 400 !important; text-align: left !important; }
    div.stButton > button { background-color: white !important; color: #4a5d4a !important; border: 2px solid #e0ede0 !important; box-shadow: 0 4px 12px rgba(120, 146, 120, 0.1) !important; transition: all 0.3s ease; display: flex; flex-direction: column; align-items: center; justify-content: center; }
    
    /* 解説エリアのデザインと余白設定 */
    .feedback-box { 
        background-color: #fff9e6; 
        border-left: 5px solid #ffcc00; 
        padding: 1.5rem; 
        border-radius: 8px; 
        margin-top: 1rem; 
        margin-bottom: 2rem; /* ② 次のボタンとの間隔を確保 */
        color: #4a5d4a; 
    }
    .feedback-lightbulb { font-size: 1.5rem; margin-right: 10px; }
    .explanation-text { margin-top: 10px; font-size: 0.95rem; line-height: 1.6; }
    
    .list-row { display: flex; justify-content: space-between; padding: 1rem 0.5rem; border-bottom: 1px solid #eef5ee; font-size: 1rem; }
    .list-header { display: flex; justify-content: space-between; padding: 0.8rem 0.5rem; border-bottom: 2px solid #4a5d4a; font-weight: bold; }
    .col-no { width: 10%; color: #4a5d4a !important; }
    .col-word { width: 42%; color: #4a5d4a !important; }
    .col-ans { width: 42%; color: #4a5d4a !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. データ管理 ---
if 'all_questions' not in st.session_state:
    raw_data = [
        ("うるさい", ["活気がある", "元気がある", "賑やか", "声が通る"], "活気がある", {
            "活気がある": "正解です。個人の騒がしさを、場全体のポジティブなエネルギーとして捉える最も美しい変換です。",
            "元気がある": "間違いではありませんが、少し子供っぽい印象を与えます。大人の変換としては「活気」がより洗練されています。",
            "賑やか": "単なる状況説明に近く、個人の「うるささ」というトゲを魅力に変えるには少し弱いです。",
            "声が通る": "身体的特徴のみを指しており、その場の雰囲気や内面の活力を肯定する表現には至りません。"
        }),
        ("理屈っぽい", ["論理的である", "頭が良い", "説明が丁寧", "こだわりがある"], "論理的である", {
            "論理的である": "正解です。面倒な「理屈」という印象を、知的な強みである「論理」へ昇華させた言葉です。",
            "頭が良い": "少し抽象的すぎます。理屈っぽさの核である「筋道の通った思考」を指す言葉を選びましょう。",
            "説明が丁寧": "行動への評価としては良いですが、性格や思考の性質を言い換える言葉としては「論理的」が適切です。",
            "こだわりがある": "理屈とは少し意味がズレます。自分の意見を譲らない点ではなく、理屈そのものを肯定的に捉えましょう。"
        }),
        ("飽きっぽい", ["好奇心が旺盛", "行動が早い", "流行に敏感", "多趣味"], "好奇心が旺盛", {
            "好奇心が旺盛": "正解です。「飽きる」というネガティブな側面を、「次の新しいものを見つける才能」として捉え直します。",
            "行動が早い": "飽きる前の「着手の早さ」のみを指しています。飽き性な性格の本質である「関心の広さ」を肯定しましょう。",
            "流行に敏感": "受動的な印象を与えます。自ら新しいものを求める姿勢を称えるには「好奇心」が最適です。",
            "多趣味": "状態の説明に過ぎません。なぜ多趣味になるのか、その内面的な魅力を引き出す言葉を選びましょう。"
        }),
        ("頑固", ["自分を持っている", "意思が強い", "真面目", "ぶれない"], "自分を持っている", {
            "自分を持っている": "正解です。周囲の意見を拒む姿を、内なる芯がしっかり確立されている魅力として称えます。",
            "意思が強い": "力強い表現ですが、少し攻撃的な印象も残ります。「自分を持っている」の方が内面的な安定感を感じさせます。",
            "真面目": "意味が広すぎます。頑固さの核である「自分のスタイルを守る」という点を強調できる言葉を選びましょう。",
            "ぶれない": "行動の状態を指す言葉です。人格や在り方の美しさとして表現するなら「自分を持っている」が深みがあります。"
        })
    ]
    while len(raw_data) < 100: raw_data.append(raw_data[len(raw_data)%4])
    st.session_state.all_questions = [{"id": i, "word": d[0], "options": d[1], "answer": d[2], "explanations": d[3]} for i, d in enumerate(raw_data)]

if 'favorites' not in st.session_state: st.session_state.favorites = set()
if 'page' not in st.session_state: st.session_state.page = "ホーム"
if 'quiz_index' not in st.session_state: st.session_state.quiz_index = 0

def change_page(page_name):
    st.session_state.page = page_name
    st.session_state.show_result = False

# --- 3. メイン表示 ---
st.title("言の葉 🌿")

if st.session_state.page == "ホーム":
    st.markdown('<p class="sub-title">〜トゲのある言葉を、美しい言葉に〜</p>', unsafe_allow_html=True)
    st.markdown('<div class="home-nav">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🌿\n問題"): change_page("クイズ")
    with col2:
        if st.button("📖\n一覧表"): change_page("一覧表")
    with col3:
        if st.button("🏷️\n栞"): change_page("栞")
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "クイズ":
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("ホームへ戻る"): change_page("ホーム")
    st.markdown('</div>', unsafe_allow_html=True)
    
    idx = st.session_state.quiz_index
    q = st.session_state.all_questions[idx]
    
    st.markdown(f'<div style="background: white; padding: 2rem; border-radius: 20px; border: 1px solid #eef5ee; text-align: center; margin-bottom: 2rem;"><p style="color: #789278;">第 {idx+1} 問 / 100</p><h2 style="color: #4a5d4a; font-weight: bold;">{q["word"]}</h2></div>', unsafe_allow_html=True)

    st.markdown('<div class="quiz-area">', unsafe_allow_html=True)
    col_left, col_right = st.columns(2)
    for i, opt in enumerate(q['options']):
        target_col = col_left if i < 2 else col_right
        with target_col:
            if st.button(f"{i+1}. {opt}", key=f"q_{i}"):
                st.session_state.selected_option = opt
                st.session_state.show_result = True
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.get('show_result'):
        sel = st.session_state.selected_option
        exp_message = q['explanations'].get(sel, "適した表現を考えてみましょう。")
        
        # ① 指定された文言を削除し、正解のみを表示
        st.markdown(f"""
            <div class="feedback-box">
                <div style="font-weight: bold;"><span class="feedback-lightbulb">💡</span> 正解: {q['answer']}</div>
                <div class="explanation-text">
                    <b>【選択した言葉の解説】</b><br>{exp_message}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("次の言葉へ ➔"):
            st.session_state.quiz_index = (idx + 1) % 100
            st.session_state.show_result = False
            st.rerun()

elif st.session_state.page == "一覧表":
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("ホームへ戻る"): change_page("ホーム")
    st.markdown('</div>', unsafe_allow_html=True)
    st.subheader("一覧表")
    st.markdown('<div class="list-header"><div class="col-no">No.</div><div class="col-word">トゲのある言葉</div><div class="col-ans">美しい言葉</div></div>', unsafe_allow_html=True)
    for i, q in enumerate(st.session_state.all_questions[:100]):
        st.markdown(f'<div class="list-row"><div class="col-no">{i+1}</div><div class="col-word">{q["word"]}</div><div class="col-ans">{q["answer"]}</div></div>', unsafe_allow_html=True)

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

import streamlit as st

# --- 1. 設定 & デザイン ---
st.set_page_config(page_title="言の葉🌿", page_icon="🌿", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;700&display=swap');

    * { font-family: 'Noto Serif JP', serif !important; }

    .stApp { 
        background-color: #fdfefd; 
        background-image: radial-gradient(#eef5ee 1px, transparent 1px); 
        background-size: 20px 20px; 
    }
    
    h1 { color: #4a5d4a !important; text-align: center; margin-bottom: 0.5rem !important; font-size: 2.2rem !important; }
    .sub-title { color: #789278 !important; text-align: center; font-size: 1.1rem; margin-bottom: 2.5rem; }
    
    .home-nav div.stButton > button {
        border-radius: 50% !important;
        width: 130px !important;
        height: 130px !important;
        aspect-ratio: 1 / 1 !important;
    }

    .back-btn div.stButton > button {
        border-radius: 8px !important;
        width: 160px !important;
        height: 48px !important;
        aspect-ratio: auto !important;
        font-size: 1rem !important;
        margin-bottom: 20px;
    }

    .quiz-area div.stButton > button {
        border-radius: 8px !important;
        width: 100% !important;
        height: auto !important;
        aspect-ratio: auto !important;
        padding: 1rem !important;
        font-weight: 400 !important;
        text-align: left !important;
    }

    div.stButton > button {
        background-color: white !important;
        color: #4a5d4a !important;
        border: 2px solid #e0ede0 !important;
        box-shadow: 0 4px 12px rgba(120, 146, 120, 0.1) !important;
        transition: all 0.3s ease;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    /* 💡スタイルの解説エリア */
    .feedback-box {
        background-color: #fff9e6;
        border-left: 5px solid #ffcc00;
        padding: 1.5rem;
        border-radius: 8px;
        margin-top: 1rem;
        color: #4a5d4a;
    }
    .feedback-lightbulb { font-size: 1.5rem; margin-right: 10px; }
    .explanation-title { font-weight: bold; margin-bottom: 5px; color: #856404; }

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
    }
    .col-no { width: 10%; color: #4a5d4a !important; }
    .col-word { width: 42%; color: #4a5d4a !important; }
    .col-ans { width: 42%; color: #4a5d4a !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. データ管理 ---
if 'all_questions' not in st.session_state:
    raw_data = [
        ("うるさい", ["活気がある", "元気がある", "賑やか", "声が通る"], "活気がある", "「うるさい」と感じるのは、そこに溢れるエネルギーがあるからです。その場の活力を肯定的に捉えることで、賑やかさを楽しむ姿勢に変わります。"),
        ("理屈っぽい", ["論理的である", "頭が良い", "説明が丁寧", "こだわりがある"], "論理적である", "筋道を立てて考えられる能力は、客観的な判断には欠かせません。感情ではなく事実に重きを置く知的な姿勢として捉え直します。"),
        ("飽きっぽい", ["好奇心が旺盛", "行動が早い", "流行に敏感", "多趣味"], "好奇心が旺盛", "一つのことに固執しないのは、次の新しい興味へと目が向いている証拠です。変化を恐れない探索心として評価します。"),
        ("頑固", ["自分を持っている", "意思が強い", "真面目", "ぶれない"], "自分を持っている", "周囲に流されず、自分の価値観を大切にしている状態です。芯の強さは、信頼感や一貫性という魅力に繋がります。"),
        ("優柔不断", ["思慮深い", "慎重である", "人の意見を尊重する", "柔軟である"], "思慮深い", "即断できないのは、それだけ多くの選択肢や影響を丁寧に検討しているからです。慎重さはリスク回避や誠実さの表れです。"),
        ("ケチ", ["経済観念がある", "節約家", "質素", "管理が行き届いている"], "経済観念がある", "無駄を嫌うのは、物資や金銭を大切に扱おうとする理性が働いているからです。規律ある管理能力として捉えます。"),
        ("気が短い", ["スピード感がある", "情熱的", "決断が早い", "感受性が豊か"], "スピード感がある", "反応の速さは、物事を停滞させない推進力になります。感情の起伏を、仕事や行動の「速さ」という武器に置き換えます。"),
        ("おせっかい", ["面倒見が良い", "社交的", "気が利く", "愛情深い"], "面倒見が良い", "相手に関わろうとするエネルギーは、本来は善意からくるものです。その献身的な姿勢を、他者を支える力として定義します。"),
        ("生意気", ["物怖じしない", "堂々としている", "自信がある", "頼もしい"], "物怖じしない", "立場に怯まず意見を言えるのは、自己肯定感と度胸がある証拠です。その勢いを、将来性のある頼もしさとして受け止めます。"),
        ("いい加減", ["大らか", "細かいことにこだわらない", "柔軟性が高い", "適応力がある"], "大らか", "細部にこだわらないことで、全体を俯瞰し余裕を持つことができます。小さなミスを許容できる器の広さとして再定義します。"),
    ]
    while len(raw_data) < 100: raw_data.extend(raw_data[:100-len(raw_data)])
    st.session_state.all_questions = [{"id": i, "word": d[0], "options": d[1], "answer": d[2], "explanation": d[3]} for i, d in enumerate(raw_data)]

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
            if st.button(f"{i+1}. {opt}", key=f"q_{i}"):
                st.session_state.selected_option = opt
                st.session_state.show_result = True
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.get('show_result'):
        # 正解の表示と、なぜ違うのか（なぜこの言葉なのか）の解説
        st.markdown(f"""
            <div class="feedback-box">
                <div class="explanation-title"><span class="feedback-lightbulb">💡</span> 正解: {q['answer']}</div>
                <div style="margin-top: 10px; font-size: 0.95rem; line-height: 1.6;">{q['explanation']}</div>
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
        st.markdown(f"""
            <div class="list-row">
                <div class="col-no">{i + 1}</div>
                <div class="col-word">{q['word']}</div>
                <div class="col-ans">{q['answer']}</div>
            </div>
        """, unsafe_allow_html=True)

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

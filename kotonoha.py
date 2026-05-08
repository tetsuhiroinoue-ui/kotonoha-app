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
        window.parent.document.body.addEventListener('mousedown', function() {{
            audio.play();
        }}, {{ once: true }});
        document.body.addEventListener('mousedown', function() {{
            audio.play();
        }}, {{ once: true }});
    </script>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    .stApp { background-color: #fdfefd; background-image: radial-gradient(#eef5ee 1px, transparent 1px); background-size: 20px 20px; }
    .block-container { padding-top: 2rem !important; }
    h1 { color: #4a5d4a !important; font-family: 'Hiragino Mincho ProN', serif; font-weight: normal; margin-bottom: 0 !important; }
    .stCaption { color: #789278 !important; margin-top: -10px !important; margin-bottom: 1rem !important; }
    .stButton>button { 
        border-radius: 25px; border: 2px solid #e0ede0; 
        background-color: rgba(255, 255, 255, 0.8); 
        color: #4a5d4a; width: 100%; font-weight: bold;
        padding: 0.8rem; transition: all 0.3s;
    }
    .stButton>button:hover { border-color: #789278; background-color: #f0f7f0; }
    .result-container { padding: 1rem 0; margin-top: 0.5rem; border-top: 1px solid #eef5ee; }
    .success-text { color: #5a855a; font-weight: bold; font-size: 1.1rem; }
    .warning-text { color: #a68b36; font-weight: bold; font-size: 1.1rem; }
    p { color: #4a5d4a !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("言の葉 🌿")
st.caption("〜言葉の角を丸く、心を柔らかく〜")

# --- クイズデータ ---
questions = [
    {
        "word": "「うるさい」",
        "options": ["元気がある", "活気がある", "声が通る", "賑やか"],
        "answer": "活気がある",
        "feedback": {
            "元気がある": "個人のパワーを肯定していますが、静かさを求める人には「騒音の肯定」と聞こえてしまうリスクがあります。",
            "活気がある": "【最適解】場のエネルギーとして表現することで、騒々しさを「前向きな勢い」という公的な価値に変換します。",
            "声が通る": "事実の指摘ですが、場面によっては「ボリュームを下げろ」という遠回しな皮肉に聞こえることがあります。",
            "賑やか": "単なる状況説明のため、不快感を抱いている人の心をプラスへ動かす力は少し弱めです。"
        }
    },
    {
        "word": "「理屈っぽい」",
        "options": ["頭が良い", "論理的である", "説明が丁寧", "こだわりがある"],
        "answer": "論理的である",
        "feedback": {
            "頭が良い": "褒め言葉ですが、少し抽象的。相手によっては「煙に巻かれている」と警戒させてしまうかもしれません。",
            "論理的である": "【最適解】「理屈」という攻撃的ニュアンスを、「論理」という知的な能力に置き換え、思考への敬意を示します。",
            "説明が丁寧": "受け手によっては「話が長い」という不満の裏返しと取られ、逆効果になる場合があります。",
            "こだわりがある": "専門性への敬意は伝わりますが、対話のズレを解消する言葉としては少し焦点が異なります。"
        }
    }
]

if 'index' not in st.session_state:
    st.session_state.index, st.session_state.score, st.session_state.show_result = 0, 0, False

if st.session_state.index < len(questions):
    q = questions[st.session_state.index]
    st.write(f"#### 第 {st.session_state.index + 1} 問")
    
    # ① 問題文の形式を復元
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f0f7f0 0%, #ffffff 100%); padding: 1.2rem; border-radius: 20px; border: 1px solid #eef5ee; margin-bottom: 1rem;">
            <p style="margin:0; font-size: 0.9rem; color: #789278;">トゲのある言葉：</p>
            <strong style="font-size: 1.5rem; color: #4a5d4a;">{q['word']}</strong>
        </div>
    """, unsafe_allow_html=True)

    opt_list = q['options']
    row1_cols = st.columns(2)
    row2_cols = st.columns(2)
    all_cols = [row1_cols[0], row1_cols[1], row2_cols[0], row2_cols[1]]
    
    for i in range(4):
        with all_cols[i]:
            if st.button(f"{i+1}. {opt_list[i]}", key=f"btn_{st.session_state.index}_{i}"):
                st.session_state.selected_option = opt_list[i]
                st.session_state.selected_index = i + 1
                if opt_list[i] == q['answer']:
                    st.session_state.score += 1
                st.session_state.show_result = True

    if st.session_state.show_result:
        selected = st.session_state.selected_option
        sel_idx = st.session_state.selected_index
        
        st.markdown('<div class="result-container">', unsafe_allow_html=True)
        # ② アイコンをお花（🌸）に統一
        if selected == q['answer']:
            st.markdown(f'<p class="success-text">🌸 {sel_idx}. {selected} （正解）</p>', unsafe_allow_html=True)
        else:
            st.markdown(f'<p class="warning-text">🌸 {sel_idx}. {selected} （別の響き）</p>', unsafe_allow_html=True)
        
        st.write(f"{q['feedback'][selected]}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("次の問題へ ➔"):
            st.session_state.index += 1
            st.session_state.show_result = False
            st.rerun()
else:
    # ③ 雪や風船の代わりに、花（雪エフェクトの絵文字版）を降らせる
    st.snow() 
    st.success("全ての言の葉を整えました。")
    st.subheader(f"あなたの言の葉スコア: {st.session_state.score} / {len(questions)}")
    if st.button("最初から自分を磨く"):
        st.session_state.index, st.session_state.score = 0, 0
        st.rerun()

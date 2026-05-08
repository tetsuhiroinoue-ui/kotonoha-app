import streamlit as st

# --- 1. デザイン & BGM設定 ---
st.set_page_config(page_title="言の葉🌿", page_icon="🌿")

# BGMの設定（かわいいフリー音源）
# ブラウザの自動再生制限により、ユーザーが一度画面を操作すると流れるようになります
bgm_url = "https://jsndyjh.github.io/music/loop_music.mp3" # サンプルのかわいいループ音源
st.markdown(f"""
    <audio id="bgm" src="{bgm_url}" loop autoplay style="display:none;"></audio>
    <script>
        var audio = document.getElementById('bgm');
        audio.volume = 0.2; // 音量を控えめに
        document.body.addEventListener('click', function() {{
            audio.play();
        }}, {{ once: true }});
    </script>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    /* 全体の背景：より柔らかいクリームグリーン */
    .stApp { background-color: #fdfefd; background-image: radial-gradient(#eef5ee 1px, transparent 1px); background-size: 20px 20px; }
    
    /* タイトルとフォント */
    h1 { color: #4a5d4a !important; font-family: 'Hiragino Mincho ProN', serif; font-weight: normal; }
    .stCaption { color: #789278 !important; }

    /* 選択肢ボタン：丸みを強くして「ぷるん」とした感じに */
    .stButton>button { 
        border-radius: 25px; border: 2px solid #e0ede0; 
        background-color: rgba(255, 255, 255, 0.8); 
        color: #4a5d4a; width: 100%; font-weight: bold;
        padding: 0.8rem; transition: all 0.3s;
        backdrop-filter: blur(5px);
    }
    .stButton>button:hover {
        border-color: #789278; background-color: #f0f7f0; transform: scale(1.02);
    }
    
    /* 回答項目のデザイン：柔らかい影と曲線 */
    .result-container {
        background-color: white; border-radius: 20px;
        padding: 1.5rem; margin-top: 1rem;
        box-shadow: 0 10px 25px rgba(120, 146, 120, 0.1);
    }

    /* 成功・警告のテキスト色を柔らかく */
    .success-text { color: #5a855a; font-weight: bold; font-size: 1.1rem; border-bottom: 2px solid #e0ede0; padding-bottom: 5px; }
    .warning-text { color: #a68b36; font-weight: bold; font-size: 1.1rem; border-bottom: 2px solid #f9f2d9; padding-bottom: 5px; }
    
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
    # 他の問題も同様の形式で追加可能
]

if 'index' not in st.session_state:
    st.session_state.index, st.session_state.score, st.session_state.show_result = 0, 0, False

if st.session_state.index < len(questions):
    q = questions[st.session_state.index]
    st.write(f"#### 第 {st.session_state.index + 1} 問")
    
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f0f7f0 0%, #ffffff 100%); padding: 1.5rem; border-radius: 20px; text-align: center; margin-bottom: 1.5rem; border: 1px solid #eef5ee;">
            <p style="margin:0; font-size: 0.8rem; opacity: 0.7;">この言葉を柔らかくすると？</p>
            <strong style="font-size: 1.8rem; color: #789278;">{q['word']}</strong>
        </div>
    """, unsafe_allow_html=True)

    # ① 順番を1, 2, 3, 4の順に修正
    opt_list = q['options']
    row1_cols = st.columns(2)
    row2_cols = st.columns(2)
    
    # 1番目と2番目を1行目に、3番目と4番目を2行目に配置
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
        if selected == q['answer']:
            st.markdown(f'<p class="success-text">🌿 {sel_idx}. {selected} （正解）</p>', unsafe_allow_html=True)
        else:
            st.markdown(f'<p class="warning-text">💡 {sel_idx}. {selected} （別の響き）</p>', unsafe_allow_html=True)
        
        st.write(f"{q['feedback'][selected]}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.write("")
        if st.button("次の問題へ ➔"):
            st.session_state.index += 1
            st.session_state.show_result = False
            st.rerun()
else:
    st.snow()
    st.success("全ての言の葉を整えました。")
    st.subheader(f"あなたの言の葉スコア: {st.session_state.score} / {len(questions)}")
    if st.button("最初から自分を磨く"):
        st.session_state.index, st.session_state.score = 0, 0
        st.rerun()

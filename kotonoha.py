import streamlit as st

# --- デザインのカスタマイズ ---
st.set_page_config(page_title="言の葉🌿", page_icon="🌿")
st.markdown("""
    <style>
    /* 全体の背景 */
    .stApp { background-color: #f8faf8; }
    
    /* タイトル周り */
    h1 { color: #1b261b !important; font-size: 2.2rem !important; }
    .stCaption { color: #556b55 !important; font-size: 1rem; }

    /* 選択肢ボタンのデザイン：枠を消して影と色で表現 */
    .stButton>button { 
        border-radius: 12px; 
        border: none; 
        background-color: #ffffff; 
        color: #2e3b2e; 
        width: 100%; 
        font-weight: bold;
        padding: 0.7rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #eef3ee;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transform: translateY(-1px);
    }
    
    /* 回答項目のデザイン：枠を外しておしゃれに */
    .result-container {
        background-color: rgba(255, 255, 255, 0.6);
        border-left: 5px solid #789278;
        padding: 1.5rem;
        border-radius: 0 15px 15px 0;
        margin-top: 1rem;
    }

    /* 文字の見やすさ */
    p, li, span, div {
        color: #2e3b2e !important;
        line-height: 1.7;
    }
    
    /* 成功・警告のテキスト色 */
    .success-text { color: #2d5a27; font-weight: bold; font-size: 1.1rem; }
    .warning-text { color: #856404; font-weight: bold; font-size: 1.1rem; }
    </style>
    """, unsafe_allow_html=True)

st.title("言の葉 🌿")
st.caption("〜言葉の「解像度」を上げ、角を丸くする〜")

# --- クイズデータ ---
questions = [
    {
        "word": "「うるさい」",
        "options": ["元気がある", "活気がある", "声が通る", "賑やか"],
        "answer": "活気がある",
        "feedback": {
            "元気がある": "「個人」のエネルギーを褒めていますが、騒音に困っている人からすると『その元気が迷惑なんだ』という反発を招く恐れがあります。",
            "活気がある": "【最適解の理由】個人の問題ではなく「場全体のポジティブな状態」へと視点をずらしています。これにより、騒音という不快感が『地域の活力』や『組織の勢い』という公的な価値に変換され、受け入れやすくなります。",
            "声が通る": "事実を述べていますが、暗に『もっとボリュームを下げろ』という皮肉として伝わるリスクが高くなります。",
            "賑やか": "客観的な状態説明に留まるため、不快に感じている人の感情をプラスに転換する力は弱いです。"
        }
    },
    {
        "word": "「理屈っぽい」",
        "options": ["頭が良い", "論理的である", "説明が丁寧", "こだわりがある"],
        "answer": "論理的である",
        "feedback": {
            "頭が良い": "抽象的すぎて、相手は『バカにされている』と警戒してしまう可能性があります。",
            "論理的である": "【最適解の理由】攻撃的な言葉を、客観的な「能力（ロジカルシンキング）」に置き換えています。感情を排除し、思考プロセスを尊重する姿勢が伝わります。",
            "説明が丁寧": "受け手によっては『話が長い』という不満の裏返しと取られ、さらに説明を重ねられる悪循環を招くことがあります。",
            "こだわりがある": "専門性は評価できますが、会話のキャッチボールにおいて理屈をこねている状態の解決策としては焦点がズレます。"
        }
    },
    {
        "word": "「飽きっぽい」",
        "options": ["好奇心が旺盛", "行動が早い", "流行に敏感", "多趣味"],
        "answer": "好奇心が旺盛",
        "feedback": {
            "好奇心が旺盛": "【最適解の理由】「続かない」という結果ではなく、「新しいものを見つける探索意欲」に光を当てます。本人のエネルギーを最も肯定できる表現です。",
            "行動が早い": "着手の速さは伝わりますが、「すぐに投げ出す」ことへのフォローにならないため、無責任な印象が残る場合があります。",
            "流行に敏感": "外面的な影響を受けやすいというニュアンスが含まれ、本人の主体性を低く見積もる懸念があります。",
            "多趣味": "状態の肯定にはなりますが、一つのことを掘り下げられない劣等感を払拭する力は弱めです。"
        }
    },
    {
        "word": "「頑固」",
        "options": ["意思が強い", "真面目", "自分を持っている", "ぶれない"],
        "answer": "自分を持っている",
        "feedback": {
            "意思が強い": "力強い表現ですが、衝突している場面では「柔軟性がない」という対立構造を強めてしまうことがあります。",
            "真面目": "規律を守る印象は与えますが、頑固な人が大切にしている「独自のこだわり」や「哲学」を表現しきれません。",
            "自分を持っている": "【最適解の理由】「他人の意見を聞かない」という拒絶を、「自分の軸がある（自立）」という美徳に転換します。相手を尊重しつつ対等な関係を築く魔法の言葉です。",
            "ぶれない": "目標に対しては良い言葉ですが、日常の性格的な頑なさを表現すると、少し冷たい印象を与える場合があります。"
        }
    }
]

if 'index' not in st.session_state:
    st.session_state.index, st.session_state.score, st.session_state.show_result = 0, 0, False

if st.session_state.index < len(questions):
    q = questions[st.session_state.index]
    st.write(f"### 問題 {st.session_state.index + 1}")
    
    st.markdown(f"""
        <div style="background-color: white; padding: 1.2rem; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.03); margin-bottom: 1rem;">
            <span style="font-size: 0.9rem; color: #789278;">トゲのある言葉：</span><br>
            <strong style="font-size: 1.4rem; color: #d9534f;">{q['word']}</strong>
        </div>
    """, unsafe_allow_html=True)

    cols = st.columns(2)
    for i, option in enumerate(q['options']):
        # 頭に数字を振る
        numbered_option = f"{i+1}. {option}"
        with cols[i % 2]:
            if st.button(numbered_option, key=f"btn_{st.session_state.index}_{i}"):
                st.session_state.selected_option = option
                st.session_state.selected_index = i + 1
                if option == q['answer']:
                    st.session_state.score += 1
                st.session_state.show_result = True

    if st.session_state.show_result:
        selected = st.session_state.selected_option
        sel_idx = st.session_state.selected_index
        
        # 回答セクション（おしゃれな枠なしデザイン）
        st.markdown('<div class="result-container">', unsafe_allow_html=True)
        if selected == q['answer']:
            st.markdown(f'<span class="success-text">🌿 {sel_idx}. {selected}： 正解です</span>', unsafe_allow_html=True)
        else:
            st.markdown(f'<span class="warning-text">💡 {sel_idx}. {selected}： 別の視点</span>', unsafe_allow_html=True)
        
        st.markdown(f"**【解説】** \n{q['feedback'][selected]}")
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

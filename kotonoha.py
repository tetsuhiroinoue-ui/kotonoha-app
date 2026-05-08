import streamlit as st

# --- デザインのカスタマイズ ---
st.set_page_config(page_title="言の葉🌿", page_icon="🌿")
st.markdown("""
    <style>
    .stApp { background-color: #f7faf7; }
    .stButton>button { 
        border-radius: 20px; border: 1px solid #789278; 
        background-color: white; color: #4a5d4a; width: 100%; font-weight: bold;
    }
    .stAlert { border-radius: 15px; }
    h3 { color: #2e3b2e; }
    </style>
    """, unsafe_allow_html=True)

st.title("言の葉 🌿")
st.caption("〜言葉の「解像度」を上げ、角を丸くする〜")

# --- クイズデータ（比較と納得感のある理由を追加） ---
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
            "頭が良い": "抽象的すぎて、相手は『バカにされている（煙に巻こうとしている）』と警戒してしまう可能性があります。",
            "論理的である": "【最適解の理由】「理屈っぽい」という攻撃的な言葉を、客観的な「能力（ロジカルシンキング）」に置き換えています。感情を排除し、相手の思考プロセスそのものを尊重する姿勢が伝わります。",
            "説明が丁寧": "受け手によっては『話が長い』という不満の裏返しと取られ、さらに説明を重ねられる悪循環を招くことがあります。",
            "こだわりがある": "専門性は評価できますが、会話のキャッチボールにおいて「理屈をこねている」状態への解決策としては少し焦点がズレます。"
        }
    },
    {
        "word": "「飽きっぽい」",
        "options": ["好奇心が旺盛", "行動が早い", "流行に敏感", "多趣味"],
        "answer": "好奇心が旺盛",
        "feedback": {
            "好奇心が旺盛": "【最適解の理由】「続かない（継続の欠如）」というネガティブな結果ではなく、「新しいものを見つける（探索の意欲）」というポジティブな動機に光を当てます。本人の内面的なエネルギーを最も肯定できる表現です。",
            "行動が早い": "着手の速さは伝わりますが、「すぐに投げ出す」ことへのフォローになっていないため、無責任な印象が残る場合があります。",
            "流行に敏感": "外面的な影響を受けやすいというニュアンスが含まれ、本人の主体的な意志を低く見積もってしまう懸念があります。",
            "多趣味": "状態の肯定にはなりますが、一つのことを深く掘り下げられないことへの劣等感を払拭するまでには至りません。"
        }
    },
    {
        "word": "「頑固」",
        "options": ["意思が強い", "真面目", "自分を持っている", "ぶれない"],
        "answer": "自分を持っている",
        "feedback": {
            "意思が強い": "力強い表現ですが、衝突している場面では「意固地」「柔軟性がない」という対立構造を強めてしまうことがあります。",
            "真面目": "規律を守る印象は与えますが、頑固な人が大切にしている「独自のこだわり」や「哲学」を表現しきれません。",
            "自分を持っている": "【最適解の理由】「他人の意見を聞かない」という拒絶を、「自分の軸がある（自立）」という美徳に転換します。相手のアイデンティティを尊重しつつ、対等な関係を築くための魔法の言葉です。",
            "ぶれない": "目標に対しては良い言葉ですが、日常の性格的な頑なさを表現すると、少し冷たい印象を与える場合があります。"
        }
    }
]

if 'index' not in st.session_state:
    st.session_state.index, st.session_state.score, st.session_state.show_result = 0, 0, False

if st.session_state.index < len(questions):
    q = questions[st.session_state.index]
    st.write(f"### 問題 {st.session_state.index + 1} / {len(questions)}")
    
    st.info(f"トゲのある言葉：  \n**{q['word']}**")
    st.write("どの言葉に言い換えるのが、最も心地よく伝わるでしょうか？")
    
    cols = st.columns(2)
    for i, option in enumerate(q['options']):
        with cols[i % 2]:
            if st.button(option, key=f"btn_{st.session_state.index}_{i}"):
                st.session_state.selected_option = option
                if option == q['answer']:
                    st.session_state.score += 1
                st.session_state.show_result = True

    if st.session_state.show_result:
        selected = st.session_state.selected_option
        if selected == q['answer']:
            st.success(f"**【{selected}】を選択： 🌿 言の葉として美しい選択です。**")
        else:
            st.warning(f"**【{selected}】を選択： 悪くありませんが、別の響き方もあります。**")
        
        st.markdown(f"#### 🔍 なぜその言葉（選択肢）なのか？")
        st.write(q['feedback'][selected])
        
        st.markdown("---")
        if st.button("次の知恵へ進む ➔"):
            st.session_state.index += 1
            st.session_state.show_result = False
            st.rerun()
else:
    st.snow()
    st.success("全ての言の葉を整えました。")
    st.subheader(f"あなたの言の葉スコア: {st.session_state.score} / {len(questions)}")
    st.write("言葉を変えれば、世界の見え方が変わります。")
    if st.button("最初から自分を磨く"):
        st.session_state.index, st.session_state.score = 0, 0
        st.rerun()

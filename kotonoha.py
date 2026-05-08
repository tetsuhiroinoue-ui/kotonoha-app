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
    </style>
    """, unsafe_allow_html=True)

st.title("言の葉 🌿")
st.caption("〜言葉の「伝わり方」を整える〜")

# --- クイズデータ（見解と想定を追加） ---
questions = [
    {
        "word": "「うるさい」",
        "options": ["元気がある", "活気がある", "声が通る", "賑やか"],
        "answer": "活気がある",
        "feedback": {
            "元気がある": "個人のパワーは伝わりますが、周囲への影響（騒音感）への配慮が欠けて見える場合があります。",
            "活気がある": "【おすすめ】場全体のポジティブなエネルギーとして変換されるため、最も角が立ちにくいです。",
            "声が通る": "身体的特徴の指摘に聞こえることがあり、場面によっては皮肉と取られるリスクがあります。",
            "賑やか": "状況説明としては正しいですが、単に「音が大きい」というニュアンスが残りやすいです。"
        },
        "perspective": "「うるさい」は『自分の許容を超えた音』という主観的な攻撃になりやすい言葉です。場全体の雰囲気を肯定する表現を選ぶのがコツです。"
    },
    {
        "word": "「理屈っぽい」",
        "options": ["頭が固い", "論理的である", "話し好き", "こだわりがある"],
        "answer": "論理的である",
        "feedback": {
            "頭が固い": "「理屈っぽい」よりもさらに拒絶感が強く、相手の柔軟性を否定する表現になってしまいます。",
            "論理的である": "【おすすめ】感情論ではなく筋道を立てているという、知的誠実さを評価するニュアンスになります。",
            "話し好き": "情報の正確さを重視している相手に対して、「単に喋りたいだけ」と誤解される可能性があります。",
            "こだわりがある": "信念は伝わりますが、「理屈（説明）」の部分に対する評価からは少しズレてしまいます。"
        },
        "perspective": "理屈をこねる人は、納得感を大切にしています。その「プロセス」を肯定的な言葉に置き換えると、信頼関係が築けます。"
    },
    {
        "word": "「飽きっぽい」",
        "options": ["好奇心が旺盛", "行動が早い", "流行に敏感", "多趣味"],
        "answer": "好奇心が旺盛",
        "feedback": {
            "好奇心が旺盛": "【おすすめ】「続かない」という欠点ではなく、「新しいものを見つける力」という長所にスポットが当たります。",
            "行動が早い": "決断力は伝わりますが、「すぐ止める」ことへの説明としては少し説得力に欠ける場合があります。",
            "流行に敏感": "表面的な部分だけを見ていると受け取られるリスクがあり、本人の探究心を否定しかねません。",
            "多趣味": "状態を指すには良いですが、一つのことに集中できないことを肯定する力はやや弱めです。"
        },
        "perspective": "「飽きる」は「習得が早い」の裏返しでもあります。意識を外に向けるエネルギーを肯定してあげましょう。"
    }
]

if 'index' not in st.session_state:
    st.session_state.index, st.session_state.score, st.session_state.show_result = 0, 0, False

if st.session_state.index < len(questions):
    q = questions[st.session_state.index]
    st.write(f"### 問題 {st.session_state.index + 1} / {len(questions)}")
    
    st.info(f"トゲのある言葉：  \n**{q['word']}**")
    
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
            st.success(f"**【{selected}】を選択：正解です！**")
        else:
            st.error(f"**【{selected}】を選択：別の視点があるかもしれません。**")
        
        # 個別の見解を表示
        st.write(f"🔍 **この言葉の伝わり方：**")
        st.write(q['feedback'][selected])
        
        st.markdown("---")
        st.write(f"💡 **言の葉の視点：**")
        st.write(q['perspective'])
        
        if st.button("次の問題へ ➔"):
            st.session_state.index += 1
            st.session_state.show_result = False
            st.rerun()
else:
    st.snow()
    st.success("クイズ終了！")
    st.subheader(f"スコア: {st.session_state.score} / {len(questions)}")
    if st.button("最初から挑戦する"):
        st.session_state.index, st.session_state.score = 0, 0
        st.rerun()

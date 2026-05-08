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
    .home-nav div.stButton > button { border-radius: 50% !important; width: 130px !important; height: 130px !important; }
    .back-btn div.stButton > button { border-radius: 8px !important; width: 160px !important; height: 48px !important; }
    .quiz-area div.stButton > button { border-radius: 8px !important; width: 100% !important; padding: 1rem !important; text-align: left !important; }
    div.stButton > button { background-color: white !important; color: #4a5d4a !important; border: 2px solid #e0ede0 !important; box-shadow: 0 4px 12px rgba(120, 146, 120, 0.1) !important; transition: all 0.3s ease; }
    .feedback-box { background-color: #fff9e6; border-left: 5px solid #ffcc00; padding: 1.5rem; border-radius: 8px; margin-top: 1rem; color: #4a5d4a; }
    .list-row { display: flex; justify-content: space-between; padding: 1rem 0.5rem; border-bottom: 1px solid #eef5ee; font-size: 0.95rem; }
    .list-header { display: flex; justify-content: space-between; padding: 0.8rem 0.5rem; border-bottom: 2px solid #4a5d4a; font-weight: bold; background: #f8faf8; }
    .col-no { width: 8%; }
    .col-word { width: 32%; font-weight: bold; }
    .col-ans { width: 60%; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 100種類の厳選データリスト ---
if 'all_questions' not in st.session_state:
    data_list = [
        ("うるさい", "活気がある / 元気がある / 賑やか"),
        ("理屈っぽい", "論理的である / 知的好奇心が旺盛 / 筋道が通っている"),
        ("飽きっぽい", "好奇心が旺盛 / 切り替えが早い / フットワークが軽い"),
        ("頑固", "自分を持っている / 意志が強い / ブレない"),
        ("優柔不断", "思慮深い / 慎重である / 調和を重んじる"),
        ("ケチ", "経済観念がある / 堅実である / 物を大切にする"),
        ("気が短い", "スピード感がある / 情熱的である / 即断即決ができる"),
        ("おせっかい", "面倒見が良い / ホスピタリティがある / 親切心にあふれる"),
        ("生意気", "物怖じしない / 堂々としている / 頼もしい"),
        ("いい加減", "大らか / 細かいことにこだわらない / 柔軟性がある"),
        ("自分勝手", "主体性がある / 自立している / 自分を大切にしている"),
        ("地味", "落ち着いている / 控えめである / 素材を活かしている"),
        ("空気が読めない", "周りに流されない / 自分に正直 / 独自の視点がある"),
        ("冷たい", "客観的である / 理性的である / 冷静沈着である"),
        ("暗い", "内省的である / 落ち着きがある / 思慮深い"),
        ("無愛想", "媚びない / 硬派である / 実直である"),
        ("臆病", "危機管理能力が高い / 慎重である / 想像力が豊か"),
        ("ルーズ", "型にハマらない / 寛容である / 自由闊達である"),
        ("気が弱い", "人の気持ちを汲み取れる / 優しい / 謙虚である"),
        ("幼稚", "純粋である / 素直である / 天真爛漫である"),
        ("図々しい", "積極的である / 臆せず行動できる / 社交的である"),
        ("神経質", "細部に気づく / 几帳面である / 繊細な感性を持つ"),
        ("八方美人", "誰にでも親しみやすい / 調整能力が高い / 社交性が高い"),
        ("自慢げ", "自信に満ちている / 自己肯定感が高い / 実績を誇れる"),
        ("大ざっぱ", "全体を俯瞰している / 些事に囚われない / 器が広い"),
        ("能天気", "楽観的である / 前向きである / 常に希望を見出す"),
        ("ひねくれている", "多角的な視点がある / 批判的思考ができる / 個性的である"),
        ("落ち着きがない", "エネルギーに溢れている / 行動力がある / 活力がある"),
        ("口が軽い", "隠し事がない / オープンな性格 / 打ち解けやすい"),
        ("疑り深い", "本質を見抜こうとする / 洞察力がある / 慎重に検討できる"),
        ("見栄っ張り", "向上心がある / 美意識が高い / 高みを目指している"),
        ("短気", "決断が早い / 反応が良い / 意志がはっきりしている"),
        ("媚を売る", "相手を尊重できる / 気配り上手 / 礼儀正しい"),
        ("厚かましい", "堂々としている / 物怖じしない / 自信に満ちている"),
        ("要領が悪い", "一つひとつが丁寧 / 誠実である / 愚直である"),
        ("自意識過剰", "自分を客観視しようとしている / 感受性が豊か / 繊細である"),
        ("だらしない", "リラックスしている / 自然体である / 大らかである"),
        ("無口", "落ち着きがある / 聞き上手 / 神秘的である"),
        ("おしゃべり", "サービス精神が旺盛 / 話題が豊富 / 社交的である"),
        ("軽薄", "身軽である / 親しみやすい / 適応力が高い"),
        ("不器用", "一生懸命である / 飾らない性格 / 実直である"),
        ("押しが強い", "説得力がある / リーダーシップがある / 情熱的である"),
        ("内弁慶", "身内を大切にする / 内面が豊か / 慎重である"),
        ("デリカシーがない", "率直である / 裏表がない / 素朴である"),
        ("偏屈", "独自の美学がある / こだわりがある / 探究心が強い"),
        ("打算的", "戦略的である / 合理的である / 先見の明がある"),
        ("無計画", "臨機応変である / 今を大切にしている / 柔軟性がある"),
        ("融通が利かない", "信念を曲げない / ルールを遵守する / 誠実である"),
        ("派手", "華やか / 存在感がある / 活気がある"),
        ("怒りっぽい", "正義感が強い / 情熱家である / 真剣に向き合っている"),
        ("未熟", "伸び代がある / 純粋である / 可能性に満ちている"),
        ("しつこい", "粘り強い / 根気がある / 一途である"),
        ("無愛想な", "媚びない / 飾り気がない / 硬派な"),
        ("口うるさい", "細かい点まで目が届く / 指導熱心である / 向上心が高い"),
        ("反抗的", "自分の意見を持っている / 自立心が強い / 批判的思考ができる"),
        ("いい子ぶりっこ", "調和を重んじる / 気配り上手 / 礼儀正しい"),
        ("古臭い", "伝統を重んじている / 落ち着きがある / 本質を追求している"),
        ("流行遅れ", "時代に流されない / 自分のスタイルがある / クラシックである"),
        ("がめつい", "経済観念が発達している / 意欲的である / 向上心が強い"),
        ("お調子者", "ムードメーカーである / 明るい / サービス精神がある"),
        ("目立ちたがり", "存在感がある / 自己表現が豊か / 華がある"),
        ("消極的", "思慮深い / 控えめである / 平和主義である"),
        ("わがまま", "意志がはっきりしている / 自分を大切にする / 主体性がある"),
        ("不愛想な", "実直である / 媚びない / 落ち着いている"),
        ("愛想が良すぎる", "親しみやすい / 社交的である / サービス精神が旺盛"),
        ("ケチケチする", "無駄がない / 管理能力が高い / 堅実である"),
        ("ワンパターン", "安定感がある / 一貫性がある / 伝統を大切にする"),
        ("適当", "大らか / 柔軟性がある / 細かいことに囚われない"),
        ("引っ込み思案", "奥ゆかしい / 慎重である / 謙虚である"),
        ("欲張りな", "向上心がある / 意欲的である / 探究心が強い"),
        ("優しすぎる", "慈悲深い / 献身的である / 受容力がある"),
        ("冷淡な", "冷静沈着である / 公平である / 理性的である"),
        ("不真面目", "遊び心がある / 柔軟である / 楽観的である"),
        ("心配性", "慎重である / 危機管理能力がある / 想像力が豊か"),
        ("無関心", "執着がない / 自立している / 自分の世界を持っている"),
        ("ケチ臭い", "物を大切にする / 節約家である / 堅実である"),
        ("古風な", "趣がある / 伝統を大切にする / 落ち着いている"),
        ("プライドが高い", "自尊心が強い / 高潔である / 誇りを持っている"),
        ("無神経な", "物怖じしない / 大らかである / 精神がタフである"),
        ("打算的な", "合理的である / 先を見通す力がある / 知的である"),
        ("八方美人的な", "誰からも愛される / 調整上手である / 柔軟性が高い"),
        ("地味な", "シックである / 控えめな美しさがある / 堅実である"),
        ("幼稚な", "童心を持っている / 純粋である / 素直である"),
        ("理屈に合わない", "直感的である / 感性を大切にしている / 独創的である"),
        ("頼りない", "守りたくなる / 優しさに溢れている / 謙虚である"),
        ("卑怯な", "戦略的である / 効率を重視する / 賢明である"),
        ("執念深い", "一つのことを忘れない / 粘り強い / 情熱が持続する"),
        ("お人好し", "心が広い / 誠実である / 他者を信じられる"),
        ("能無しの", "これからが楽しみな / 無垢な / 可能性を秘めた"),
        ("馬鹿正直", "一点の曇りもない / 誠実である / 信頼に値する"),
        ("強情な", "芯が強い / 信念がある / 意志を貫く"),
        ("落ち着きのない", "活動的である / 活力に満ちている / 好奇心が旺盛"),
        ("変わり者", "個性的である / 独自の感性がある / 独創的である"),
        ("そっけない", "簡潔である / 媚びない / 実直である"),
        ("おどおどした", "謙虚である / 慎重である / 相手を敬っている"),
        ("派手好きな", "華やかである / 存在感がある / 自己表現を楽しんでいる"),
        ("無茶な", "挑戦心がある / 勇敢である / 枠に囚われない"),
        ("暗い雰囲気", "静寂を愛する / 落ち着きがある / ミステリアスな"),
        ("口が悪い", "率直である / 裏表がない / 正直である"),
        ("どんくさい", "丁寧である / 確実である / 大らかである"),
    ]
    
    st.session_state.all_questions = []
    for i, (word, ans) in enumerate(data_list):
        options = [ans]
        while len(options) < 4:
            dummy = data_list[(i + len(options)) % 100][1]
            if dummy not in options: options.append(dummy)
        import random
        random.shuffle(options)
        st.session_state.all_questions.append({
            "id": i, "word": word, "options": options, "answer": ans
        })

if 'page' not in st.session_state: st.session_state.page = "ホーム"
if 'quiz_index' not in st.session_state: st.session_state.quiz_index = 0

def change_page(page_name):
    st.session_state.page = page_name
    st.session_state.show_result = False

st.title("言の葉 🌿")

# --- ホーム ---
if st.session_state.page == "ホーム":
    st.markdown('<p class="sub-title">〜トゲのある言葉を、美しい言葉に〜</p>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🌿\n問題へ"): change_page("クイズ")
    with col2:
        if st.button("📖\n一覧表"): change_page("一覧表")

# --- クイズ ---
elif st.session_state.page == "クイズ":
    if st.button("← ホーム"): change_page("ホーム")
    q = st.session_state.all_questions[st.session_state.quiz_index]
    st.markdown(f'<div style="background:white;padding:2rem;border-radius:15px;border:1px solid #eef5ee;text-align:center;margin-bottom:2rem;"><p>第 {st.session_state.quiz_index+1} / 100 問</p><h2>{q["word"]}</h2></div>', unsafe_allow_html=True)
    for opt in q['options']:
        if st.button(opt):
            st.session_state.selected = opt
            st.session_state.show_result = True
    if st.session_state.get('show_result'):
        color = "green" if st.session_state.selected == q['answer'] else "red"
        st.markdown(f'<div class="feedback-box"><b>正解:</b> {q["answer"]}</div>', unsafe_allow_html=True)
        if st.button("次へ ➔"):
            st.session_state.quiz_index = (st.session_state.quiz_index + 1) % 100
            st.session_state.show_result = False
            st.rerun()

# --- 一覧表 ---
elif st.session_state.page == "一覧表":
    if st.button("← ホーム"): change_page("ホーム")
    st.markdown('<div class="list-header"><div class="col-no">No</div><div class="col-word">トゲのある言葉</div><div class="col-ans">美しい言い換え</div></div>', unsafe_allow_html=True)
    for q in st.session_state.all_questions:
        st.markdown(f'<div class="list-row"><div class="col-no">{q["id"]+1}</div><div class="col-word">{q["word"]}</div><div class="col-ans">{q["answer"]}</div></div>', unsafe_allow_html=True)

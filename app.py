import streamlit as st
import random

# 页面配置
st.set_page_config(page_title="船长赵毅主役剧抽签", page_icon="🎙️")

# 完整作品数据
DRAMA_DATA = [
    ("开封奇谈 这个包公不太行", "白玉堂"), ("铜钱龛世", "玄悯"), ("离婚前后", "苏言"),
    ("韫色过浓", "周时韫"), ("燎原", "陶晓东"), ("全世界都在等我们分手", "傅落银"),
    ("江山许你", "梁祯"), ("请勿洞察 上", "列维"), ("天才基本法", "林兆生"),
    ("禁止犯规", "霍听澜"), ("伪装者", "明台"), ("年花", "沈落"),
    ("设计师", "陈西安"), ("暗火", "陆迟歇"), ("有药", "楼主"),
    ("遇蛇", "伊墨"), ("剑名不奈何", "徐霜策"), ("长相守", "沈凉生"),
    ("一枝", "易青巍"), ("十号酒馆·判官", "丁通"), ("千秋", "晏无师"),
    ("无双", "崔不去"), ("入赘", "程瀚良"), ("满城衣冠", "傅云宪"),
    ("雪中悍刀行", "徐凤年"), ("北斗", "岳定唐")
]

# 初始化会话状态（记忆用户操作）
if 'history' not in st.session_state:
    st.session_state.history = []  # 记录本次打开页面抽中过的剧
if 'listened' not in st.session_state:
    st.session_state.listened = [] # 记录用户勾选已听的剧

st.title("🎧 船长赵毅主役剧抽签")
st.caption("注：抽中过的剧出现概率会降低；勾选“已听”后不再抽到。")

# --- 侧边栏：用户记录功能 ---
with st.sidebar:
    st.header("我的记录")
    st.write("勾选你已经听完的剧：")
    for drama, role in DRAMA_DATA:
        is_checked = st.checkbox(f"{drama}", key=f"check_{drama}")
        if is_checked and drama not in st.session_state.listened:
            st.session_state.listened.append(drama)
        elif not is_checked and drama in st.session_state.listened:
            st.session_state.listened.remove(drama)
    
    if st.button("清除所有记录"):
        st.session_state.listened = []
        st.session_state.history = []
        st.rerun()

# --- 主界面：抽签逻辑 ---
# 1. 过滤掉已经听过的剧
available_pool = [d for d in DRAMA_DATA if d[0] not in st.session_state.listened]

if st.button("🎲 开始抽取", type="primary", use_container_width=True):
    if not available_pool:
        st.error("所有剧集都听完啦！请在侧边栏取消部分勾选再抽取。")
    else:
        # 2. 计算权重：没抽过的权重10，抽过(history)的权重1
        weights = []
        for d in available_pool:
            if d[0] in st.session_state.history:
                weights.append(5)  # 降低概率
            else:
                weights.append(10) # 正常概率
        
        # 3. 根据权重抽取
        picked = random.choices(available_pool, weights=weights, k=1)[0]
        picked_drama, role = picked
        
        # 4. 更新抽中历史
        if picked_drama not in st.session_state.history:
            st.session_state.history.append(picked_drama)
        
        # 5. 展示结果
        st.balloons()
        st.markdown("### 🎯 抽中作品：")
        st.info(f"《{picked_drama}》")
        st.markdown(f"**角色：** {role}")
        
        if picked_drama in st.session_state.history and weights[available_pool.index(picked)] == 1:
            st.caption("（注：此剧之前抽中过，本次是低概率再次抽中）")

st.divider()

# --- 统计展示 ---
col1, col2 = st.columns(2)
with col1:
    st.metric("剩余待抽", len(available_pool))
with col2:
    st.metric("已标记听完", len(st.session_state.listened))

# 完整清单预览
with st.expander("📖 查看完整库"):
    st.table([{"作品": d[0], "角色": d[1]} for d in DRAMA_DATA])

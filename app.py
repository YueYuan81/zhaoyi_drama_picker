import streamlit as st
import random
import json
from streamlit_javascript import st_javascript

# 1. 页面配置
st.set_page_config(page_title="船长赵毅主役剧抽签", page_icon="🎙️")

# 数据集
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

# 2. 核心：从浏览器读取数据 (增加 key 确保唯一性)
st_data = st_javascript("localStorage.getItem('zhaoyi_records');", key="ls_reader")

# 3. 初始化或更新 session_state
if "listened" not in st.session_state:
    st.session_state.listened = []

# 关键：当 JavaScript 返回数据时，立即同步到 Python
if st_data and st_data != "null":
    try:
        loaded_list = json.loads(st_data)
        # 只有当 session_state 为空（刚打开页面）时才覆盖，避免循环刷新
        if not st.session_state.listened:
            st.session_state.listened = loaded_list
    except:
        pass

if 'history' not in st.session_state:
    st.session_state.history = []

st.title("🎧 船长赵毅主役剧抽签")
st.caption("注：抽中过的剧概率降低；勾选“已听”后不再抽到。")
# --- 侧边栏：记录功能 ---
with st.sidebar:
    st.header("我的记录")
    st.write("勾选已听剧集：")
    
    # 使用临时列表收集勾选结果
    new_selection = []
    for drama, role in DRAMA_DATA:
        # 根据当前 session_state 决定初始值
        default_val = drama in st.session_state.listened
        if st.checkbox(f"{drama}", value=default_val, key=f"chk_{drama}"):
            new_selection.append(drama)
    
    # 只要勾选有变动，就更新 session_state 并保存到浏览器
    if set(new_selection) != set(st.session_state.listened):
        st.session_state.listened = new_selection
        save_js = f"localStorage.setItem('zhaoyi_records', '{json.dumps(new_selection)}');"
        st_javascript(save_js, key="ls_writer")
    
    if st.button("清除所有保存记录"):
        st_javascript("localStorage.removeItem('zhaoyi_records');", key="ls_cleaner")
        st.session_state.listened = []
        st.rerun()

# --- 主界面：抽签逻辑 ---
available_pool = [d for d in DRAMA_DATA if d[0] not in st.session_state.listened]

if st.button("🎲 开始抽取", type="primary", use_container_width=True):
    if not available_pool:
        st.error("所有剧集都听完啦！")
    else:
        # 权重：历史抽中的权重6，没抽中的权重10
        weights = [6 if d[0] in st.session_state.history else 10 for d in available_pool]
        picked = random.choices(available_pool, weights=weights, k=1)[0]
        
        if picked[0] not in st.session_state.history:
            st.session_state.history.append(picked[0])
            
        st.balloons()
        st.markdown(f"### 🎯 抽中作品：\n## 《{picked[0]}》\n**角色：** {picked[1]}")

st.divider()
col1, col2 = st.columns(2)
col1.metric("剩余待抽", len(available_pool))
col2.metric("已标记听完", len(st.session_state.listened))

with st.expander("📖 查看完整库"):
    st.table([{"作品": d[0], "角色": d[1]} for d in DRAMA_DATA])

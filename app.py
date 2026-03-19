import streamlit as st
import random
import json
from streamlit_javascript import st_javascript

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

# --- 关键修改：持久化逻辑 ---

# 1. 从浏览器本地存储读取数据
# st_javascript 会执行 JS 代码并返回结果
get_local_storage = """
    (function() {
        return localStorage.getItem('zhaoyi_listened_records');
    })()
"""
stored_data = st_javascript(get_local_storage)

# 2. 初始化 session_state
if 'listened' not in st.session_state:
    # 如果浏览器里有存过，就加载，否则为空
    if stored_data and stored_data != "null":
        try:
            st.session_state.listened = json.loads(stored_data)
        except:
            st.session_state.listened = []
    else:
        st.session_state.listened = []

if 'history' not in st.session_state:
    st.session_state.history = []

st.title("🎧 船长赵毅主役剧抽签")
st.caption("注：记录保存在您的浏览器中；抽中过的剧概率降低；勾选“已听”后不再抽到。")

# --- 侧边栏：用户记录功能 ---
with st.sidebar:
    st.header("我的记录")
    st.write("勾选你已经听完的剧：")
    
    temp_listened = []
    for drama, role in DRAMA_DATA:
        # 根据 session_state 设定默认打钩状态
        is_already_listened = drama in st.session_state.listened
        if st.checkbox(f"{drama}", value=is_already_listened, key=f"check_{drama}"):
            temp_listened.append(drama)
    
    # 如果勾选发生变化，同步到浏览器存储
    if temp_listened != st.session_state.listened:
        st.session_state.listened = temp_listened
        # 将数据转为 JSON 存入浏览器
        listened_json = json.dumps(temp_listened)
        set_local_storage = f"localStorage.setItem('zhaoyi_listened_records', '{listened_json}');"
        st_javascript(set_local_storage)
    
    if st.button("清除所有记录"):
        st_javascript("localStorage.removeItem('zhaoyi_listened_records');")
        st.session_state.listened = []
        st.session_state.history = []
        st.rerun()

# --- 主界面：抽签逻辑 ---
available_pool = [d for d in DRAMA_DATA if d[0] not in st.session_state.listened]

if st.button("🎲 开始抽取", type="primary", use_container_width=True):
    if not available_pool:
        st.error("所有剧集都听完啦！请在侧边栏取消部分勾选再抽取。")
    else:
        weights = []
        for d in available_pool:
            if d[0] in st.session_state.history:
                weights.append(1)  # 抽过的权重设为1
            else:
                weights.append(10) # 没抽过的权重设为10
        
        picked = random.choices(available_pool, weights=weights, k=1)[0]
        picked_drama, role = picked
        
        if picked_drama not in st.session_state.history:
            st.session_state.history.append(picked_drama)
        
        st.balloons()
        st.markdown("### 🎯 抽中作品：")
        st.info(f"《{picked_drama}》")
        st.markdown(f"**角色：** {role}")
        
        # 如果再次抽中历史里的，给个提示
        if picked_drama in st.session_state.history and len(available_pool) > 1 and weights[available_pool.index(picked)] == 1:
            st.caption("（提示：此剧此前已抽中过，现以较低概率再次出现）")

st.divider()

col1, col2 = st.columns(2)
with col1:
    st.metric("剩余待抽", len(available_pool))
with col2:
    st.metric("已标记听完", len(st.session_state.listened))

with st.expander("📖 查看完整库"):
    st.table([{"作品": d[0], "角色": d[1]} for d in DRAMA_DATA])

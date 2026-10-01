from navigation import home_page, recommender_page
from pathlib import Path
import base64,io,json
from PIL import Image
import streamlit as st
from neo4j_service import *
ROOT=Path(__file__).parent
st.markdown('''<style>
:root{--primary:#1e7ba8;--primary-light:#2b9cc2;--accent:#ff6b5a;--success:#2ecc71;--secondary:#6c5ce7;--text:#2d3436;--text-light:#636e72;--bg-light:#f5f7fa;--border:#dfe6e9;--border-light:#ecf0f1}
.stApp{background:linear-gradient(135deg,#f0f8fb 0%,#f5f7fa 50%,#fafbfd 100%);color:var(--text)}
.block-container{max-width:1280px;padding-top:2.5rem;padding-bottom:3rem}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#1e7ba8 0%,#2b9cc2 100%);border-right:1px solid #ffffff20}
[data-testid="stSidebar"] *{color:#fff!important}
[data-testid="stSidebar"] [role="radiogroup"] label{padding:.6rem .8rem;border-radius:14px;margin:.2rem 0;font-weight:500;transition:all .2s}
[data-testid="stSidebar"] [role="radiogroup"] label:hover{background:#ffffff25;transform:translateX(2px)}
.hero{background:linear-gradient(135deg,#1e7ba8 0%,#2b9cc2 50%,#ff6b5a 100%);padding:48px 40px;border-radius:24px;color:white;box-shadow:0 16px 40px rgba(30,123,168,0.3);margin-bottom:24px;border:1px solid rgba(255,255,255,0.2)}
.hero h1{font-size:2.8rem;margin:0 0 12px;font-weight:800;letter-spacing:-1px}.hero p{font-size:1.1rem;margin:0;color:rgba(255,255,255,0.95)}
.stat{background:white;border:2px solid var(--border-light);border-radius:18px;padding:24px;text-align:center;box-shadow:0 4px 16px rgba(0,0,0,0.08);transition:all .3s}
.stat:hover{transform:translateY(-4px);box-shadow:0 8px 24px rgba(0,0,0,0.12);border-color:var(--primary)}
.stat b{font-size:2.2rem;color:var(--primary);font-weight:800;display:block}.stat span{display:block;color:var(--text-light);margin-top:8px;font-size:.95rem;font-weight:500}
.card,.bike-card{border:2px solid var(--border-light);border-radius:18px;padding:18px;margin-bottom:16px;background:white;box-shadow:0 4px 12px rgba(0,0,0,0.06);transition:all .3s;overflow:hidden}
.card:hover,.bike-card:hover{transform:translateY(-4px);box-shadow:0 8px 24px rgba(30,123,168,0.15);border-color:var(--primary)}
.bike-image{width:100%;height:220px;border-radius:14px;overflow:hidden;background:linear-gradient(135deg,#e8f4fa 0%,#f0f8fb 100%);display:flex;align-items:center;justify-content:center;border:2px solid var(--border-light);margin-bottom:14px}
.bike-image img{width:100%;height:100%;object-fit:cover;display:block}.bike-placeholder{font-size:4rem;opacity:.4}
.bike-name{font-size:1.15rem;font-weight:700;color:var(--text);margin:8px 0 6px;line-height:1.4}.bike-price{color:var(--text-light);font-size:.95rem;margin-bottom:8px}
.pill{display:inline-block;background:linear-gradient(135deg,#e8f4fa,#f0f8fb);color:var(--primary);padding:6px 14px;border-radius:22px;margin:4px;border:1.5px solid var(--primary);font-weight:500;font-size:.85rem;transition:all .2s}
.pill:hover{background:var(--primary);color:white}
.stButton>button{border:0;border-radius:12px;background:linear-gradient(90deg,var(--primary),var(--primary-light));color:white;padding:.6rem 1.4rem;box-shadow:0 6px 16px rgba(30,123,168,0.25);font-weight:600;transition:all .3s;border:2px solid transparent}
.stButton>button:hover{background:linear-gradient(90deg,#165a8e,#2286ab);transform:translateY(-2px);box-shadow:0 8px 20px rgba(30,123,168,0.35);color:white;border:0}
div[data-baseweb="select"]>div,[data-testid="stNumberInput"] input,[data-testid="stTextInput"] input{background:white;border:2px solid var(--border-light)!important;border-radius:12px!important;transition:border .2s;color:var(--text)!important;font-weight:500}
div[data-baseweb="select"]>div:hover,[data-testid="stNumberInput"] input:hover,[data-testid="stTextInput"] input:hover{border-color:var(--primary)!important}
[data-testid="stFileUploader"] section{background:linear-gradient(135deg,#f5f7fa,#f0f8fb);border:2px dashed var(--border);border-radius:16px;transition:all .2s}
[data-baseweb="tab-list"]{gap:.5rem;border-bottom:2px solid var(--border-light)}
[data-baseweb="tab"]{border-radius:12px 12px 0 0;color:var(--text-light);border:2px solid transparent;background:var(--bg-light);transition:all .2s;font-weight:600}
[data-baseweb="tab"][aria-selected="true"]{background:white;color:var(--primary);border-color:var(--primary)}
hr{border-color:var(--border-light)!important}
.section-title{font-size:1.4rem;font-weight:700;color:var(--text);margin:24px 0 16px;padding-bottom:12px;border-bottom:3px solid var(--primary)}
.success-msg{background:linear-gradient(135deg,#d4edda 0%,#c3e6cb 100%);border-left:4px solid #2ecc71;padding:16px;border-radius:12px;color:#155724;font-weight:500}
.info-msg{background:linear-gradient(135deg,#cfe2ff 0%,#b6d4fe 100%);border-left:4px solid var(--primary);padding:16px;border-radius:12px;color:var(--primary);font-weight:500}
</style>''',unsafe_allow_html=True)
with st.sidebar:
 st.markdown('<div style="text-align:center;padding:20px 0;border-bottom:2px solid rgba(255,255,255,0.2);margin-bottom:24px"><h2 style="margin:0;font-size:1.8rem;font-weight:800">🍽️ Food Hub</h2><p style="margin:8px 0 0;font-size:.9rem;opacity:.9">Recommendation System</p></div>', unsafe_allow_html=True)
 if st.button('← กลับหน้าหลัก', use_container_width=True): st.switch_page(home_page)
 st.divider()
 st.markdown('### 👤 ข้อมูลผู้ใช้')
 st.markdown('**ชื่อ:** เนติภัทร์ ใจเด็ด')
 st.markdown('**รหัส:** 664245020')
 st.divider()
 st.markdown('### 📋 เมนูหลัก')
 page=st.radio('เลือกเมนู', ['🎯 แนะนำอาหาร','👥 จัดการคน','🍴 จัดการอาหาร','🕸️ กราฟ'],label_visibility='collapsed')
try: query('RETURN 1')
except Exception as e: st.error('❌ ไม่สามารถเชื่อมต่อ Neo4j'); st.code(str(e)); st.stop()
setup_data()
def hero(): st.markdown('<div class="hero"><h1>🍽️ Food Recommendation</h1><p>ค้นหาเมนูอาหารใหม่จากคำแนะนำของเพื่อน ด้วย Neo4j Graph Database</p></div>',unsafe_allow_html=True)
def summary():
 s=stats(); cols=st.columns(4); vals=[(s['users'],'👤 คน'),(s['foods'],'🍽️ เมนูอาหาร'),(s['friendships'],'🤝 ความเป็นเพื่อน'),(s['orders'],'💬 การเลือก')]
 for c,(v,l) in zip(cols,vals): c.markdown(f'<div class="stat"><b>{v}</b><span>{l}</span></div>',unsafe_allow_html=True)
def image_src(r):
 try:
  if r.get('image_data'):
   return 'data:image/jpeg;base64,' + r['image_data']
  if r.get('image_url'):
   return r['image_url']
 except Exception:
  pass
 return ''

def img(r):
 src=image_src(r)
 if src:
  st.markdown(f'<div class="bike-image"><img src="{src}" alt="food"></div>',unsafe_allow_html=True)
 else:
  st.markdown('<div class="bike-image"><div class="bike-placeholder">🍽️</div></div>',unsafe_allow_html=True)
hero(); summary(); st.write('')
U=users()
if page.startswith('🎯'):
 col1, col2 = st.columns([3, 1])
 with col1:
  u=st.selectbox('เลือกชื่อของคุณ',U,key='rec_user')
 with col2:
  st.write('')
  if st.button('🔄 รีเฟรช', use_container_width=True):
   st.rerun()
 fs=friends(u)
 if fs:
  st.markdown(f'<div class="info-msg"><strong>👥 เพื่อนของ {u}:</strong> {len(fs)} คน</div>', unsafe_allow_html=True)
  st.markdown(' '.join(f'<span class="pill">{x}</span>' for x in fs),unsafe_allow_html=True)
 else:
  st.markdown(f'<div class="info-msg">⚠️ {u} ยังไม่มีเพื่อนในระบบ</div>', unsafe_allow_html=True)
 st.markdown('<div class="section-title">✨ เมนูอาหารแนะนำ</div>', unsafe_allow_html=True)
 rec=recommendations(u)
 if not rec:
  st.markdown(f'<div class="info-msg">💡 ยังไม่มีคำแนะนำใหม่ เพิ่มเพื่อนหรือเลือกเมนูอาหารเพิ่มเติม</div>', unsafe_allow_html=True)
 else:
  st.markdown(f'**พบ {len(rec)} เมนูแนะนำ**')
  cols=st.columns(3)
  for i,r in enumerate(rec):
   with cols[i%3]:
    st.markdown('<div class="card">',unsafe_allow_html=True); img(r); st.markdown(f'<div class="bike-name">{r["name"]}</div>',unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:.85rem;color:#636e72;margin-bottom:12px">💬 เพื่อนที่เลือก</div>', unsafe_allow_html=True)
    st.markdown(' '.join(f'<span class="pill">{x}</span>' for x in r['friend_names']),unsafe_allow_html=True)
    if st.button(f'✅ เลือกอาหารนี้',key='rec'+r['name'], use_container_width=True): order(u,r['name']); st.rerun()
    st.markdown('</div>',unsafe_allow_html=True)
elif page.startswith('👥'):
 t1,t2,t3=st.tabs(['➕ เพิ่มคน','🤝 เพิ่มเพื่อน','🗑️ ลบข้อมูล'])
 with t1:
  st.markdown('<div class="section-title">➕ เพิ่มคนใหม่</div>', unsafe_allow_html=True)
  n=st.text_input('ชื่อคนใหม่', placeholder='เช่น: สมชาย')
  col1, col2 = st.columns([3, 1])
  with col1:
   if st.button('➕ เพิ่มคน', use_container_width=True):
    if n.strip():
     add_user(n)
     st.markdown(f'<div class="success-msg">✅ เพิ่ม {n} สำเร็จ!</div>', unsafe_allow_html=True)
     st.rerun()
    else:
     st.markdown('<div class="info-msg">⚠️ กรุณาใส่ชื่อคน</div>', unsafe_allow_html=True)
 with t2:
  st.markdown('<div class="section-title">🤝 เชื่อมเพื่อนกัน</div>', unsafe_allow_html=True)
  c1,c2=st.columns(2)
  with c1: a=st.selectbox('คนที่ 1',U)
  with c2: b=st.selectbox('คนที่ 2',U,index=min(1,len(U)-1))

  if a != b:
   current_friends = friends(a)
   st.markdown(f'**👥 เพื่อนของ {a} ตอนนี้:** ({len(current_friends)} คน)')
   if current_friends:
    st.markdown(' '.join(f'<span class="pill">{x}</span>' for x in current_friends),unsafe_allow_html=True)
   else:
    st.markdown('*ยังไม่มีเพื่อน*')
   if st.button('🤝 เชื่อมเป็นเพื่อนกัน', use_container_width=True):
    add_friend(a,b)
    st.markdown(f'<div class="success-msg">✅ เพิ่ม {a} และ {b} เป็นเพื่อนสำเร็จ!</div>', unsafe_allow_html=True)
    st.rerun()
  else:
   st.markdown('<div class="info-msg">⚠️ ไม่สามารถเชื่อมคนเดียวกันเป็นเพื่อนได้</div>', unsafe_allow_html=True)
 with t3:
  st.markdown('<div class="section-title">🗑️ ลบข้อมูล</div>', unsafe_allow_html=True)
  delete_option = st.radio('เลือกสิ่งที่ต้องการลบ:', ['ลบความสัมพันธ์เพื่อน', 'ลบคน'], label_visibility='collapsed')

  if delete_option == 'ลบความสัมพันธ์เพื่อน':
   a=st.selectbox('เลือกคน',U,key='rf')
   f=friends(a)
   if f:
    b=st.selectbox('เลือกเพื่อนที่จะลบ',f, key='rf_friend')
    col1, col2 = st.columns([3, 1])
    with col1:
     if st.button('🗑️ ลบความสัมพันธ์', use_container_width=True):
      remove_friend(a,b)
      st.markdown(f'<div class="success-msg">✅ ลบความสัมพันธ์สำเร็จ!</div>', unsafe_allow_html=True)
      st.rerun()
   else:
    st.markdown(f'<div class="info-msg">ℹ️ {a} ไม่มีเพื่อน</div>', unsafe_allow_html=True)
  else:
   st.warning('⚠️ การลบคนจะลบความสัมพันธ์และการเลือกอาหารด้วย')
   d=st.selectbox('เลือกคนที่จะลบ',U,key='du')
   ok=st.checkbox(f'✓ ยืนยันลบ {d}')
   if st.button('🗑️ ลบคน', use_container_width=True) and ok:
    delete_user(d)
    st.markdown(f'<div class="success-msg">✅ ลบ {d} สำเร็จ!</div>', unsafe_allow_html=True)
    st.rerun()
elif page.startswith('🍴'):
 t1,t2,t3=st.tabs(['➕ เพิ่มอาหาร','📋 บันทึกการเลือก','🗑️ ลบอาหาร'])
 with t1:
  st.markdown('<div class="section-title">➕ เพิ่มเมนูอาหารใหม่</div>', unsafe_allow_html=True)
  col1, col2 = st.columns([2, 1])
  with col1:
   n=st.text_input('ชื่ออาหาร', placeholder='เช่น: ส้มตำ')
  with col2:
   st.write('')
  up=st.file_uploader('📸 อัปโหลดรูปภาพ (ไม่บังคับ)',type=['jpg','jpeg','png','webp'], key='food_image')
  if st.button('➕ เพิ่มอาหาร', use_container_width=True):
   if n.strip():
    data=''
    if up:
     im=Image.open(up).convert('RGB'); im.thumbnail((1200,900)); b=io.BytesIO(); im.save(b,'JPEG',quality=88); data=base64.b64encode(b.getvalue()).decode()
    add_food(n,data=data)
    st.markdown(f'<div class="success-msg">✅ เพิ่ม {n} สำเร็จ!</div>', unsafe_allow_html=True)
    st.rerun()
   else:
    st.markdown('<div class="info-msg">⚠️ กรุณาใส่ชื่ออาหาร</div>', unsafe_allow_html=True)
  st.divider()
  st.markdown('<div class="section-title">🍽️ เมนูอาหารในระบบ</div>', unsafe_allow_html=True)
  existing=foods()
  if not existing:
   st.markdown('<div class="info-msg">ℹ️ ยังไม่มีเมนูอาหารในระบบ</div>', unsafe_allow_html=True)
  else:
   st.markdown(f'**ทั้งหมด {len(existing)} เมนู**')
   grid=st.columns(3)
   for i,r in enumerate(existing):
    with grid[i%3]:
     st.markdown('<div class="bike-card">',unsafe_allow_html=True); img(r)
     st.markdown(f'<div class="bike-name">{r["name"]}</div>',unsafe_allow_html=True)
     st.markdown('</div>',unsafe_allow_html=True)
 with t2:
  st.markdown('<div class="section-title">📋 บันทึกการเลือกอาหาร</div>', unsafe_allow_html=True)
  u=st.selectbox('👤 ใครเลือก?',U, key='order_user')
  M=[x['name'] for x in foods()]
  choices=st.multiselect('🍽️ เลือกอาหาร',M, key='order_foods')
  if st.button('📋 บันทึกการเลือก', use_container_width=True):
   if choices:
    for m in choices: order(u,m)
    st.markdown(f'<div class="success-msg">✅ บันทึก {len(choices)} เมนูสำเร็จ!</div>', unsafe_allow_html=True)
    st.rerun()
   else:
    st.markdown('<div class="info-msg">⚠️ กรุณาเลือกอาหาร</div>', unsafe_allow_html=True)
  st.divider()
  st.markdown(f'**📝 {u} เลือกไปแล้ว:**')
  old=ordered(u)
  if not old:
   st.markdown('*ยังไม่มีการเลือก*')
  else:
   for x in old:
    col1, col2, col3 = st.columns([8, 1, 1])
    with col1:
     st.markdown(f'<span class="pill">{x["name"]}</span>',unsafe_allow_html=True)
    with col3:
     if st.button('🗑️', key='o'+x['name'], use_container_width=True):
      remove_order(u,x['name'])
      st.rerun()
 with t3:
  st.markdown('<div class="section-title">🗑️ ลบเมนูอาหาร</div>', unsafe_allow_html=True)
  M=[x['name'] for x in foods()]
  if not M:
   st.markdown('<div class="info-msg">ℹ️ ไม่มีเมนูอาหารให้ลบ</div>', unsafe_allow_html=True)
  else:
   d=st.selectbox('เลือกอาหารที่จะลบ',M, key='del_food')
   st.warning(f'⚠️ การลบ "{d}" จะลบข้อมูลทั้งหมดที่เกี่ยวข้อง')
   if st.button('🗑️ ลบเมนูอาหาร', use_container_width=True):
    delete_food(d)
    st.markdown(f'<div class="success-msg">✅ ลบสำเร็จ!</div>', unsafe_allow_html=True)
    st.rerun()
else:
 st.markdown('<div class="section-title">🕸️ กราฟความสัมพันธ์</div>', unsafe_allow_html=True)
 c1,c2=st.columns([2,1])
 with c1:
  who=c1.selectbox('ไฮไลต์คน',['— ทุกคน —']+U, key='graph_user')
 with c2:
  st.write('')
  show=c2.checkbox('แสดงการเลือก',True)

 fs,os=edges(None if who=='— ทุกคน —' else who,show)
 dot=['graph G {','layout=neato; overlap=false; splines=true; bgcolor="transparent";','node [fontname="Arial"];']
 hi=None if who=='— ทุกคน —' else who
 people=set([x['a'] for x in fs]+[x['b'] for x in fs]+[x['a'] for x in os])
 bikes=set(x['b'] for x in os)
 for p in people:
  color='#1e7ba8' if p==hi else '#b6d4fe'; dot.append(f'{json.dumps("u"+p)} [label={json.dumps(p)},shape=circle,style=filled,fillcolor="{color}",color="white",width=1.2,fontsize="11"];')
 for m in bikes: dot.append(f'{json.dumps("m"+m)} [label={json.dumps(m)},shape=box,style="rounded,filled",fillcolor="#ffd580",color="white",fontsize="10"];')
 seen=set()
 for e in fs:
  k=tuple(sorted((e['a'],e['b'])))
  if k not in seen: dot.append(f'{json.dumps("u"+e["a"])} -- {json.dumps("u"+e["b"])} [color="#2b9cc2",penwidth=2.5];'); seen.add(k)
 for e in os: dot.append(f'{json.dumps("u"+e["a"])} -- {json.dumps("m"+e["b"])} [color="#ff6b5a",style=dashed,penwidth=1.5];')
 dot.append('}')
 st.graphviz_chart('\n'.join(dot),use_container_width=True)

 st.divider()
 col1, col2, col3 = st.columns(3)
 with col1:
  st.markdown(f'<div class="stat"><b>{len(people)}</b><span>👤 ผู้ใช้</span></div>', unsafe_allow_html=True)
 with col2:
  st.markdown(f'<div class="stat"><b>{len(fs)}</b><span>🤝 ความเป็นเพื่อน</span></div>', unsafe_allow_html=True)
 with col3:
  st.markdown(f'<div class="stat"><b>{len(bikes)}</b><span>🍽️ เมนูอาหาร</span></div>', unsafe_allow_html=True)

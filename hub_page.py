from pathlib import Path
import html
import streamlit as st
from navigation import recommender_page

ROOT = Path(__file__).resolve().parent
REPOSITORY = "https://github.com/Poomza999/recommendation_hub"

st.markdown('''<style>
:root{--primary:#1e7ba8;--primary-light:#2b9cc2;--accent:#ff6b5a;--text:#2d3436;--text-light:#636e72;--bg-light:#f5f7fa;--border:#dfe6e9;--border-light:#ecf0f1}
.stApp{background:linear-gradient(135deg,#f0f8fb 0%,#f5f7fa 50%,#fafbfd 100%);color:var(--text)}
[data-testid="stHeader"]{background:transparent}
.block-container{max-width:1600px;padding:2rem 2rem}
.hub-hero{text-align:center;padding:2rem 0 1.5rem}
.hub-badge{display:inline-block;padding:8px 20px;border:2px solid var(--primary);border-radius:30px;font-size:11px;letter-spacing:.16em;color:var(--primary);background:#f0f8fb;font-weight:600}
.hub-hero h1{font-size:clamp(32px,5vw,48px);line-height:1.2;font-weight:800;color:var(--primary);margin:16px 0 12px;padding:0}
.hub-hero p{font-size:16px;color:var(--text-light);line-height:1.8;margin:0}
.st-key-club,.st-key-graph,.st-key-neo4j,.st-key-recommendation{background:white;border:2px solid var(--border-light)!important;border-radius:20px!important;padding:24px!important;box-shadow:0 6px 20px rgba(30,123,168,0.08);box-sizing:border-box!important;transition:all .3s}
.st-key-club:hover,.st-key-graph:hover,.st-key-neo4j:hover,.st-key-recommendation:hover{transform:translateY(-6px);box-shadow:0 12px 32px rgba(30,123,168,0.15);border-color:var(--primary)!important}
.hub-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px}
.hub-icon{width:52px;height:52px;border-radius:14px;background:linear-gradient(135deg,#e8f4fa,#f0f8fb);display:flex;align-items:center;justify-content:center;color:var(--primary)}
.hub-icon svg{width:28px;height:28px;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.hub-number{color:var(--accent);font-size:12px;letter-spacing:.06em;font-weight:600}
.hub-card-title{min-height:68px;color:var(--text);font-size:22px;font-weight:700;line-height:1.6;margin:0 0 8px}
.hub-card-copy{color:var(--text-light);font-size:14px;line-height:1.7;margin:0;min-height:90px}
.st-key-club>[data-testid="stVerticalBlock"],.st-key-graph>[data-testid="stVerticalBlock"],.st-key-neo4j>[data-testid="stVerticalBlock"],.st-key-recommendation>[data-testid="stVerticalBlock"]{min-height:360px;justify-content:space-between}
[data-testid="stLinkButton"] a,[data-testid="stButton"] button,[data-testid="stDownloadButton"] button{border:2px solid var(--primary)!important;border-radius:12px!important;background:linear-gradient(90deg,var(--primary),var(--primary-light))!important;color:white!important;font-size:14px;min-height:44px;box-shadow:0 4px 12px rgba(30,123,168,0.2)!important;font-weight:600;transition:all .3s}
[data-testid="stLinkButton"] a:hover,[data-testid="stButton"] button:hover,[data-testid="stDownloadButton"] button:hover{background:linear-gradient(90deg,#165a8e,#2286ab)!important;border-color:#0d4a7e!important;transform:translateY(-2px);box-shadow:0 6px 16px rgba(30,123,168,0.3)!important;color:white!important}
.hub-footer{border-top:2px solid var(--border-light);margin-top:32px;padding-top:24px;text-align:center;color:var(--text-light);font-size:12px;line-height:1.8;font-weight:500}
@media(max-width:760px){.block-container{padding:1.5rem 1rem}.hub-hero h1{font-size:32px}.hub-card-title{font-size:20px}}
</style>''', unsafe_allow_html=True)

ICONS = {
    "club": '<circle cx="9" cy="7" r="3"/><path d="M3 20v-3a6 6 0 0 1 12 0v3M16 4a3 3 0 0 1 0 6M18 14a5 5 0 0 1 3 5"/>',
    "graph": '<rect x="4" y="3" width="16" height="6" rx="2"/><rect x="4" y="15" width="6" height="6" rx="2"/><rect x="14" y="15" width="6" height="6" rx="2"/><path d="M12 9v3M7 15v-3h10v3"/>',
    "neo4j": '<circle cx="6" cy="6" r="3"/><circle cx="18" cy="8" r="3"/><circle cx="10" cy="19" r="3"/><path d="m9 6 6 1M7 9l2 7m7-5-4 5"/>',
    "recommendation": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><path d="m10 12 2 2 4-5"/>',
}

def heading(kind, number, title, copy):
    st.markdown(f'''<div class="hub-top"><div class="hub-icon"><svg viewBox="0 0 24 24" aria-hidden="true">{ICONS[kind]}</svg></div><span class="hub-number">{number}</span></div><div class="hub-card-title" role="heading" aria-level="2">{html.escape(title)}</div><p class="hub-card-copy">{html.escape(copy)}</p>''', unsafe_allow_html=True)

def notebook_actions(path, colab_link=None, github_link=None):
    if colab_link:
        st.link_button("เปิดการบ้านใน Colab ↗", colab_link, use_container_width=True)
    else:
        st.link_button("เปิดการบ้านใน Colab ↗", f"https://colab.research.google.com/github/Poomza999/recommendation_hub/blob/main/{path}", use_container_width=True)

    if github_link:
        st.link_button("ดูไฟล์บน GitHub ↗", github_link, use_container_width=True)
    else:
        st.link_button("ดูไฟล์บน GitHub ↗", f"{REPOSITORY}/blob/main/{path}", use_container_width=True)

st.markdown('''<div class="hub-hero"><span class="hub-badge">HOMEWORK · RECOMMENDATION HUB</span><h1>รวมการบ้านและระบบแนะนำ</h1><p>ระบบชมรม · กราฟอาหาร · Neo4j<br>เลือกงานที่ต้องการเปิดดูได้จากการ์ดด้านล่าง</p></div>''', unsafe_allow_html=True)

columns = st.columns(4, gap="medium")
with columns[0], st.container(border=True, height=400, key="club"):
    heading("club", "01 / CLUB", "ระบบชมรมด้วย Neo4j", "งานระบบชมรม: นักศึกษา ชมรม ความสัมพันธ์ และคำสั่ง Cypher พร้อมเอกสาร PDF")
    with st.container():
        st.link_button("เปิดการบ้านบน GitHub ↗", f"{REPOSITORY}/blob/main/homework/664245020_club_system.pdf", use_container_width=True)
        pdf_path = ROOT / "homework/664245020_club_system.pdf"
        if pdf_path.exists():
            st.download_button("ดาวน์โหลดเอกสาร PDF ↓", pdf_path.read_bytes(), file_name="664245020_club_system.pdf", mime="application/pdf", use_container_width=True)
        else:
            st.info("ไฟล์ PDF ไม่พบในเซิร์ฟเวอร์นี้")
with columns[1], st.container(border=True, height=400, key="graph"):
    heading("graph", "02 / GRAPH", "อาหารด้วย Graph", "สร้างกราฟผู้ใช้และอาหารด้วย Python / NetworkX เพื่อสำรวจความชอบและแนวทางแนะนำ")
    with st.container():
        notebook_actions("Food_Recommender_664245020.ipynb", "https://colab.research.google.com/drive/16CKky7HnsxLHrYA6MP7TEHohKO9UVZwx?usp=sharing", "https://github.com/Poomza999/recommendation_hub/blob/main/homework/Food_Recommender_664245020.ipynb")

with columns[2], st.container(border=True, height=400, key="neo4j"):
    heading("neo4j", "03 / NEO4J", "อาหารด้วย Neo4j", "วิเคราะห์ความสัมพันธ์และแนะนำอาหารด้วย Neo4j จากไฟล์การบ้าน Food Recommendation ที่แนบมา")
    with st.container():
        notebook_actions("homework/Food_recommendation_neo4j.ipynb")
with columns[3], st.container(border=True, height=400, key="recommendation"):
    heading("recommendation", "04 / APPLICATION", "ระบบแนะนำอาหาร", "ทดลองระบบแนะนำ เลือกผู้ใช้ จัดการข้อมูลอาหาร และสำรวจกราฟความสัมพันธ์ภายในแอป")
    with st.container():
        if st.button("เข้าสู่ระบบแนะนำ →", use_container_width=True):
            st.switch_page(recommender_page)
        st.link_button("ดูโค้ดโปรเจกต์บน GitHub ↗", REPOSITORY, use_container_width=True)

st.markdown('''<div class="hub-footer">เนติภัทร์ ใจเด็ด · รหัสนักศึกษา 664245020<br>Food Recommendation Project</div>''', unsafe_allow_html=True)

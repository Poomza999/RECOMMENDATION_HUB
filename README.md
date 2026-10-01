# 🍽️ Food Recommendation Hub

> ระบบแนะนำอาหารฉลาดด้วย Neo4j Graph Database - ค้นหาเมนูอาหารใหม่จากคำแนะนำของเพื่อน

[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red?style=flat-square&logo=streamlit)](https://streamlit.io/)
[![Neo4j](https://img.shields.io/badge/Neo4j-5.0+-brightgreen?style=flat-square&logo=neo4j)](https://neo4j.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-Poomza999-black?style=flat-square&logo=github)](https://github.com/Poomza999/recommendation_hub)

---

## 📑 สารบัญ

- [ภาพรวม](#ภาพรวม)
- [คุณสมบัติ](#-คุณสมบัติ)
- [ติดตั้ง](#-ติดตั้ง)
- [การใช้งาน](#-การใช้งาน)
- [โครงสร้างโปรเจกต์](#-โครงสร้างโปรเจกต์)
- [ฐานข้อมูล](#-ฐานข้อมูล)
- [งานการศึกษา](#-งานการศึกษา)
- [ผู้จัดทำ](#-ผู้จัดทำ)

---

## 📖 ภาพรวม

**Food Recommendation Hub** เป็นระบบแนะนำอาหารฉลาด ที่ใช้ **Neo4j Graph Database** ในการวิเคราะห์ความสัมพันธ์ระหว่าง:

| องค์ประกอบ | รายละเอียด |
|-----------|----------|
| 👤 **ผู้ใช้** | ข้อมูลคนในระบบ |
| 🍽️ **เมนูอาหาร** | ข้อมูลอาหารพร้อมรูปภาพ |
| 🤝 **ความเป็นเพื่อน** | ความสัมพันธ์ระหว่างคน |
| 💬 **การเลือกอาหาร** | ประวัติการเลือกเมนู |

ระบบจะวิเคราะห์เส้นทาง: `User → ORDERED → Food ← ORDERED ← User → ORDERED → Food` เพื่อแนะนำเมนูอาหารใหม่

---

## ✨ คุณสมบัติ

### 🎯 แนะนำอาหาร
- 🔍 วิเคราะห์เมนูที่เพื่อนชอบ
- 💡 แนะนำเมนูใหม่ที่ผู้ใช้ยังไม่ได้ลอง
- 📊 แสดงจำนวนเพื่อนที่เลือกแต่ละเมนู

### 👥 จัดการผู้ใช้
- ➕ เพิ่มผู้ใช้ใหม่
- 🤝 เชื่อมความสัมพันธ์เพื่อน
- 🗑️ ลบผู้ใช้และข้อมูลที่เกี่ยวข้อง

### 🍴 จัดการเมนูอาหาร
- 📸 อัปโหลดรูปภาพพร้อมเพิ่มเมนู
- 📋 บันทึกประวัติการเลือกอาหาร
- 🗑️ ลบเมนูออกจากระบบ

### 🕸️ กราฟความสัมพันธ์
- 📡 แสดงกราฟ Network ของผู้ใช้และอาหาร
- 🎨 ไฮไลต์ผู้ใช้เฉพาะเพื่อดูรายละเอียด
- 👁️ เปิด/ปิดการแสดงข้อมูลการเลือก

---

## 🔧 ติดตั้ง

### ข้อกำหนดของระบบ

```bash
Python 3.8+
Neo4j 5.0+ (AuraDB Free หรือ Local Instance)
pip (Python Package Manager)
```

### ขั้นตอนการติดตั้ง

**1️⃣ Clone Repository**
```bash
git clone https://github.com/Poomza999/recommendation_hub.git
cd recommendation_hub
```

**2️⃣ สร้าง Virtual Environment**
```bash
# Linux / Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

**3️⃣ ติดตั้ง Dependencies**
```bash
pip install -r requirements.txt
```

**4️⃣ ตั้งค่า Neo4j Credentials**

สร้างไฟล์ `.env` ในโฟลเดอร์หลัก:
```bash
cp .env.example .env
```

แก้ไขไฟล์ `.env` ด้วย Neo4j Credentials ของคุณ:
```env
NEO4J_URI=neo4j+s://your_uri.databases.neo4j.io
NEO4J_USERNAME=your_username
NEO4J_PASSWORD=your_password
NEO4J_DATABASE=your_database
```

**5️⃣ รันแอปพลิเคชัน**
```bash
streamlit run app.py
```

หน้าเว็บจะเปิดที่ **http://localhost:8501**

---

## 🚀 การใช้งาน

### 📱 หน้าแรม (Hub Page)
- 📊 แสดงภาพรวมโปรเจกต์ 4 ส่วน
- 🔗 ลิงก์ไปยัง Colab และ GitHub
- ▶️ ปุ่มเข้าสู่ระบบแนะนำอาหาร

### 🎯 เมนู: แนะนำอาหาร
```
1. เลือกชื่อของคุณ
   ↓
2. ดูเพื่อนของคุณ
   ↓
3. ดูรายการเมนูแนะนำ
   ↓
4. คลิก "✅ เลือกอาหารนี้" เพื่อบันทึก
```

### 👥 เมนู: จัดการคน
| Tab | ฟังก์ชัน |
|-----|---------|
| ➕ เพิ่มคน | ใส่ชื่อและคลิก "เพิ่มคน" |
| 🤝 เพิ่มเพื่อน | เลือกคน 2 คนและเชื่อม |
| 🗑️ ลบ | ลบความสัมพันธ์หรือลบคน |

### 🍴 เมนู: จัดการอาหาร
| Tab | ฟังก์ชัน |
|-----|---------|
| ➕ เพิ่มอาหาร | ใส่ชื่อและอัปโหลดรูป |
| 📋 บันทึกการเลือก | เลือกคนและเมนู |
| 🗑️ ลบ | ลบเมนูออกจากระบบ |

### 🕸️ เมนู: กราฟความสัมพันธ์
```
1. เลือกผู้ใช้ (ไฮไลต์)
   ↓
2. เปิด/ปิดการแสดงการเลือก
   ↓
3. ดูกราฟ Network ของทุกคน
   ↓
4. ดูสถิติด้านล่าง
```

---

## 📁 โครงสร้างโปรเจกต์

```
recommendation_hub/
│
├── app.py                      # ไฟล์หลัก - จุดเข้าแอป
├── navigation.py               # การนำทางระหว่างหน้า
├── hub_page.py                 # หน้าแรกรวมโปรเจกต์
├── recommender_page.py         # หน้าระบบแนะนำอาหาร
├── neo4j_service.py            # บริการ Neo4j
│
├── data.json                   # ข้อมูล (ผู้ใช้, อาหาร, ความสัมพันธ์)
├── .env                        # ตั้งค่า Neo4j (สร้างจาก .env.example)
├── .env.example                # ตัวอย่าง .env
│
├── assets/                     # โฟลเดอร์เก็บรูปภาพอาหาร
│   ├── Basil Minced Pork.jpg
│   ├── Tom Yum Goong.jpg
│   ├── Crab Fried Rice.jpg
│   ├── Green Curry.jpg
│   ├── Pad Thai.jpg
│   ├── Massaman Curry.jpg
│   ├── Stir-fried Morning Glory.jpg
│   ├── Papaya Salad.jpg
│   ├── Khao Soi.jpg
│   └── Stir-fried Mixed Vegetables.jpg
│
├── homework/                   # ไฟล์การศึกษา
│   ├── 664245020_club_system.pdf
│   └── Food_recommendation_neo4j.ipynb
│
├── requirements.txt            # Dependencies
└── README.md                   # ไฟล์นี้
```

---

## 🗄️ ฐานข้อมูล

### โหนด (Nodes)

#### User Node
```cypher
CREATE (u:User {name: "John"})
```
- `name` - ชื่อผู้ใช้ (UNIQUE)

#### Food Node
```cypher
CREATE (f:Food {
  name: "Pad Thai",
  image_url: "assets/Pad Thai.jpg",
  image_data: "... base64 image ..."
})
```
- `name` - ชื่ออาหาร (UNIQUE)
- `image_url` - URL รูปภาพ
- `image_data` - รูปภาพ Base64

### ความสัมพันธ์ (Relationships)

#### FRIEND - ความเป็นเพื่อน
```cypher
(User)-[:FRIEND]-(User)
```
เชื่อมความสัมพันธ์เพื่อน 2 ทิศทาง

#### ORDERED - การเลือกอาหาร
```cypher
(User)-[:ORDERED]->(Food)
{ordered_at: date("2026-09-01")}
```
บันทึกว่าผู้ใช้เลือกอาหาร

### Cypher Query Examples

**ค้นหาเพื่อนของ John:**
```cypher
MATCH (u:User {name:"John"})-[:FRIEND]-(f:User)
RETURN f.name ORDER BY f.name
```

**ค้นหาอาหารที่ John เลือก:**
```cypher
MATCH (u:User {name:"John"})-[:ORDERED]->(f:Food)
RETURN f.name, f.image_url, f.image_data
```

**แนะนำอาหารสำหรับ John:**
```cypher
MATCH (me:User {name:"John"})
      -[:FRIEND]-(friend:User)
      -[:ORDERED]->(food:Food)
WHERE NOT EXISTS {
    MATCH (me)-[:ORDERED]->(food)
}
RETURN 
    food.name AS name,
    food.image_url AS image_url,
    food.image_data AS image_data,
    COLLECT(DISTINCT friend.name) AS friend_names,
    COUNT(DISTINCT friend) AS score
ORDER BY score DESC, food.name
```

---

## 📊 ข้อมูลตัวอย่าง

### สถิติ
```
👤 10 คน
🍽️ 10 เมนูอาหาร
🤝 10 ความเป็นเพื่อน
💬 31 การเลือก
```

### ผู้ใช้ (10 คน)
John, Alice, Bob, Emma, David, Sarah, Michael, Laura, James, Emily

### เมนูอาหาร (10 จาน)
1. Basil Minced Pork
2. Tom Yum Goong
3. Crab Fried Rice
4. Green Curry
5. Pad Thai
6. Massaman Curry
7. Stir-fried Morning Glory
8. Papaya Salad
9. Khao Soi
10. Stir-fried Mixed Vegetables

---

## 💻 เทคโนโลยี

| เทคโนโลยี | รุ่น | วัตถุประสงค์ |
|-----------|------|-----------|
| **Python** | 3.8+ | ภาษาโปรแกรมหลัก |
| **Streamlit** | 1.28+ | Web UI Framework |
| **Neo4j** | 5.0+ | Graph Database |
| **Pillow** | 9.0+ | จัดการรูปภาพ |
| **python-dotenv** | 1.0+ | Environment Config |

ดู [requirements.txt](requirements.txt) สำหรับรายละเอียดเต็ม

---

## 🎓 งานการศึกษา

โปรเจกต์นี้ได้จาก **3 งานการศึกษา**:

### 01 - ระบบชมรมด้วย Neo4j
- 📄 [เปิดไฟล์ PDF](homework/664245020_club_system.pdf)
- ✍️ วิเคราะห์ระบบชมรม นักศึกษา และเขียน Cypher Query

### 02 - Food Recommender ด้วย Graph
- 📓 [เปิด Notebook](https://github.com/Poomza999/recommendation_hub/blob/main/homework/Food_Recommender_664245020.ipynb)
- ☁️ [เปิด Google Colab](https://colab.research.google.com/drive/16CKky7HnsxLHrYA6MP7TEHohKO9UVZwx?usp=sharing)
- 🔗 สร้างกราฟด้วย NetworkX

### 03 - Food Recommender ด้วย Neo4j
- 📓 [เปิด Notebook](homework/Food_recommendation_neo4j.ipynb)
- 💾 ใช้ Neo4j Graph Database สำหรับแนะนำอาหาร

---

## 📈 Workflow

```
🚀 เปิดแอป
   ↓
🗂️ เลือกหน้า
   ├─ 📄 Hub Page
   └─ 🎯 Recommender Page
   ↓
💾 เชื่อมต่อ Neo4j
   ↓
📦 โหลดข้อมูล (data.json)
   ↓
🎮 ทำงาน
   ├─ ➕ เพิ่ม (Create)
   ├─ 📖 ดึง (Read)
   ├─ ✏️ แก้ไข (Update)
   └─ 🗑️ ลบ (Delete)
   ↓
💡 แนะนำอาหาร (Graph Analysis)
```

---

## 👤 ผู้จัดทำ

| ข้อมูล | รายละเอียด |
|-------|-----------|
| **ชื่อ** | เนติภัทร์ ใจเด็ด |
| **รหัสนักศึกษา** | 664245020 |
| **สถาบัน** | Chiang Mai University |
| **GitHub** | [@Poomza999](https://github.com/Poomza999) |
| **Email** | netiphat.2502@gmail.com |

---

## 📜 License

[MIT License](LICENSE) - อิสระในการใช้งาน แก้ไข และแจกจ่าย

---

## 🤝 Contribute

ยินดีรับการมีส่วนร่วม:
1. Fork Repository
2. สร้าง Feature Branch (`git checkout -b feature/YourFeature`)
3. Commit Changes (`git commit -m 'Add YourFeature'`)
4. Push to Branch (`git push origin feature/YourFeature`)
5. Open Pull Request

---

## 🙏 ขอบคุณ

- **Neo4j** - Graph Database Platform
- **Streamlit** - Web Framework
- **Chiang Mai University** - สนับสนุน

---

<div align="center">

**สร้างสรรค์และพัฒนาเพื่ออนาคต** 🚀

[⬆ กลับขึ้นด้านบน](#-food-recommendation-hub)

</div>

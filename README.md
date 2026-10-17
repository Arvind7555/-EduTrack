# EduTrack: Student Attendance & Grade Management System
### (विद्यार्थी उपस्थिति एवं ग्रेड प्रबंधन प्रणाली)

एक आधुनिक, सुरक्षित और परिपूर्ण वेब-आधारित प्रबंधन प्रणाली (Student Attendance & Grade Management System) जो कॉलेज और विश्वविद्यालय स्तर के लिए डिज़ाइन की गई है।

---

## 🌟 मुख्य फोकस क्षेत्र (Core Focus Areas)

### 1. 🎓 Students (विद्यार्थी प्रबंधन)
- **छात्र पंजीकरण**: Roll Number, पूरा नाम, ईमेल, फोन, विभाग (Department), सेमेस्टर और लिंग।
- **विस्तृत छात्र प्रोफाइल (Student Profile)**: 
  - व्यक्तिगत जानकारी एवं स्थिति (Active/Inactive)
  - संचयी सीजीपीए (Cumulative CGPA) और क्लास मेरिट रैंक
  - कुल उपस्थिति प्रतिशत और पात्रता स्थिति (Eligible / Warning / Critical)
  - विषयवार उपस्थिति और अंक रिकॉर्ड
- **कोर्स नामांकन (Course Enrollment)**: किसी भी छात्र को किसी भी कोर्स में तुरंत नामांकित या हटाना।

### 2. 📚 Courses (कोर्स एवं विषय)
- **कोर्स विवरण**: Course Code (उदा. CS301), Course Title, Department, Credits (3-4 credits), और Professor/Instructor।
- **नामांकित छात्र गणना**: प्रत्येक कोर्स में कितने छात्र नामांकित हैं, उसकी लाइव स्थिति।
- **कोर्स CRUD**: नए कोर्स जोड़ें, अपडेट करें या हटाएं।

### 3. 📅 Attendance Percentage (उपस्थिति प्रतिशत एवं 75% पात्रता नियम)
- **दैनिक उपस्थिति प्रविष्टि (Daily Attendance Sheet)**:
  - तारीख और कोर्स चुनें।
  - एक क्लिक में **"Mark All Present"** या **"Mark All Absent"**।
  - 4 स्थितियां: **Present** (हरा), **Late** (पीला), **Excused** (नीला), **Absent** (लाल)।
- **स्वचालित उपस्थिति प्रतिशत गणना (Automatic % Calculation)**:
  $$\text{Attendance \%} = \frac{\text{Attended Sessions}}{\text{Total Sessions Held}} \times 100$$
  *(Present = 1.0, Late = 0.5, Excused = 1.0)*
- **75% पात्रता थ्रेशोल्ड और अलर्ट्स (Exam Eligibility Rules)**:
  - 🟢 **Safe ($\ge 75\%$)**: परीक्षा के लिए पूरी तरह पात्र (Eligible).
  - 🟡 **Warning ($65\% - 74.9\%$)**: सतर्कता सूचना (Attendance Warning).
  - 🔴 **Critical ($< 65\%$)**: परीक्षा से वंचित होने का जोखिम (Disqualification Alert).
- **उपस्थिति रिपोर्ट और CSV डाउनलोड**: सभी छात्रों की पूरी उपस्थिति मैट्रिक्स को CSV फॉर्मेट में एक्सपोर्ट करें।

### 4. 📝 Marks, Grading & CGPA (अंक और ग्रेडिंग प्रणाली)
- **अंक प्रविष्टि संरचना**:
  - मिडटर्म परीक्षा (Midterm Exam) - अधिकतम 30 अंक
  - असाइनमेंट / आंतरिक मूल्यांकन (Assignments / Quizzes) - अधिकतम 20 अंक
  - अंतिम परीक्षा (Final Examination) - अधिकतम 50 अंक
  - **कुल योग**: 100 अंक
- **लाइव ग्रेड गणना (Real-time Dynamic Grade Calculation)**: अंक टाइप करते ही बिना पेज रीलोड किए कुल अंक, लेटर ग्रेड और ग्रेड पॉइंट अपडेट होते हैं।
- **यूनिवर्सिटी ग्रेडिंग पैमाना (Standard Scale)**:
  - **$90 - 100$**: **A+** (Grade Point: 10.0) — *Outstanding*
  - **$80 - 89.9$**: **A** (Grade Point: 9.0) — *Excellent*
  - **$70 - 79.9$**: **B+** (Grade Point: 8.0) — *Very Good*
  - **$60 - 69.9$**: **B** (Grade Point: 7.0) — *Good*
  - **$50 - 59.9$**: **C** (Grade Point: 6.0) — *Average*
  - **$40 - 49.9$**: **D** (Grade Point: 5.0) — *Pass*
  - **$< 40$**: **F** (Grade Point: 0.0) — *Fail*
- **सीजीपीए सूत्र (Cumulative GPA)**:
  $$\text{CGPA} = \frac{\sum (\text{Course Credits} \times \text{Grade Point})}{\sum \text{Course Credits}}$$

### 5. 🏆 Grade Ranking & Leaderboard (रैंकिंग और मेरिट सूची)
- **पोडियम डिस्प्ले (Top 3 Rankers)**:
  - 🥇 **Rank #1**: गोल्ड मेडल बैज, टॉपर विवरण
  - 🥈 **Rank #2**: सिल्वर मेडल बैज
  - 🥉 **Rank #3**: ब्रॉन्ज मेडल बैज
- **क्लास मेरिट तालिका (Full Class Ranking Table)**:
  - रैंक क्रम (Rank #1, #2, ...)
  - कुल क्रेडिट्स, कुल अंक, औसत प्रतिशत (Average %)
  - संचयी सीजीपीए (CGPA / 10)
  - पर्सेंटाइल स्कोर (Percentile Standing)
  - उपस्थिति प्रतिशत और स्थिति
- **आधिकारिक ट्रांसक्रिप्ट / रिपोर्ट कार्ड (Official Printable Report Card)**:
  - प्रत्येक छात्र के लिए तैयार प्रिंटेबल ग्रेड शीट (`window.print()` / Save as PDF).
  - कॉलेज हेडर, विषयवार अंक विवरण, उपस्थिति प्रमाणपत्र, और आधिकारिक हस्ताक्षर ब्लॉक (Class Advisor, Controller of Examinations, Principal).
- **रैंकिंग डेटा CSV एक्सपोर्ट**: पूरी मेरिट सूची को एक क्लिक में डाउनलोड करें।

---

## 🛠️ तकनीकी संरचना (Tech Stack)

| घटक | तकनीक |
| :--- | :--- |
| **Backend** | Python 3.15, Flask 3.1.3 |
| **Database** | SQLite3 (Zero-setup, auto-created in `data/school.db`) |
| **Frontend** | HTML5, CSS3, JavaScript (ES6+), Bootstrap 5.3, FontAwesome 6 |
| **Charts** | Chart.js 4.4 (Doughnut & Bar charts) |
| **Styling** | Custom Responsive CSS (Glassmorphism, Badges, Print Styles) |

---

## 📂 प्रोजेक्ट फाइल स्ट्रक्चर (Project Structure)

```text
Student Attendance & Grade Management/
│
├── app.py                     # मुख्य फ्लास्क एप्लिकेशन और सभी रूट हैंडलर्स
├── database.py                # डेटाबेस कनेक्शन, स्कीमा और टेबल्स
├── models.py                  # बिजनेस लॉजिक, अटेंडेंस %, ग्रेडिंग और रैंकिंग एल्गोरिदम
├── seed_data.py               # रियलिस्टिक टेस्ट डेटा (12 छात्र, 5 कोर्सेज, 1000+ उपस्थिति, अंक)
│
├── static/
│   ├── css/
│   │   └── style.css          # कस्टम डिज़ाइन, पोडियम, बैज और A4 प्रिंट स्टाइलशीट
│   └── js/
│       └── main.js            # लाइव अंक गणना, बल्क उपस्थिति टॉगल, लाइव टेबल सर्च
│
├── templates/
│   ├── base.html              # साइडबार नेविगेशन, अलर्ट्स और लेआउट
│   ├── dashboard.html         # मुख्य एनालिटिक्स डैशबोर्ड (KPI कार्ड्स, चार्ट्स, वॉचलिस्ट)
│   ├── students.html          # छात्र डायरेक्टरी, सर्च, फिल्टर, ऐड/डिलीट मोडल
│   ├── student_detail.html    # विस्तृत छात्र प्रोफाइल, उपस्थिति मैट्रिक्स, मार्क्स
│   ├── courses.html           # कोर्स प्रबंधन और नामांकन संख्या
│   ├── attendance.html        # दैनिक उपस्थिति प्रविष्टि शीट
│   ├── attendance_report.html # उपस्थिति प्रतिशत विश्लेषण और 75% थ्रेशोल्ड
│   ├── marks.html             # अंक प्रविष्टि और रियल-टाइम ग्रेड कैलकुलेटर
│   ├── ranking.html           # क्लास-वाइज ग्रेड रैंकिंग लीडरबोर्ड और पोडियम
│   └── report_card.html       # आधिकारिक प्रिंटेबल रिपोर्ट कार्ड / ट्रांसक्रिप्ट
│
├── data/
│   └── school.db              # SQLite डेटाबेस फाइल
│
├── run.bat                    # Windows के लिए 1-क्लिक स्टार्टर बैच फाइल
├── requirements.txt           # आवश्यक पायथन लाइब्रेरीज़
└── README.md                  # विस्तृत गाइड और डाक्यूमेंटेशन
```

---

## 🚀 चलाने का तरीका (How to Run)

### तरीका 1: एक क्लिक में (Recommended for Windows)
प्रोजेक्ट फोल्डर में मौजूद `run.bat` फाइल पर डबल-क्लिक करें:
1. यह स्वचालित रूप से डेटाबेस जांचेगा।
2. यदि डेटाबेस नहीं है, तो तुरंत रियलिस्टिक सैंपल डेटा भर देगा।
3. आपके ब्राउज़र में `http://127.0.0.1:5000` खुल जाएगा!

---

### तरीका 2: टर्मिनल / कमांड प्रॉम्प्ट के माध्यम से

1. **कमांड प्रॉम्प्ट खोलें और प्रोजेक्ट डायरेक्टरी में जाएं:**
   ```bash
   cd "c:\Users\ASUS\Desktop\Student Attendance & Grade Management"
   ```

2. **आवश्यक लाइब्रेरी इंस्टॉल करें (यदि पहले से न हों):**
   ```bash
   python -m pip install -r requirements.txt
   ```

3. **डेमो डेटा भरें (Optional - यदि फ्रेश डेटा चाहिए):**
   ```bash
   python seed_data.py
   ```

4. **सर्वर प्रारंभ करें:**
   ```bash
   python app.py
   ```

5. **ब्राउज़र में खोलें:**
   ```text
   http://127.0.0.1:5000
   ```

---

## 💡 मुख्य विशेषताएं और उपयोग निर्देश

1. **Dashboard (`/`)**:
   - कुल छात्र, सक्रिय कोर्स, कक्षा औसत उपस्थिति %, और औसत अंक का तुरंत अवलोकन।
   - 75% से कम उपस्थिति वाले छात्रों का ऑटो-अलर्ट बॉक्स।
   - इंटरैक्टिव चार्ट्स: ग्रेड वितरण और कोर्स परफॉरमेंस।

2. **Mark Attendance (`/attendance`)**:
   - कोर्स और तारीख चुनें।
   - "Mark All Present" पर क्लिक करें और जो छात्र अनुपस्थित हैं उनके आगे "Absent" या "Late" सेलेक्ट करके सेव करें।

3. **Attendance % Report (`/attendance/report`)**:
   - विषयवार या पूरे कॉलेज का अटेंडेंस प्रतिशत देखें।
   - 75% क्राइटेरिया के आधार पर Safe, Warning, या Critical स्थिति।
   - CSV में डाउनलोड करने की सुविधा।

4. **Marks & Grades (`/marks`)**:
   - कोर्स चुनें और छात्रों के Midterm (30), Assignment (20), Final (50) अंक दर्ज करें।
   - अंक टाइप करते ही Total, Grade, और Grade Point स्क्रीन पर तुरंत बदल जाते हैं।

5. **Grade Ranking (`/ranking`)**:
   - क्लास के टॉप 3 छात्रों के लिए गोल्ड 🥇, सिल्वर 🥈, और ब्रॉन्ज 🥉 पोडियम कार्ड।
   - सीजीपीए और पर्सेंटाइल के अनुसार पूरी मेरिट सूची।
   - CSV एक्सपोर्ट बटन।

6. **Official Report Card (`/report-card/<id>`)**:
   - किसी भी छात्र के सामने "Report" बटन दबाएं।
   - एक A4 साइज फॉर्मेटेड ट्रांसक्रिप्ट खुलेगा। "Print / Save as PDF" दबाकर प्रिंट या पीडीएफ बनाएं।

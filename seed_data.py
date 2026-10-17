import random
from datetime import datetime, timedelta
from database import init_db, get_db
from models import calculate_grade

def seed_database():
    print("Initializing fresh database tables...")
    init_db()

    with get_db() as conn:
        cursor = conn.cursor()
        
        # Clear existing data
        cursor.execute("DELETE FROM attendance")
        cursor.execute("DELETE FROM marks")
        cursor.execute("DELETE FROM enrollments")
        cursor.execute("DELETE FROM courses")
        cursor.execute("DELETE FROM students")
        
        # 1. Sample Courses
        courses_data = [
            ("CS301", "Data Structures & Algorithms", "Computer Science", 4, "Dr. Rajesh Sharma", 3),
            ("CS302", "Database Management Systems", "Computer Science", 4, "Prof. Anita Verma", 3),
            ("CS303", "Operating Systems", "Computer Science", 3, "Dr. Vikram Sethi", 3),
            ("CS304", "Computer Networks", "Computer Science", 3, "Prof. Priya Nair", 3),
            ("CS305", "Software Engineering", "Computer Science", 3, "Dr. Amit Kulkarni", 3),
        ]
        
        course_ids = []
        for code, name, dept, cred, inst, sem in courses_data:
            cursor.execute('''
                INSERT INTO courses (course_code, course_name, department, credits, instructor, semester)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (code, name, dept, cred, inst, sem))
            course_ids.append(cursor.lastrowid)
        
        print(f"Added {len(course_ids)} courses.")

        # 2. Sample Students
        students_data = [
            ("CS2024-001", "Aarav", "Sharma", "aarav.sharma@college.edu", "9876543210", "Computer Science", 3, "Male"),
            ("CS2024-002", "Diya", "Patel", "diya.patel@college.edu", "9876543211", "Computer Science", 3, "Female"),
            ("CS2024-003", "Rohan", "Mehta", "rohan.mehta@college.edu", "9876543212", "Computer Science", 3, "Male"),
            ("CS2024-004", "Ananya", "Iyer", "ananya.iyer@college.edu", "9876543213", "Computer Science", 3, "Female"),
            ("CS2024-005", "Kabir", "Singh", "kabir.singh@college.edu", "9876543214", "Computer Science", 3, "Male"),
            ("CS2024-006", "Sneha", "Gupta", "sneha.gupta@college.edu", "9876543215", "Computer Science", 3, "Female"),
            ("CS2024-007", "Arjun", "Reddy", "arjun.reddy@college.edu", "9876543216", "Computer Science", 3, "Male"),
            ("CS2024-008", "Pooja", "Chopra", "pooja.chopra@college.edu", "9876543217", "Computer Science", 3, "Female"),
            ("CS2024-009", "Vivaan", "Joshi", "vivaan.joshi@college.edu", "9876543218", "Computer Science", 3, "Male"),
            ("CS2024-010", "Ishita", "Roy", "ishita.roy@college.edu", "9876543219", "Computer Science", 3, "Female"),
            ("CS2024-011", "Aditya", "Verma", "aditya.verma@college.edu", "9876543220", "Computer Science", 3, "Male"),
            ("CS2024-012", "Kavya", "Nair", "kavya.nair@college.edu", "9876543221", "Computer Science", 3, "Female"),
        ]

        student_ids = []
        for roll, fn, ln, email, phone, dept, sem, gender in students_data:
            cursor.execute('''
                INSERT INTO students (roll_number, first_name, last_name, email, phone, department, semester, gender)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (roll, fn, ln, email, phone, dept, sem, gender))
            student_ids.append(cursor.lastrowid)

        print(f"Added {len(student_ids)} students.")

        # 3. Enroll students into all courses
        for sid in student_ids:
            for cid in course_ids:
                cursor.execute('''
                    INSERT INTO enrollments (student_id, course_id)
                    VALUES (?, ?)
                ''', (sid, cid))

        # 4. Generate 18 Class Dates for Attendance
        today = datetime.now()
        dates = []
        cur = today - timedelta(days=28)
        while len(dates) < 18:
            if cur.weekday() < 5: # Monday to Friday
                dates.append(cur.strftime('%Y-%m-%d'))
            cur += timedelta(days=1)

        # Student attendance profile profiles:
        # High attendees (>90%): Aarav, Diya, Ananya, Aditya
        # Medium attendees (75-88%): Sneha, Rohan, Pooja, Ishita, Kavya
        # Warning attendees (65-74%): Kabir, Vivaan
        # Critical low attendance (<65%): Arjun Reddy
        attendance_probabilities = {
            1: 0.96, # Aarav
            2: 0.94, # Diya
            3: 0.83, # Rohan
            4: 0.97, # Ananya
            5: 0.70, # Kabir (Warning)
            6: 0.88, # Sneha
            7: 0.58, # Arjun (Critical <65%)
            8: 0.82, # Pooja
            9: 0.68, # Vivaan (Warning)
            10: 0.85, # Ishita
            11: 0.92, # Aditya
            12: 0.86  # Kavya
        }

        attendance_records = 0
        for sid in student_ids:
            prob = attendance_probabilities.get(sid, 0.85)
            for cid in course_ids:
                for dt in dates:
                    rand_val = random.random()
                    if rand_val < prob:
                        status = 'Present'
                    elif rand_val < prob + 0.05:
                        status = 'Late'
                    elif rand_val < prob + 0.08:
                        status = 'Excused'
                    else:
                        status = 'Absent'

                    cursor.execute('''
                        INSERT INTO attendance (student_id, course_id, date, status, remarks)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (sid, cid, dt, status, 'Regular class'))
                    attendance_records += 1

        print(f"Generated {attendance_records} attendance records.")

        # 5. Generate Marks for Each Student & Course
        # Profiles for academic performance:
        # Top rankers (88-98 avg): Diya Patel, Ananya Iyer, Aarav Sharma
        # Strong performers (75-87 avg): Sneha Gupta, Aditya Verma, Rohan Mehta
        # Average performers (60-74 avg): Pooja Chopra, Ishita Roy, Kavya Nair
        # Struggling performers: Vivaan Joshi, Kabir Singh, Arjun Reddy
        student_performance_ranges = {
            1: (24, 29, 16, 20, 40, 48), # Aarav (High)
            2: (26, 30, 18, 20, 43, 50), # Diya (Topper #1 / #2)
            3: (20, 26, 14, 18, 33, 42), # Rohan
            4: (27, 30, 19, 20, 45, 50), # Ananya (Topper)
            5: (14, 20, 10, 15, 22, 34), # Kabir
            6: (22, 27, 15, 19, 36, 44), # Sneha
            7: (12, 18, 8, 14, 18, 30),  # Arjun (Low)
            8: (18, 24, 13, 17, 30, 39), # Pooja
            9: (15, 21, 11, 16, 24, 35), # Vivaan
            10: (20, 25, 14, 18, 32, 41), # Ishita
            11: (23, 28, 16, 20, 38, 46), # Aditya
            12: (19, 25, 13, 18, 31, 40), # Kavya
        }

        marks_count = 0
        for sid in student_ids:
            ranges = student_performance_ranges.get(sid, (18, 25, 12, 18, 30, 42))
            for cid in course_ids:
                mid = round(random.uniform(ranges[0], ranges[1]), 1)
                assign = round(random.uniform(ranges[2], ranges[3]), 1)
                final = round(random.uniform(ranges[4], ranges[5]), 1)
                total = round(mid + assign + final, 1)
                total = min(100.0, max(0.0, total))
                
                grade, gp, desc = calculate_grade(total)

                cursor.execute('''
                    INSERT INTO marks (student_id, course_id, midterm_marks, assignment_marks, final_marks, total_marks, grade, grade_point, remarks)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (sid, cid, mid, assign, final, total, grade, gp, desc))
                marks_count += 1

        print(f"Generated {marks_count} marks evaluations.")
        conn.commit()

    print("Sample demo data seeded successfully!")

if __name__ == '__main__':
    seed_database()

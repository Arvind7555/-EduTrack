from database import get_db

def calculate_grade(total_marks):
    """
    Calculate letter grade and grade point based on total marks (0-100).
    Scale:
      90 - 100: A+ (10.0) - Outstanding
      80 - 89.9: A  (9.0) - Excellent
      70 - 79.9: B+ (8.0) - Very Good
      60 - 69.9: B  (7.0) - Good
      50 - 59.9: C  (6.0) - Average
      40 - 49.9: D  (5.0) - Pass
      Below 40:  F  (0.0) - Fail
    """
    marks = round(float(total_marks), 2)
    if marks >= 90:
        return 'A+', 10.0, 'Outstanding'
    elif marks >= 80:
        return 'A', 9.0, 'Excellent'
    elif marks >= 70:
        return 'B+', 8.0, 'Very Good'
    elif marks >= 60:
        return 'B', 7.0, 'Good'
    elif marks >= 50:
        return 'C', 6.0, 'Average'
    elif marks >= 40:
        return 'D', 5.0, 'Pass'
    else:
        return 'F', 0.0, 'Fail'

# ----------------- Students -----------------
def get_all_students(search_query=None, department=None, semester=None):
    with get_db() as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM students WHERE 1=1"
        params = []
        if search_query:
            query += " AND (roll_number LIKE ? OR first_name LIKE ? OR last_name LIKE ? OR email LIKE ?)"
            wildcard = f"%{search_query.strip()}%"
            params.extend([wildcard, wildcard, wildcard, wildcard])
        if department:
            query += " AND department = ?"
            params.append(department)
        if semester:
            query += " AND semester = ?"
            params.append(semester)
        
        query += " ORDER BY roll_number ASC"
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

def get_student_by_id(student_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def add_student(roll_number, first_name, last_name, email, phone, department, semester, gender):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO students (roll_number, first_name, last_name, email, phone, department, semester, gender)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (roll_number.strip().upper(), first_name.strip(), last_name.strip(), email.strip().lower(), phone.strip() if phone else None, department, semester, gender))
        conn.commit()
        return cursor.lastrowid

def update_student(student_id, roll_number, first_name, last_name, email, phone, department, semester, gender, status):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE students
            SET roll_number = ?, first_name = ?, last_name = ?, email = ?, phone = ?, department = ?, semester = ?, gender = ?, status = ?
            WHERE id = ?
        ''', (roll_number.strip().upper(), first_name.strip(), last_name.strip(), email.strip().lower(), phone.strip() if phone else None, department, semester, gender, status, student_id))
        conn.commit()

def delete_student(student_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        conn.commit()

# ----------------- Courses -----------------
def get_all_courses(search_query=None):
    with get_db() as conn:
        cursor = conn.cursor()
        query = '''
            SELECT c.*, COUNT(e.student_id) as enrolled_count
            FROM courses c
            LEFT JOIN enrollments e ON c.id = e.course_id
            WHERE 1=1
        '''
        params = []
        if search_query:
            query += " AND (c.course_code LIKE ? OR c.course_name LIKE ? OR c.instructor LIKE ?)"
            wildcard = f"%{search_query.strip()}%"
            params.extend([wildcard, wildcard, wildcard])
        query += " GROUP BY c.id ORDER BY c.course_code ASC"
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

def get_course_by_id(course_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT c.*, COUNT(e.student_id) as enrolled_count
            FROM courses c
            LEFT JOIN enrollments e ON c.id = e.course_id
            WHERE c.id = ?
            GROUP BY c.id
        ''', (course_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def add_course(course_code, course_name, department, credits, instructor, semester):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO courses (course_code, course_name, department, credits, instructor, semester)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (course_code.strip().upper(), course_name.strip(), department, credits, instructor.strip(), semester))
        conn.commit()
        return cursor.lastrowid

def update_course(course_id, course_code, course_name, department, credits, instructor, semester):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE courses
            SET course_code = ?, course_name = ?, department = ?, credits = ?, instructor = ?, semester = ?
            WHERE id = ?
        ''', (course_code.strip().upper(), course_name.strip(), department, credits, instructor.strip(), semester, course_id))
        conn.commit()

def delete_course(course_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM courses WHERE id = ?", (course_id,))
        conn.commit()

# ----------------- Enrollments -----------------
def enroll_student(student_id, course_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO enrollments (student_id, course_id)
            VALUES (?, ?)
        ''', (student_id, course_id))
        # Also ensure a default marks row exists
        cursor.execute('''
            INSERT OR IGNORE INTO marks (student_id, course_id, midterm_marks, assignment_marks, final_marks, total_marks, grade, grade_point)
            VALUES (?, ?, 0, 0, 0, 0, 'F', 0.0)
        ''', (student_id, course_id))
        conn.commit()

def unenroll_student(student_id, course_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM enrollments WHERE student_id = ? AND course_id = ?", (student_id, course_id))
        cursor.execute("DELETE FROM marks WHERE student_id = ? AND course_id = ?", (student_id, course_id))
        cursor.execute("DELETE FROM attendance WHERE student_id = ? AND course_id = ?", (student_id, course_id))
        conn.commit()

def get_enrolled_courses_for_student(student_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT c.*, e.enrollment_date
            FROM courses c
            JOIN enrollments e ON c.id = e.course_id
            WHERE e.student_id = ?
            ORDER BY c.course_code ASC
        ''', (student_id,))
        return [dict(row) for row in cursor.fetchall()]

def get_enrolled_students_for_course(course_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT s.*, e.enrollment_date
            FROM students s
            JOIN enrollments e ON s.id = e.student_id
            WHERE e.course_id = ?
            ORDER BY s.roll_number ASC
        ''', (course_id,))
        return [dict(row) for row in cursor.fetchall()]

# ----------------- Attendance Management -----------------
def record_bulk_attendance(course_id, date, attendance_data):
    """
    attendance_data: list of dicts with keys: student_id, status, remarks
    """
    with get_db() as conn:
        cursor = conn.cursor()
        for item in attendance_data:
            student_id = item['student_id']
            status = item['status']
            remarks = item.get('remarks', '')
            cursor.execute('''
                INSERT INTO attendance (student_id, course_id, date, status, remarks)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(student_id, course_id, date) DO UPDATE SET
                    status = excluded.status,
                    remarks = excluded.remarks
            ''', (student_id, course_id, date, status, remarks))
        conn.commit()

def get_attendance_for_course_and_date(course_id, date):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT s.id as student_id, s.roll_number, s.first_name, s.last_name,
                   COALESCE(a.status, 'Present') as status,
                   a.remarks
            FROM students s
            JOIN enrollments e ON s.id = e.student_id
            LEFT JOIN attendance a ON a.student_id = s.id AND a.course_id = ? AND a.date = ?
            WHERE e.course_id = ?
            ORDER BY s.roll_number ASC
        ''', (course_id, date, course_id))
        return [dict(row) for row in cursor.fetchall()]

def get_attendance_percentage(student_id=None, course_id=None):
    """
    Calculates total classes, attended classes, and percentage.
    Weightage: Present = 1, Late = 0.5, Excused = 1, Absent = 0.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        query = '''
            SELECT 
                COUNT(*) as total_records,
                SUM(CASE WHEN status = 'Present' THEN 1 
                         WHEN status = 'Late' THEN 0.5 
                         WHEN status = 'Excused' THEN 1 
                         ELSE 0 END) as attended_weighted,
                SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END) as present_count,
                SUM(CASE WHEN status = 'Absent' THEN 1 ELSE 0 END) as absent_count,
                SUM(CASE WHEN status = 'Late' THEN 1 ELSE 0 END) as late_count,
                SUM(CASE WHEN status = 'Excused' THEN 1 ELSE 0 END) as excused_count
            FROM attendance
            WHERE 1=1
        '''
        params = []
        if student_id:
            query += " AND student_id = ?"
            params.append(student_id)
        if course_id:
            query += " AND course_id = ?"
            params.append(course_id)

        cursor.execute(query, params)
        row = cursor.fetchone()
        
        total = row['total_records'] if row and row['total_records'] else 0
        attended = row['attended_weighted'] if row and row['attended_weighted'] else 0.0
        
        percentage = round((attended / total) * 100, 1) if total > 0 else 0.0
        
        # Determine status
        if total == 0:
            status = 'No Data'
            status_class = 'secondary'
        elif percentage >= 75.0:
            status = 'Safe'
            status_class = 'success'
        elif percentage >= 65.0:
            status = 'Warning'
            status_class = 'warning'
        else:
            status = 'Critical'
            status_class = 'danger'

        return {
            'total_classes': total,
            'attended_weighted': attended,
            'present_count': row['present_count'] or 0,
            'absent_count': row['absent_count'] or 0,
            'late_count': row['late_count'] or 0,
            'excused_count': row['excused_count'] or 0,
            'percentage': percentage,
            'status': status,
            'status_class': status_class
        }

def get_student_course_attendance_matrix(student_id):
    """Get breakdown of attendance across all enrolled courses for a given student."""
    courses = get_enrolled_courses_for_student(student_id)
    matrix = []
    for c in courses:
        stats = get_attendance_percentage(student_id=student_id, course_id=c['id'])
        matrix.append({
            'course_id': c['id'],
            'course_code': c['course_code'],
            'course_name': c['course_name'],
            'credits': c['credits'],
            **stats
        })
    return matrix

def get_all_students_attendance_summary(course_id=None):
    """Returns attendance summary for all students (optionally filtered by course)."""
    with get_db() as conn:
        cursor = conn.cursor()
        query = '''
            SELECT s.id as student_id, s.roll_number, s.first_name, s.last_name, s.department, s.semester,
                   COUNT(a.id) as total_classes,
                   SUM(CASE WHEN a.status = 'Present' THEN 1 
                            WHEN a.status = 'Late' THEN 0.5 
                            WHEN a.status = 'Excused' THEN 1 
                            ELSE 0 END) as attended_weighted,
                   SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) as present_count,
                   SUM(CASE WHEN a.status = 'Absent' THEN 1 ELSE 0 END) as absent_count,
                   SUM(CASE WHEN a.status = 'Late' THEN 1 ELSE 0 END) as late_count
            FROM students s
        '''
        params = []
        if course_id:
            query += '''
                JOIN enrollments e ON s.id = e.student_id AND e.course_id = ?
                LEFT JOIN attendance a ON s.id = a.student_id AND a.course_id = ?
            '''
            params.extend([course_id, course_id])
        else:
            query += " LEFT JOIN attendance a ON s.id = a.student_id "
            
        query += " GROUP BY s.id ORDER BY s.roll_number ASC"
        cursor.execute(query, params)
        rows = cursor.fetchall()

        summary = []
        for r in rows:
            tot = r['total_classes'] or 0
            att = r['attended_weighted'] or 0.0
            pct = round((att / tot) * 100, 1) if tot > 0 else 0.0
            
            if tot == 0:
                status = 'No Records'
                status_class = 'secondary'
            elif pct >= 75.0:
                status = 'Safe'
                status_class = 'success'
            elif pct >= 65.0:
                status = 'Warning'
                status_class = 'warning'
            else:
                status = 'Critical'
                status_class = 'danger'
                
            summary.append({
                'student_id': r['student_id'],
                'roll_number': r['roll_number'],
                'name': f"{r['first_name']} {r['last_name']}",
                'department': r['department'],
                'semester': r['semester'],
                'total_classes': tot,
                'attended_weighted': att,
                'present_count': r['present_count'] or 0,
                'absent_count': r['absent_count'] or 0,
                'late_count': r['late_count'] or 0,
                'percentage': pct,
                'status': status,
                'status_class': status_class
            })
        return summary

# ----------------- Marks & Grades -----------------
def save_student_marks(student_id, course_id, midterm_marks, assignment_marks, final_marks, remarks=''):
    mid = round(float(midterm_marks or 0), 2)
    assign = round(float(assignment_marks or 0), 2)
    fin = round(float(final_marks or 0), 2)
    
    # Cap to max values if necessary: Midterm 30, Assign 20, Final 50 => Total 100
    total = round(mid + assign + fin, 2)
    total = min(100.0, max(0.0, total))
    
    grade, grade_point, desc = calculate_grade(total)
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO marks (student_id, course_id, midterm_marks, assignment_marks, final_marks, total_marks, grade, grade_point, remarks)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(student_id, course_id) DO UPDATE SET
                midterm_marks = excluded.midterm_marks,
                assignment_marks = excluded.assignment_marks,
                final_marks = excluded.final_marks,
                total_marks = excluded.total_marks,
                grade = excluded.grade,
                grade_point = excluded.grade_point,
                remarks = excluded.remarks
        ''', (student_id, course_id, mid, assign, fin, total, grade, grade_point, remarks))
        conn.commit()

def get_marks_for_student(student_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT m.*, c.course_code, c.course_name, c.credits, c.instructor
            FROM courses c
            JOIN enrollments e ON c.id = e.course_id
            LEFT JOIN marks m ON m.student_id = e.student_id AND m.course_id = c.id
            WHERE e.student_id = ?
            ORDER BY c.course_code ASC
        ''', (student_id,))
        return [dict(row) for row in cursor.fetchall()]

def get_course_marks_sheet(course_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT s.id as student_id, s.roll_number, s.first_name, s.last_name, s.department,
                   m.id as mark_id,
                   COALESCE(m.midterm_marks, 0) as midterm_marks,
                   COALESCE(m.assignment_marks, 0) as assignment_marks,
                   COALESCE(m.final_marks, 0) as final_marks,
                   COALESCE(m.total_marks, 0) as total_marks,
                   COALESCE(m.grade, 'F') as grade,
                   COALESCE(m.grade_point, 0.0) as grade_point,
                   m.remarks
            FROM students s
            JOIN enrollments e ON s.id = e.student_id
            LEFT JOIN marks m ON m.student_id = s.id AND m.course_id = e.course_id
            WHERE e.course_id = ?
            ORDER BY m.total_marks DESC, s.roll_number ASC
        ''', (course_id,))
        return [dict(row) for row in cursor.fetchall()]

# ----------------- Grade Ranking & Leaderboard -----------------
def get_overall_rankings():
    """
    Computes overall CGPA and percentage ranking for all students.
    CGPA = Sum(credits * grade_point) / Sum(credits)
    Percentile = ((Total - Rank + 1) / Total) * 100
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                s.id as student_id,
                s.roll_number,
                s.first_name,
                s.last_name,
                s.department,
                s.semester,
                COUNT(m.course_id) as enrolled_count,
                COALESCE(SUM(c.credits * m.grade_point), 0.0) as total_weighted_gp,
                COALESCE(SUM(c.credits), 0) as total_credits,
                COALESCE(SUM(m.total_marks), 0.0) as aggregate_marks,
                COALESCE(AVG(m.total_marks), 0.0) as average_marks,
                COALESCE(SUM(CASE WHEN m.grade = 'F' THEN 1 ELSE 0 END), 0) as failed_courses
            FROM students s
            JOIN enrollments e ON s.id = e.student_id
            JOIN courses c ON e.course_id = c.id
            LEFT JOIN marks m ON m.student_id = s.id AND m.course_id = c.id
            GROUP BY s.id
            ORDER BY (CASE WHEN SUM(c.credits) > 0 THEN SUM(c.credits * m.grade_point)*1.0 / SUM(c.credits) ELSE 0 END) DESC,
                     SUM(m.total_marks) DESC
        ''')
        rows = cursor.fetchall()

    rankings = []
    total_students = len(rows)

    for idx, r in enumerate(rows):
        rank = idx + 1
        tot_credits = r['total_credits'] or 0
        weighted_gp = r['total_weighted_gp'] or 0.0
        cgpa = round(weighted_gp / tot_credits, 2) if tot_credits > 0 else 0.0
        avg_marks = round(r['average_marks'] or 0.0, 2)
        
        # Calculate overall letter grade from CGPA
        if cgpa >= 9.0:
            overall_grade = 'A+'
        elif cgpa >= 8.0:
            overall_grade = 'A'
        elif cgpa >= 7.0:
            overall_grade = 'B+'
        elif cgpa >= 6.0:
            overall_grade = 'B'
        elif cgpa >= 5.0:
            overall_grade = 'C'
        elif cgpa >= 4.0:
            overall_grade = 'D'
        else:
            overall_grade = 'F'

        percentile = round(((total_students - rank + 1) / total_students) * 100, 1) if total_students > 0 else 100.0

        # Attendance stats
        att_stats = get_attendance_percentage(student_id=r['student_id'])

        rankings.append({
            'rank': rank,
            'student_id': r['student_id'],
            'roll_number': r['roll_number'],
            'name': f"{r['first_name']} {r['last_name']}",
            'department': r['department'],
            'semester': r['semester'],
            'enrolled_count': r['enrolled_count'],
            'total_credits': tot_credits,
            'aggregate_marks': round(r['aggregate_marks'], 2),
            'average_marks': avg_marks,
            'cgpa': cgpa,
            'overall_grade': overall_grade,
            'failed_courses': r['failed_courses'],
            'percentile': percentile,
            'attendance_pct': att_stats['percentage'],
            'attendance_status': att_stats['status'],
            'attendance_class': att_stats['status_class']
        })

    return rankings

def get_student_report_card(student_id):
    """Generates all details needed for an official student transcript / report card."""
    student = get_student_by_id(student_id)
    if not student:
        return None

    marks_list = get_marks_for_student(student_id)
    attendance_matrix = get_student_course_attendance_matrix(student_id)
    overall_attendance = get_attendance_percentage(student_id=student_id)
    
    # Calculate GPA
    total_credits = sum(m.get('credits', 0) for m in marks_list)
    weighted_gp = sum(m.get('credits', 0) * (m.get('grade_point') or 0.0) for m in marks_list)
    cgpa = round(weighted_gp / total_credits, 2) if total_credits > 0 else 0.0
    
    total_marks_obtained = sum(m.get('total_marks', 0) or 0 for m in marks_list)
    max_possible_marks = len(marks_list) * 100
    overall_percentage = round((total_marks_obtained / max_possible_marks) * 100, 2) if max_possible_marks > 0 else 0.0
    
    # Find rank
    rankings = get_overall_rankings()
    student_rank = None
    total_class_students = len(rankings)
    for r in rankings:
        if r['student_id'] == student_id:
            student_rank = r['rank']
            break

    # Determine final result
    has_failed = any((m.get('grade') == 'F') for m in marks_list)
    result_status = 'FAIL' if has_failed else 'PASS'

    return {
        'student': student,
        'marks': marks_list,
        'attendance_matrix': attendance_matrix,
        'overall_attendance': overall_attendance,
        'total_credits': total_credits,
        'cgpa': cgpa,
        'total_marks_obtained': total_marks_obtained,
        'max_possible_marks': max_possible_marks,
        'overall_percentage': overall_percentage,
        'rank': student_rank or '-',
        'total_students': total_class_students,
        'result_status': result_status
    }

# ----------------- Dashboard Analytics -----------------
def get_dashboard_analytics():
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Student count
        cursor.execute("SELECT COUNT(*) FROM students")
        total_students = cursor.fetchone()[0]

        # Course count
        cursor.execute("SELECT COUNT(*) FROM courses")
        total_courses = cursor.fetchone()[0]

        # Total attendance records and present percentage
        cursor.execute('''
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN status = 'Present' THEN 1 
                         WHEN status = 'Late' THEN 0.5 
                         WHEN status = 'Excused' THEN 1 
                         ELSE 0 END) as attended
            FROM attendance
        ''')
        att_row = cursor.fetchone()
        tot_att = att_row['total'] or 0
        attended = att_row['attended'] or 0.0
        avg_attendance_pct = round((attended / tot_att) * 100, 1) if tot_att > 0 else 0.0

        # Class average marks
        cursor.execute("SELECT AVG(total_marks) FROM marks WHERE total_marks > 0")
        avg_marks_row = cursor.fetchone()[0]
        class_avg_marks = round(avg_marks_row, 1) if avg_marks_row else 0.0

        # Grade distribution (A+, A, B+, B, C, D, F)
        cursor.execute('''
            SELECT grade, COUNT(*) as count 
            FROM marks 
            WHERE total_marks > 0 
            GROUP BY grade
        ''')
        grade_dist_raw = {row['grade']: row['count'] for row in cursor.fetchall()}
        grade_distribution = {
            'A+': grade_dist_raw.get('A+', 0),
            'A': grade_dist_raw.get('A', 0),
            'B+': grade_dist_raw.get('B+', 0),
            'B': grade_dist_raw.get('B', 0),
            'C': grade_dist_raw.get('C', 0),
            'D': grade_dist_raw.get('D', 0),
            'F': grade_dist_raw.get('F', 0),
        }

        # Course performance averages
        cursor.execute('''
            SELECT c.course_code, c.course_name, AVG(m.total_marks) as avg_score
            FROM courses c
            LEFT JOIN marks m ON c.id = m.course_id
            GROUP BY c.id
            ORDER BY c.course_code ASC
        ''')
        course_performance = [
            {
                'course_code': r['course_code'],
                'course_name': r['course_name'],
                'avg_score': round(r['avg_score'] or 0, 1)
            } for r in cursor.fetchall()
        ]

    # Overall rankings for Top 5
    all_rankings = get_overall_rankings()
    top_5 = all_rankings[:5]

    # Low attendance alert (< 75%)
    all_att = get_all_students_attendance_summary()
    low_attendance_students = [s for s in all_att if s['total_classes'] > 0 and s['percentage'] < 75.0]

    return {
        'total_students': total_students,
        'total_courses': total_courses,
        'avg_attendance_pct': avg_attendance_pct,
        'class_avg_marks': class_avg_marks,
        'grade_distribution': grade_distribution,
        'course_performance': course_performance,
        'top_rankers': top_5,
        'low_attendance_students': low_attendance_students
    }

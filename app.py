import os
import io
import csv
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, Response, jsonify
import models
from database import init_db, get_db
from seed_data import seed_database

app = Flask(__name__)
app.secret_key = 'edutrack_secret_key_student_management_2024'

# Ensure database and tables exist at startup
init_db()
try:
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM students")
        if cur.fetchone()[0] == 0:
            seed_database()
except Exception as e:
    print(f"Startup check: {e}")

# ----------------- Dashboard -----------------
@app.route('/')
def dashboard():
    stats = models.get_dashboard_analytics()
    return render_template('dashboard.html', stats=stats)

# ----------------- Students -----------------
@app.route('/students')
def students():
    search = request.args.get('search', '').strip()
    department = request.args.get('department', '').strip()
    semester = request.args.get('semester', '').strip()
    
    student_list = models.get_all_students(
        search_query=search or None,
        department=department or None,
        semester=int(semester) if semester and semester.isdigit() else None
    )
    all_courses = models.get_all_courses()
    return render_template('students.html', students=student_list, courses=all_courses, search=search, selected_dept=department, selected_sem=semester)

@app.route('/students/add', methods=['POST'])
def add_student():
    roll_number = request.form.get('roll_number')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    department = request.form.get('department', 'Computer Science')
    semester = int(request.form.get('semester', 1))
    gender = request.form.get('gender', 'Male')
    course_ids = request.form.getlist('course_ids')

    try:
        student_id = models.add_student(roll_number, first_name, last_name, email, phone, department, semester, gender)
        # Enroll in selected courses
        for cid in course_ids:
            models.enroll_student(student_id, int(cid))
        flash(f"Student {first_name} {last_name} ({roll_number}) successfully added!", "success")
    except Exception as e:
        flash(f"Error adding student: {str(e)}", "danger")

    return redirect(url_for('students'))

@app.route('/students/<int:student_id>')
def student_detail(student_id):
    student = models.get_student_by_id(student_id)
    if not student:
        flash("Student not found.", "warning")
        return redirect(url_for('students'))

    enrolled_courses = models.get_enrolled_courses_for_student(student_id)
    all_courses = models.get_all_courses()
    attendance_matrix = models.get_student_course_attendance_matrix(student_id)
    marks_list = models.get_marks_for_student(student_id)
    overall_attendance = models.get_attendance_percentage(student_id=student_id)

    # Calculate CGPA
    tot_credits = sum(m.get('credits', 0) for m in marks_list)
    weighted_gp = sum(m.get('credits', 0) * (m.get('grade_point') or 0.0) for m in marks_list)
    cgpa = round(weighted_gp / tot_credits, 2) if tot_credits > 0 else 0.0

    # Determine rank
    rankings = models.get_overall_rankings()
    student_rank = '-'
    for r in rankings:
        if r['student_id'] == student_id:
            student_rank = r['rank']
            break

    enrolled_ids = {c['id'] for c in enrolled_courses}
    available_courses = [c for c in all_courses if c['id'] not in enrolled_ids]

    return render_template(
        'student_detail.html',
        student=student,
        enrolled_courses=enrolled_courses,
        available_courses=available_courses,
        attendance_matrix=attendance_matrix,
        marks_list=marks_list,
        overall_attendance=overall_attendance,
        cgpa=cgpa,
        rank=student_rank
    )

@app.route('/students/<int:student_id>/edit', methods=['POST'])
def edit_student(student_id):
    roll_number = request.form.get('roll_number')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    department = request.form.get('department')
    semester = int(request.form.get('semester', 1))
    gender = request.form.get('gender')
    status = request.form.get('status', 'Active')

    try:
        models.update_student(student_id, roll_number, first_name, last_name, email, phone, department, semester, gender, status)
        flash("Student updated successfully!", "success")
    except Exception as e:
        flash(f"Error updating student: {str(e)}", "danger")

    return redirect(url_for('student_detail', student_id=student_id))

@app.route('/students/<int:student_id>/delete', methods=['POST'])
def delete_student(student_id):
    try:
        models.delete_student(student_id)
        flash("Student removed successfully.", "info")
    except Exception as e:
        flash(f"Error deleting student: {str(e)}", "danger")
    return redirect(url_for('students'))

@app.route('/students/<int:student_id>/enroll', methods=['POST'])
def enroll_student_course(student_id):
    course_id = request.form.get('course_id')
    if course_id:
        models.enroll_student(student_id, int(course_id))
        flash("Enrolled in course successfully!", "success")
    return redirect(url_for('student_detail', student_id=student_id))

@app.route('/students/<int:student_id>/unenroll/<int:course_id>', methods=['POST'])
def unenroll_student_course(student_id, course_id):
    models.unenroll_student(student_id, course_id)
    flash("Unenrolled from course.", "info")
    return redirect(url_for('student_detail', student_id=student_id))

# ----------------- Courses -----------------
@app.route('/courses')
def courses():
    search = request.args.get('search', '').strip()
    course_list = models.get_all_courses(search_query=search or None)
    return render_template('courses.html', courses=course_list, search=search)

@app.route('/courses/add', methods=['POST'])
def add_course():
    code = request.form.get('course_code')
    name = request.form.get('course_name')
    dept = request.form.get('department', 'Computer Science')
    credits = int(request.form.get('credits', 3))
    instructor = request.form.get('instructor')
    semester = int(request.form.get('semester', 1))

    try:
        models.add_course(code, name, dept, credits, instructor, semester)
        flash(f"Course {code} - {name} created successfully!", "success")
    except Exception as e:
        flash(f"Error adding course: {str(e)}", "danger")

    return redirect(url_for('courses'))

@app.route('/courses/<int:course_id>/edit', methods=['POST'])
def edit_course(course_id):
    code = request.form.get('course_code')
    name = request.form.get('course_name')
    dept = request.form.get('department')
    credits = int(request.form.get('credits', 3))
    instructor = request.form.get('instructor')
    semester = int(request.form.get('semester', 1))

    try:
        models.update_course(course_id, code, name, dept, credits, instructor, semester)
        flash("Course updated successfully!", "success")
    except Exception as e:
        flash(f"Error updating course: {str(e)}", "danger")

    return redirect(url_for('courses'))

@app.route('/courses/<int:course_id>/delete', methods=['POST'])
def delete_course(course_id):
    try:
        models.delete_course(course_id)
        flash("Course deleted successfully.", "info")
    except Exception as e:
        flash(f"Error deleting course: {str(e)}", "danger")
    return redirect(url_for('courses'))

# ----------------- Attendance Management -----------------
@app.route('/attendance')
def attendance():
    all_courses = models.get_all_courses()
    selected_course_id = request.args.get('course_id')
    selected_date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))

    enrolled_students = []
    selected_course = None

    if selected_course_id and selected_course_id.isdigit():
        selected_course_id = int(selected_course_id)
        selected_course = models.get_course_by_id(selected_course_id)
        enrolled_students = models.get_attendance_for_course_and_date(selected_course_id, selected_date)
    elif all_courses:
        # Default to first course
        selected_course_id = all_courses[0]['id']
        selected_course = all_courses[0]
        enrolled_students = models.get_attendance_for_course_and_date(selected_course_id, selected_date)

    return render_template(
        'attendance.html',
        courses=all_courses,
        selected_course=selected_course,
        selected_course_id=selected_course_id,
        selected_date=selected_date,
        students=enrolled_students
    )

@app.route('/attendance/save', methods=['POST'])
def save_attendance():
    course_id = int(request.form.get('course_id'))
    date = request.form.get('date')
    student_ids = request.form.getlist('student_id')

    attendance_data = []
    for sid in student_ids:
        status = request.form.get(f'status_{sid}', 'Present')
        remarks = request.form.get(f'remarks_{sid}', '')
        attendance_data.append({
            'student_id': int(sid),
            'status': status,
            'remarks': remarks
        })

    try:
        models.record_bulk_attendance(course_id, date, attendance_data)
        flash(f"Attendance recorded for {len(attendance_data)} students on {date}!", "success")
    except Exception as e:
        flash(f"Error recording attendance: {str(e)}", "danger")

    return redirect(url_for('attendance', course_id=course_id, date=date))

@app.route('/attendance/report')
def attendance_report():
    all_courses = models.get_all_courses()
    selected_course_id = request.args.get('course_id', '')
    
    course_id_int = int(selected_course_id) if selected_course_id and selected_course_id.isdigit() else None
    summary = models.get_all_students_attendance_summary(course_id=course_id_int)
    
    selected_course = models.get_course_by_id(course_id_int) if course_id_int else None

    # Calculate summary metrics
    safe_count = sum(1 for s in summary if s['percentage'] >= 75.0 and s['total_classes'] > 0)
    warning_count = sum(1 for s in summary if 65.0 <= s['percentage'] < 75.0 and s['total_classes'] > 0)
    critical_count = sum(1 for s in summary if s['percentage'] < 65.0 and s['total_classes'] > 0)

    return render_template(
        'attendance_report.html',
        courses=all_courses,
        selected_course=selected_course,
        selected_course_id=course_id_int,
        summary=summary,
        safe_count=safe_count,
        warning_count=warning_count,
        critical_count=critical_count
    )

# ----------------- Marks & Grades -----------------
@app.route('/marks')
def marks():
    all_courses = models.get_all_courses()
    selected_course_id = request.args.get('course_id')
    
    selected_course = None
    marks_sheet = []

    if selected_course_id and selected_course_id.isdigit():
        selected_course_id = int(selected_course_id)
        selected_course = models.get_course_by_id(selected_course_id)
        marks_sheet = models.get_course_marks_sheet(selected_course_id)
    elif all_courses:
        selected_course_id = all_courses[0]['id']
        selected_course = all_courses[0]
        marks_sheet = models.get_course_marks_sheet(selected_course_id)

    return render_template(
        'marks.html',
        courses=all_courses,
        selected_course=selected_course,
        selected_course_id=selected_course_id,
        marks_sheet=marks_sheet
    )

@app.route('/marks/save', methods=['POST'])
def save_marks():
    course_id = int(request.form.get('course_id'))
    student_ids = request.form.getlist('student_id')

    try:
        for sid in student_ids:
            mid = request.form.get(f'midterm_{sid}', 0)
            assign = request.form.get(f'assignment_{sid}', 0)
            fin = request.form.get(f'final_{sid}', 0)
            rem = request.form.get(f'remarks_{sid}', '')
            models.save_student_marks(int(sid), course_id, mid, assign, fin, rem)

        flash("Marks and grades updated successfully!", "success")
    except Exception as e:
        flash(f"Error saving marks: {str(e)}", "danger")

    return redirect(url_for('marks', course_id=course_id))

# ----------------- Grade Ranking & Leaderboard -----------------
@app.route('/ranking')
def ranking():
    rankings = models.get_overall_rankings()
    all_courses = models.get_all_courses()
    
    # Calculate toppers
    top_3 = rankings[:3] if len(rankings) >= 3 else rankings
    class_average_cgpa = round(sum(r['cgpa'] for r in rankings) / len(rankings), 2) if rankings else 0.0

    return render_template(
        'ranking.html',
        rankings=rankings,
        top_3=top_3,
        class_average_cgpa=class_average_cgpa,
        courses=all_courses
    )

# ----------------- Printable Report Card -----------------
@app.route('/report-card/<int:student_id>')
def report_card(student_id):
    data = models.get_student_report_card(student_id)
    if not data:
        flash("Student record not found.", "warning")
        return redirect(url_for('students'))

    return render_template('report_card.html', data=data)

# ----------------- CSV Exports -----------------
@app.route('/export/ranking/csv')
def export_ranking_csv():
    rankings = models.get_overall_rankings()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        'Rank', 'Roll Number', 'Student Name', 'Department', 'Semester', 
        'Courses Enrolled', 'Total Credits', 'Aggregate Marks', 'Average Marks (%)', 
        'CGPA', 'Grade', 'Attendance %', 'Attendance Status'
    ])

    for r in rankings:
        writer.writerow([
            r['rank'], r['roll_number'], r['name'], r['department'], r['semester'],
            r['enrolled_count'], r['total_credits'], r['aggregate_marks'], r['average_marks'],
            r['cgpa'], r['overall_grade'], f"{r['attendance_pct']}%", r['attendance_status']
        ])

    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment;filename=grade_ranking_{datetime.now().strftime('%Y%m%d')}.csv"}
    )

@app.route('/export/attendance/csv')
def export_attendance_csv():
    course_id = request.args.get('course_id')
    course_id_int = int(course_id) if course_id and course_id.isdigit() else None
    summary = models.get_all_students_attendance_summary(course_id=course_id_int)
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        'Roll Number', 'Student Name', 'Department', 'Semester', 
        'Total Classes', 'Attended Classes', 'Present', 'Late', 'Absent', 
        'Attendance %', 'Status'
    ])

    for s in summary:
        writer.writerow([
            s['roll_number'], s['name'], s['department'], s['semester'],
            s['total_classes'], s['attended_weighted'], s['present_count'],
            s['late_count'], s['absent_count'], f"{s['percentage']}%", s['status']
        ])

    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment;filename=attendance_report_{datetime.now().strftime('%Y%m%d')}.csv"}
    )

# ----------------- Demo Data Seeding Route -----------------
@app.route('/seed-demo')
def seed_demo():
    seed_database()
    flash("Demo data seeded successfully with realistic students, courses, attendance, and marks!", "success")
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("=" * 60)
    print(f" EduTrack: Student Attendance & Grade Management System")
    print(f" Server running at: http://0.0.0.0:{port}")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=port)

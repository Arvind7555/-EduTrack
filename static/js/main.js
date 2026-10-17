// EduTrack Main JavaScript

document.addEventListener('DOMContentLoaded', function () {
    // 1. Live Client-side Table Filter
    const searchInputs = document.querySelectorAll('.table-search-input');
    searchInputs.forEach(input => {
        const tableId = input.getAttribute('data-table-id');
        const table = document.getElementById(tableId);
        if (!table) return;

        input.addEventListener('input', function () {
            const query = this.value.toLowerCase().trim();
            const rows = table.querySelectorAll('tbody tr');

            rows.forEach(row => {
                const text = row.innerText.toLowerCase();
                if (text.includes(query)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    });

    // 2. Bulk Attendance Selection Helpers
    const markAllPresentBtn = document.getElementById('markAllPresent');
    const markAllAbsentBtn = document.getElementById('markAllAbsent');

    if (markAllPresentBtn) {
        markAllPresentBtn.addEventListener('click', function () {
            document.querySelectorAll('input[type="radio"][value="Present"]').forEach(radio => {
                radio.checked = true;
            });
        });
    }

    if (markAllAbsentBtn) {
        markAllAbsentBtn.addEventListener('click', function () {
            document.querySelectorAll('input[type="radio"][value="Absent"]').forEach(radio => {
                radio.checked = true;
            });
        });
    }

    // 3. Dynamic Marks Calculation & Grade Determination
    const markInputs = document.querySelectorAll('.mark-input');
    markInputs.forEach(input => {
        input.addEventListener('input', function () {
            const row = this.closest('tr');
            if (!row) return;

            const mid = parseFloat(row.querySelector('.input-midterm')?.value) || 0;
            const assign = parseFloat(row.querySelector('.input-assignment')?.value) || 0;
            const final = parseFloat(row.querySelector('.input-final')?.value) || 0;

            const total = Math.min(100, Math.max(0, Math.round((mid + assign + final) * 10) / 10));
            const totalDisplay = row.querySelector('.total-marks-display');
            const gradeBadge = row.querySelector('.grade-badge-display');
            const gpDisplay = row.querySelector('.gp-display');

            if (totalDisplay) totalDisplay.innerText = total.toFixed(1);

            let grade = 'F';
            let gp = 0.0;
            let badgeClass = 'badge-grade-f';

            if (total >= 90) {
                grade = 'A+';
                gp = 10.0;
                badgeClass = 'badge-grade-aplus';
            } else if (total >= 80) {
                grade = 'A';
                gp = 9.0;
                badgeClass = 'badge-grade-a';
            } else if (total >= 70) {
                grade = 'B+';
                gp = 8.0;
                badgeClass = 'badge-grade-bplus';
            } else if (total >= 60) {
                grade = 'B';
                gp = 7.0;
                badgeClass = 'badge-grade-b';
            } else if (total >= 50) {
                grade = 'C';
                gp = 6.0;
                badgeClass = 'badge-grade-c';
            } else if (total >= 40) {
                grade = 'D';
                gp = 5.0;
                badgeClass = 'badge-grade-d';
            }

            if (gradeBadge) {
                gradeBadge.className = 'badge ' + badgeClass;
                gradeBadge.innerText = grade;
            }

            if (gpDisplay) {
                gpDisplay.innerText = gp.toFixed(1);
            }
        });
    });

    // 4. Auto-dismiss alerts after 5 seconds
    setTimeout(function () {
        const alerts = document.querySelectorAll('.alert-dismissible');
        alerts.forEach(alert => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        });
    }, 5000);
});

// Helper function to print report card
function printReportCard() {
    window.print();
}

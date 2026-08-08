from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from extensions import mysql
import datetime
import os
from werkzeug.utils import secure_filename

visitor_bp = Blueprint('visitor', __name__, url_prefix='/visitor')

#  Dashboard: Show all visitors
@visitor_bp.route('/dashboard')
@login_required
def dashboard():
    cursor = mysql.connection.cursor()
    if session['role'] == 'admin':
        cursor.execute("SELECT v.id, v.name, v.phone, v.purpose, v.check_in, v.check_out, d.name AS department, h.name AS host FROM visitors v JOIN departments d ON v.department_id = d.id JOIN hosts h ON v.host_id = h.id")
    else:
        cursor.execute("SELECT v.id, v.name, v.phone, v.purpose, v.check_in, v.check_out, d.name AS department, h.name AS host FROM visitors v JOIN departments d ON v.department_id = d.id JOIN hosts h ON v.host_id = h.id WHERE v.created_by = %s", (current_user.id,))
    
    visitors = cursor.fetchall()
    cursor.close()
    return render_template('dashboard.html', visitors=visitors)


#  Add Visitor
@visitor_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_visitor():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM departments")
    departments = cursor.fetchall()

    cursor.execute("SELECT * FROM hosts")
    hosts = cursor.fetchall()

    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        purpose = request.form['purpose']
        department_id = request.form['department']
        host_id = request.form['host']

        cursor.execute("""
            INSERT INTO visitors (name, email, phone, address, purpose, department_id, host_id, created_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (name, email, phone, address, purpose, department_id, host_id, current_user.id))
        mysql.connection.commit()
        flash('Visitor added successfully!', 'success')
        return redirect(url_for('visitor.dashboard'))

    return render_template('add_visitor.html', departments=departments, hosts=hosts)
    
    visitor_bp = Blueprint('visitor', __name__, url_prefix='/visitor')

@visitor_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_visitor(id):
    cursor = mysql.connection.cursor()
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        purpose = request.form['purpose']
        department = request.form['department']
        host = request.form['host']

        file = request.files.get('photo')
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file_path = os.path.join('static/images', filename)
            file.save(file_path)

            cursor.execute("""
                UPDATE visitors SET name=%s, phone=%s, email=%s, address=%s, purpose=%s,
                department=%s, host=%s, photo=%s WHERE id=%s
            """, (name, phone, email, address, purpose, department, host, filename, id))
        else:
            cursor.execute("""
                UPDATE visitors SET name=%s, phone=%s, email=%s, address=%s, purpose=%s,
                department=%s, host=%s WHERE id=%s
            """, (name, phone, email, address, purpose, department, host, id))

        mysql.connection.commit()
        cursor.close()
        flash('Visitor updated successfully!', 'success')
        return redirect(url_for('visitor.dashboard'))

    
    cursor.execute("SELECT * FROM visitors WHERE id = %s", (id,))
    visitor = cursor.fetchone()

    cursor.execute("SELECT name FROM departments")
    departments = cursor.fetchall()

    cursor.execute("SELECT name FROM hosts")
    hosts = cursor.fetchall()

    cursor.close()
    return render_template('edit_visitor.html', visitor=visitor, departments=departments, hosts=hosts)


@visitor_bp.route('/view/<int:id>')
@login_required
def view_visitor(id):
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT v.*, d.name AS department, h.name AS host 
        FROM visitors v 
        JOIN departments d ON v.department_id = d.id 
        JOIN hosts h ON v.host_id = h.id 
        WHERE v.id = %s
    """, (id,))
    visitor = cursor.fetchone()
    cursor.close()

    if not visitor:
        flash('Visitor not found', 'danger')
        return redirect(url_for('visitor.dashboard'))

    return render_template('view_visitor.html', visitor=visitor)

@visitor_bp.route('/delete/<int:id>', methods=['GET'])
@login_required
def delete_visitor(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM visitors WHERE id = %s", (id,))
    mysql.connection.commit()
    cursor.close()
    flash('Visitor deleted successfully!', 'success')
    return redirect(url_for('visitor.dashboard'))

@visitor_bp.route('/export', methods=['GET', 'POST'])
@login_required
def export_visitors():
    if request.method == 'POST':
        from_date = request.form['from_date']
        to_date = request.form['to_date']

        cursor = mysql.connection.cursor()

        query = """
            SELECT v.name, v.phone, v.email, v.purpose, v.check_in, v.check_out,
                   d.name AS department, h.name AS host
            FROM visitors v
            JOIN departments d ON v.department_id = d.id
            JOIN hosts h ON v.host_id = h.id
            WHERE DATE(v.check_in) BETWEEN %s AND %s
        """

        cursor.execute(query, (from_date, to_date))
        data = cursor.fetchall()
        cursor.close()

        # Create CSV in memory
        import csv
        from io import StringIO
        si = StringIO()
        writer = csv.writer(si)
        writer.writerow(['Name', 'Phone', 'Email', 'Purpose', 'Check-in', 'Check-out', 'Department', 'Host'])
        for row in data:
            writer.writerow(row)

        output = si.getvalue()
        from flask import Response
        return Response(output, mimetype="text/csv",
                        headers={"Content-Disposition": "attachment;filename=visitors_export.csv"})

    return render_template('export.html')

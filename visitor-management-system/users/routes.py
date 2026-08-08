from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import mysql
from werkzeug.security import generate_password_hash

user_bp = Blueprint('user', __name__, url_prefix='/user')


# Manage Departments
@user_bp.route('/departments', methods=['GET', 'POST'])
@login_required
def manage_departments():
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('visitor.dashboard'))

    cursor = mysql.connection.cursor()

    if request.method == 'POST':
        dept_name = request.form['department']
        cursor.execute("INSERT INTO departments (name) VALUES (%s)", (dept_name,))
        mysql.connection.commit()
        flash('Department added.', 'success')

    cursor.execute("SELECT * FROM departments")
    departments = cursor.fetchall()
    cursor.close()

    return render_template('manage_departments.html', departments=departments)


@user_bp.route('/departments/delete/<int:id>')
@login_required
def delete_department(id):
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('visitor.dashboard'))

    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM departments WHERE id = %s", (id,))
    mysql.connection.commit()
    cursor.close()
    flash('Department deleted.', 'info')
    return redirect(url_for('user.manage_departments'))


# Manage Hosts
@user_bp.route('/hosts', methods=['GET', 'POST'])
@login_required
def manage_hosts():
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('visitor.dashboard'))

    cursor = mysql.connection.cursor()

    if request.method == 'POST':
        name = request.form['host_name']
        dept_id = request.form['department_id']
        cursor.execute("INSERT INTO hosts (name, department_id) VALUES (%s, %s)", (name, dept_id))
        mysql.connection.commit()
        flash('Host added.', 'success')

    cursor.execute("SELECT * FROM departments")
    departments = cursor.fetchall()

    cursor.execute("SELECT h.id, h.name, d.name FROM hosts h JOIN departments d ON h.department_id = d.id")
    hosts = cursor.fetchall()

    cursor.close()
    return render_template('manage_hosts.html', hosts=hosts, departments=departments)


@user_bp.route('/hosts/delete/<int:id>')
@login_required
def delete_host(id):
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('visitor.dashboard'))

    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM hosts WHERE id = %s", (id,))
    mysql.connection.commit()
    cursor.close()
    flash('Host deleted.', 'info')
    return redirect(url_for('user.manage_hosts'))

@user_bp.route('/users', methods=['GET', 'POST'])
@login_required
def manage_users():
    if current_user.role != 'admin':
        flash('Access denied. Only administrators can manage users.', 'danger')
        return redirect(url_for('visitor.dashboard'))

    cursor = mysql.connection.cursor()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role'] # 'admin' or 'subuser'

        hashed_password = generate_password_hash(password)

        try:
            cursor.execute("INSERT INTO admin_users (username, password_hash, role) VALUES (%s, %s, %s)",
                           (username, hashed_password, role))
            mysql.connection.commit()
            flash(f'User "{username}" ({role}) added successfully!', 'success')
        except Exception as e:
            mysql.connection.rollback() # Rollback on error
            flash(f'Error adding user: {e}', 'danger')

        return redirect(url_for('user.manage_users')) # Redirect to refresh the list

    cursor.execute("SELECT id, username, role FROM admin_users")
    users = cursor.fetchall()
    cursor.close()

    return render_template('manage_users.html', users=users)

@user_bp.route('/users/delete/<int:id>')
@login_required
def delete_user(id):
    if current_user.role != 'admin':
        flash('Access denied. Only administrators can manage users.', 'danger')
        return redirect(url_for('visitor.dashboard'))

    if int(id) == current_user.id: # Prevent admin from deleting themselves
        flash("You cannot delete your own account!", "danger")
        return redirect(url_for('user.manage_users'))

    cursor = mysql.connection.cursor()
    try:
        cursor.execute("DELETE FROM admin_users WHERE id = %s", (id,))
        mysql.connection.commit()
        flash('User deleted successfully.', 'info')
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error deleting user: {e}', 'danger')
    finally:
        cursor.close()

    return redirect(url_for('user.manage_users'))
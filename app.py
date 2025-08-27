from flask import Flask, render_template, redirect, url_for, flash, request, abort
from config import Config
from models import db, User, Employee
from forms import LoginForm, RegisterForm, EmployeeForm
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from sqlalchemy.exc import IntegrityError

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    with app.app_context():
        db.create_all()
        # Create a default admin if none exists
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', is_admin=True)
            admin.set_password('admin123')  # Change after first login
            db.session.add(admin)
            db.session.commit()

    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        return redirect(url_for('login'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash('Logged in successfully.', 'success')
                next_page = request.args.get('next')
                return redirect(next_page or url_for('dashboard'))
            flash('Invalid username or password.', 'danger')
        return render_template('login.html', form=form)

    @app.route('/register', methods=['GET', 'POST'])
    @login_required
    def register():
        if not current_user.is_admin:
            abort(403) # Forbidden
        form = RegisterForm()
        if form.validate_on_submit():
            new_user = User(username=form.username.data)
            new_user.set_password(form.password.data)
            try:
                db.session.add(new_user)
                db.session.commit()
                flash('User created successfully.', 'success')
                return redirect(url_for('dashboard'))
            except IntegrityError:
                db.session.rollback()
                flash('Username already exists.', 'danger')
        return render_template('register.html', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('You have been logged out.', 'info')
        return redirect(url_for('login'))

    @app.route('/dashboard')
    @login_required
    def dashboard():
        total_employees = Employee.query.count()
        return render_template('dashboard.html', total_employees=total_employees)

    # --- Employees CRUD ---
    @app.route('/employees')
    @login_required
    def employees():
        q = request.args.get('q', '').strip()
        page = request.args.get('page', 1, type=int)
        per_page = 10
        
        query = Employee.query.order_by(Employee.id.asc())
        
        if q:
            # Simple search by name or email
            search_term = f'%{q}%'
            query = query.filter(
                (Employee.first_name.ilike(search_term)) |
                (Employee.last_name.ilike(search_term)) |
                (Employee.email.ilike(search_term))
            )
        
        paginated_employees = query.paginate(page=page, per_page=per_page, error_out=False)
        return render_template('employees.html', employees=paginated_employees, q=q)

    @app.route('/employee/new', methods=['GET', 'POST'])
    @login_required
    def new_employee():
        form = EmployeeForm()
        if form.validate_on_submit():
            emp = Employee(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                phone=form.phone.data,
                position=form.position.data,
                department=form.department.data,
                salary=form.salary.data
            )
            try:
                db.session.add(emp)
                db.session.commit()
                flash('Employee created successfully.', 'success')
                return redirect(url_for('employees'))
            except IntegrityError:
                db.session.rollback()
                flash('Email already exists.', 'danger')
        return render_template('employees_form.html', form=form, action='Create')

    @app.route('/employee/<int:emp_id>/edit', methods=['GET', 'POST'])
    @login_required
    def edit_employee(emp_id):
        emp = Employee.query.get_or_404(emp_id)
        form = EmployeeForm(obj=emp)
        if form.validate_on_submit():
            form.populate_obj(emp)
            try:
                db.session.commit()
                flash('Employee updated successfully.', 'success')
                return redirect(url_for('employees'))
            except IntegrityError:
                db.session.rollback()
                flash('Email already exists.', 'danger')
        return render_template('employee_form.html', form=form, action='Update')

    @app.route('/employee/<int:emp_id>/delete', methods=['GET', 'POST'])
    @login_required
    def delete_employee(emp_id):
        emp = Employee.query.get_or_404(emp_id)
        if request.method == 'POST':
            db.session.delete(emp)
            db.session.commit()
            flash('Employee deleted successfully.', 'success')
            return redirect(url_for('employees'))
        return render_template('confirm_delete.html', employee=emp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
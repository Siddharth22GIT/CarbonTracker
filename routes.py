from flask import render_template, url_for, flash, redirect, request, jsonify
from app import db
from models import Company, Activity, EmissionTarget
from forms import RegistrationForm, LoginForm, ActivityForm, EmissionTargetForm
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from sqlalchemy import func
import json
from utils import get_emission_stats, generate_pdf, get_global_co2_data

def register_routes(app):
    
    @app.route('/')
    def index():
        # Get global CO2 data for the ticker
        global_co2_data = get_global_co2_data()
        return render_template('index.html', title='Carbon Footprint Tracker', global_co2_data=global_co2_data)
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        
        form = RegistrationForm()
        if form.validate_on_submit():
            company = Company(
                name=form.name.data,
                email=form.email.data,
                industry=form.industry.data,
                size=form.size.data
            )
            company.set_password(form.password.data)
            
            db.session.add(company)
            db.session.commit()
            
            flash(f'Account created for {form.name.data}! You can now log in.', 'success')
            return redirect(url_for('login'))
            
        return render_template('register.html', title='Register', form=form)
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
            
        form = LoginForm()
        if form.validate_on_submit():
            company = Company.query.filter_by(email=form.email.data).first()
            
            if company and company.check_password(form.password.data):
                login_user(company)
                next_page = request.args.get('next')
                flash('Login successful!', 'success')
                return redirect(next_page) if next_page else redirect(url_for('dashboard'))
            else:
                flash('Login unsuccessful. Please check email and password.', 'danger')
                
        return render_template('login.html', title='Login', form=form)
    
    @app.route('/logout')
    def logout():
        logout_user()
        flash('You have been logged out.', 'info')
        return redirect(url_for('index'))
    
    @app.route('/dashboard')
    @login_required
    def dashboard():
        # Get summary statistics
        total_emissions = current_user.get_total_emissions()
        emissions_by_category = current_user.get_emissions_by_category()
        
        # Get recent activities (last 5)
        recent_activities = Activity.query.filter_by(company_id=current_user.id)\
            .order_by(Activity.date.desc()).limit(5).all()
        
        # Get emissions target
        target = EmissionTarget.query.filter_by(
            company_id=current_user.id, 
            category='overall'
        ).order_by(EmissionTarget.target_date.desc()).first()
        
        # Prepare chart data
        chart_data = {
            'labels': [cat for cat, _ in emissions_by_category],
            'data': [float(val) for _, val in emissions_by_category]
        }
        
        # Monthly emissions for trend chart
        monthly_emissions = db.session.query(
            func.to_char(Activity.date, 'YYYY-MM').label('month'),
            func.sum(Activity.emission_value).label('total')
        ).filter_by(company_id=current_user.id)\
         .group_by('month')\
         .order_by('month')\
         .limit(12)\
         .all()
        
        trend_data = {
            'labels': [month for month, _ in monthly_emissions],
            'data': [float(total) for _, total in monthly_emissions]
        }
        
        return render_template(
            'dashboard.html', 
            title='Dashboard',
            total_emissions=total_emissions,
            emissions_by_category=emissions_by_category,
            recent_activities=recent_activities,
            target=target,
            chart_data=json.dumps(chart_data),
            trend_data=json.dumps(trend_data)
        )
    
    @app.route('/add_activity', methods=['GET', 'POST'])
    @login_required
    def add_activity():
        form = ActivityForm()
        
        if form.validate_on_submit():
            activity = Activity(
                title=form.title.data,
                category=form.category.data,
                description=form.description.data,
                date=form.date.data,
                emission_value=form.emission_value.data,
                emission_unit=form.emission_unit.data,
                company_id=current_user.id
            )
            
            db.session.add(activity)
            db.session.commit()
            
            flash('Activity has been added successfully!', 'success')
            return redirect(url_for('activities'))
            
        return render_template('add_activity.html', title='Add Activity', form=form)
    
    @app.route('/activities')
    @login_required
    def activities():
        # Get filter parameters
        category = request.args.get('category', '')
        from_date = request.args.get('from_date', '')
        to_date = request.args.get('to_date', '')
        
        # Base query
        query = Activity.query.filter_by(company_id=current_user.id)
        
        # Apply filters
        if category:
            query = query.filter_by(category=category)
        
        if from_date:
            query = query.filter(Activity.date >= datetime.strptime(from_date, '%Y-%m-%d').date())
            
        if to_date:
            query = query.filter(Activity.date <= datetime.strptime(to_date, '%Y-%m-%d').date())
        
        # Get all activities with filters applied
        activities = query.order_by(Activity.date.desc()).all()
        
        # Get available categories for filter dropdown
        categories = db.session.query(Activity.category)\
            .filter_by(company_id=current_user.id)\
            .distinct()\
            .all()
        categories = [cat[0] for cat in categories]
        
        return render_template(
            'activities.html', 
            title='Activities',
            activities=activities,
            categories=categories,
            category_filter=category,
            from_date=from_date,
            to_date=to_date
        )
    
    @app.route('/delete_activity/<int:activity_id>', methods=['POST'])
    @login_required
    def delete_activity(activity_id):
        activity = Activity.query.get_or_404(activity_id)
        
        # Check if the activity belongs to the current user
        if activity.company_id != current_user.id:
            flash('You do not have permission to delete this activity.', 'danger')
            return redirect(url_for('activities'))
        
        db.session.delete(activity)
        db.session.commit()
        
        flash('Activity has been deleted.', 'success')
        return redirect(url_for('activities'))
    
    @app.route('/targets', methods=['GET', 'POST'])
    @login_required
    def targets():
        form = EmissionTargetForm()
        
        if form.validate_on_submit():
            target = EmissionTarget(
                target_value=form.target_value.data,
                target_unit=form.target_unit.data,
                target_date=form.target_date.data,
                category=form.category.data,
                company_id=current_user.id
            )
            
            db.session.add(target)
            db.session.commit()
            
            flash('Emission target has been set!', 'success')
            return redirect(url_for('targets'))
        
        # Get current targets
        targets = EmissionTarget.query.filter_by(company_id=current_user.id)\
            .order_by(EmissionTarget.category, EmissionTarget.target_date).all()
            
        # Current emissions for comparison
        emissions_by_category = dict(current_user.get_emissions_by_category())
        total_emissions = current_user.get_total_emissions()
        
        return render_template(
            'targets.html',
            title='Emission Targets',
            form=form,
            targets=targets,
            emissions_by_category=emissions_by_category,
            total_emissions=total_emissions
        )
    
    @app.route('/reports')
    @login_required
    def reports():
        # Get filter parameters
        from_date = request.args.get('from_date', '')
        to_date = request.args.get('to_date', '')
        
        # Get emission stats for the period
        stats = get_emission_stats(current_user.id, from_date, to_date)
        
        return render_template(
            'reports.html',
            title='Emission Reports',
            stats=stats,
            from_date=from_date,
            to_date=to_date
        )
    
    @app.route('/generate_report_pdf')
    @login_required
    def generate_report_pdf():
        # Get filter parameters
        from_date = request.args.get('from_date', '')
        to_date = request.args.get('to_date', '')
        
        # Get stats for PDF
        stats = get_emission_stats(current_user.id, from_date, to_date)
        
        # Generate PDF
        pdf_path = generate_pdf(current_user, stats, from_date, to_date)
        
        flash('PDF report has been generated and will download shortly.', 'success')
        return redirect(url_for('reports'))
    
    @app.route('/api/chart_data')
    @login_required
    def chart_data():
        # Get emissions by category for the pie chart
        emissions_by_category = current_user.get_emissions_by_category()
        
        chart_data = {
            'labels': [cat for cat, _ in emissions_by_category],
            'data': [float(val) for _, val in emissions_by_category]
        }
        
        return jsonify(chart_data)

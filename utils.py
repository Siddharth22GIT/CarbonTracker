from flask import flash
from sqlalchemy import func
from datetime import datetime
from models import Activity

def get_emission_stats(company_id, from_date=None, to_date=None):
    """
    Get emission statistics for a company within a date range
    """
    query = Activity.query.filter_by(company_id=company_id)
    
    # Apply date filters if provided
    if from_date and from_date.strip():
        try:
            from_date_obj = datetime.strptime(from_date, '%Y-%m-%d').date()
            query = query.filter(Activity.date >= from_date_obj)
        except ValueError:
            flash('Invalid from date format. Please use YYYY-MM-DD', 'warning')
    
    if to_date and to_date.strip():
        try:
            to_date_obj = datetime.strptime(to_date, '%Y-%m-%d').date()
            query = query.filter(Activity.date <= to_date_obj)
        except ValueError:
            flash('Invalid to date format. Please use YYYY-MM-DD', 'warning')
    
    # Calculate total emissions
    total_emissions = query.with_entities(func.sum(Activity.emission_value)).scalar() or 0
    
    # Get emissions by category
    emissions_by_category = query.with_entities(
        Activity.category,
        func.sum(Activity.emission_value).label('total')
    ).group_by(Activity.category).all()
    
    # Get monthly trend
    monthly_trend = query.with_entities(
        func.to_char(Activity.date, 'YYYY-MM').label('month'),
        func.sum(Activity.emission_value).label('total')
    ).group_by('month').order_by('month').all()
    
    # Get highest emission activities
    highest_emissions = query.order_by(Activity.emission_value.desc()).limit(5).all()
    
    return {
        'total_emissions': total_emissions,
        'by_category': emissions_by_category,
        'monthly_trend': monthly_trend,
        'highest_emissions': highest_emissions
    }

def generate_pdf(company, stats, from_date, to_date):
    """
    Generate a PDF report of emissions data
    
    Note: In a real implementation, this would use a PDF generation 
    library like ReportLab, pdfkit, or WeasyPrint. For this example,
    we'll just simulate PDF generation.
    """
    # In a production app, this would generate an actual PDF
    # For this example, we're just simulating the generation
    
    # We'd generate the PDF and save it to a temporary location
    # Then return the path or send the file to the user
    
    # For now, we'll just return a placeholder string
    flash('PDF report generation is a premium feature. This is a simulation.', 'info')
    return "simulated_pdf_path.pdf"

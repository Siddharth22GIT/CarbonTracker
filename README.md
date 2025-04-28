# Carbon Footprint Tracker

A Flask web application for companies to track, manage, and visualize their carbon footprint data.

## Features

- User registration and authentication for companies
- Activity logging with emission values and categories
- Dashboard with visualizations and statistics
- Reports generation and target setting
- Global CO2 level tracking

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- VSCode (recommended)
- Git (optional)

### Installation Steps

1. Clone or download this repository to your local machine.

2. Open the project in VSCode.

3. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

5. Install the dependencies using the dependencies.txt file:
   ```bash
   pip install -r dependencies.txt
   ```

6. Run the application:
   ```bash
   python main.py
   ```
   or
   ```bash
   flask run
   ```

7. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

## Database

The application uses SQLite for data storage, which requires no additional setup.

## File Structure

- `app.py`: Main application configuration
- `main.py`: Entry point for running the application
- `models.py`: Database models (Company, Activity, EmissionTarget)
- `routes.py`: Application routes and views
- `forms.py`: Form definitions
- `utils.py`: Utility functions
- `templates/`: HTML templates
- `static/`: Static files (CSS, JS)

## License

This project is available as open source under the terms of the MIT License.
# BankFlow-Pro

A comprehensive banking management system built with Streamlit and SQLite. This modern web application provides a secure and user-friendly interface for managing banking operations, including account creation, money transfers, and transaction tracking. Perfect for small to medium-sized banking operations, educational purposes, or as a foundation for larger banking projects.

Repository: https://github.com/yourusername/BankFlow-Pro

## Features
- User-friendly web interface built with Streamlit
- Secure account management system
- Real-time transaction processing
- Detailed transaction history tracking
- Balance enquiry and account statements
- Multi-user support with authentication
- Data persistence using SQLite database
- Clean and modern UI design

## Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/BankFlow-Pro
cd Bank_final
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
```

3. Activate the virtual environment:
- On Windows:
```bash
venv\Scripts\activate
```
- On macOS/Linux:
```bash
source venv/bin/activate
```

4. Install the required dependencies:
```bash
pip install -r requirements.txt
```

If requirements.txt is not present, install the following packages:
```bash
pip install streamlit
pip install pandas
pip install sqlite3
```

## Running the Application

1. Make sure your virtual environment is activated

2. Run the Streamlit application:
```bash
streamlit run bank_app.py
```

3. The application will start and automatically open in your default web browser. If it doesn't, you can access it at:
```
http://localhost:8501
```

## Project Structure
- `bank_app.py`: Main application file
- `database.db`: SQLite database file for storing user and transaction data
- `requirements.txt`: List of Python dependencies

## Troubleshooting

1. If you encounter any database-related errors, ensure that the database file exists and has proper permissions.

2. If you see "Module not found" errors, make sure all dependencies are properly installed:
```bash
pip install -r requirements.txt
```

3. If the application doesn't start, check if Streamlit is properly installed:
```bash
pip install --upgrade streamlit
```

## Support

For any issues or questions, please open an issue in the repository or contact the development team.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

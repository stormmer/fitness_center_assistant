# Fitness Center Assistant

A comprehensive Python application for managing fitness center operations, featuring both a command-line interface and a Streamlit web dashboard. Built for the University of the Pacific's Baun Fitness Center.

## Features

- **Personalized Greetings**: Welcome users with customized messages
- **Class Reminders**: View scheduled classes by day of the week
- **Membership Pricing Calculator**: Calculate membership costs with student/staff discounts and promo codes
- **Attendance Tracking**: Record and summarize attendance across different activities
- **Session Summary Export**: Export attendance and pricing summaries to text files
- **Streamlit Dashboard**: Interactive web interface with University of the Pacific branding

## Project Structure

```
fitness_center_assistant/
├── README.md
├── .env.example
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── data.py              # Core data structures
│   ├── logic/
│   │   ├── pricing.py       # Pricing calculations
│   │   ├── messaging.py     # Greetings and reminders
│   │   ├── schedule.py      # Schedule utilities
│   │   ├── attendance.py    # Attendance tracking
│   │   └── export.py        # Export utilities
│   ├── cli.py               # Command-line interface
│   ├── app.py               # Streamlit dashboard
│   └── theme.py             # Pacific theme styling
├── tests/
│   ├── test_pricing.py
│   └── test_attendance.py
└── assets/
    └── pacific_logo.png
```

## Setup

### Prerequisites

- Python 3.11 or higher
- pip (Python package installer)

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd fitness_center_assistant
   ```

2. **Create a virtual environment:**
   
   On Windows:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
   
   On macOS/Linux:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables (optional):**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

## Usage

### Command-Line Interface

Run the interactive CLI application:

```bash
python -m src.cli
```

The CLI will guide you through:
1. Entering your name for a personalized greeting
2. Viewing class reminders for a specific day
3. Calculating membership pricing
4. Tracking attendance
5. Exporting a session summary

### Streamlit Dashboard

Launch the web dashboard:

```bash
streamlit run src/app.py
```

The dashboard includes:
- **Home**: Welcome page with quick links
- **Pricing Calculator**: Interactive membership pricing with discounts
- **Class Schedule**: View classes by day, add custom notes
- **Attendance**: Track attendance with visualizations
- **Summary & Export**: View summaries and download reports

### Running Tests

Run the test suite:

```bash
pytest -q
```

For verbose output:

```bash
pytest -v
```

## Configuration

### Membership Plans

Default plans are defined in `src/data.py`:
- Basic: $25/month
- Plus: $35/month
- Premium: $50/month

### Promo Codes

Available promo codes:
- `WELCOME10`: 10% discount
- `FALL5`: 5% discount

### Discounts

- Student/Staff: 15% discount on base membership cost
- Promo codes: Applied after student/staff discount

## Screenshots

*Screenshots to be added:*
- CLI interface in action
- Streamlit dashboard home page
- Pricing calculator with breakdown
- Attendance tracking with charts

## Extensibility

The project is designed for easy extension:

### CSV Persistence

Add CSV file handling to persist attendance data:
```python
import pandas as pd
# Save attendance to CSV
pd.DataFrame(attendance_data).to_csv('attendance.csv', index=False)
```

### Authentication

Integrate user authentication:
- Add login/logout functionality
- Store user preferences
- Track user-specific attendance

### Email/SMS Integration

Send reminders and notifications:
- Class reminders via email
- Membership renewal notifications
- Attendance summaries

### Database Integration

Replace in-memory storage with a database:
- SQLite for local development
- PostgreSQL for production
- Store membership records, attendance history

## Development

### Code Style

- Type hints throughout
- Docstrings for all functions
- Modular design with clear separation of concerns

### Adding Features

1. Add data structures to `src/data.py`
2. Implement logic in `src/logic/`
3. Update CLI in `src/cli.py`
4. Add dashboard pages in `src/app.py`
5. Write tests in `tests/`

## License

This project is for educational and internal use at University of the Pacific.

## Support

For issues or questions, please contact the development team.


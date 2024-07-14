# PennyWise

PennyWise is a Django-based web application designed to help users manage their finances effectively. This application provides various features including expense tracking, budget management, and financial analysis.

## Features

- **Expense Tracking**: Log your daily expenses with ease.
- **Budget Management**: Set and monitor budgets for different categories.
- **Financial Analysis**: Visualize your spending patterns and analyze your financial health.
- **User Authentication**: Secure login and registration system using Django's built-in authentication.
- **Custom User Model**: Utilizes a custom user model for enhanced user management.
- **API Interactions**: Implements RESTful APIs for data interaction, including POST and GET requests.
- **Class-Based Views**: Uses Django's class-based views (CBVs) for structured and efficient view management.
- **Model-Based Views**: Incorporates Django's model-based views to interact with database models efficiently.

## Technologies Used

- **Python**: Programming language used for backend logic.
- **Django**: Web framework for rapid development and clean design.
- **MySQL**: Database management system for storing application data.
- **HTML/CSS**: Frontend development for user interface and styling.
- **JavaScript**: Used for frontend interactivity and AJAX requests.

## Installation

### Prerequisites

- Python 3.8+
- Django 3.2+
- MySQL

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/Mehnaz2004/PennyWise_Django.git
   cd PennyWise_Django

2. Create a virtual environment and activate it:
   ```bash
   python -m venv env
   source env/bin/activate   # On Windows use `env\Scripts\activate`

   
3. Install the required packages:
   ```bash
   pip install -r requirements.txt

4. Set up the database:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   
5. Create a superuser:
    ```bash
    python manage.py createsuperuser

6. Run the development server:
    ```bash
    python manage.py runserver

7. Open your browser and go to http://127.0.0.1:8000/ to see the application in action.

### Usage

- Register for a new account or log in with existing credentials.
- Navigate through the dashboard to add expenses, set budgets, and view financial analysis.
- Use the profile section to update personal details and manage account settings.

### Contact

For any questions or suggestions, feel free to reach out:

- GitHub: Mehnaz2004
- LinkedIn: Mehnaz Ali

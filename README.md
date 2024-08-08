# Terminal Dashboard

This project is a Django-based web application that connects to a PostgreSQL database and displays terminal data in tabular and graphical forms. It aims to provide an easy-to-use interface for visualizing and managing terminal data.

## Features

- Display data from PostgreSQL in a table
- Visualize data with charts
- User authentication and authorization
- Responsive web design

## Webpages

### Login Screen
![Uploading Screenshot 2024-08-08 at 5.18.09 PM.png…]()


## Technologies Used

- Python
- Django
- PostgreSQL
- HTML/CSS
- JavaScript
- Bootstrap (optional for styling)
- Leaflet.js
- Geographic Information System (GIS)

## Setup

### Prerequisites

- Python 3.x
- PostgreSQL
- Git

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/kartiktripat/terminal-dashboard.git
    cd terminal-dashboard
    ```

2. **Create a virtual environment and activate it:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure your PostgreSQL database:**

    Update the database settings in `settings.py`:

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'terminals',
            'USER': 'kt',
            'PASSWORD': '*****',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
    ```

5. **Apply migrations:**

    ```bash
    python manage.py migrate
    ```

6. **Create a superuser (optional but recommended for accessing the admin interface):**

    ```bash
    python manage.py createsuperuser
    ```

7. **Run the development server:**

    ```bash
    python manage.py runserver
    ```

8. **Access the application:**

    Open your web browser and go to `http://localhost:8000`.

## Usage

### Accessing the Admin Interface

If you created a superuser, you can access the Django admin interface at `http://localhost:8000/admin`. Use the credentials you set up for the superuser to log in.

### Adding Data

You can add data to the PostgreSQL database through the Django admin interface or by creating custom views and forms in your application.

### Viewing Data

The main page of the application will display the terminal data in a table. You can customize this view by editing the corresponding template and view in your Django application.

### Visualizing Data

Graphs and charts can be added using JavaScript libraries like Chart.js or Plotly. Include the necessary scripts in your templates and create views that provide the data in JSON format.

## Contributing

Contributions are welcome! Please fork the repository and use a feature branch. Pull requests are reviewed on a regular basis.

1. **Fork the repository**
2. **Create a feature branch:**

    ```bash
    git checkout -b feature/your-feature-name
    ```

3. **Commit your changes:**

    ```bash
    git commit -m 'Add some feature'
    ```

4. **Push to the branch:**

    ```bash
    git push origin feature/your-feature-name
    ```

5. **Create a new Pull Request**

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Django Documentation](https://docs.djangoproject.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Chart.js Documentation](https://www.chartjs.org/docs/)
- [Plotly Documentation](https://plotly.com/javascript/)

# Hotel Management System

A comprehensive Flask-based hotel management application designed to streamline hotel operations including guest management, room management, and booking reservations.

## Features

- **Guest Management**: Manage guest information and profiles
- **Room Management**: Track room inventory, status, and pricing
- **Booking System**: Create and manage hotel reservations
- **Dashboard**: Overview of hotel operations and statistics
- **User-Friendly Interface**: Clean and intuitive web interface

## Technologies Used

- **Backend**: Python Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML, CSS, Jinja2 Templates
- **Styling**: Bootstrap CSS Framework

## Installation

1. Clone the repository:
```bash
git clone https://github.com/massawes/hotel_management.git
cd hotel_management
```

2. Create a virtual environment:
```bash
python -m venv flask
source flask/Scripts/activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Project Structure

```
hotel_management/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── instance/
│   └── hotel.db          # SQLite database
├── static/
│   └── css/
│       └── style.css     # Application styles
├── templates/
│   ├── base.html         # Base template
│   ├── dashboard.html    # Dashboard page
│   ├── guests.html       # Guests listing
│   ├── guest_form.html   # Guest form
│   ├── rooms.html        # Rooms listing
│   ├── room_form.html    # Room form
│   ├── bookings.html     # Bookings listing
│   └── booking_form.html # Booking form
└── flask/                # Virtual environment
```

## Usage

### Dashboard
View an overview of your hotel operations including guest count, room availability, and active bookings.

### Manage Guests
- Add new guest information
- Update existing guest profiles
- View all registered guests

### Manage Rooms
- Add rooms with pricing and capacity information
- Update room details and status
- Track room availability

### Manage Bookings
- Create new reservations
- Update booking information
- Track booking status

## Dependencies

- Flask 3.1.3
- Flask-SQLAlchemy 3.1.1
- SQLAlchemy 2.0.51
- Jinja2 3.1.6
- Click 8.4.2
- Werkzeug 3.1.8

## License

This project is open source and available under the MIT License.

## Author

Developed by massawes

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## Contact

For questions or suggestions, please open an issue on the GitHub repository.

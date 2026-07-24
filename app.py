from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'change-this-secret-key-in-production'

db = SQLAlchemy(app)


# ---------------------- MODELS ----------------------

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(10), unique=True, nullable=False)
    room_type = db.Column(db.String(50), nullable=False)   # Single, Double, Suite, Deluxe
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Available')  # Available, Occupied, Maintenance
    bookings = db.relationship('Booking', backref='room', lazy=True)

    def __repr__(self):
        return f'<Room {self.room_number}>'


class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200))
    bookings = db.relationship('Booking', backref='guest', lazy=True)

    def __repr__(self):
        return f'<Guest {self.full_name}>'


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guest_id = db.Column(db.Integer, db.ForeignKey('guest.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    check_in_date = db.Column(db.Date, nullable=False)
    check_out_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Booked')  # Booked, Checked In, Checked Out, Cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def total_nights(self):
        return (self.check_out_date - self.check_in_date).days

    def total_amount(self):
        return self.total_nights() * self.room.price


# ---------------------- DASHBOARD ----------------------

@app.route('/')
def dashboard():
    total_rooms = Room.query.count()
    available_rooms = Room.query.filter_by(status='Available').count()
    occupied_rooms = Room.query.filter_by(status='Occupied').count()
    total_guests = Guest.query.count()
    active_bookings = Booking.query.filter_by(status='Checked In').count()
    recent_bookings = Booking.query.order_by(Booking.created_at.desc()).limit(5).all()

    return render_template('dashboard.html',
                            total_rooms=total_rooms,
                            available_rooms=available_rooms,
                            occupied_rooms=occupied_rooms,
                            total_guests=total_guests,
                            active_bookings=active_bookings,
                            recent_bookings=recent_bookings)


# ---------------------- ROOMS ----------------------

@app.route('/rooms')
def rooms():
    all_rooms = Room.query.order_by(Room.room_number).all()
    return render_template('rooms.html', rooms=all_rooms)


@app.route('/rooms/add', methods=['GET', 'POST'])
def add_room():
    if request.method == 'POST':
        room_number = request.form['room_number']
        if Room.query.filter_by(room_number=room_number).first():
            flash('Room number already exists!', 'danger')
            return redirect(url_for('add_room'))

        new_room = Room(
            room_number=room_number,
            room_type=request.form['room_type'],
            price=float(request.form['price']),
            status=request.form.get('status', 'Available')
        )
        db.session.add(new_room)
        db.session.commit()
        flash('Room added successfully!', 'success')
        return redirect(url_for('rooms'))

    return render_template('room_form.html', room=None)


@app.route('/rooms/edit/<int:room_id>', methods=['GET', 'POST'])
def edit_room(room_id):
    room = Room.query.get_or_404(room_id)
    if request.method == 'POST':
        room.room_number = request.form['room_number']
        room.room_type = request.form['room_type']
        room.price = float(request.form['price'])
        room.status = request.form['status']
        db.session.commit()
        flash('Room updated successfully!', 'success')
        return redirect(url_for('rooms'))

    return render_template('room_form.html', room=room)


@app.route('/rooms/delete/<int:room_id>', methods=['POST'])
def delete_room(room_id):
    room = Room.query.get_or_404(room_id)
    if room.bookings:
        flash('Cannot delete room with existing bookings!', 'danger')
        return redirect(url_for('rooms'))
    db.session.delete(room)
    db.session.commit()
    flash('Room deleted successfully!', 'success')
    return redirect(url_for('rooms'))


# ---------------------- GUESTS ----------------------

@app.route('/guests')
def guests():
    all_guests = Guest.query.order_by(Guest.full_name).all()
    return render_template('guests.html', guests=all_guests)


@app.route('/guests/add', methods=['GET', 'POST'])
def add_guest():
    if request.method == 'POST':
        new_guest = Guest(
            full_name=request.form['full_name'],
            email=request.form['email'],
            phone=request.form['phone'],
            address=request.form.get('address', '')
        )
        db.session.add(new_guest)
        db.session.commit()
        flash('Guest added successfully!', 'success')
        return redirect(url_for('guests'))

    return render_template('guest_form.html', guest=None)


@app.route('/guests/edit/<int:guest_id>', methods=['GET', 'POST'])
def edit_guest(guest_id):
    guest = Guest.query.get_or_404(guest_id)
    if request.method == 'POST':
        guest.full_name = request.form['full_name']
        guest.email = request.form['email']
        guest.phone = request.form['phone']
        guest.address = request.form.get('address', '')
        db.session.commit()
        flash('Guest updated successfully!', 'success')
        return redirect(url_for('guests'))

    return render_template('guest_form.html', guest=guest)


@app.route('/guests/delete/<int:guest_id>', methods=['POST'])
def delete_guest(guest_id):
    guest = Guest.query.get_or_404(guest_id)
    if guest.bookings:
        flash('Cannot delete guest with existing bookings!', 'danger')
        return redirect(url_for('guests'))
    db.session.delete(guest)
    db.session.commit()
    flash('Guest deleted successfully!', 'success')
    return redirect(url_for('guests'))


# ---------------------- BOOKINGS ----------------------

@app.route('/bookings')
def bookings():
    all_bookings = Booking.query.order_by(Booking.created_at.desc()).all()
    return render_template('bookings.html', bookings=all_bookings)


@app.route('/bookings/add', methods=['GET', 'POST'])
def add_booking():
    guests_list = Guest.query.order_by(Guest.full_name).all()
    rooms_list = Room.query.filter_by(status='Available').order_by(Room.room_number).all()

    if request.method == 'POST':
        check_in = datetime.strptime(request.form['check_in_date'], '%Y-%m-%d').date()
        check_out = datetime.strptime(request.form['check_out_date'], '%Y-%m-%d').date()

        if check_out <= check_in:
            flash('Check-out date must be after check-in date!', 'danger')
            return redirect(url_for('add_booking'))

        room = Room.query.get(int(request.form['room_id']))

        new_booking = Booking(
            guest_id=int(request.form['guest_id']),
            room_id=room.id,
            check_in_date=check_in,
            check_out_date=check_out,
            status='Booked'
        )
        db.session.add(new_booking)
        db.session.commit()
        flash('Booking created successfully!', 'success')
        return redirect(url_for('bookings'))

    return render_template('booking_form.html', guests=guests_list, rooms=rooms_list, today=date.today().isoformat())


@app.route('/bookings/checkin/<int:booking_id>', methods=['POST'])
def checkin_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    booking.status = 'Checked In'
    booking.room.status = 'Occupied'
    db.session.commit()
    flash('Guest checked in successfully!', 'success')
    return redirect(url_for('bookings'))


@app.route('/bookings/checkout/<int:booking_id>', methods=['POST'])
def checkout_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    booking.status = 'Checked Out'
    booking.room.status = 'Available'
    db.session.commit()
    flash('Guest checked out successfully!', 'success')
    return redirect(url_for('bookings'))


@app.route('/bookings/cancel/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.status == 'Checked In':
        booking.room.status = 'Available'
    booking.status = 'Cancelled'
    db.session.commit()
    flash('Booking cancelled.', 'info')
    return redirect(url_for('bookings'))


@app.route('/bookings/delete/<int:booking_id>', methods=['POST'])
def delete_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.status == 'Checked In':
        booking.room.status = 'Available'
    db.session.delete(booking)
    db.session.commit()
    flash('Booking deleted.', 'info')
    return redirect(url_for('bookings'))


# ---------------------- MAIN ----------------------

def create_tables():
    with app.app_context():
        db.create_all()


if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

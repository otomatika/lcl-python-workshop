from flask import Flask, request, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv("notebooks/.env")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mariadb+mariadbconnector://{os.environ["M_USER"]}:{os.environ["M_PW"]}@{os.environ["M_SERVER"]}/{os.environ["M_DB"]}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Reuse the Truck model class definition
class Truck(db.Model):
    __tablename__ = 'orm-trucks'

    truck_id = db.Column(db.Integer, primary_key=True)
    license_plate = db.Column(db.String(15), nullable=False)
    model = db.Column(db.String(40), nullable=False)
    capacity_ton = db.Column(db.Integer)
    maintenance_date = db.Column(db.Date)

    def __repr__(self):
        return f"<Truck(license_plate='{self.license_plate}', model='{self.model}')>"
    
@app.route('/init')
def init_db():
    db.create_all()
    
@app.route('/add', methods=['GET', 'POST'])
def add_truck():
    if request.method == 'POST':
        license_plate = request.form['license_plate']
        model = request.form['model']
        capacity_ton = request.form.get('capacity_ton', type=int)
        new_truck = Truck(license_plate=license_plate, model=model, capacity_ton=capacity_ton)
        db.session.add(new_truck)
        db.session.commit()
        return redirect(url_for('list_trucks'))
    return render_template('add_truck.html')


#### Listing All Trucks
@app.route('/')
@app.route('/trucks')
def list_trucks():
    trucks = Truck.query.all()
    return render_template('list_trucks.html', trucks=trucks)

#### Editing a Truck
@app.route('/edit/<int:truck_id>', methods=['GET', 'POST'])
def edit_truck(truck_id):
    truck = Truck.query.get_or_404(truck_id)
    if request.method == 'POST':
        truck.license_plate = request.form['license_plate']
        truck.model = request.form['model']
        truck.capacity_ton = request.form.get('capacity_ton', type=int)
        db.session.commit()
        return redirect(url_for('list_trucks'))
    return render_template('edit_truck.html', truck=truck)

#### Deleting a Truck
@app.route('/delete/<int:truck_id>', methods=['POST'])
def delete_truck(truck_id):
    truck = Truck.query.get_or_404(truck_id)
    db.session.delete(truck)
    db.session.commit()
    return redirect(url_for('list_trucks'))

if __name__ == '__main__':
    app.run(debug=True)
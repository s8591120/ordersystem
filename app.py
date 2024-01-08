from flask import Flask, render_template, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import qrcode

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)
admin = Admin(app, name='menu_admin', template_mode='bootstrap3')


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Integer, nullable=False)


with app.app_context():
    db.create_all()

admin.add_view(ModelView(Item, db.session))
admin.add_view(ModelView(Order, db.session))

# Generate QR Code dynamically
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
# Replace with your actual server URL
qr.add_data("http://192.168.1.101:5000/")
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
img.save("static/menu_qrcode.png")


@app.route('/')
def menu():
    menu_items = Item.query.all()
    return render_template('menu.html', menu_items=menu_items)


@app.route('/checkout', methods=['POST'])
def checkout():
    try:
        data = request.json
        total_price = 0

        for item in data:
            quantity = int(item.get('quantity', 1))
            total_price += int(item['price']) * quantity

            order = Order(
                item_name=item['name'],
                quantity=quantity,
                total_price=int(item['price']) * quantity
            )

            db.session.add(order)

        db.session.commit()
        return jsonify({'message': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)})
    print("Data received:", data)


@app.route('/qrcode')
def get_qrcode():
    return send_file("static/menu_qrcode.png", mimetype="image/png")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

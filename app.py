from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

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
    table_number = db.Column(db.String(255), nullable=False)
    takeout = db.Column(db.Boolean, nullable=False)
    item_name = db.Column(db.String(255), nullable=False)  # 品名
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Integer, nullable=False)

    # 增加外鍵關係
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    item = db.relationship('Item', backref='orders')


# 應用程式上下文中創建資料庫
with app.app_context():
    db.create_all()


admin.add_view(ModelView(Item, db.session))
admin.add_view(ModelView(Order, db.session))


# 路由 - 菜單頁面
@app.route('/')
def menu():
    menu_items = Item.query.all()
    return render_template('menu.html', menu_items=menu_items)


# 路由 - 購物車頁面
@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if request.method == 'POST':
        # 處理購物車表單提交
        table_number = request.form['table_number']
        takeout = int(request.form['takeout'])
        item_id = int(request.form['item'])
        quantity = int(request.form['quantity'])

        item = Item.query.get(item_id)
        total_price = item.price * quantity

        order = Order(table_number=table_number,
                      takeout=takeout,
                      item_name=item.name,  # 使用品名
                      quantity=quantity,
                      total_price=total_price,
                      item=item  # 增加 item 欄位的設定
                      )
        db.session.add(order)
        db.session.commit()

        return redirect(url_for('menu'))

    orders = Order.query.all()
    return render_template('cart.html', orders=orders)


# 路由 - 結帳
@app.route('/checkout', methods=['POST'])
def checkout():
    # 在這裡處理結帳，將訂單傳送到資料庫，然後清空購物車

    return redirect(url_for('menu'))


if __name__ == '__main__':
    app.run(debug=True)

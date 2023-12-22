from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

import csv
import json

app = Flask(__name__)
app.secret_key = 'some_secure_random_key'

# Остальная часть вашего кода
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:rootroot@127.0.0.1/postgres'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<News %r>' % self.id

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True)
    text = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255))  # URL изображения

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    # Связь с Category
    category = db.relationship('Category', backref=db.backref('items', lazy=True))

    # для вывода названия
    def __repr__(self):
        return self.title

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(512))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    quantity = db.Column(db.Integer, default=1)

    user = db.relationship('User', backref=db.backref('carts', lazy=True))
    item = db.relationship('Item', backref=db.backref('carts', lazy=True))

    def __repr__(self):
        return '<Cart User: {} Item: {} Quantity: {}>'.format(self.user_id, self.item_id, self.quantity)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    total_price = db.Column(db.Float)
    status = db.Column(db.String(100))
    order_date = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('orders', lazy=True))
    delivery_address_id = db.Column(db.Integer, db.ForeignKey('delivery_address.id'))

    # Связь с DeliveryAddress
    delivery_address = db.relationship('DeliveryAddress')

    def __repr__(self):
        return '<Order {}>'.format(self.id)


class OrderItem(db.Model):
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key=True)
    quantity = db.Column(db.Integer, default=1)

    order = db.relationship('Order', backref=db.backref('order_items', lazy=True))
    item = db.relationship('Item', backref=db.backref('order_items', lazy=True))


class DeliveryAddress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    country = db.Column(db.String(100))
    city = db.Column(db.String(100))
    street = db.Column(db.String(100))
    phone = db.Column(db.String(20))

    user = db.relationship('User', backref=db.backref('delivery_addresses', lazy=True))

    def __repr__(self):
        return f'<DeliveryAddress {self.country}, {self.city}, {self.street}>'

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f'<Category {self.name}>'




# Создание экземпляра LoginManager
login_manager = LoginManager()

# Инициализируйте LoginManager
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['email']  # Убедитесь, что здесь должно быть 'email', а не 'username'
        password = request.form['password']
        user = User.query.filter_by(email=username).first()  # Проверьте, что фильтр по email, а не по username

        if user and user.check_password(password):
            login_user(user)
            return redirect('catalog')  # Убедитесь, что маршрут 'catalog' существует
        # Если ошибка, добавьте сообщение об ошибке
    return render_template('login.html')




@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            # Обработка ситуации, когда пользователь уже существует
            return '''<h1>Пользователь с таким именем уже существует. Пожалуйста, выберите другое имя.</h1>
                      <a href="{}"><button>Вернуться</button></a>'''.format(url_for('register'))

        email = request.form['email']
        password = request.form['password']

        new_user = User(username=username, email=email)

        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('catalog')  # Убедитесь, что маршрут 'catalog' существует

    return render_template('register.html')



@app.route('/forgot_password')
def forgot_password():
    # Логика восстановления пароля
    return render_template('forgot_password.html')



@app.route('/profile')
@login_required
def profile():
    orders = Order.query.filter_by(user_id=current_user.id).all()

    # Экспорт в JSON
    orders_json = [{'id': o.id, 'total_price': o.total_price, 'status': o.status, 'order_date': o.order_date.strftime("%Y-%m-%d %H:%M:%S")} for o in orders]
    with open('user_orders.json', 'w', encoding='utf-8') as jsonfile:
        json.dump(orders_json, jsonfile, ensure_ascii=False, indent=4)

    # Экспорт в CSV
    with open('user_orders.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['id', 'total_price', 'status', 'order_date'])
        for o in orders:
            writer.writerow([o.id, o.total_price, o.status, o.order_date.strftime("%Y-%m-%d %H:%M:%S")])

    return render_template('profile.html', orders=orders)



@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/create', methods=['POST', 'GET'])
def create():
    # Загружаем список категорий для отображения в форме
    categories = Category.query.all()

    if request.method == "POST":
        # Получение данных из формы
        title = request.form['title']
        price = request.form['price']
        text = request.form['text']
        image_url = request.form['image_url']
        category_id = request.form.get('category_id')

        # Создание и сохранение нового товара
        item = Item(title=title, price=price, text=text, image_url=image_url, category_id=category_id)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/catalog')
        except Exception as e:
            print(e)  # Вывод информации об ошибке в консоль
            return "Произошла ошибка при добавлении товара"

    # Отображаем форму с передачей списка категорий
    return render_template("create.html", categories=categories)


@app.route('/posts')
def posts():
    news = News.query.order_by(News.date.desc()).all()

    # Экспорт в JSON
    news_json = [{'id': n.id, 'title': n.title, 'intro': n.intro, 'text': n.text, 'date': n.date.strftime("%Y-%m-%d %H:%M:%S")} for n in news]
    with open('news_data.json', 'w', encoding='utf-8') as jsonfile:
        json.dump(news_json, jsonfile, ensure_ascii=False, indent=4)

    # Экспорт в CSV
    with open('news_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['id', 'title', 'intro', 'text', 'date'])
        for n in news:
            writer.writerow([n.id, n.title, n.intro, n.text, n.date.strftime("%Y-%m-%d %H:%M:%S")])

    return render_template("posts.html", news=news)


@app.route('/posts/<int:id>')
def posts_id(id):
    # запрос бд, сортиврока по дате возрастающей
    new = News.query.get(id)
    return render_template("posts_id.html", new=new)


@app.route('/posts/<int:id>/delete')
def posts_id_delete(id):
    new = News.query.get_or_404(id)

    # Сохранение данных перед удалением
    news_data = {'id': new.id, 'title': new.title, 'intro': new.intro, 'text': new.text,
                 'date': new.date.strftime("%Y-%m-%d %H:%M:%S")}

    # Экспорт в JSON
    with open(f'news_deleted_{new.id}.json', 'w', encoding='utf-8') as jsonfile:
        json.dump(news_data, jsonfile, ensure_ascii=False, indent=4)

    # Экспорт в CSV
    with open(f'news_deleted_{new.id}.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['id', 'title', 'intro', 'text', 'date'])
        writer.writerow([new.id, new.title, new.intro, new.text, new.date.strftime("%Y-%m-%d %H:%M:%S")])

    try:
        db.session.delete(new)
        db.session.commit()
        return redirect('/posts')
    except:
        return "При удалении новости произошла ошибка"

# получение данных и их обработка
@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    new = News.query.get(id)
    if request.method == "POST":
        # подставляем значение из формочки
        new.title = request.form['title']
        new.intro = request.form['intro']
        new.text = request.form['text']

        # сохранение полученного объекта в бд
        try:
            #сохранение
            db.session.commit()
            return redirect('/posts')
        except:
            return "При редактировании статьи произошла ошибка"
    else:
        # поиск статьи определенной
        return render_template("post_update.html", new=new)


# получение данных и их обработка
@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        # создение полученного объекта
        news = News(title=title, intro=intro, text=text)

        # сохранение полученного объекта в бд
        try:
            db.session.add(news)
            #сохранение
            db.session.commit()
            return redirect('/posts')
        except:
            return "При добавлении статьи произошла ошибка"
    else:
        return render_template("create-article.html")


@app.route('/cart')
def cart():
    # Логика для отображения страницы корзины
    return render_template('cart.html')

@app.route('/catalog')
def catalog():
    categories = Category.query.all()
    cart_items = Cart.query.filter_by(user_id=current_user.id).all() if current_user.is_authenticated else []
    cart_dict = {item.item_id: item.quantity for item in cart_items}

    # Проход по каждой категории и добавление информации о количестве в корзине для каждого товара
    for category in categories:
        for item in category.items:
            item.in_cart = item.id in cart_dict
            item.quantity_in_cart = cart_dict.get(item.id, 0)

    # Экспорт данных категорий и товаров в JSON
    categories_json = [{
        'category_id': cat.id,
        'category_name': cat.name,
        'items': [{'id': item.id, 'title': item.title, 'price': item.price, 'isActive': item.isActive, 'quantity_in_cart': cart_dict.get(item.id, 0)} for item in cat.items]
    } for cat in categories]

    with open('catalog_data.json', 'w', encoding='utf-8') as jsonfile:
        json.dump(categories_json, jsonfile, ensure_ascii=False, indent=4)

    # Экспорт данных категорий и товаров в CSV
    with open('catalog_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['category_id', 'category_name', 'item_id', 'item_title', 'item_price', 'item_isActive', 'item_quantity_in_cart'])
        for cat in categories:
            for item in cat.items:
                writer.writerow([cat.id, cat.name, item.id, item.title, item.price, item.isActive, cart_dict.get(item.id, 0)])

    return render_template("catalog.html", categories=categories)



@app.route('/add_to_cart/<int:item_id>', methods=['POST'])
@login_required
def add_to_cart(item_id):
    cart_item = Cart.query.filter_by(user_id=current_user.id, item_id=item_id).first()
    if cart_item:
        cart_item.quantity += 1
    else:
        new_cart_item = Cart(user_id=current_user.id, item_id=item_id, quantity=1)
        db.session.add(new_cart_item)
    db.session.commit()
    return redirect(url_for('catalog'))

@app.route('/update_cart/<int:item_id>/<int:quantity>', methods=['POST'])
@login_required
def update_cart(item_id, quantity):
    cart_item = Cart.query.filter_by(user_id=current_user.id, item_id=item_id).first()
    if cart_item:
        cart_item.quantity = quantity
        db.session.commit()
    return redirect(url_for('catalog'))


@app.route('/increase_quantity/<int:cart_id>')
@login_required
def increase_quantity(cart_id):
    cart_item = Cart.query.get_or_404(cart_id)
    if cart_item.user_id == current_user.id:
        cart_item.quantity += 1
        db.session.commit()
    return redirect(url_for('cart'))

@app.route('/decrease_quantity/<int:cart_id>')
@login_required
def decrease_quantity(cart_id):
    cart_item = Cart.query.get_or_404(cart_id)
    if cart_item.user_id == current_user.id:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            db.session.commit()
        else:
            # Если количество равно 1, удаляем товар из корзины
            db.session.delete(cart_item)
            db.session.commit()
    return redirect(url_for('cart'))



@app.route('/remove_from_cart/<int:cart_id>')
@login_required
def remove_from_cart(cart_id):
    cart_item = Cart.query.get_or_404(cart_id)
    if cart_item.user_id == current_user.id:
        db.session.delete(cart_item)
        db.session.commit()
    return redirect(url_for('cart'))


@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    if request.method == 'POST':
        country = request.form.get('country')
        city = request.form.get('city')
        street = request.form.get('street')
        phone = request.form.get('phone')

        # Создаем адрес доставки
        delivery_address = DeliveryAddress(user_id=current_user.id, country=country, city=city, street=street, phone=phone)
        db.session.add(delivery_address)

        # Подсчет общей стоимости заказа
        total_price = 0
        cart_items = Cart.query.filter_by(user_id=current_user.id).all()
        for item in cart_items:
            total_price += item.item.price * item.quantity

        # Создаем заказ
        new_order = Order(user_id=current_user.id, total_price=total_price, status='Processing', order_date=datetime.utcnow())
        db.session.add(new_order)

        # Переносим товары из корзины в заказ
        for item in cart_items:
            order_item = OrderItem(order=new_order, item_id=item.item_id, quantity=item.quantity)
            db.session.add(order_item)
            db.session.delete(item)

        db.session.commit()

        # Перенаправление на страницу подтверждения заказа
        return redirect(url_for('order_confirmation', order_id=new_order.id))

    elif request.method == 'GET':
        # Получаем товары из корзины
        cart_items = Cart.query.filter_by(user_id=current_user.id).all()

        # Передаем список товаров в шаблон
        return render_template('checkout.html', cart_items=cart_items)

    return render_template('checkout.html')



@app.route('/order_confirmation')
@login_required
def order_confirmation():
    order_id = request.args.get('order_id')
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first()

    if not order:
        return redirect(url_for('index'))

    return render_template('order_confirmation.html', order=order)


@app.route('/order_details/<int:order_id>')
@login_required
def order_details(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        # Если пользователь пытается посмотреть чужой заказ, отправляем его обратно на профиль или главную.
        return redirect(url_for('profile'))

    # Собираем данные заказа для экспорта
    order_items = OrderItem.query.filter_by(order_id=order_id).all()
    order_items_json = []
    order_items_csv = [['item_id', 'quantity', 'price_each', 'total_price']]

    for item in order_items:
        item_data = {
            'item_id': item.item_id,
            'quantity': item.quantity,
            'price_each': item.item.price,
            'total_price': item.quantity * item.item.price
        }
        order_items_json.append(item_data)
        order_items_csv.append([item.item_id, item.quantity, item.item.price, item.quantity * item.item.price])

    # Экспорт данных заказа в JSON
    with open(f'order_{order_id}_details.json', 'w', encoding='utf-8') as jsonfile:
        json.dump(order_items_json, jsonfile, ensure_ascii=False, indent=4)

    # Экспорт данных заказа в CSV
    with open(f'order_{order_id}_details.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(order_items_csv)

    # Подразумевается, что есть страница order_details.html для показа деталей заказа
    return render_template('order_details.html', order=order)




if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
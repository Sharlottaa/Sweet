from config import *


# Модель новостей с полями для идентификатора, заголовка, введения, полного текста и даты публикации
class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<News %r>' % self.id


# Модель товара с полями для идентификатора, названия, цены, статуса активности, описания и URL изображения
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True)
    text = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255))  # URL изображения

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref=db.backref('items', lazy=True))

    def __repr__(self):
        return self.title


# Модель пользователя с полями для идентификатора, имени пользователя, электронной почты и хэшированного пароля
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(512))
    role = db.Column(db.String(50), nullable=False, default='Пользователь')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == 'Администратор'


# Модель корзины с полями для идентификатора, связей с пользователем и товаром, а также количеством товара
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    quantity = db.Column(db.Integer, default=1)

    user = db.relationship('User', backref=db.backref('carts', lazy=True))
    item = db.relationship('Item', backref=db.backref('carts', lazy=True))

    def __repr__(self):
        return '<Cart User: {} Item: {} Quantity: {}>'.format(self.user_id, self.item_id, self.quantity)


# Модель заказа с полями для идентификатора, связи с пользователем, общей стоимости, статуса и даты заказа
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    total_price = db.Column(db.Float)
    status = db.Column(db.String(100))
    order_date = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('orders', lazy=True))
    delivery_address_id = db.Column(db.Integer, db.ForeignKey('delivery_address.id'))
    delivery_address = db.relationship('DeliveryAddress')

    def __repr__(self):
        return '<Order {}>'.format(self.id)


# Модель элемента заказа с полями для идентификатора заказа и товара, а также количеством заказанного товара
class OrderItem(db.Model):
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key=True)
    quantity = db.Column(db.Integer, default=1)

    order = db.relationship('Order', backref=db.backref('order_items', lazy=True))
    item = db.relationship('Item', backref=db.backref('order_items', lazy=True))


# Модель адреса доставки с полями для идентификатора, связи с пользователем, страны, города, улицы и телефона
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


# Модель категории с полем для идентификатора и уникального названия категории
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f'<Category {self.name}>'

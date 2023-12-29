from models import *  # Импорт всех классов из файла models.py
from flask_login import current_user
from functools import wraps


# Декоратор для проверки административной роли
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != 'Администратор':
            return redirect(url_for('index', next=request.url))
        return f(*args, **kwargs)

    return decorated_function


# Создание экземпляра LoginManager, который управляет процессом авторизации пользователей
login_manager = LoginManager()

# Инициализация LoginManager с приложением Flask
login_manager.init_app(app)


# Функция загрузки пользователя, используемая Flask-Login для связи идентификатора пользователя с объектом пользователя
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Загрузка пользователя по его ID


# Маршрут и функция для страницы входа в систему
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':  # Если метод запроса POST, обрабатываем отправленные данные формы
        username = request.form['email']  # Получаем email введенный пользователем
        password = request.form['password']  # Получаем пароль, введенный пользователем
        user = User.query.filter_by(email=username).first()  # Ищем пользователя в базе данных по email

        # Проверяем, есть ли пользователь и верен ли пароль
        if user and user.check_password(password):
            login_user(user)  # Авторизуем пользователя
            return redirect('catalog')  # Перенаправляем пользователя в каталог
    return render_template('login.html')  # Отображаем страницу входа


# Маршрут и функция для выхода из системы
@app.route('/logout')
@login_required  # Требуется быть авторизованным для доступа
def logout():
    logout_user()  # Выход пользователя из системы
    return redirect(url_for('index'))  # Перенаправляем на главную страницу


# Маршрут и функция для страницы регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':  # Если метод запроса POST, обрабатываем отправленные данные формы
        username = request.form['username']  # Получаем имя пользователя
        existing_user = User.query.filter_by(
            username=username).first()  # Проверяем, не зарегистрирован ли уже такой пользователь

        # Если пользователь уже существует, возвращаем ошибку
        if existing_user:
            return '''<h1>Пользователь с таким именем уже существует. Пожалуйста, выберите другое имя.</h1>
                      <a href="{}"><button>Вернуться</button></a>'''.format(url_for('register'))

        email = request.form['email']  # Получаем email
        password = request.form['password']  # Получаем пароль

        new_user = User(username=username, email=email)  # Создаем нового пользователя

        new_user.set_password(password)  # Устанавливаем пароль пользователя
        db.session.add(new_user)  # Добавляем пользователя в базу данных
        db.session.commit()  # Сохраняем изменения
        return redirect('catalog')  # Перенаправляем в каталог

    return render_template('register.html')  # Отображаем страницу регистрации


# Маршрут и функция для страницы восстановления пароля
@app.route('/forgot_password')
def forgot_password():
    # Логика восстановления пароля (не реализована в представленном коде)
    return render_template('forgot_password.html')


import json
import csv


# Функция для экспорта данных в JSON
def export_to_json(data, file_name):
    with open(file_name, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=4)



# Функция для экспорта данных в CSV
def export_to_csv(data, headers, file_name):
    with open(file_name, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(data)


# Маршрут и функция для страницы профиля пользователя
@app.route('/profile')
@login_required  # Требуется быть авторизованным для доступа
def profile():
    orders = Order.query.filter_by(user_id=current_user.id).all()  # Получаем все заказы текущего пользователя

    # Экспорт информации о заказах в JSON
    orders_json = [{'id': o.id, 'total_price': o.total_price, 'status': o.status,
                    'order_date': o.order_date.strftime("%Y-%m-%d %H:%M:%S")} for o in orders]
    export_to_json(orders_json, 'user_orders.json')

    # Экспорт информации о заказах в CSV
    orders_csv = [[o.id, o.total_price, o.status, o.order_date.strftime("%Y-%m-%d %H:%M:%S")] for o in orders]
    headers = ['id', 'total_price', 'status', 'order_date']
    export_to_csv(orders_csv, headers, 'user_orders.csv')

    return render_template('profile.html', orders=orders)


# (Продолжение комментариев будет в следующем сообщении...)


# Маршрут для главной страницы
@app.route('/')
def index():
    return render_template("index.html")


# Маршрут для страницы "О нас"
@app.route('/about')
def about():
    return render_template("about.html")


# Маршрут для страницы создания товара
@app.route('/create', methods=['POST', 'GET'])
@login_required
@admin_required
def create():
    # Проверяем, является ли пользователь администратором
    if current_user.is_admin():

        categories = Category.query.all()  # Загрузка категорий для отображения в форме
        if request.method == "POST":
            title = request.form['title']
            price = request.form['price']
            text = request.form['text']
            image_url = request.form['image_url']
            category_id = request.form.get('category_id')

            item = Item(title=title, price=price, text=text, image_url=image_url, category_id=category_id)

            try:
                db.session.add(item)
                db.session.commit()
                return redirect('/catalog')
            except Exception as e:
                print(e)  # Вывод информации об ошибке в консоль
                return "Произошла ошибка при добавлении товара"

        return render_template("create.html", categories=categories)
    else:
        return "У вас нет прав доступа к этой странице", 403


@app.route('/item/<int:item_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)

    # Make sure this matches the method or attribute in your User model
    if current_user.is_admin():
        db.session.delete(item)
        db.session.commit()
        return redirect(url_for('catalog'))  # Or wherever you want to redirect
    else:
        return 'You do not have permission to perform this action', 403


# Маршрут для страницы со списком всех новостей
@app.route('/posts')
@login_required
def posts():
    news = News.query.order_by(News.date.desc()).all()

    # Подготовка данных для экспорта в JSON
    news_json = [
        {'id': n.id, 'title': n.title, 'intro': n.intro, 'text': n.text, 'date': n.date.strftime("%Y-%m-%d %H:%M:%S")}
        for n in news]
    export_to_json(news_json, 'news_data.json')

    # Подготовка данных для экспорта в CSV
    news_csv = [[n.id, n.title, n.intro, n.text, n.date.strftime("%Y-%m-%d %H:%M:%S")] for n in news]
    headers = ['id', 'title', 'intro', 'text', 'date']
    export_to_csv(news_csv, headers, 'news_data.csv')

    return render_template("posts.html", news=news)


@app.route('/posts/<int:id>')
@login_required
def posts_id(id):
    # запрос бд, сортиврока по дате возрастающей
    new = News.query.get(id)
    return render_template("posts_id.html", new=new)


@app.route('/posts/<int:id>/delete')
@login_required
@admin_required
def posts_id_delete(id):
    new = News.query.get_or_404(id)

    # Сохранение данных перед удалением
    news_data = [{'id': new.id, 'title': new.title, 'intro': new.intro, 'text': new.text,
                  'date': new.date.strftime("%Y-%m-%d %H:%M:%S")}]

    # Экспорт в JSON
    export_to_json(news_data, f'news_deleted_{new.id}.json')

    # Подготовка данных и заголовков для экспорта в CSV
    news_csv = [[new.id, new.title, new.intro, new.text, new.date.strftime("%Y-%m-%d %H:%M:%S")]]
    headers = ['id', 'title', 'intro', 'text', 'date']
    export_to_csv(news_csv, headers, f'news_deleted_{new.id}.csv')

    try:
        db.session.delete(new)
        db.session.commit()
        return redirect('/posts')
    except:
        return "При удалении новости произошла ошибка"


# получение данных и их обработка
@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
@login_required
@admin_required
def post_update(id):
    new = News.query.get(id)
    if request.method == "POST":
        # подставляем значение из формочки
        new.title = request.form['title']
        new.intro = request.form['intro']
        new.text = request.form['text']

        # сохранение полученного объекта в бд
        try:
            # сохранение
            db.session.commit()
            return redirect('/posts')
        except:
            return "При редактировании статьи произошла ошибка"
    else:
        # поиск статьи определенной
        return render_template("post_update.html", new=new)


# получение данных и их обработка
@app.route('/create-article', methods=['POST', 'GET'])
@login_required
@admin_required
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
            # сохранение
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

    # Adding information about quantity in the cart for each item
    for category in categories:
        for item in category.items:
            item.in_cart = item.id in cart_dict
            item.quantity_in_cart = cart_dict.get(item.id, 0)

    # Preparing data for JSON export
    categories_json = [{
        'category_id': cat.id,
        'category_name': cat.name,
        'items': [{'id': item.id, 'title': item.title, 'price': item.price, 'isActive': item.isActive,
                   'quantity_in_cart': cart_dict.get(item.id, 0)} for item in cat.items]
    } for cat in categories]
    export_to_json(categories_json, 'catalog_data.json')

    # Preparing data for CSV export
    catalog_csv = []
    for cat in categories:
        for item in cat.items:
            catalog_csv.append(
                [cat.id, cat.name, item.id, item.title, item.price, item.isActive, cart_dict.get(item.id, 0)])
    headers = ['category_id', 'category_name', 'item_id', 'item_title', 'item_price', 'item_isActive',
               'item_quantity_in_cart']
    export_to_csv(catalog_csv, headers, 'catalog_data.csv')

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
        delivery_address = DeliveryAddress(user_id=current_user.id, country=country, city=city, street=street,
                                           phone=phone)
        db.session.add(delivery_address)

        # Подсчет общей стоимости заказа
        total_price = 0
        cart_items = Cart.query.filter_by(user_id=current_user.id).all()
        for item in cart_items:
            total_price += item.item.price * item.quantity

        # Создаем заказ
        new_order = Order(user_id=current_user.id, total_price=total_price, status='Processing',
                          order_date=datetime.utcnow())
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

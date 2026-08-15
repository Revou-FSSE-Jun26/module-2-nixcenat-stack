from app import create_app
from app.database import db
from app.models import User, Category, Product, Order, order_items

app = create_app()

with app.app_context():
    # Buat User, Kategori & Produk
    user = User(username="seeder_user", email="seeder@example.com", password_hash="dummy_hash", role="customer")
    cat = Category(category_name="Electronics", description="Gadgets and devices")
    p1 = Product(product_name="Mechanical Keyboard", price=89.99, stock_quantity=10, category=cat)
    p2 = Product(product_name="Wireless Mouse", price=49.99, stock_quantity=20, category=cat)
    
    db.session.add_all([user, cat, p1, p2])
    db.session.commit()

    # Buat 1 Order
    order = Order(user_id=user.user_id, total_amount=139.98, status="completed")
    db.session.add(order)
    db.session.commit()

    # Hubungkan 1 Order ke 2 Produk melalui Association Table
    item1 = order_items.insert().values(order_id=order.order_id, product_id=p1.product_id, quantity=1, unit_price=89.99)
    item2 = order_items.insert().values(order_id=order.order_id, product_id=p2.product_id, quantity=1, unit_price=49.99)
    
    db.session.execute(item1)
    db.session.execute(item2)
    db.session.commit()

    print("Data sampel Many-to-Many berhasil diisi!")
    
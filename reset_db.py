
from app import app, db
from models import User, MenuItem, StoreSettings
from werkzeug.security import generate_password_hash

def reset_database():
    """Reset database and create default users and data"""
    with app.app_context():
        # Drop all tables and recreate
        db.drop_all()
        db.create_all()
        
        # Create admin user
        admin_user = User(
            username='admin',
            email='admin@biryaniclub.com',
            full_name='Admin User',
            phone='9999999999',
            role='admin',
            is_active=True
        )
        admin_user.set_password('admin123')
        
        # Create delivery user
        delivery_user = User(
            username='delivery1',
            email='delivery@biryaniclub.com',
            full_name='Delivery Person',
            phone='8888888888',
            role='delivery',
            is_active=True
        )
        delivery_user.set_password('delivery123')
        
        # Create regular user
        customer_user = User(
            username='customer',
            email='customer@biryaniclub.com',
            full_name='Test Customer',
            phone='7777777777',
            role='customer',
            is_active=True
        )
        customer_user.set_password('customer123')
        
        db.session.add_all([admin_user, delivery_user, customer_user])
        
        # Store settings
        store_open = StoreSettings(key='store_open', value='true')
        db.session.add(store_open)
        
        # Sample menu items
        menu_items = [
            MenuItem(name='Chicken Biryani', description='Aromatic basmati rice with tender chicken pieces', price=299, category='Biryani', emoji='🍛', popularity=45, in_stock=True),
            MenuItem(name='Mutton Biryani', description='Royal mutton biryani with fragrant spices', price=399, category='Biryani', emoji='🍛', popularity=38, in_stock=True),
            MenuItem(name='Vegetable Biryani', description='Mixed vegetables with basmati rice', price=249, category='Biryani', emoji='🍛', popularity=22, in_stock=True),
            MenuItem(name='Chicken Tikka', description='Grilled chicken pieces with spices', price=199, category='Starters', emoji='🥘', popularity=31, in_stock=True),
            MenuItem(name='Paneer Tikka', description='Cottage cheese cubes marinated and grilled', price=179, category='Starters', emoji='🥘', popularity=19, in_stock=True),
            MenuItem(name='Raita', description='Yogurt with cucumber and spices', price=49, category='Sides', emoji='🥗', popularity=28, in_stock=True),
            MenuItem(name='Papad', description='Crispy lentil wafer', price=29, category='Sides', emoji='🥗', popularity=15, in_stock=True),
            MenuItem(name='Gulab Jamun', description='Sweet milk dumplings in sugar syrup', price=79, category='Desserts', emoji='🍰', popularity=25, in_stock=True),
            MenuItem(name='Lassi', description='Traditional yogurt drink', price=69, category='Beverages', emoji='🥤', popularity=18, in_stock=True),
            MenuItem(name='Masala Chai', description='Spiced tea', price=39, category='Beverages', emoji='🥤', popularity=33, in_stock=True)
        ]
        
        for item in menu_items:
            db.session.add(item)
        
        db.session.commit()
        
        print("✅ Database reset successfully!")
        print("\n🔑 Login Credentials:")
        print("👤 Admin: admin / admin123")
        print("🚚 Delivery: delivery1 / delivery123")
        print("🛒 Customer: customer / customer123")

if __name__ == '__main__':
    reset_database()

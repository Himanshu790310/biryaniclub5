from datetime import datetime
import pytz
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
import re
import random
import string

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(100))
    phone = db.Column(db.String(15), unique=True)
    role = db.Column(db.String(20), default='customer')  # customer, admin, delivery
    loyalty_points = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    # Relationships
    orders = db.relationship('Order', foreign_keys='Order.user_id', backref='user', lazy=True)
    delivered_orders = db.relationship('Order', foreign_keys='Order.delivery_person_id', backref='delivery_person_user', lazy=True)
    cart_items = db.relationship('CartItem', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == 'admin'

    def is_delivery_person(self):
        return self.role == 'delivery'

    def __repr__(self):
        return f'<User {self.username}>'

class MenuItem(db.Model):
    __tablename__ = 'menu_item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    emoji = db.Column(db.String(10))
    in_stock = db.Column(db.Boolean, default=True)
    popularity = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<MenuItem {self.name}>'

class CartItem(db.Model):
    __tablename__ = 'cart_item'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_item.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    menu_item = db.relationship('MenuItem', backref='cart_items')

    @property
    def total(self):
        return self.quantity * self.menu_item.price

    def __repr__(self):
        return f'<CartItem {self.menu_item.name} x{self.quantity}>'

class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Nullable for guest orders
    
    # Guest customer info (for non-registered users)
    guest_name = db.Column(db.String(100))
    guest_phone = db.Column(db.String(15))
    guest_email = db.Column(db.String(120))
    
    # Order details
    customer_name = db.Column(db.String(100), nullable=False)
    customer_phone = db.Column(db.String(15), nullable=False)
    customer_address = db.Column(db.Text, nullable=False)
    
    # Payment and totals
    subtotal = db.Column(db.Float, nullable=False)
    delivery_charges = db.Column(db.Float, default=0)
    discount = db.Column(db.Float, default=0)
    total_amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(20), nullable=False)  # cash, upi
    payment_status = db.Column(db.String(20), default='pending')  # pending, confirmed, failed
    coupon_code = db.Column(db.String(20))
    
    # Order status and tracking
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, preparing, out_for_delivery, delivered, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    confirmed_at = db.Column(db.DateTime)
    delivery_time = db.Column(db.DateTime)
    
    # Delivery
    delivery_person_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    delivery_notes = db.Column(db.Text)
    
    # Relationships
    order_items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')

    @property
    def is_guest_order(self):
        return self.user_id is None

    # Add random order number field
    order_number = db.Column(db.String(20), unique=True, nullable=False)
    
    @staticmethod
    def generate_order_number():
        """Generate random order number"""
        prefix = "BC"
        random_part = ''.join(random.choices(string.digits, k=6))
        return f"{prefix}{random_part}"
    
    @property
    def created_at_ist(self):
        """Convert created_at to IST"""
        ist = pytz.timezone('Asia/Kolkata')
        utc_time = self.created_at.replace(tzinfo=pytz.utc)
        return utc_time.astimezone(ist)
    
    @property
    def confirmed_at_ist(self):
        """Convert confirmed_at to IST"""
        if self.confirmed_at:
            ist = pytz.timezone('Asia/Kolkata')
            utc_time = self.confirmed_at.replace(tzinfo=pytz.utc)
            return utc_time.astimezone(ist)
        return None
    
    @property
    def delivery_time_ist(self):
        """Convert delivery_time to IST"""
        if self.delivery_time:
            ist = pytz.timezone('Asia/Kolkata')
            utc_time = self.delivery_time.replace(tzinfo=pytz.utc)
            return utc_time.astimezone(ist)
        return None

    @property
    def customer_display_name(self):
        if self.is_guest_order:
            return f"{self.guest_name or self.customer_name} (Guest)"
        return self.user.full_name or self.user.username

    def __repr__(self):
        return f'<Order {self.order_number}>'

class OrderItem(db.Model):
    __tablename__ = 'order_item'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_item.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Float, nullable=False)

    # Relationships
    menu_item = db.relationship('MenuItem')

    def __repr__(self):
        return f'<OrderItem {self.menu_item.name} x{self.quantity}>'

class StoreSettings(db.Model):
    __tablename__ = 'store_settings'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.String(500))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def get_setting(key, default_value=None):
        setting = StoreSettings.query.filter_by(key=key).first()
        return setting.value if setting else default_value

    @staticmethod
    def set_setting(key, value):
        setting = StoreSettings.query.filter_by(key=key).first()
        if setting:
            setting.value = value
            setting.updated_at = datetime.utcnow()
        else:
            setting = StoreSettings(key=key, value=value)
            db.session.add(setting)
        db.session.commit()

    def __repr__(self):
        return f'<StoreSettings {self.key}: {self.value}>'

class Promotion(db.Model):
    __tablename__ = 'promotion'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.String(200))
    discount_type = db.Column(db.String(20), nullable=False)  # 'percentage' or 'fixed'
    discount_value = db.Column(db.Float, nullable=False)
    min_order_amount = db.Column(db.Float, default=0)
    max_discount = db.Column(db.Float)  # For percentage discounts
    usage_limit = db.Column(db.Integer)  # Max number of uses
    used_count = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)

    @property
    def created_at_ist(self):
        """Convert created_at to IST"""
        ist = pytz.timezone('Asia/Kolkata')
        utc_time = self.created_at.replace(tzinfo=pytz.utc)
        return utc_time.astimezone(ist)

    @property
    def expires_at_ist(self):
        """Convert expires_at to IST"""
        if self.expires_at:
            ist = pytz.timezone('Asia/Kolkata')
            utc_time = self.expires_at.replace(tzinfo=pytz.utc)
            return utc_time.astimezone(ist)
        return None

    @property
    def is_expired(self):
        """Check if promotion has expired"""
        if self.expires_at:
            return datetime.utcnow() > self.expires_at
        return False

    @property
    def is_usage_exceeded(self):
        """Check if usage limit has been exceeded"""
        if self.usage_limit:
            return self.used_count >= self.usage_limit
        return False

    @property
    def is_valid(self):
        """Check if promotion is valid for use"""
        return (self.is_active and 
                not self.is_expired and 
                not self.is_usage_exceeded)

    def calculate_discount(self, subtotal):
        """Calculate discount amount for given subtotal"""
        if not self.is_valid or subtotal < self.min_order_amount:
            return 0

        if self.discount_type == 'percentage':
            discount = subtotal * (self.discount_value / 100)
            if self.max_discount:
                discount = min(discount, self.max_discount)
            return discount
        else:  # fixed amount
            return min(self.discount_value, subtotal)

    def use_promotion(self):
        """Mark promotion as used"""
        self.used_count += 1
        db.session.commit()

    def __repr__(self):
        return f'<Promotion {self.code}>'

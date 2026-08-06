import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import hashlib

app = Flask(__name__)

# CHIAVE SEGRETA – PRESA DALLE VARIABILI D'AMBIENTE DI RENDER
app.secret_key = os.environ.get('SECRET_KEY', 'supersecretkeychangeit')

# CONFIGURAZIONE DATABASE SQLITE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ------------------ CRYPTO WALLET CONFIG ------------------
CRYPTO_WALLETS = {
    "BTC": "17b5YpKcwMejoNvoqKNcMbzKcMzKwqcVwH",
    "ETH": "0x2e7edD5154Be461bae0BD9F79473FC54B0eeEE59",
    "LTC": "ltcmweb1qqtgle7hv2em03sd4llk3l006xec2mdu0dn2k9xwcrgcy2j3urrzfuqckemt5czlv0r3e50g7gg5a2dwklxvfdncd9kpkfpw8pk3yxjuy35ulkct7",
    "XMR": "459uXRXZknoRy3eq9TfZxKZ85jKWCZniBEh2U5GEg9VCYjT6f5U57cNjerJcpw2eF7jSmQwzh6sgmAQEL79HhM3NRmSu6ZT"
}
NETWORK_FEE = 0.0005
PAYPAL_LINK = "https://www.paypal.me/BotAi36"

# ------------------ MODELS ------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, pwd):
        self.password_hash = hashlib.sha256(pwd.encode()).hexdigest()

    def check_password(self, pwd):
        return self.password_hash == hashlib.sha256(pwd.encode()).hexdigest()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    price_usd = db.Column(db.Float, nullable=False)
    price_btc = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(200))
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    vendor = db.Column(db.String(50))
    rating = db.Column(db.Integer, default=5)

# ------------------ SEED DATABASE (80+ products) ------------------
def seed_products():
    if Product.query.count() > 0:
        return

    products_data = [
        # ------ CARDING ------
        ("Visa Prepaid Card 3000 USD x1", 109.00, 0.0171, "visa_3000_1.jpg", "Visa card with PIN. Worldwide ATM.", "Carding", "PLATINUM", 5),
        ("Visa Prepaid Card 3000 USD x3", 327.00, 0.0513, "visa_3000_3.jpg", "Three Visa cards, same balance.", "Carding", "PLATINUM", 5),
        ("Visa Prepaid Card 3000 USD x5", 545.00, 0.0855, "visa_3000_5.jpg", "Five Visa cards.", "Carding", "PLATINUM", 5),
        ("Visa Prepaid Card 3000 USD x10", 1090.00, 0.1710, "visa_3000_10.jpg", "Ten Visa cards.", "Carding", "PLATINUM", 5),
        ("Visa Prepaid Card 5000 USD x1", 175.00, 0.0275, "visa_5000_1.jpg", "High balance Visa.", "Carding", "A1 Quality", 4),
        ("Visa Prepaid Card 5000 USD x3", 525.00, 0.0824, "visa_5000_3.jpg", "Three high-balance Visa.", "Carding", "A1 Quality", 4),
        ("MasterCard Prepaid 3000 USD x1", 109.00, 0.0171, "mastercard_3000_1.jpg", "MasterCard with chip.", "Carding", "PLATINUM", 5),
        ("MasterCard Prepaid 3000 USD x3", 327.00, 0.0513, "mastercard_3000_3.jpg", "Three MasterCards.", "Carding", "PLATINUM", 5),
        ("MasterCard Prepaid 3000 USD x5", 545.00, 0.0855, "mastercard_3000_5.jpg", "Five MasterCards.", "Carding", "PLATINUM", 5),
        ("MasterCard Prepaid 3000 USD x10", 1190.00, 0.1868, "mastercard_3000_10.jpg", "Ten MasterCards.", "Carding", "PLATINUM", 5),
        ("American Express Prepaid 3000 USD x1", 109.00, 0.0171, "amex_3000_1.jpg", "Amex prepaid.", "Carding", "PLATINUM", 5),
        ("American Express Prepaid 3000 USD x3", 327.00, 0.0513, "amex_3000_3.jpg", "Three Amex.", "Carding", "PLATINUM", 5),
        ("American Express Prepaid 3000 USD x5", 545.00, 0.0855, "amex_3000_5.jpg", "Five Amex.", "Carding", "PLATINUM", 5),
        ("American Express Prepaid 3000 USD x10", 1190.00, 0.1868, "amex_3000_10.jpg", "Ten Amex.", "Carding", "PLATINUM", 5),
        ("PayPal Prepaid Mastercard - $2548", 127.00, 0.0199, "paypal_2548.jpg", "PayPal prepaid.", "Carding", "Evil Shop", 4),
        ("PayPal Prepaid Mastercard - $2746", 137.00, 0.0215, "paypal_2746.jpg", "Balance $2746.", "Carding", "Evil Shop", 4),
        ("PayPal Prepaid Mastercard - $2953", 148.00, 0.0232, "paypal_2953.jpg", "Balance $2953.", "Carding", "Evil Shop", 4),
        ("PayPal Prepaid Mastercard - $3200", 160.00, 0.0251, "paypal_3200.jpg", "High balance PayPal.", "Carding", "Evil Shop", 4),
        ("Chime Visa Debit Card - $4576", 229.00, 0.0359, "chime_4576.jpg", "Chime Visa $4576.", "Carding", "BeRich", 4),
        ("Chime Visa Debit Card - $4764", 238.00, 0.0373, "chime_4764.jpg", "Chime Visa $4764.", "Carding", "BeRich", 4),
        ("Chime Visa Debit Card - $4984", 249.00, 0.0391, "chime_4984.jpg", "Chime Visa $4984.", "Carding", "BeRich", 4),
        ("Chime Visa Debit Card - $5100", 255.00, 0.0400, "chime_5100.jpg", "Chime Visa $5100.", "Carding", "BeRich", 4),
        ("Walmart MoneyCard - $1566", 78.00, 0.0122, "walmart_1566.jpg", "Walmart prepaid.", "Carding", "indulge", 3),
        ("Walmart MoneyCard - $1743", 87.00, 0.0136, "walmart_1743.jpg", "Balance $1743.", "Carding", "indulge", 3),
        ("Walmart MoneyCard - $1983", 99.00, 0.0155, "walmart_1983.jpg", "Balance $1983.", "Carding", "indulge", 3),
        ("Walmart MoneyCard - $2200", 110.00, 0.0172, "walmart_2200.jpg", "Balance $2200.", "Carding", "indulge", 3),
        ("MileagePlus GO Visa - $3567", 178.00, 0.0279, "mileage_3567.jpg", "MileagePlus prepaid.", "Carding", "indulge", 4),
        ("MileagePlus GO Visa - $3742", 187.00, 0.0293, "mileage_3742.jpg", "Balance $3742.", "Carding", "indulge", 4),
        ("MileagePlus GO Visa - $3956", 198.00, 0.0310, "mileage_3956.jpg", "Balance $3956.", "Carding", "indulge", 4),
        ("Cloned Visa $2000-3000", 50.00, 0.0078, "cloned_visa_2000.jpg", "Cloned Visa with PIN.", "Carding", "A1 Quality", 5),
        ("Cloned Visa $3000-4000", 75.00, 0.0118, "cloned_visa_3000.jpg", "Balance up to $4000.", "Carding", "A1 Quality", 5),
        ("Cloned Visa $4000-5000", 100.00, 0.0157, "cloned_visa_4000.jpg", "Balance up to $5000.", "Carding", "A1 Quality", 5),
        ("Cloned Visa $5000-6000", 125.00, 0.0196, "cloned_visa_5000.jpg", "Balance up to $6000.", "Carding", "A1 Quality", 5),
        ("Cloned Visa $6000-7000", 150.00, 0.0235, "cloned_visa_6000.jpg", "Balance up to $7000.", "Carding", "A1 Quality", 5),

        # ------ PREMIUM CREDIT CARDS ------
        ("Visa Infinite Credit Card - $5000 limit", 250.00, 0.0392, "visa_infinite.jpg", "Visa Infinite with high limit.", "Credit Cards", "PLATINUM", 5),
        ("Visa Infinite Credit Card - $10000 limit", 450.00, 0.0706, "visa_infinite_10k.jpg", "Visa Infinite $10k limit.", "Credit Cards", "PLATINUM", 5),
        ("Mastercard World Elite - $7500 limit", 350.00, 0.0549, "mastercard_world_elite.jpg", "World Elite Mastercard.", "Credit Cards", "PLATINUM", 5),
        ("Mastercard World Elite - $15000 limit", 600.00, 0.0941, "mastercard_world_elite_15k.jpg", "World Elite $15k.", "Credit Cards", "PLATINUM", 5),
        ("American Express Platinum - $8000 limit", 400.00, 0.0628, "amex_platinum.jpg", "Amex Platinum with perks.", "Credit Cards", "PLATINUM", 5),
        ("American Express Platinum - $20000 limit", 750.00, 0.1177, "amex_platinum_20k.jpg", "Amex Platinum $20k.", "Credit Cards", "PLATINUM", 5),
        ("Discover it Card - $3000 limit", 120.00, 0.0188, "discover_it.jpg", "Discover it cashback.", "Credit Cards", "Gift Land", 4),
        ("Discover it Card - $6000 limit", 220.00, 0.0345, "discover_it_6k.jpg", "Discover it $6k.", "Credit Cards", "Gift Land", 4),
        ("Capital One Venture - $5000 limit", 230.00, 0.0361, "capital_one_venture.jpg", "Capital One Venture.", "Credit Cards", "BeRich", 4),
        ("Capital One Venture - $10000 limit", 430.00, 0.0675, "capital_one_venture_10k.jpg", "Capital One Venture $10k.", "Credit Cards", "BeRich", 4),
        ("Chase Sapphire Preferred - $6000 limit", 280.00, 0.0439, "chase_sapphire.jpg", "Chase Sapphire Preferred.", "Credit Cards", "BeRich", 5),
        ("Chase Sapphire Reserve - $12000 limit", 520.00, 0.0816, "chase_sapphire_reserve.jpg", "Chase Sapphire Reserve.", "Credit Cards", "BeRich", 5),

        # ------ DOCUMENTS (Fake IDs, Passports) ------
        ("Fake Passport - USA", 180.00, 0.0282, "passport_fake_us.jpg", "High-quality fake US passport.", "Documents", "Dead Presidents", 4),
        ("Fake Passport - UK", 190.00, 0.0298, "passport_fake_uk.jpg", "Fake UK passport.", "Documents", "Dead Presidents", 4),
        ("Fake Passport - EU (Schengen)", 200.00, 0.0314, "passport_fake_eu.jpg", "Fake EU passport.", "Documents", "Dead Presidents", 4),
        ("Fake Driver License - USA", 120.00, 0.0188, "drivers_license_fake_us.jpg", "Fake US driver license.", "Documents", "Dead Presidents", 3),
        ("Fake Driver License - UK", 130.00, 0.0204, "drivers_license_fake_uk.jpg", "Fake UK driving license.", "Documents", "Dead Presidents", 3),
        ("Fake National ID Card - EU", 100.00, 0.0157, "id_card_fake_eu.jpg", "Fake EU ID card.", "Documents", "Dead Presidents", 3),
        ("Fake Social Security Card - USA", 80.00, 0.0126, "ssn_fake_us.jpg", "Fake SSN card.", "Documents", "Dead Presidents", 3),
        ("Fake Residence Permit - UK", 140.00, 0.0220, "residence_permit_fake_uk.jpg", "Fake UK residence permit.", "Documents", "Dead Presidents", 3),

        # ------ GIFT CARDS, ELECTRONICS, TRANSFERS, COUNTERFEITS ------
        ("Apple Gift Card $100", 85.00, 0.0133, "apple_gift_100.jpg", "Apple gift card.", "Gift Cards", "iStore", 5),
        ("Apple Gift Card $200", 170.00, 0.0267, "apple_gift_200.jpg", "$200 Apple card.", "Gift Cards", "iStore", 5),
        ("Apple Gift Card $500", 425.00, 0.0667, "apple_gift_500.jpg", "$500 Apple card.", "Gift Cards", "iStore", 5),
        ("Amazon Gift Card $100", 90.00, 0.0141, "amazon_gift_100.jpg", "Amazon gift card.", "Gift Cards", "Gift Land", 4),
        ("Amazon Gift Card $250", 225.00, 0.0353, "amazon_gift_250.jpg", "Amazon $250.", "Gift Cards", "Gift Land", 4),
        ("Amazon Gift Card $500", 450.00, 0.0706, "amazon_gift_500.jpg", "Amazon $500.", "Gift Cards", "Gift Land", 4),
        ("iPhone 15 Pro Max 256GB", 999.00, 0.1568, "iphone_15_pro_max.jpg", "Brand new iPhone.", "Electronics", "iStore", 5),
        ("iPhone 15 Pro 128GB", 899.00, 0.1411, "iphone_15_pro.jpg", "Latest iPhone.", "Electronics", "iStore", 5),
        ("MacBook Pro 14\" M3", 1599.00, 0.2509, "macbook_pro_14.jpg", "Apple MacBook.", "Electronics", "iStore", 5),
        ("AirPods Pro 2", 199.00, 0.0312, "airpods_pro_2.jpg", "Noise cancelling.", "Electronics", "iStore", 4),
        ("iPad Air 5th Gen", 599.00, 0.0940, "ipad_air_5.jpg", "iPad Air.", "Electronics", "iStore", 4),
        ("Western Union Transfer $500", 25.00, 0.0039, "wu_500.jpg", "WU transfer.", "Money Transfers", "24TransferBank", 4),
        ("Western Union Transfer $1000", 45.00, 0.0071, "wu_1000.jpg", "WU $1000.", "Money Transfers", "24TransferBank", 4),
        ("Western Union Transfer $2000", 80.00, 0.0126, "wu_2000.jpg", "WU $2000.", "Money Transfers", "24TransferBank", 4),
        ("PayPal Transfer $500", 30.00, 0.0047, "paypal_transfer_500.jpg", "PayPal $500.", "Money Transfers", "24TransferBank", 4),
        ("PayPal Transfer $1000", 55.00, 0.0086, "paypal_transfer_1000.jpg", "PayPal $1000.", "Money Transfers", "24TransferBank", 4),
        ("Bank Wire $5000", 150.00, 0.0235, "bank_wire_5000.jpg", "Bank wire.", "Money Transfers", "24TransferBank", 4),
        ("Counterfeit $100 bills x50", 200.00, 0.0314, "counterfeit_100_50.jpg", "Fake $100 bills.", "Money counterfeits", "Dead Presidents", 3),
        ("Counterfeit $50 bills x100", 250.00, 0.0392, "counterfeit_50_100.jpg", "Fake $50 bills.", "Money counterfeits", "Dead Presidents", 3),
        ("Counterfeit $20 bills x200", 300.00, 0.0471, "counterfeit_20_200.jpg", "Fake $20 bills.", "Money counterfeits", "Dead Presidents", 3),
    ]

    for name, usd, btc, img, desc, cat, vendor, rating in products_data:
        p = Product(
            name=name,
            price_usd=usd,
            price_btc=btc,
            image=img,
            description=desc,
            category=cat,
            vendor=vendor,
            rating=rating
        )
        db.session.add(p)
    db.session.commit()

# ------------------ ROUTES ------------------
@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        u = request.form['username']
        e = request.form['email']
        p = request.form['password']
        c = request.form['confirm_password']
        if p != c:
            return "Passwords do not match"
        if User.query.filter_by(username=u).first():
            return "Username already exists"
        if User.query.filter_by(email=e).first():
            return "Email already registered"
        user = User(username=u, email=e)
        user.set_password(p)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        user = User.query.filter_by(username=u).first()
        if user and user.check_password(p):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('index'))
        return "Invalid credentials"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/product/<int:pid>')
def product(pid):
    p = Product.query.get_or_404(pid)
    return render_template('product.html', product=p)

@app.route('/buy/<int:pid>', methods=['GET', 'POST'])
def buy(pid):
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(pid)
    session.modified = True
    return redirect(url_for('checkout'))

@app.route('/add_cart/<int:pid>')
def add_cart(pid):
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(pid)
    return redirect(url_for('index'))

@app.route('/cart')
def cart():
    cart_ids = session.get('cart', [])
    if not cart_ids:
        return render_template('cart.html', products=[], total_usd=0, total_btc=0)
    products = Product.query.filter(Product.id.in_(cart_ids)).all()
    total_usd = sum(p.price_usd for p in products)
    total_btc = sum(p.price_btc for p in products)
    return render_template('cart.html', products=products, total_usd=total_usd, total_btc=total_btc)

@app.route('/checkout')
def checkout():
    cart_ids = session.get('cart', [])
    if not cart_ids:
        return redirect(url_for('index'))
    
    products = Product.query.filter(Product.id.in_(cart_ids)).all()
    total_usd = sum(p.price_usd for p in products)
    total_btc = sum(p.price_btc for p in products)
    total_btc += NETWORK_FEE
    
    btc_to_eth = 15.5
    btc_to_ltc = 70.0
    btc_to_xmr = 4.2
    
    total_eth = total_btc * btc_to_eth
    total_ltc = total_btc * btc_to_ltc
    total_xmr = total_btc * btc_to_xmr
    
    return render_template('checkout.html', 
                         products=products, 
                         total_usd=total_usd,
                         total_btc=total_btc,
                         total_eth=total_eth,
                         total_ltc=total_ltc,
                         total_xmr=total_xmr,
                         wallets=CRYPTO_WALLETS,
                         network_fee=NETWORK_FEE,
                         paypal_link=PAYPAL_LINK)

@app.route('/payment/<crypto>')
def payment(crypto):
    cart_ids = session.get('cart', [])
    if not cart_ids:
        return redirect(url_for('index'))
    
    products = Product.query.filter(Product.id.in_(cart_ids)).all()
    total_usd = sum(p.price_usd for p in products)
    total_btc = sum(p.price_btc for p in products)
    total_btc += NETWORK_FEE
    
    btc_to_eth = 15.5
    btc_to_ltc = 70.0
    btc_to_xmr = 4.2
    
    amounts = {
        'BTC': total_btc,
        'ETH': total_btc * btc_to_eth,
        'LTC': total_btc * btc_to_ltc,
        'XMR': total_btc * btc_to_xmr
    }
    
    amount = amounts.get(crypto.upper(), total_btc)
    wallet = CRYPTO_WALLETS.get(crypto.upper(), '')
    
    if not wallet:
        return "Cryptocurrency not supported", 404
    
    return render_template('payment.html', 
                         crypto=crypto.upper(),
                         amount=amount,
                         wallet=wallet,
                         total_usd=total_usd)

@app.route('/payment_success')
def payment_success():
    session['cart'] = []
    session.modified = True
    return render_template('payment_success.html')

# ------------------ RUN ------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_products()
    # La porta viene presa dalle variabili d'ambiente (Render le assegna)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

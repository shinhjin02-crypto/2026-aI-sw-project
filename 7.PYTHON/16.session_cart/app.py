from flask import Flask, render_template, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "hello1234"

items = [
    {'id': 'item1', 'name': '햄버거', 'price': 3000},
    {'id': 'item2', 'name': '핫도그', 'price': 2000},
    {'id': 'item3', 'name': '콜라', 'price': 1500}
]

@app.route('/')
def index():
    return render_template('product.html', items=items) # 여기 상품 채워넣기

@app.route('/add-to-cart/<item_id>')
def add_to_cart(item_id):
    print("장바구니에 담을 상품: ", item_id)
    if 'cart' not in session:
        session['cart'] = {}
    if item_id in session['cart']:
        session['cart'][item_id] += 1
    else:
        session['cart'][item_id] = 1

    session.modified = True

    return redirect(url_for('view_cart'))

@app.route('/cart')
def view_cart():
    cart_items = {}
    total_price = 0

    for item_id, quantity in session.get('cart', {}).items():
        item = next((item for item in items if item['id'] == item_id), None)
        cart_items[item_id] = {
            'name': item['name'],
            'quantity': quantity,
            'price': item['price']
        }
        total_price += item['price'] * quantity

    return render_template('cart.html', cart_items = cart_items, total_price = total_price) #여기에 장바구니에 담긴 상품 채워넣기

if __name__ == "__main__":
    app.run(debug=True)
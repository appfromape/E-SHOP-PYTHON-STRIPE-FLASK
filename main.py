from flask import Flask, render_template, url_for, request, redirect, jsonify
import stripe
import os

app = Flask(__name__)
app.secret_key = "any-string-you-want-just-keep-it-secret"
stripe.api_key = "sk_test_xxxxxxxx"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/shopcar')
def shopcar():
    return render_template("shopcar.html")

@app.route('/lists')
def lists():
    return render_template('list.html')

@app.route('/checkout')
def checkout():
    return render_template("checkout.html")

YOUR_DOMAIN = 'http://127.0.0.1:5000/'
@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': 4000,
                        'product_data': {
                            'name': 'Stubborn Attachments',
                            'images': ['https://i.imgur.com/EHyR2nP.png'],
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success.html',
            cancel_url=YOUR_DOMAIN + '/cancel.html',
        )
        return jsonify({'id': checkout_session.id})
    except Exception as e:
        return jsonify(error=str(e)), 403


if __name__ == "__main__":
    app.run(debug=True)
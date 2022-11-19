from flask import Flask, render_template, url_for

app = Flask(__name__)


 
@app.route("/")
def index():
    return render_template("blog/base.html")


    

@app.route("/home")
def home():
    return render_template("blog/home.html")


@app.route("/customer")
def customer():
    return  render_template('blog/customer.html')



@app.route("/product")
def product():
    return  render_template('blog/product.html')
def fr():
     return render_template("blog/frame.html")


@app.route("/inventory")
def inventrory():
    return  render_template('blog/inventory.html')


@app.route("/transaction")
def transaction():
    return  render_template('blog/transaction.html')


@app.route("/supplier")
def supplier():
    return  render_template('blog/supplier.html')

@app.route("/account")
def account():
    return  render_template('blog/account.html')

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)
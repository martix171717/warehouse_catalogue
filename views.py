from flask import Flask, render_template, url_for, request, redirect, flash
from models import Product
from forms import ProductForm, ProductSaleForm
import csv


app=Flask(__name__)
app.config["SECRET_KEY"] = "usdhcgducguqdbquj"


ITEMS = {"Tofu" : Product("Tofu", "kg", "%.2f" % 2.3, "%.2f" % 2.60, 130),
         "Hummus" : Product("Hummus", "kg", "%.2f" % 3.11,"%.2f" % 3.56, 145),
         "Soya" : Product("Soya", "kg", "%.2f" % 3.9, "%.2f" %4.2, 120),
         "Melon" : Product("Melon", "kg", "%.2f" % 3.21, "%.2f" % 3.55, 250)}

SOLD_ITEMS={}

@app.route('/')
def homepage():
    return render_template("homepage.html")

@app.route('/products/', methods=["GET", "POST"])
def product_list():
    form = ProductForm()
    error=""
    if request.method=="POST":
        if form.validate_on_submit():
            # jeśli klucz istnieje ilość i cena się nadpiszą
            ITEMS[form.data['name']] = Product(form.data['name'], form.data['unit'], form.data['unit_cost'], form.data['unit_price'], form.data['quantity'])
        else:
            error=form.errors
        return redirect(url_for("product_list"))    
    return render_template("product_list.html", items=ITEMS, form=form, error=error)

@app.route('/sell/<product_name>', methods=["GET", "POST"])
def sell_product(product_name):
    form = ProductSaleForm()
    error=""
    if request.method =="POST":
        ITEMS[product_name].quantity = int(ITEMS[product_name].quantity) - int(form.data['quantity_sold'])
        SOLD_ITEMS.update({"Name": ITEMS[product_name].name, "Unit": ITEMS[product_name].unit, "Unit cost":ITEMS[product_name].unit_cost, "Unit price" :ITEMS[product_name].unit_price, "Quantity sold":form.data['quantity_sold']})
        if ITEMS[product_name].quantity <0:
            flash(f"Oops! There are not enough goods to sell. Please enter a lower quantity.")
            ITEMS[product_name].quantity = int(ITEMS[product_name].quantity + form.data['quantity_sold'])
        else:
            pass
        return redirect(url_for("product_list"))
    return render_template("sell_product.html", form=form, error=error, product_name=product_name, items=ITEMS, sold_items=SOLD_ITEMS) 

# Export do pliku csv
@app.route('/product_list/', methods=["POST"])
def export_items_to_csv():
    form = ProductForm()
    error = ""
    if request.method == "POST":
        with open('C:\Python\Projekty\warehouse_project\warehouse_catalogue\magazyn.csv', 'w', newline='') as csvfile:
            fieldnames = ["name", "quantity", "unit", "unit_cost","unit_price"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')
            writer.writeheader()
            for item in ITEMS.values():
                record = {"name" : item.name, "quantity" : item.quantity, "unit": item.unit, "unit_cost" : item.unit_cost, "unit_price" : item.unit_price}
                writer.writerow(record)
    return render_template("product_list.html", form=form, fieldnames=fieldnames, csvfile=csvfile, items=ITEMS, error=error)


# Import z pliku csv
@app.route('/product_list/', methods=["GET"])
def import_items_from_csv():
    form = ProductForm()
    error = ""
    if request.method == "GET":
        with open('C:\Python\Projekty\warehouse_project\warehouse_catalogue\magazyn.csv', newline='') as csvfile:
            fieldnames = ["name", "quantity", "unit", "unit_cost", "unit_price"]
            reader = csv.DictReader(csvfile, fieldnames=fieldnames, delimiter=',')
            ITEMS.clear()
            for row in reader:
                if row["name"] != "name":
                    ITEMS[row["name"]] = Product(row["name"], row["unit"], row["unit_cost"], row["unit_price"], row["quantity"])
        return render_template("product_list.html", form=form, items=ITEMS, error=error)   


@app.route('/sold_products')
def sold_products():
    return render_template("sold_products.html", sold_items=SOLD_ITEMS, items=ITEMS)

if __name__ == "__main__":
    app.run(debug=True)

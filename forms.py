from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField
from wtforms.validators import DataRequired

class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    unit = StringField('Unit', validators=[DataRequired()])
    unit_cost = DecimalField('Unit cost', validators=[DataRequired()])
    unit_price = DecimalField('Unit price', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    
class ProductSaleForm(FlaskForm):
    quantity_sold = IntegerField('Quantity Sold', validators=[DataRequired()])
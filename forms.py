from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField
from wtforms.validators import DataRequired

class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    unit = StringField('Unit', validators=[DataRequired()])
    unit_price = DecimalField('Unit price', places=2, rounding=None, validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    
class ProductSaleForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[DataRequired()])
from flask import Flask, request, render_template, redirect, flash

from flask_debugtoolbar import DebugToolbarExtension
from forex_python.converter import CurrencyRates, CurrencyCodes



app = Flask(__name__)
app.config["SECRET_KEY"] = "oh-so-secret"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

debug = DebugToolbarExtension(app)

c = CurrencyRates()
rates_dict = c.get_rates('USD')
currency_array_upper = list(rates_dict.keys())
currency_array_upper.append('USD')
currency_array = []
for currency in currency_array_upper:
    currency_array.append(currency.lower())


@app.route('/')
def show_home_page():
    
    return render_template('home.html')

@app.route('/result', methods=['POST', 'GET'])
def show_results():
    converting_from_actual = request.form['converting_from']
    converting_to_actual = request.form['converting_to']
    converting_from = converting_from_actual.lower()
    converting_to = converting_to_actual.lower()
    amount = request.form['amount']
    
    if "." in amount:
        amount = float(amount)
    
    
    if converting_from not in currency_array or converting_to not in currency_array:
        if converting_from not in currency_array and converting_to not in currency_array:
            flash(f"Not a valid 3 letter currency: {converting_from_actual}", 'error')
            flash(f"Not a valid 3 letter currency: {converting_to_actual}", 'error')
            return redirect('/')    
        elif converting_from not in currency_array and converting_to in currency_array:
            flash(f"Not a valid 3 letter currency: {converting_from_actual}", 'error')
            return redirect('/')   
        elif converting_from in currency_array and converting_to not in currency_array:
            flash(f"Not a valid 3 letter currency: {converting_to_actual}", 'error')
            return redirect('/')    
        
    if not isinstance(amount, float) and not amount.isdigit():
        flash(f"Not a valid amount: {amount}", 'error')
        return redirect('/')
    
    
    converted_amount_float = c.convert(converting_from.upper(), converting_to.upper(), float(amount))
    converted_amount = "{:,}".format(round(converted_amount_float, 2))
    formatted_amount = "{:,}".format(float(amount))
    
    
    b = CurrencyCodes()
    to_currency_symbol = b.get_symbol(converting_to.upper())
    from_currency_symbol = b.get_symbol(converting_from.upper())
    
    return render_template('result.html', converting_from=converting_from, converting_to=converting_to, amount=formatted_amount, converted_amount=converted_amount, to_currency_symbol=to_currency_symbol, from_currency_symbol=from_currency_symbol)
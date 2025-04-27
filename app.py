from flask import Flask, render_template, request
import math

app = Flask(__name__)

def calculate_sip(monthly_investment, expected_return, time_period):
    """
    Calculate the future value of SIP investments
    
    Args:
        monthly_investment: Monthly investment amount (in currency units)
        expected_return: Expected annual return rate (in percentage)
        time_period: Investment time period (in years)
        
    Returns:
        dict: Contains investment amount, returns, and final value
    """
    # Convert annual return rate to monthly
    monthly_rate = expected_return / (12 * 100)
    
    # Total number of months
    months = time_period * 12
    
    # Calculate future value using SIP formula
    future_value = monthly_investment * ((math.pow(1 + monthly_rate, months) - 1) / monthly_rate) * (1 + monthly_rate)
    
    # Calculate total invested amount
    total_invested = monthly_investment * months
    
    # Calculate wealth gained
    wealth_gained = future_value - total_invested
    
    return {
        "total_invested": round(total_invested, 2),
        "wealth_gained": round(wealth_gained, 2),
        "future_value": round(future_value, 2)
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    
    if request.method == 'POST':
        try:
            monthly_investment = float(request.form['monthly_investment'])
            expected_return = float(request.form['expected_return'])
            time_period = float(request.form['time_period'])
            
            result = calculate_sip(monthly_investment, expected_return, time_period)
        except ValueError:
            result = "Error: Please enter valid numbers"
    
    return render_template('index.html', result=result)

# HTML template
@app.route('/templates/index.html')
def get_template():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
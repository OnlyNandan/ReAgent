from flask import Flask, request, render_template
import pickle
import os

app = Flask(__name__)

filename = "chemicals.pickle"
chemicals = {}

if os.path.exists(filename):
    with open(filename, 'rb') as f:
        chemicals = pickle.load(f)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/input', methods=['GET', 'POST'])
def input_chemical():
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        quantity = request.form['quantity']
        formula = request.form['formula']
        expiry_date = request.form['expiry_date']
        manufacturer = request.form['manufacturer']

        chemical_data = {
            "location": location,
            "quantity": quantity,
            "formula": formula,
            "expiry_date": expiry_date,
            "manufacturer": manufacturer
        }

        chemicals[name] = chemical_data

        with open(filename, 'wb') as f:
            pickle.dump(chemicals, f)

        return f"Chemical data for {name} has been successfully stored."

    return render_template('input.html')

@app.route('/display', methods=['GET', 'POST'])
def display_chemical():
    if request.method == 'POST':
        name = request.form['name']
        chemical_data = chemicals.get(name)

        if chemical_data is None:
            return f"Chemical '{name}' not found."
        else:
            return render_template('display.html', name=name, chemical_data=chemical_data)

    return render_template('display.html')

if __name__ == '__main__':
    app.run(debug=True)

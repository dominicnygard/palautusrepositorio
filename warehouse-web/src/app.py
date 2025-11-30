"""Flask web application for managing warehouses (Varasto)."""
import os
from flask import Flask, render_template, request, redirect, url_for
from src.varasto import Varasto


# Get the directory where this file is located and find templates relative to parent
_base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
template_dir = os.path.join(_base_dir, 'templates')
app = Flask(__name__, template_folder=template_dir)

# In-memory storage for warehouses
warehouses = {}
_warehouse_counter = [0]  # Using list to avoid global statement


def get_next_id():
    """Generate the next warehouse ID."""
    _warehouse_counter[0] += 1
    return _warehouse_counter[0]


@app.route('/')
def index():
    """Display the list of all warehouses."""
    return render_template('index.html', warehouses=warehouses)


@app.route('/create', methods=['GET', 'POST'])
def create_warehouse():
    """Create a new warehouse."""
    if request.method == 'POST':
        name = request.form.get('name', 'Unnamed Warehouse')
        tilavuus = float(request.form.get('tilavuus', 0))
        alku_saldo = float(request.form.get('alku_saldo', 0))

        warehouse_id = get_next_id()
        warehouses[warehouse_id] = {
            'id': warehouse_id,
            'name': name,
            'varasto': Varasto(tilavuus, alku_saldo)
        }
        return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/warehouse/<int:warehouse_id>')
def view_warehouse(warehouse_id):
    """View details of a specific warehouse."""
    warehouse = warehouses.get(warehouse_id)
    if warehouse is None:
        return "Warehouse not found", 404
    return render_template('warehouse.html', warehouse=warehouse)


@app.route('/warehouse/<int:warehouse_id>/add', methods=['POST'])
def add_to_warehouse(warehouse_id):
    """Add items to a warehouse."""
    warehouse = warehouses.get(warehouse_id)
    if warehouse is None:
        return "Warehouse not found", 404

    maara = float(request.form.get('maara', 0))
    warehouse['varasto'].lisaa_varastoon(maara)
    return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))


@app.route('/warehouse/<int:warehouse_id>/remove', methods=['POST'])
def remove_from_warehouse(warehouse_id):
    """Remove items from a warehouse."""
    warehouse = warehouses.get(warehouse_id)
    if warehouse is None:
        return "Warehouse not found", 404

    maara = float(request.form.get('maara', 0))
    warehouse['varasto'].ota_varastosta(maara)
    return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))


@app.route('/warehouse/<int:warehouse_id>/delete', methods=['POST'])
def delete_warehouse(warehouse_id):
    """Delete a warehouse."""
    if warehouse_id in warehouses:
        del warehouses[warehouse_id]
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

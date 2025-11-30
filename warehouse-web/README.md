# Warehouse Web Application (Varasto)

A Flask web application for managing warehouses with limited capacity.

## Features

- Create multiple warehouses with custom names and capacities
- Add items to warehouses
- Remove items from warehouses
- View warehouse details and fill levels
- Delete warehouses

## Installation

Make sure you have Python 3.12+ and Poetry installed.

```bash
# Navigate to the project directory
cd warehouse-web

# Install dependencies
poetry install

# Run the application
poetry run python src/app.py
```

The application will be available at `http://localhost:5000`.

## Development

### Running Tests

```bash
poetry run pytest
```

### Running Linter

```bash
poetry run pylint src/
```

## Varasto Class

The `Varasto` class represents a warehouse with the following functionality:

- `__init__(tilavuus, alku_saldo=0)`: Create a warehouse with given volume and optional initial balance
- `paljonko_mahtuu()`: Get available space in the warehouse
- `lisaa_varastoon(maara)`: Add items to the warehouse
- `ota_varastosta(maara)`: Remove items from the warehouse

### Validation

- Negative volume is set to 0
- Negative initial balance is set to 0
- Initial balance larger than volume fills the warehouse
- Adding more than available space fills the warehouse
- Taking more than available balance returns all available items

## Project Structure

```
warehouse-web/
├── src/
│   ├── __init__.py
│   ├── app.py          # Flask application
│   └── varasto.py      # Varasto class
├── templates/
│   ├── base.html       # Base template
│   ├── index.html      # List of warehouses
│   ├── create.html     # Create warehouse form
│   └── warehouse.html  # Warehouse details
├── tests/
│   ├── __init__.py
│   ├── test_app.py     # Flask route tests
│   └── test_varasto.py # Varasto class tests
├── pyproject.toml      # Poetry configuration
└── README.md
```

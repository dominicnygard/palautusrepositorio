"""Tests for the Flask web application."""
import pytest
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.app import app, warehouses, get_next_id


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as test_client:
        yield test_client
    # Clean up warehouses after each test
    warehouses.clear()


@pytest.fixture
def sample_warehouse(client):
    """Create a sample warehouse for testing."""
    response = client.post('/create', data={
        'name': 'Test Warehouse',
        'tilavuus': '100',
        'alku_saldo': '50'
    }, follow_redirects=True)
    # Find the warehouse ID (it's the first warehouse)
    warehouse_id = list(warehouses.keys())[0] if warehouses else None
    return warehouse_id


class TestIndexRoute:
    """Tests for the index route."""

    def test_index_returns_200(self, client):
        """Index page returns 200 OK."""
        response = client.get('/')
        assert response.status_code == 200

    def test_index_shows_no_warehouses_initially(self, client):
        """Index shows message when no warehouses exist."""
        response = client.get('/')
        assert b'Ei varastoja' in response.data

    def test_index_shows_warehouse_after_creation(self, client, sample_warehouse):
        """Index shows warehouse after it's created."""
        response = client.get('/')
        assert b'Test Warehouse' in response.data


class TestCreateWarehouseRoute:
    """Tests for the create warehouse route."""

    def test_create_page_returns_200(self, client):
        """Create page returns 200 OK."""
        response = client.get('/create')
        assert response.status_code == 200

    def test_create_warehouse_redirects(self, client):
        """Creating a warehouse redirects to index."""
        response = client.post('/create', data={
            'name': 'New Warehouse',
            'tilavuus': '50',
            'alku_saldo': '10'
        })
        assert response.status_code == 302

    def test_create_warehouse_adds_to_warehouses(self, client):
        """Creating a warehouse adds it to the warehouses dict."""
        client.post('/create', data={
            'name': 'New Warehouse',
            'tilavuus': '50',
            'alku_saldo': '10'
        })
        assert len(warehouses) == 1
        warehouse = list(warehouses.values())[0]
        assert warehouse['name'] == 'New Warehouse'
        assert warehouse['varasto'].tilavuus == 50
        assert warehouse['varasto'].saldo == 10


class TestViewWarehouseRoute:
    """Tests for the view warehouse route."""

    def test_view_existing_warehouse_returns_200(self, client, sample_warehouse):
        """Viewing existing warehouse returns 200 OK."""
        response = client.get(f'/warehouse/{sample_warehouse}')
        assert response.status_code == 200
        assert b'Test Warehouse' in response.data

    def test_view_nonexistent_warehouse_returns_404(self, client):
        """Viewing non-existent warehouse returns 404."""
        response = client.get('/warehouse/9999')
        assert response.status_code == 404


class TestAddToWarehouseRoute:
    """Tests for adding to warehouse route."""

    def test_add_to_warehouse_increases_saldo(self, client, sample_warehouse):
        """Adding to warehouse increases balance."""
        original_saldo = warehouses[sample_warehouse]['varasto'].saldo
        client.post(f'/warehouse/{sample_warehouse}/add', data={'maara': '25'})
        new_saldo = warehouses[sample_warehouse]['varasto'].saldo
        assert new_saldo == original_saldo + 25

    def test_add_to_warehouse_redirects(self, client, sample_warehouse):
        """Adding to warehouse redirects back to warehouse view."""
        response = client.post(f'/warehouse/{sample_warehouse}/add', data={'maara': '10'})
        assert response.status_code == 302

    def test_add_to_nonexistent_warehouse_returns_404(self, client):
        """Adding to non-existent warehouse returns 404."""
        response = client.post('/warehouse/9999/add', data={'maara': '10'})
        assert response.status_code == 404


class TestRemoveFromWarehouseRoute:
    """Tests for removing from warehouse route."""

    def test_remove_from_warehouse_decreases_saldo(self, client, sample_warehouse):
        """Removing from warehouse decreases balance."""
        original_saldo = warehouses[sample_warehouse]['varasto'].saldo
        client.post(f'/warehouse/{sample_warehouse}/remove', data={'maara': '20'})
        new_saldo = warehouses[sample_warehouse]['varasto'].saldo
        assert new_saldo == original_saldo - 20

    def test_remove_from_warehouse_redirects(self, client, sample_warehouse):
        """Removing from warehouse redirects back to warehouse view."""
        response = client.post(f'/warehouse/{sample_warehouse}/remove', data={'maara': '10'})
        assert response.status_code == 302

    def test_remove_from_nonexistent_warehouse_returns_404(self, client):
        """Removing from non-existent warehouse returns 404."""
        response = client.post('/warehouse/9999/remove', data={'maara': '10'})
        assert response.status_code == 404


class TestDeleteWarehouseRoute:
    """Tests for deleting warehouse route."""

    def test_delete_warehouse_removes_from_dict(self, client, sample_warehouse):
        """Deleting warehouse removes it from warehouses dict."""
        assert sample_warehouse in warehouses
        client.post(f'/warehouse/{sample_warehouse}/delete')
        assert sample_warehouse not in warehouses

    def test_delete_warehouse_redirects(self, client, sample_warehouse):
        """Deleting warehouse redirects to index."""
        response = client.post(f'/warehouse/{sample_warehouse}/delete')
        assert response.status_code == 302

    def test_delete_nonexistent_warehouse_redirects(self, client):
        """Deleting non-existent warehouse just redirects."""
        response = client.post('/warehouse/9999/delete')
        assert response.status_code == 302

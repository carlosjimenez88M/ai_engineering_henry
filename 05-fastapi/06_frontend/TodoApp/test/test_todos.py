"""
Tests del router de tareas con prefijo /todos y dependency_overrides.

Prueba el CRUD completo usando rutas con prefijo /todos,
base de datos SQLite en memoria y usuarios simulados.

Copyright 2026 Henry Academy.
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

# Clase 6: Frontend con Jinja2 y StaticFiles - Henry AI Engineering

from fastapi import status

from ..models import Todos
from ..routers.todos import get_current_user, get_db
from .utils import (
    TestingSessionLocal,
    app,
    client,
    override_get_current_user,
    override_get_db,
)

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_read_all_authenticated(test_todo):
    response = client.get("/todos")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'complete': False, 'title': 'Learn to code!',
                                'description': 'Need to learn everyday!', 'id': 1,
                                'priority': 5, 'owner_id': 1}]


def test_read_one_authenticated(test_todo):
    response = client.get("/todos/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'complete': False, 'title': 'Learn to code!',
                                'description': 'Need to learn everyday!', 'id': 1,
                                'priority': 5, 'owner_id': 1}


def test_read_one_authenticated_not_found():
    response = client.get("/todos/todo/999")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found.'}


def test_create_todo(test_todo):
    request_data = {
        'title': 'New Todo!',
        'description': 'New todo description',
        'priority': 5,
        'complete': False,
    }

    response = client.post('/todos/todo/', json=request_data)
    assert response.status_code == 201

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')


def test_update_todo(test_todo):
    request_data = {
        'title': 'Change the title of the todo already saved!',
        'description': 'Need to learn everyday!',
        'priority': 5,
        'complete': False,
    }

    response = client.put('/todos/todo/1', json=request_data)
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == 'Change the title of the todo already saved!'


def test_update_todo_not_found(test_todo):
    request_data = {
        'title': 'Change the title of the todo already saved!',
        'description': 'Need to learn everyday!',
        'priority': 5,
        'complete': False,
    }

    response = client.put('/todos/todo/999', json=request_data)
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found.'}


def test_delete_todo(test_todo):
    response = client.delete('/todos/todo/1')
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None


def test_delete_todo_not_found():
    response = client.delete('/todos/todo/999')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found.'}

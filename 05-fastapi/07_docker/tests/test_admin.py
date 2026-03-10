"""
Tests del router de administración con dependency_overrides (Docker).

Prueba lectura global y eliminación de todos como admin
usando override de dependencias en la base de datos de test.

Copyright 2026 Henry Academy.
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

# Clase 7: Docker - Henry AI Engineering

from fastapi import status

from TodoApp.models import Todos
from TodoApp.routers.admin import get_current_user, get_db
from tests.utils import (
    TestingSessionLocal,
    app,
    client,
    override_get_current_user,
    override_get_db,
)

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_admin_read_all_authenticated(test_todo):
    response = client.get("/admin/todo")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'complete': False, 'title': 'Learn to code!',
                                'description': 'Need to learn everyday!', 'id': 1,
                                'priority': 5, 'owner_id': 1}]


def test_admin_delete_todo(test_todo):
    response = client.delete("/admin/todo/1")
    assert response.status_code == 204

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None


def test_admin_delete_todo_not_found():
    response = client.delete("/admin/todo/9999")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found.'}

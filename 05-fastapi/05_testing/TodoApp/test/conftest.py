"""
Fixtures compartidos para los tests de la TodoApp (sección testing).

Usa sys.path para imports absolutos desde el directorio de la sección,
garantizando compatibilidad con --import-mode=importlib de pytest.

Copyright 2026 Henry Academy.
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

# Clase 5: Testing con pytest - Henry AI Engineering

import os
import sys

import pytest
from sqlalchemy import text

# Asegurar que 05_testing/ esté en sys.path para imports absolutos
_section_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if _section_dir not in sys.path:
    sys.path.insert(0, _section_dir)

from TodoApp.models import Todos, Users  # noqa: E402
from TodoApp.routers.auth import bcrypt_context  # noqa: E402
from TodoApp.test.utils import TestingSessionLocal, engine  # noqa: E402


@pytest.fixture
def test_todo():
    todo = Todos(
        title="Learn to code!",
        description="Need to learn everyday!",
        priority=5,
        complete=False,
        owner_id=1,
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


@pytest.fixture
def test_user():
    user = Users(
        username="codingwithrobytest",
        email="codingwithrobytest@email.com",
        first_name="Eric",
        last_name="Roby",
        hashed_password=bcrypt_context.hash("testpassword"),
        role="admin",
        phone_number="(111)-111-1111",
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()

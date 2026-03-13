"""
Tests del endpoint principal de la TodoApp con frontend.

Verifica el health check y comportamiento base usando TestClient.

Copyright 2026 Henry Academy.
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

# Clase 6: Frontend con Jinja2 y StaticFiles - Henry AI Engineering

from fastapi import status
from fastapi.testclient import TestClient

from TodoApp.main import app

client = TestClient(app)


def test_return_health_check():
    response = client.get("/healthy")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'status': 'Healthy'}

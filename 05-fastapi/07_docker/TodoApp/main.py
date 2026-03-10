"""
Punto de entrada principal de la TodoApp para la sección de Docker.

Expone el health check endpoint para verificar que la aplicación
está funcionando, junto con los routers completos.

Copyright 2026 Henry Academy.
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

# Clase 7: Docker - Henry AI Engineering

from fastapi import FastAPI

from TodoApp.models import Base
from TodoApp.database import engine
from TodoApp.routers import admin, auth, todos, users

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/healthy")
def health_check():
    return {'status': 'Healthy'}


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

"""
Punto de entrada principal de la TodoApp con migraciones Alembic.

Las tablas se gestionan mediante alembic upgrade en lugar de
create_all, aunque se mantiene create_all para desarrollo rápido.

Copyright 2026 Henry Academy.
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

# Clase 4: Migraciones con Alembic - Henry AI Engineering

from fastapi import FastAPI

from . import models
from .database import engine
from .routers import admin, auth, todos, users

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

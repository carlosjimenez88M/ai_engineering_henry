"""
Punto de entrada principal de la TodoApp con frontend web.

Monta archivos estáticos con pathlib para rutas absolutas portables,
redirige la raíz a la página de todos y expone el health check.

Copyright 2026 Henry Academy.
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

# Clase 6: Frontend con Jinja2 y StaticFiles - Henry AI Engineering

from pathlib import Path

from fastapi import FastAPI, Request, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from TodoApp.database import engine
from TodoApp.models import Base
from TodoApp.routers import admin, auth, todos, users

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent

Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


@app.get("/")
def test(request: Request):
    return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)


@app.get("/healthy")
def health_check():
    return {'status': 'Healthy'}


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

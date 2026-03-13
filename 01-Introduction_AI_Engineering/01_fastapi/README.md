# Módulo 05 — FastAPI: De Cero a Producción

Curso progresivo de FastAPI organizado en 6 secciones que van desde endpoints básicos
hasta una aplicación web completa con autenticación JWT, base de datos SQLite/SQLAlchemy 2.0,
migraciones con Alembic, testing con pytest y frontend con Jinja2.

---

## Tabla de secciones

| Sección | Tema | Comando |
|---------|------|---------|
| `01_fundamentos/` | CRUD básico sin DB, path/query params | `make run-01` |
| `02_modelos_pydantic/` | Pydantic v2, Field validators, status codes | `make run-02` |
| `03_todo_app_base/` | SQLAlchemy 2.0, JWT, routers, dependency injection | `make run-03` |
| `04_migraciones/` | Alembic upgrade/downgrade, schema evolution | `make run-04` |
| `05_testing/` | pytest, TestClient, dependency_overrides, fixtures | `make run-05` |
| `06_frontend/` | Jinja2 templates, StaticFiles, pathlib, cookies | `make run-06` |

---

## Instalación

```bash
cd ai_engineering_henry/05-fastapi
uv sync --extra dev
```

---

## Ejecución de cada sección

```bash
make run-01   # http://localhost:8001/docs
make run-02   # http://localhost:8002/docs
make run-03   # http://localhost:8003/docs
make run-06   # http://localhost:8006 (interfaz web)
```

---

## Tests

```bash
make test     # Ejecuta 05_testing (27 tests) + 06_frontend (27 tests)
```

La suite corre en dos procesos separados para evitar colisión de paquetes:

```bash
# Solo sección 5
uv run pytest --override-ini="testpaths=05_testing/TodoApp/test" \
              --override-ini="pythonpath=05_testing"

# Solo sección 6
uv run pytest --override-ini="testpaths=06_frontend/TodoApp/test" \
              --override-ini="pythonpath=06_frontend"
```

---

## Conceptos clave por sección

### Clase 1 — Fundamentos

- Rutas `GET`, `POST`, `PUT`, `DELETE`
- Path parameters y query parameters
- Request body con `Body()`
- Sin base de datos, datos en memoria

### Clase 2 — Modelos Pydantic

- `BaseModel` con `Field` validators (`min_length`, `gt`, `lt`)
- `HTTPException` para errores controlados
- `Path()` y `Query()` con validación automática
- `status_code` en decoradores

### Clase 3 — TodoApp Base

- **SQLAlchemy 2.0**: `DeclarativeBase` en lugar del deprecado `declarative_base()`
- ORM models con `Column`, `ForeignKey`
- `SessionLocal` + dependency injection con `Depends(get_db)`
- **JWT**: `python-jose`, `OAuth2PasswordBearer`, `OAuth2PasswordRequestForm`
- **bcrypt**: hashing de contraseñas con `CryptContext`
- Imports relativos en routers (`from ..database import SessionLocal`)

### Clase 4 — Migraciones Alembic

- `alembic init` y configuración de `alembic.ini`
- `alembic/env.py` con `target_metadata = models.Base.metadata`
- `alembic revision --autogenerate -m "descripcion"`
- `alembic upgrade head` / `alembic downgrade -1`
- Ejemplo real: agregar columna `phone_number` a `users`

### Clase 5 — Testing

- `TestClient` de FastAPI/Starlette para HTTP tests
- `dependency_overrides` para reemplazar DB y usuario real
- SQLite en memoria con `StaticPool` para tests aislados
- Fixtures pytest (`@pytest.fixture`) con cleanup automático
- `@pytest.mark.asyncio` para funciones async (JWT decode)
- Tests: CRUD todos, admin, auth, users (~27 tests)

### Clase 6 — Frontend

- `Jinja2Templates` para renderizar HTML dinámico
- `StaticFiles` para CSS/JS
- **pathlib fix**: `BASE_DIR = Path(__file__).resolve().parent` para rutas portables
- Cookies para autenticación (`request.cookies.get('access_token')`)
- `RedirectResponse` para navegación entre páginas
- Router con prefix `/todos` para endpoints y páginas

---

## Estructura de directorios

```
05-fastapi/
├── pyproject.toml           # uv project, deps + pytest config
├── Makefile                 # install, test, run-01..run-06
├── README.md
├── .gitignore
├── 01_fundamentos/
│   └── books.py             # CRUD en memoria
├── 02_modelos_pydantic/
│   └── books2.py            # Pydantic v2 + HTTPException
├── 03_todo_app_base/
│   └── TodoApp/             # SQLAlchemy 2.0 + JWT
│       ├── database.py, models.py, main.py
│       └── routers/ (auth, todos, admin, users)
├── 04_migraciones/
│   └── TodoApp/             # + alembic
│       ├── alembic.ini
│       ├── alembic/env.py + versions/
│       └── routers/...
├── 05_testing/
│   └── TodoApp/             # + test suite
│       ├── routers/...
│       └── test/
│           ├── conftest.py  # fixtures: test_todo, test_user
│           ├── utils.py     # engine, client, overrides
│           ├── test_example.py, test_main.py
│           ├── test_todos.py, test_admin.py
│           ├── test_auth.py, test_users.py
└── 06_frontend/
    └── TodoApp/             # + Jinja2 + static + pathlib
        ├── routers/...
        ├── static/ (css/, js/)
        ├── templates/ (login, register, todo, add-todo, edit-todo)
        └── test/...
```

---

## Verificación rápida

```bash
# SQLAlchemy 2.0 OK
uv run python -c "from sqlalchemy.orm import DeclarativeBase; print('SQLAlchemy 2.0 OK')"

# Módulo desde root
cd ai_engineering_henry && make module-05
```

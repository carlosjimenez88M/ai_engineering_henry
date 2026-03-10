"""
Configuración de base de datos SQLAlchemy para la TodoApp con migraciones.

Define el engine SQLite, la sesión local y la clase Base
usando la API moderna DeclarativeBase de SQLAlchemy 2.0.

Copyright 2026 Henry Academy.
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

# Clase 4: Migraciones con Alembic - Henry AI Engineering

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass

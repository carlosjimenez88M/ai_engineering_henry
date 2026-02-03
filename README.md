![](https://www.soyhenry.com/_next/static/media/HenryLogo.bb57fd6f.svg)

# AI Engineering - Henry Academy

Bienvenido al curso de AI Engineering de Henry Academy. Este repositorio contiene material práctico diseñado para estudiantes que quieren entender las diferencias fundamentales entre Software Engineering tradicional y AI Engineering moderno, siguiendo los principios de **Chip Huyen** ("Designing Machine Learning Systems" y "AI Engineering").

## ¿Por qué este curso?

En la industria tech actual, no basta con saber usar un LLM API. Los mejores AI Engineers entienden:
- Cómo diseñar sistemas que sean **reproducibles, testeables y observables**
- Cuándo usar AI vs software tradicional (y cuándo combinarlos)
- Cómo medir costos, latencia y calidad en sistemas AI
- Patrones de producción que separan prototipos de sistemas reales

Este curso te prepara para construir sistemas AI que escalan en producción, no solo demos que funcionan una vez.

## Estructura del Curso

El curso se divide en 4 clases progresivas:

### **Clase 1: Software vs AI Engineering** ✅
**Estado:** Completa y lista para usar

Contenido:
- Comparación crítica: ¿Cuándo usar qué?
- Ejemplo práctico: Sistema de brief generation con OpenAI
- Testing, validación, métricas y observabilidad
- Trade-offs y anti-patrones comunes

**Ubicación:** `01_class/`

### **Clase 2: Fundamentos de Prompting y LLM APIs** 🚧
**Estado:** Próximamente

Temas planeados:
- Prompt engineering: system/user prompts, few-shot learning
- Temperature, top-p y otros parámetros del modelo
- Streaming vs batch responses
- Manejo de contexto y tokens

### **Clase 3: Evaluación y Monitoreo de Sistemas AI** 🚧
**Estado:** Próximamente

Temas planeados:
- Eval sets y métricas de calidad
- Human-in-the-loop evaluation
- Monitoreo en producción (data drift, model drift)
- A/B testing para sistemas AI

### **Clase 4: Deployment y Producción** 🚧
**Estado:** Próximamente

Temas planeados:
- Serving patterns (sync, async, batch)
- Caching y optimización de costos
- Rate limiting y fallbacks
- CI/CD para sistemas AI

## Comenzando

### Requisitos Previos

- **Python 3.10 o superior**
- **Cuenta de OpenAI** con API key activa ([obtener aquí](https://platform.openai.com/api-keys))
- **uv** instalado ([instrucciones de instalación](https://github.com/astral-sh/uv))
- Conocimientos básicos de:
  - Python (funciones, clases, imports)
  - Terminal/CLI
  - Git (opcional pero recomendado)

### Instalación Paso a Paso

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/yourusername/ai_engineering_henry.git
   cd ai_engineering_henry
   ```

2. **Instala dependencias con uv:**
   ```bash
   make install
   # o directamente: uv sync
   ```

3. **Configura tu API key de OpenAI:**

   Crea un archivo `.env` en la raíz del proyecto:
   ```bash
   cp .env.example .env
   ```

   Edita `.env` y agrega tu API key:
   ```
   OPENAI_API_KEY=sk-proj-tu-api-key-aqui
   OPENAI_MODEL=gpt-4o-mini  # opcional, default: gpt-4o-mini
   ```

4. **Verifica la instalación:**
   ```bash
   make test-se
   ```

   Si ves tests pasando, ¡estás listo! ✅

### Primer Comando

Genera tu primer brief comparativo:
```bash
make run-ai
```

El brief se guardará en `01_class/ai_engineering/briefs/software_vs_ai_engineering.md`.

Con contexto personalizado:
```bash
make run-ai-context CONTEXT="Startup de fintech B2B"
```

## Filosofía del Curso

Este curso sigue los principios de **Chip Huyen** sobre sistemas AI en producción:

### 1. **Reproducibilidad**
- Versionamos prompts en Git
- Trackeamos model version, temperature y parámetros
- Logs detallados para debugging

### 2. **Modularidad**
- Separación clara de concerns (config, prompts, validation, metrics)
- Componentes reusables y testeables
- No "God functions" que hacen todo

### 3. **Testing Riguroso**
- Tests unitarios para lógica de negocio
- Tests de integración con mocks de APIs
- Validación de inputs y outputs
- Target: 85%+ code coverage

### 4. **Observabilidad**
- Métricas de costo por request
- Latency tracking
- Quality checks automatizados
- Error logging estructurado

### 5. **Error Handling Resiliente**
- Retry logic con exponential backoff
- Excepciones específicas (no "catch all")
- Graceful degradation cuando sea posible

### 6. **Budget Awareness**
- Estimación de costos antes de ejecutar
- Logs de tokens y USD por operación
- Alertas cuando se exceden thresholds

## Distribución del Repositorio

```
ai_engineering_henry/
├── 01_class/                    # Clase 1: Software vs AI Engineering
│   ├── ai_engineering/          # Ejemplo de AI Engineering
│   │   ├── brief_builder/       # Sistema de generación de briefs
│   │   │   ├── main.py         # Entry point con CLI
│   │   │   ├── config.py       # Configuración y secrets
│   │   │   ├── prompts.py      # Prompts versionados
│   │   │   ├── validator.py    # Validación de inputs/outputs
│   │   │   ├── exceptions.py   # Excepciones específicas
│   │   │   ├── retry.py        # Retry logic con backoff
│   │   │   ├── metrics.py      # Tracking de costos/latencia
│   │   │   └── logger.py       # Logging estructurado
│   │   ├── tests/              # Tests del sistema AI
│   │   ├── briefs/             # Briefs generados
│   │   └── README.md           # Guía detallada de Clase 1
│   │
│   └── python_software_engineering/  # Ejemplo de Software tradicional
│       ├── src/app.py          # Lógica de negocio determinista
│       └── tests/test_app.py   # Tests unitarios
│
├── Makefile                    # Comandos para desarrollo
├── pyproject.toml             # Dependencias y configuración
├── .env.example               # Template para variables de entorno
└── README.md                  # Este archivo
```

## Comandos Disponibles

### Desarrollo
```bash
make install        # Instalar dependencias
make run-ai         # Generar brief básico
make run-ai-context CONTEXT="texto"  # Brief con contexto
make run-se         # Ejecutar ejemplo de software clásico
```

### Testing
```bash
make test-se        # Tests de software engineering
make test-ai        # Tests de AI engineering
make test-all       # Todos los tests
make test-ai-cov    # Tests con reporte de cobertura
```

### Utilidades
```bash
make check          # Verificar sintaxis Python
make clean          # Limpiar artefactos
```

## Recursos Adicionales

### Libros Recomendados
- 📚 **"Designing Machine Learning Systems"** - Chip Huyen
  - Capítulos clave: 5 (Model Development), 7 (Monitoring), 8 (Data Distribution Shifts)
- 📚 **"AI Engineering"** - Chip Huyen
  - Especialmente: Resilient Systems, Evaluation, Production Patterns

### Artículos y Referencias
- [Rules of Machine Learning](https://developers.google.com/machine-learning/guides/rules-of-ml) - Google
- [OpenAI API Best Practices](https://platform.openai.com/docs/guides/production-best-practices)
- [The Twelve-Factor App](https://12factor.net/) - Metodología para aplicaciones modernas

### Comunidad Henry
- 💬 **Slack:** Canal #ai-engineering
- 📧 **Email:** ai-support@soyhenry.com
- 🎓 **Office Hours:** Consulta el calendario interno

## Notas de Seguridad

### ⚠️ IMPORTANTE: Nunca subas secretos a Git

El `.gitignore` está configurado para prevenir:
- ✅ Claves API (`.env`, archivos `secrets.*`)
- ✅ Certificados y llaves privadas (`.pem`, `.key`)
- ✅ Entornos virtuales (`.venv/`, `venv/`)
- ✅ Artefactos de desarrollo (`__pycache__`, `.pytest_cache`)

### Buenas Prácticas

1. **Usa `.env` para secrets** (nunca hardcodees API keys)
2. **Rotate API keys** si sospechas exposición
3. **Limita permisos** de API keys (solo los necesarios)
4. **Monitorea uso** en el dashboard de OpenAI
5. **Set spending limits** en tu cuenta de OpenAI

### ¿Qué hacer si expones un secret?

1. **Inmediatamente:** Revoca la API key en OpenAI dashboard
2. **Genera nueva key** y actualiza tu `.env`
3. **Reporta** al equipo si fue en repo compartido
4. **Aprende:** Usa `git-secrets` o pre-commit hooks

## Contribuyendo

Este es un curso en evolución. Si encuentras:
- 🐛 Bugs o errores
- 📝 Documentación poco clara
- 💡 Ideas para mejorar
- 🎯 Ejemplos adicionales que ayudarían

Por favor abre un issue o pull request. Todas las contribuciones son bienvenidas.

## Licencia

Este material es propiedad de Henry Academy y está disponible para estudiantes del programa. No redistribuir sin autorización.

---

## Próximos Pasos

1. ✅ Completa la **Clase 1** siguiendo `01_class/README.md`
2. 🧪 Experimenta con diferentes valores de `temperature` y observa los resultados
3. 📊 Revisa los archivos `.metrics.json` para entender costos
4. 🧐 Lee el brief generado y compáralo con el prompt
5. 🔍 Explora el código en `brief_builder/` para ver los patrones

**¿Listo para empezar?** → Ve a `01_class/README.md`

---

**Made with ❤️ by Henry Academy**

*"The best way to predict the future is to build it."* - Alan Kay

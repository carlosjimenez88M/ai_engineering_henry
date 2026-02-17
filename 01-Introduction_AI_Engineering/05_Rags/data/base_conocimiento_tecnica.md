# Base de Conocimiento - Guia Tecnica y Operaciones NovaTech

## 1. Arquitectura de infraestructura

### Stack tecnologico
- **Backend**: Python 3.11 + FastAPI
- **Frontend**: React 18 + TypeScript
- **Base de datos**: PostgreSQL 15 (principal), Redis 7 (cache)
- **Message queue**: RabbitMQ 3.12
- **Orquestacion**: Kubernetes 1.28 en AWS EKS
- **CI/CD**: GitHub Actions + ArgoCD
- **Monitoreo**: Datadog (metricas), Sentry (errores), PagerDuty (alertas)

### Diagrama de servicios
El sistema esta compuesto por 12 microservicios:
- `api-gateway`: Punto de entrada, rate limiting, autenticacion
- `auth-service`: Gestion de usuarios, tokens JWT, SAML
- `analytics-engine`: Motor de consultas y agregaciones
- `dashboard-service`: CRUD de dashboards y widgets
- `connector-service`: Gestion de conexiones a fuentes de datos
- `pipeline-service`: Ejecucion de pipelines ETL
- `scheduler-service`: Programacion de tareas (cron)
- `notification-service`: Envio de alertas y notificaciones
- `ai-service`: Modelo de lenguaje, embeddings, RAG
- `billing-service`: Facturacion, suscripciones, uso
- `admin-service`: Panel de administracion interno
- `file-service`: Almacenamiento y procesamiento de archivos

## 2. Procedimientos de deploy

### Deploy a produccion (standard)
1. Crear PR contra `main` con al menos 2 approvals
2. CI ejecuta: lint, unit tests, integration tests, security scan
3. Al hacer merge, ArgoCD detecta cambio y sincroniza
4. Rolling deployment: pods nuevos se crean antes de terminar los viejos
5. Health check automatico a los 60 segundos post-deploy
6. Si health check falla: rollback automatico al tag anterior

### Deploy de emergencia (hotfix)
1. Crear branch `hotfix/TICKET-XXX` desde `main`
2. Solo requiere 1 approval del on-call senior
3. Agregar label `hotfix` al PR para bypass de integration tests
4. Merge y deploy manual via: `kubectl rollout restart deployment/<service> -n production`
5. Notificar en canal #incidents de Slack con ticket y descripcion

### Rollback de emergencia
```bash
# Ver historial de deploys
kubectl rollout history deployment/<service> -n production

# Rollback a la version anterior
kubectl rollout undo deployment/<service> -n production

# Rollback a una revision especifica
kubectl rollout undo deployment/<service> --to-revision=<N> -n production

# Verificar estado
kubectl rollout status deployment/<service> -n production
```

## 3. Gestion de secretos

### Almacenamiento
- Los secretos se almacenan en AWS Secrets Manager
- Cada ambiente tiene su propio prefix: `prod/`, `staging/`, `dev/`
- Los secretos se inyectan como variables de entorno via External Secrets Operator

### Rotacion de secretos
- **API keys externas**: Rotacion manual cada 90 dias. Calendario en Confluence.
- **Database passwords**: Rotacion automatica cada 30 dias via AWS Secrets Manager rotation lambda
- **JWT signing keys**: Rotacion cada 6 meses. Requiere deploy coordinado de `auth-service` y `api-gateway`
- **SSL certificates**: Renovacion automatica via cert-manager + Let's Encrypt

### Procedimiento de rotacion manual
1. Generar nuevo secreto en AWS Secrets Manager
2. Actualizar referencia en External Secrets: `kubectl edit externalsecret <name> -n <namespace>`
3. Forzar sincronizacion: `kubectl annotate externalsecret <name> force-sync=$(date +%s) -n <namespace>`
4. Verificar que los pods tomaron el nuevo valor: `kubectl rollout restart deployment/<service>`
5. Invalidar secreto viejo despues de 24 horas (periodo de gracia)

## 4. Monitoreo y alertas

### Metricas clave (SLIs)
- **Latencia P99**: < 500ms para API responses
- **Error rate**: < 0.1% de requests con 5xx
- **Availability**: 99.9% uptime mensual
- **Pipeline success rate**: > 99% de pipelines completados sin error

### Dashboards principales (Datadog)
- `NovaTech Overview`: Vision general de todos los servicios
- `API Performance`: Latencia, throughput, error rates por endpoint
- `Pipeline Health`: Estado de pipelines ETL, tiempos de ejecucion
- `AI Service Metrics`: Latencia de inferencia, tokens consumidos, cache hit rate
- `Business Metrics`: Usuarios activos, consultas por hora, revenue impact

### Alertas configuradas (PagerDuty)
- **P1 (Critical, 5min response)**: Servicio caido, perdida de datos, breach de seguridad
- **P2 (High, 30min response)**: Error rate > 1%, latencia P99 > 2s, pipeline failure en Enterprise
- **P3 (Medium, 4h response)**: Error rate > 0.5%, disk usage > 80%, certificate expiring in < 7 days
- **P4 (Low, next business day)**: Warning de deprecation, test flaky, dependency update needed

### On-call
- Rotacion semanal, calendario en PagerDuty
- Handoff los lunes a las 10:00 UTC
- Runbook de on-call en Confluence: `wiki/spaces/OPS/on-call-handbook`
- Escalamiento si no hay respuesta en tiempo de SLA: Team Lead → Engineering Manager → VP Engineering

## 5. Troubleshooting comun

### Error: "Connection refused to analytics-engine"
**Causa probable**: El pod de analytics-engine no esta respondiendo health checks
**Solucion**:
1. Verificar estado: `kubectl get pods -n production -l app=analytics-engine`
2. Si estado es CrashLoopBackOff: `kubectl logs <pod-name> -n production --previous`
3. Causa comun: conexion a PostgreSQL fallida. Verificar `kubectl get externalsecret db-credentials -n production`
4. Reiniciar si necesario: `kubectl rollout restart deployment/analytics-engine -n production`

### Error: "Pipeline timeout after 300s"
**Causa probable**: La transformacion Python excede el timeout de 5 minutos
**Solucion**:
1. Revisar logs del pipeline en Datadog: `service:pipeline-service @pipeline_id:<ID>`
2. Identificar la transformacion lenta
3. Opciones: optimizar query, aumentar timeout (solo Scale), dividir en sub-pipelines

### Error: "Rate limit exceeded (429)"
**Causa probable**: El cliente excedio su cuota de API calls
**Solucion**:
1. Verificar uso actual: `GET /api/v1/billing/usage`
2. Si es pico legitimo: aumentar rate limit temporalmente en `api-gateway` config
3. Si es abuso: investigar patron de uso, contactar al cliente

### Error: "AI Assistant response confidence < 0.3"
**Causa probable**: La base de conocimiento no tiene informacion relevante para la consulta
**Solucion**:
1. Revisar query logs en AI service dashboard
2. Verificar que la base de conocimiento esta actualizada
3. Si el tema es nuevo: agregar documentacion relevante y re-indexar
4. Si el tema existe pero no se recupera: revisar chunking strategy y embeddings quality

### Error: "SSL certificate expiring in 3 days"
**Causa probable**: cert-manager no pudo renovar automaticamente
**Solucion**:
1. Verificar cert-manager logs: `kubectl logs -n cert-manager -l app=cert-manager`
2. Causa comun: DNS challenge fallo. Verificar Route53 permissions
3. Renovacion manual: `kubectl delete certificate <name> -n <namespace>` (cert-manager re-crea automaticamente)
4. Verificar nueva fecha: `kubectl get certificate <name> -n <namespace> -o yaml | grep -A5 status`

## 6. Seguridad

### Autenticacion
- OAuth 2.0 + OpenID Connect para login de usuarios
- API keys con scopes para integraciones M2M
- MFA obligatorio para cuentas admin (TOTP o WebAuthn)
- Session timeout: 8 horas (configurable por Enterprise)

### Autorizacion
- RBAC con 4 roles predefinidos: Viewer, Editor, Admin, Owner
- Custom roles disponibles en plan Enterprise
- Permisos granulares por recurso (dashboard, pipeline, connector)
- Audit log de todas las acciones admin (retencion 1 ano)

### Compliance
- SOC 2 Type II certificado
- GDPR compliance con DPA disponible
- Cifrado en transito (TLS 1.3) y en reposo (AES-256)
- Penetration testing anual por tercero independiente
- Bug bounty program activo (HackerOne)

### Respuesta a incidentes
1. Detectar y contener (< 15 minutos)
2. Evaluar impacto y clasificar severidad
3. Notificar stakeholders segun matriz de comunicacion
4. Remediar y documentar
5. Post-mortem dentro de 48 horas (blameless)
6. Action items con owner y deadline

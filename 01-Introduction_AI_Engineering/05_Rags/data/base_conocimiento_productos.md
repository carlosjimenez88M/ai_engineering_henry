# Base de Conocimiento - Productos NovaTech Solutions

## 1. NovaTech Analytics Pro

NovaTech Analytics Pro es nuestra plataforma principal de business intelligence diseñada para empresas medianas y grandes. Permite crear dashboards interactivos, reportes automatizados y alertas en tiempo real sobre metricas clave del negocio.

### Caracteristicas principales
- Dashboards drag-and-drop con mas de 50 tipos de visualizacion
- Conexion nativa a mas de 30 fuentes de datos (PostgreSQL, MySQL, BigQuery, Snowflake, APIs REST)
- Motor de alertas configurable con notificaciones por email, Slack y webhook
- Reportes programados con exportacion a PDF, Excel y Google Sheets
- Role-based access control (RBAC) con integracion SAML/SSO
- API REST para integracion con sistemas externos

### Planes y precios
- **Starter**: $49/mes por usuario. Hasta 5 dashboards, 3 fuentes de datos, soporte por email.
- **Professional**: $99/mes por usuario. Dashboards ilimitados, 15 fuentes de datos, alertas, soporte prioritario.
- **Enterprise**: Precio personalizado. Todo incluido, fuentes ilimitadas, SLA 99.9%, dedicated account manager.

### Requisitos tecnicos
- Navegador moderno (Chrome 90+, Firefox 88+, Safari 15+, Edge 90+)
- Conexion a internet estable (minimo 5 Mbps)
- Para on-premise: Docker 20.10+, 8 GB RAM minimo, 4 CPU cores

## 2. NovaTech DataSync

DataSync es nuestra herramienta de ETL (Extract, Transform, Load) para sincronizar datos entre multiples sistemas. Soporta sincronizacion en tiempo real y batch.

### Caracteristicas principales
- Pipelines visuales sin codigo para transformaciones de datos
- Mas de 100 conectores pre-construidos (Salesforce, HubSpot, Stripe, AWS S3, etc.)
- Monitoreo de pipelines con logging detallado y alertas de fallo
- Transformaciones SQL y Python personalizadas
- Versionado de pipelines con rollback automatico
- Scheduling flexible: cron, intervalo, trigger por evento

### Planes y precios
- **Free**: Hasta 1000 registros/dia, 2 pipelines, 5 conectores
- **Growth**: $199/mes. 100K registros/dia, pipelines ilimitados, todos los conectores
- **Scale**: $599/mes. 1M registros/dia, prioridad de ejecucion, soporte 24/7

### Limites y consideraciones
- Los pipelines en tiempo real consumen 3x mas creditos que batch
- Las transformaciones Python tienen un timeout de 5 minutos por ejecucion
- La retencion de logs es de 30 dias en Growth y 90 dias en Scale
- No soporta escritura directa a bases de datos on-premise sin VPN connector

## 3. NovaTech AI Assistant

AI Assistant es nuestro producto de chatbot empresarial impulsado por IA. Permite a las empresas crear asistentes virtuales que responden preguntas basados en su documentacion interna.

### Caracteristicas principales
- RAG (Retrieval-Augmented Generation) con base de conocimiento personalizable
- Soporte multiidioma (espanol, ingles, portugues, frances)
- Integracion con Slack, Microsoft Teams, WhatsApp Business y web widget
- Panel de analitica con metricas de satisfaccion, precision y cobertura
- Escalamiento a agente humano cuando la confianza es baja
- Fine-tuning del modelo con datos propios (plan Enterprise)

### Planes y precios
- **Starter**: $299/mes. 1000 consultas/mes, 1 base de conocimiento, web widget
- **Business**: $799/mes. 10K consultas/mes, 5 bases de conocimiento, todas las integraciones
- **Enterprise**: Precio personalizado. Consultas ilimitadas, fine-tuning, SLA dedicado

### Limites conocidos
- El modelo puede generar respuestas imprecisas cuando la base de conocimiento tiene informacion contradictoria
- Archivos PDF escaneados (no-OCR) no son indexables directamente
- El tiempo de indexacion para bases de conocimiento grandes (>10K documentos) puede ser de hasta 2 horas
- Las consultas en idiomas no soportados se responden en ingles por defecto

## 4. Politicas de soporte

### Tiempos de respuesta por plan
- **Free/Starter**: Email, respuesta en 48 horas habiles
- **Professional/Growth/Business**: Email + chat, respuesta en 4 horas habiles
- **Enterprise/Scale**: Telefono + email + chat + Slack dedicado, respuesta en 1 hora, 24/7

### Proceso de escalamiento
1. Nivel 1 (Soporte General): Preguntas frecuentes, configuracion basica, billing
2. Nivel 2 (Soporte Tecnico): Bugs, integraciones, performance
3. Nivel 3 (Ingenieria): Incidentes criticos, perdida de datos, vulnerabilidades

### SLA por producto
- Analytics Pro: 99.9% uptime (Enterprise), 99.5% (Professional)
- DataSync: 99.9% uptime (Scale), 99.5% (Growth)
- AI Assistant: 99.5% uptime (Enterprise), 99.0% (Business)

### Politica de reembolso
- Cancelacion dentro de los primeros 14 dias: reembolso completo
- Despues de 14 dias: se cobra proporcional al uso del mes
- Enterprise: segun contrato individual

## 5. Preguntas frecuentes

### Puedo migrar datos entre planes?
Si, la migracion es automatica al hacer upgrade. Al hacer downgrade, los dashboards/pipelines que excedan el limite del nuevo plan quedan en modo solo-lectura.

### Los datos se almacenan en la nube?
Si, usamos AWS con regiones en us-east-1 (Virginia), eu-west-1 (Irlanda) y sa-east-1 (Sao Paulo). Enterprise puede elegir region y opcion on-premise.

### Ofrecen descuentos por volumen?
Si, a partir de 50 usuarios ofrecemos descuentos del 15-30% dependiendo del compromiso anual. Contactar a sales@novatech.example.com.

### Como se manejan las actualizaciones?
Las actualizaciones son automaticas y sin downtime (rolling deployment). Los clientes Enterprise pueden programar ventanas de actualizacion.

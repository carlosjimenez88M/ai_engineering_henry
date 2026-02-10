"""
Herramientas especializadas para sistema ReAct de coqueteo.

Este modulo implementa 4 herramientas avanzadas que permiten al agente ReAct
analizar compatibilidad, generar icebreakers, predecir respuestas y escalar
conversaciones de manera estrategica.

NOTA: En produccion, estas herramientas usarian modelos ML reales, bases de datos
de patrones, y analisis de comportamiento. Esta implementacion usa heuristicas
simplificadas con fines educativos.

Uso:
    from common.coqueteo_tools import (
        analizar_compatibilidad,
        generar_icebreaker,
        predecir_respuesta,
        escalar_conversacion
    )

    tools = [
        analizar_compatibilidad,
        generar_icebreaker,
        predecir_respuesta,
        escalar_conversacion
    ]
"""

import json
from langchain_core.tools import tool


@tool
def analizar_compatibilidad(perfil_usuario: str, perfil_match: str) -> str:
    """
    Analiza compatibilidad entre dos perfiles usando multiples dimensiones.

    Esta herramienta evalua la compatibilidad potencial entre el usuario y un
    match considerando: gustos compartidos, estilos compatibles, y red flags.

    Args:
        perfil_usuario: JSON string del perfil del usuario (quien busca match)
        perfil_match: JSON string del perfil del match potencial

    Returns:
        JSON string con estructura:
        {
            "compatibilidad_porcentaje": int (0-100),
            "areas_conexion": List[str],
            "diferencias_complementarias": List[str],
            "red_flags_detectadas": List[str],
            "recomendacion": str,
            "estrategia_apertura": str
        }

    Example:
        >>> resultado = analizar_compatibilidad(
        ...     '{"gustos": ["jazz", "cine arte"], "estilo": "profundo"}',
        ...     '{"intereses": ["musica", "fotografia"], "personalidad": "creativa"}'
        ... )
        >>> print(json.loads(resultado)["compatibilidad_porcentaje"])
        75
    """
    try:
        usuario = json.loads(perfil_usuario)
        match = json.loads(perfil_match)
    except json.JSONDecodeError:
        return json.dumps({
            "error": "Formato JSON invalido en perfiles",
            "compatibilidad_porcentaje": 0
        })

    # Extraer datos relevantes con defaults
    gustos_usuario = usuario.get("gustos", [])
    intereses_match = match.get("intereses", [])
    estilo_usuario = usuario.get("estilo", "")
    personalidad_match = match.get("personalidad", "")
    red_flags_usuario = usuario.get("red_flags", [])
    red_flags_match = match.get("red_flags_para_ella", [])

    # 1. Calcular gustos compartidos (peso: 40%)
    gustos_score = 0
    areas_conexion = []

    # Detectar overlaps semanticos (simplificado)
    keywords_map = {
        "musica": ["jazz", "salsa", "boleros", "reggaeton", "concierto"],
        "cultura": ["cine", "arte", "fotografia", "literatura", "libros", "museo"],
        "gastronomia": ["cafes", "vino", "cocina", "restaurantes"],
        "aventura": ["escalada", "viajar", "caminatas", "deportes"],
        "intelectual": ["filosofia", "ciencia", "documentales", "tertulias"]
    }

    for categoria, keywords in keywords_map.items():
        usuario_match = any(
            any(kw in str(gusto).lower() for kw in keywords)
            for gusto in gustos_usuario
        )
        match_match = any(
            any(kw in str(interes).lower() for kw in keywords)
            for interes in intereses_match
        )

        if usuario_match and match_match:
            gustos_score += 8  # Max 40 puntos (5 categorias * 8)
            areas_conexion.append(f"Ambos disfrutan {categoria}")

    # 2. Evaluar compatibilidad de estilos (peso: 30%)
    estilos_score = 0
    diferencias_complementarias = []

    # Matriz de compatibilidad de estilos (simplificada)
    estilo_compatibility = {
        "romantico tradicional": ["curiosa", "sensibilidad", "profund"],
        "casual pero intencional": ["independiente", "autentic", "creativ"],
        "profundo": ["introvertida", "perfeccionista", "intelectual"]
    }

    for estilo_key, personalidades_compatibles in estilo_compatibility.items():
        if estilo_key in estilo_usuario.lower():
            if any(p in personalidad_match.lower() for p in personalidades_compatibles):
                estilos_score = 30
                diferencias_complementarias.append(
                    f"Tu estilo {estilo_key} complementa su personalidad {personalidad_match}"
                )
                break
            else:
                estilos_score = 15  # Compatibilidad media
                diferencias_complementarias.append(
                    "Estilos diferentes pero potencialmente complementarios"
                )

    # 3. Detectar red flags (peso: 30%, negativo)
    red_flags_detectadas = []
    red_flags_penalty = 0

    # Verificar si red flags del usuario coinciden con lo que ella rechaza
    for flag_usuario in red_flags_usuario:
        for flag_match in red_flags_match:
            if any(
                keyword in flag_usuario.lower() and keyword in flag_match.lower()
                for keyword in ["machismo", "superficial", "posesiv", "invasiv"]
            ):
                red_flags_detectadas.append(
                    f"Cuidado: Tu potencial '{flag_usuario}' "
                    f"coincide con su rechazo de '{flag_match}'"
                )
                red_flags_penalty += 10  # -10 puntos por red flag

    # 4. Calcular compatibilidad total
    compatibilidad_base = gustos_score + estilos_score
    compatibilidad_final = max(0, min(100, compatibilidad_base - red_flags_penalty))

    # 5. Generar recomendacion estrategica
    if compatibilidad_final >= 70:
        recomendacion = (
            "Alta compatibilidad. Procede con confianza pero sin arrogancia."
        )
        estrategia = (
            "Abre con referencia especifica a una de las areas de conexion. "
            "Se autentico y propositivo."
        )
    elif compatibilidad_final >= 50:
        recomendacion = (
            "Compatibilidad media-alta. Hay potencial si ejecutas bien."
        )
        estrategia = (
            "Enfocate en las areas de conexion identificadas. "
            "Se creativo para destacar. Evita red flags detectadas."
        )
    elif compatibilidad_final >= 30:
        recomendacion = (
            "Compatibilidad media-baja. Requiere ejecucion excepcional."
        )
        estrategia = (
            "Busca angulo unico que no sea obvio. "
            "Tal vez humor autoironico sobre diferencias. Alto riesgo."
        )
    else:
        recomendacion = (
            "Baja compatibilidad. Considera si vale la pena el esfuerzo."
        )
        estrategia = (
            "Si decides intentar, se completamente autentico. "
            "No trates de forzar conexion que no existe."
        )

    resultado = {
        "compatibilidad_porcentaje": int(compatibilidad_final),
        "areas_conexion": areas_conexion if areas_conexion else [
            "No se detectaron areas obvias de conexion - busca mas profundo"
        ],
        "diferencias_complementarias": diferencias_complementarias if diferencias_complementarias else [
            "Estilos muy diferentes - puede ser desafio o oportunidad"
        ],
        "red_flags_detectadas": red_flags_detectadas if red_flags_detectadas else [
            "No se detectaron red flags obvias - procede con precaucion normal"
        ],
        "recomendacion": recomendacion,
        "estrategia_apertura": estrategia
    }

    return json.dumps(resultado, ensure_ascii=False, indent=2)


@tool
def generar_icebreaker(perfil: str, tono: str) -> str:
    """
    Genera 3 opciones de mensaje de apertura (icebreaker) calibradas al tono.

    Esta herramienta crea mensajes de apertura optimizados basados en el perfil
    del match y el tono deseado (conservador, medio, atrevido).

    Args:
        perfil: JSON string del perfil del match
        tono: Uno de: "conservador", "medio", "atrevido"

    Returns:
        JSON string con estructura:
        {
            "opciones": [
                {
                    "texto": str,
                    "probabilidad_exito": int (0-100),
                    "por_que_funciona": str,
                    "riesgos": str
                }
            ]
        }

    Example:
        >>> resultado = generar_icebreaker(
        ...     '{"intereses": ["escalada"], "bio_app": "aventurera"}',
        ...     "medio"
        ... )
    """
    try:
        match_data = json.loads(perfil)
    except json.JSONDecodeError:
        return json.dumps({
            "error": "Formato JSON invalido en perfil"
        })

    tono = tono.lower()
    if tono not in ["conservador", "medio", "atrevido"]:
        return json.dumps({
            "error": "Tono debe ser: conservador, medio, o atrevido"
        })

    # Extraer datos del perfil
    intereses = match_data.get("intereses", [])
    bio = match_data.get("bio_app", "")
    nombre = match_data.get("nombre", "")
    profesion = match_data.get("profesion", "")

    # Generar opciones segun tono
    opciones = []

    if tono == "conservador":
        # Opcion 1: Referencia directa a interes
        if intereses and len(intereses) > 0:
            primer_interes = intereses[0]
            opciones.append({
                "texto": (
                    f"Hola {nombre}, vi que te gusta {primer_interes}. "
                    f"Yo tambien! Cual ha sido tu experiencia favorita relacionada con eso?"
                ),
                "probabilidad_exito": 65,
                "por_que_funciona": (
                    "Conexion directa sobre interes compartido. "
                    "Pregunta abierta invita a conversacion. Tono respetuoso."
                ),
                "riesgos": "Puede ser demasiado generico si muchos abren igual."
            })

        # Opcion 2: Referencia a profesion con curiosidad genuina
        if profesion:
            opciones.append({
                "texto": (
                    f"Hola! Veo que eres {profesion}. "
                    f"Siempre me ha fascinado ese campo. "
                    f"Que es lo que mas te apasiona de tu trabajo?"
                ),
                "probabilidad_exito": 60,
                "por_que_funciona": (
                    "Muestra interes genuino en su vida profesional. "
                    "Pregunta abierta y respetuosa."
                ),
                "riesgos": "Si no esta apasionada por su trabajo, puede caer plano."
            })

        # Opcion 3: Comentario sobre bio
        if bio:
            opciones.append({
                "texto": (
                    f"Tu bio me hizo sonreir. "
                    f"'{bio[:50]}...' suena a alguien que sabe lo que quiere. "
                    f"Cuentame mas sobre ti."
                ),
                "probabilidad_exito": 55,
                "por_que_funciona": (
                    "Referencia especifica a su bio (no generica). "
                    "Cumplido sutil sin ser abrumador."
                ),
                "riesgos": "Muy seguro, pero puede ser poco memorable."
            })

    elif tono == "medio":
        # Opcion 1: Humor ligero + referencia especifica
        if "escalada" in str(intereses).lower() or "aventur" in bio.lower():
            opciones.append({
                "texto": (
                    f"Hola {nombre}! Vi tu perfil y pense: "
                    f"'definitivamente alguien que me dejaria atras en una montana'. "
                    f"Pero me encantaria intentarlo. Cual es tu ruta favorita?"
                ),
                "probabilidad_exito": 75,
                "por_que_funciona": (
                    "Humor autoironico (vulnerable pero confiado). "
                    "Muestra que leiste perfil. Pregunta especifica invita a respuesta."
                ),
                "riesgos": "Si no tiene sentido del humor, puede fallar."
            })

        # Opcion 2: Observacion inteligente sobre contraste
        if profesion and intereses:
            opciones.append({
                "texto": (
                    f"{profesion} de dia, {intereses[0]} de noche. "
                    f"Me gusta esa dualidad. Yo tambien creo que la vida "
                    f"necesita balance entre lo cerebral y lo aventurero. "
                    f"Como llegaste a ese equilibrio?"
                ),
                "probabilidad_exito": 70,
                "por_que_funciona": (
                    "Muestra que notaste algo no obvio (dualidad). "
                    "Conexion intelectual + curiosidad genuina."
                ),
                "riesgos": "Requiere que realmente haya esa dualidad en perfil."
            })

        # Opcion 3: Challenge playful
        opciones.append({
            "texto": (
                f"Hola {nombre}! Propuesta: tu me recomiendas algo que crees "
                f"que deberia probar (relacionado con {intereses[0] if intereses else 'tus intereses'}), "
                f"y yo hago lo mismo. Deal?"
            ),
            "probabilidad_exito": 72,
            "por_que_funciona": (
                "Crea dinamica de intercambio (reciprocidad). "
                "Playful pero no invasivo. Baja presion."
            ),
            "riesgos": "Requiere que ella quiera invertir energia en responder."
        })

    else:  # atrevido
        # Opcion 1: Cumplido directo pero inteligente
        opciones.append({
            "texto": (
                f"Ok, admito que tu perfil me hizo pausar mid-scroll. "
                f"{bio[:60] if bio else 'Lo que describes'} suena exactamente "
                f"al tipo de persona con la que me encantaria tomar un cafe "
                f"y perder la nocion del tiempo. Cuando tienes un hueco esta semana?"
            ),
            "probabilidad_exito": 65,
            "por_que_funciona": (
                "Directo y honesto sobre atraccion. Propone accion concreta. "
                "Confiado sin ser arrogante."
            ),
            "riesgos": (
                "Alto riesgo si ella prefiere slow burn. "
                "Puede parecer too much si no hay quimica en perfil."
            )
        })

        # Opcion 2: Playful desafio
        if "intelectual" in str(match_data).lower() or "ciencia" in profesion.lower():
            opciones.append({
                "texto": (
                    f"Plot twist: {profesion} que tambien {intereses[0] if intereses else 'tiene vida interesante'}. "
                    f"Apuesto a que tienes opiniones fuertes sobre [tema relevante]. "
                    f"Desafio: convenceme de algo en 3 mensajes."
                ),
                "probabilidad_exito": 60,
                "por_que_funciona": (
                    "Crea tension intelectual playful. "
                    "Muestra que no tienes miedo a debate. Memorable."
                ),
                "riesgos": (
                    "Puede ser intimidante. Requiere que ella disfrute banter intelectual."
                )
            })

        # Opcion 3: Vulnerable + atrevido
        opciones.append({
            "texto": (
                f"Confesion: lei tu bio dos veces porque me parecio genuina "
                f"en un mar de perfiles copy-paste. '{bio[:50]}...' - eso. "
                f"Soy [tu descripcion breve]. Si te interesa alguien [cualidad tuya], "
                f"escribeme de vuelta. Si no, suerte en la busqueda!"
            ),
            "probabilidad_exito": 70,
            "por_que_funciona": (
                "Vulnerable (admite interes) pero da salida digna. "
                "Autentico y directo. No ruega atencion."
            ),
            "riesgos": (
                "Requiere que tu descripcion breve sea realmente interesante. "
                "Puede sonar como ultimatum si mal ejecutado."
            )
        })

    # Si no se generaron opciones, crear defaults
    if not opciones:
        opciones = [
            {
                "texto": f"Hola {nombre}! Me gusto tu perfil. Cuentame mas sobre ti.",
                "probabilidad_exito": 45,
                "por_que_funciona": "Seguro y directo",
                "riesgos": "Muy generico"
            }
        ]

    return json.dumps({"opciones": opciones}, ensure_ascii=False, indent=2)


@tool
def predecir_respuesta(mensaje_propuesto: str, perfil_destinatario: str) -> str:
    """
    Predice probabilidad de respuesta y sugiere mejoras al mensaje.

    Esta herramienta analiza un mensaje propuesto y predice su efectividad
    basandose en el perfil del destinatario, identificando factores positivos,
    negativos, y sugerencias de mejora.

    Args:
        mensaje_propuesto: El texto del mensaje que se planea enviar
        perfil_destinatario: JSON string del perfil del match

    Returns:
        JSON string con estructura:
        {
            "probabilidad_respuesta": int (0-100),
            "factores_positivos": List[str],
            "factores_negativos": List[str],
            "mejoras_sugeridas": List[str],
            "version_mejorada": str
        }

    Example:
        >>> resultado = predecir_respuesta(
        ...     "Hola hermosa",
        ...     '{"personalidad": "independiente", "red_flags": ["superficial"]}'
        ... )
    """
    try:
        perfil = json.loads(perfil_destinatario)
    except json.JSONDecodeError:
        return json.dumps({
            "error": "Formato JSON invalido en perfil_destinatario"
        })

    mensaje = mensaje_propuesto.strip()
    probabilidad_base = 50  # Start at 50%

    factores_positivos = []
    factores_negativos = []
    mejoras_sugeridas = []

    # Extraer datos del perfil
    personalidad = perfil.get("personalidad", "").lower()
    red_flags = [rf.lower() for rf in perfil.get("red_flags_para_ella", [])]
    intereses = perfil.get("intereses", [])
    nombre = perfil.get("nombre", "")

    # 1. Analizar longitud del mensaje
    palabra_count = len(mensaje.split())
    if palabra_count < 5:
        probabilidad_base -= 15
        factores_negativos.append("Mensaje muy corto - parece poco esfuerzo")
        mejoras_sugeridas.append("Expande a al menos 2-3 oraciones con contenido especifico")
    elif palabra_count > 60:
        probabilidad_base -= 10
        factores_negativos.append("Mensaje muy largo para primer contacto")
        mejoras_sugeridas.append("Reduce a 2-3 oraciones puntuales")
    else:
        probabilidad_base += 5
        factores_positivos.append("Longitud apropiada para primer mensaje")

    # 2. Detectar red flags comunes
    red_flag_keywords = {
        "superficial": ["hermosa", "linda", "bella", "preciosa", "reina", "mami"],
        "invasivo": ["celular", "telefono", "numero", "whatsapp", "instagram"],
        "desesperado": ["por favor", "dame una oportunidad", "chance"],
        "generico": ["hola", "como estas", "que tal", "saludos"]
    }

    mensaje_lower = mensaje.lower()
    for red_flag_type, keywords in red_flag_keywords.items():
        if any(keyword in mensaje_lower for keyword in keywords):
            if any(red_flag_type in rf for rf in red_flags):
                probabilidad_base -= 20
                factores_negativos.append(
                    f"Uso de terminos que coinciden con sus red flags ({red_flag_type})"
                )
                mejoras_sugeridas.append(
                    f"Evita terminos como {keywords[:2]} que pueden sonar {red_flag_type}"
                )

    # 3. Verificar personalizacion
    if nombre and nombre.lower() in mensaje_lower:
        probabilidad_base += 10
        factores_positivos.append("Usa su nombre (personalizacion)")
    else:
        probabilidad_base -= 5
        factores_negativos.append("No menciona su nombre")
        mejoras_sugeridas.append(f"Comienza con 'Hola {nombre}' para personalizar")

    # 4. Verificar referencias a perfil
    referencias_detectadas = False
    for interes in intereses:
        if any(word in mensaje_lower for word in str(interes).lower().split()):
            referencias_detectadas = True
            probabilidad_base += 15
            factores_positivos.append(
                f"Menciona su interes en {interes} (muestra que leiste perfil)"
            )
            break

    if not referencias_detectadas:
        probabilidad_base -= 10
        factores_negativos.append("No hace referencia a sus intereses o bio")
        mejoras_sugeridas.append(
            "Incluye referencia especifica a uno de sus intereses: "
            f"{', '.join(intereses[:2]) if intereses else 'revisa su bio'}"
        )

    # 5. Detectar preguntas abiertas
    tiene_pregunta = "?" in mensaje
    if tiene_pregunta:
        # Verificar que no sea pregunta cerrada
        preguntas_cerradas = ["como estas", "que tal", "todo bien"]
        if not any(pc in mensaje_lower for pc in preguntas_cerradas):
            probabilidad_base += 10
            factores_positivos.append("Incluye pregunta abierta (invita a conversacion)")
        else:
            factores_negativos.append("Pregunta muy generica")
            mejoras_sugeridas.append(
                "Cambia pregunta generica por algo especifico a sus intereses"
            )
    else:
        probabilidad_base -= 8
        factores_negativos.append("No incluye pregunta (dificulta respuesta)")
        mejoras_sugeridas.append("Agrega pregunta abierta al final para facilitar respuesta")

    # 6. Detectar tono apropiado segun personalidad
    if "independiente" in personalidad or "introvertida" in personalidad:
        if any(term in mensaje_lower for term in ["salir", "conocernos", "date", "cita"]):
            probabilidad_base -= 12
            factores_negativos.append(
                "Propones salir demasiado rapido para su personalidad introvertida/independiente"
            )
            mejoras_sugeridas.append("Construye conexion primero, propone salir despues")

    # 7. Calcular probabilidad final
    probabilidad_final = max(0, min(100, probabilidad_base))

    # 8. Generar version mejorada (si hay mejoras que hacer)
    if mejoras_sugeridas:
        version_mejorada = f"Hola {nombre}! "
        if intereses:
            version_mejorada += (
                f"Vi que te gusta {intereses[0]} - yo tambien! "
                f"Cual ha sido tu experiencia favorita con eso?"
            )
        else:
            version_mejorada += (
                "Me gusto tu perfil porque [razon especifica que notaste]. "
                "Cuentame mas sobre [algo de su bio]."
            )
    else:
        version_mejorada = "Tu mensaje ya esta bien optimizado."

    resultado = {
        "probabilidad_respuesta": int(probabilidad_final),
        "factores_positivos": factores_positivos if factores_positivos else [
            "No se detectaron factores claramente positivos"
        ],
        "factores_negativos": factores_negativos if factores_negativos else [
            "No se detectaron factores claramente negativos"
        ],
        "mejoras_sugeridas": mejoras_sugeridas if mejoras_sugeridas else [
            "El mensaje esta razonablemente bien"
        ],
        "version_mejorada": version_mejorada
    }

    return json.dumps(resultado, ensure_ascii=False, indent=2)


@tool
def escalar_conversacion(historial_mensajes: str, objetivo: str) -> str:
    """
    Sugiere proximo paso estrategico en la conversacion.

    Esta herramienta analiza el historial de mensajes intercambiados y sugiere
    como escalar la conversacion segun el objetivo (profundizar, proponer cita,
    mantener ritmo, retomar).

    Args:
        historial_mensajes: JSON string con array de mensajes:
            [{"autor": "usuario"|"match", "texto": str, "timestamp": str}]
        objetivo: Uno de: "profundizar", "proponer_cita", "mantener_ritmo", "retomar"

    Returns:
        JSON string con estructura:
        {
            "sugerencia_accion": str,
            "mensaje_sugerido": str,
            "timing_recomendado": str,
            "riesgos": str,
            "indicadores_exito": List[str]
        }

    Example:
        >>> resultado = escalar_conversacion(
        ...     '[{"autor": "usuario", "texto": "Hola"}, {"autor": "match", "texto": "Hola!"}]',
        ...     "profundizar"
        ... )
    """
    try:
        mensajes = json.loads(historial_mensajes)
    except json.JSONDecodeError:
        return json.dumps({
            "error": "Formato JSON invalido en historial_mensajes"
        })

    objetivo = objetivo.lower()
    if objetivo not in ["profundizar", "proponer_cita", "mantener_ritmo", "retomar"]:
        return json.dumps({
            "error": "Objetivo debe ser: profundizar, proponer_cita, mantener_ritmo, o retomar"
        })

    # Analizar historial
    num_mensajes = len(mensajes)
    ultimo_mensaje = mensajes[-1] if mensajes else {}
    ultimo_autor = ultimo_mensaje.get("autor", "")

    # Calcular ratio de mensajes (balance)
    mensajes_usuario = sum(1 for m in mensajes if m.get("autor") == "usuario")
    mensajes_match = sum(1 for m in mensajes if m.get("autor") == "match")

    # Analizar engagement (longitud de respuestas)
    if mensajes_match > 0:
        avg_length_match = sum(
            len(m.get("texto", "").split())
            for m in mensajes
            if m.get("autor") == "match"
        ) / mensajes_match
    else:
        avg_length_match = 0

    engagement_level = "alto" if avg_length_match > 20 else "medio" if avg_length_match > 10 else "bajo"

    # Generar sugerencias segun objetivo
    if objetivo == "profundizar":
        if engagement_level == "bajo":
            sugerencia = {
                "sugerencia_accion": (
                    "Engagement bajo detectado. Antes de profundizar, "
                    "asegurate de que hay interes genuino."
                ),
                "mensaje_sugerido": (
                    "Oye, siento que tal vez estoy escribiendo de mas. "
                    "Dime honestamente: te interesa seguir conversando o prefieres que lo dejemos aqui? "
                    "Sin presion!"
                ),
                "timing_recomendado": "Inmediatamente (si ella no esta respondiendo con energia)",
                "riesgos": (
                    "Puede sonar inseguro, pero es mejor que seguir invirtiendo "
                    "en conversacion unilateral."
                ),
                "indicadores_exito": [
                    "Ella responde honestamente (si o no)",
                    "Si dice si, sus proximos mensajes son mas largos/energeticos"
                ]
            }
        else:
            sugerencia = {
                "sugerencia_accion": (
                    "Engagement medio-alto. Momento ideal para profundizar con pregunta vulnerable."
                ),
                "mensaje_sugerido": (
                    "Me gusta hacia donde va esta conversacion. "
                    "Pregunta mas personal: que es algo que te apasiona tanto "
                    "que podrias hablar de eso por horas sin aburrirte?"
                ),
                "timing_recomendado": (
                    "Despues de al menos 10-15 mensajes intercambiados con buen ritmo"
                ),
                "riesgos": (
                    "Si es demasiado pronto, puede intimidar. "
                    "Asegurate de que ya hay comodidad."
                ),
                "indicadores_exito": [
                    "Ella comparte algo genuinamente personal",
                    "La conversacion se vuelve mas bidireccional y profunda",
                    "Ella hace preguntas personales de vuelta"
                ]
            }

    elif objetivo == "proponer_cita":
        if num_mensajes < 15:
            sugerencia = {
                "sugerencia_accion": (
                    "PRECAUCION: Solo {} mensajes intercambiados. "
                    "Es pronto para proponer cita. Considera esperar.".format(num_mensajes)
                ),
                "mensaje_sugerido": (
                    "Esta conversacion me esta gustando mucho. "
                    "Me encantaria seguir conociendote. "
                    "[Continua conversacion 5-10 mensajes mas antes de proponer cita]"
                ),
                "timing_recomendado": "Espera al menos 20 mensajes o 2-3 dias de conversacion",
                "riesgos": (
                    "Proponer demasiado rapido puede espantarla. "
                    "La mayoria de las personas necesitan sentir conexion antes."
                ),
                "indicadores_exito": [
                    "Ella misma menciona algo sobre 'conocerse en persona'",
                    "Pregunta donde vives o que haces los fines de semana"
                ]
            }
        elif engagement_level == "bajo":
            sugerencia = {
                "sugerencia_accion": (
                    "Engagement bajo. No es buen momento para proponer cita."
                ),
                "mensaje_sugerido": (
                    "Primero reaviva la conversacion con algo interesante/gracioso "
                    "antes de proponer salir."
                ),
                "timing_recomendado": "NO AHORA - espera a que engagement suba",
                "riesgos": "Alta probabilidad de rechazo si propones ahora.",
                "indicadores_exito": []
            }
        else:
            sugerencia = {
                "sugerencia_accion": (
                    "Momento optimo para proponer cita. Engagement alto, suficientes mensajes."
                ),
                "mensaje_sugerido": (
                    "Mira, esta conversacion es genial pero definitivamente seria mejor "
                    "tomarla en persona. Que te parece si [actividad especifica relacionada "
                    "a interes de ella] este [dia concreto]? "
                    "Conozco [lugar especifico] que te gustaria."
                ),
                "timing_recomendado": (
                    "En momento alto de la conversacion (cuando ambos estan respondiendo rapido)"
                ),
                "riesgos": (
                    "Si dice no, no insistas. Respeta su decision y mantente amigable."
                ),
                "indicadores_exito": [
                    "Ella dice si inmediatamente",
                    "Ella propone alternativa (otro dia/lugar) = buena senal",
                    "Ella pregunta detalles (donde, que hora) = muy buena senal"
                ]
            }

    elif objetivo == "mantener_ritmo":
        if mensajes_usuario > mensajes_match * 1.5:
            sugerencia = {
                "sugerencia_accion": (
                    "Estas escribiendo mucho mas que ella. FRENA. "
                    "Deja espacio para que ella invierta tambien."
                ),
                "mensaje_sugerido": (
                    "[NO ENVIES MENSAJE TODAVIA] "
                    "Espera a que ella responda antes de continuar."
                ),
                "timing_recomendado": (
                    "Dale al menos 2-4 horas antes de tu proximo mensaje. "
                    "Si no responde en 24hrs, considera que tal vez no esta interesada."
                ),
                "riesgos": (
                    "Seguir escribiendo mucho puede parecer desesperado o abrumador."
                ),
                "indicadores_exito": [
                    "Ella responde con energia renovada",
                    "El balance de mensajes se equilibra"
                ]
            }
        else:
            sugerencia = {
                "sugerencia_accion": (
                    "Balance bueno. Mantener ritmo natural de conversacion."
                ),
                "mensaje_sugerido": (
                    "[Continua respondiendo a lo que ella comparte con curiosidad genuina. "
                    "Alterna entre compartir sobre ti y hacer preguntas sobre ella.]"
                ),
                "timing_recomendado": (
                    "Responde con tiempo similar al que ella tarda (espejo natural)"
                ),
                "riesgos": "Bajo - solo mantente autentico.",
                "indicadores_exito": [
                    "La conversacion fluye naturalmente",
                    "Ambos hacen preguntas",
                    "Ambos comparten informacion personal gradualmente"
                ]
            }

    else:  # retomar
        if not mensajes or ultimo_autor == "usuario":
            # En produccion: calcular dias desde ultimo mensaje
            # dias_desde_ultimo = (datetime.now() - ultimo_timestamp).days
            sugerencia = {
                "sugerencia_accion": (
                    "Tu fuiste el ultimo en escribir y ella no respondio. "
                    "Retomar requiere estrategia cuidadosa."
                ),
                "mensaje_sugerido": (
                    "Hey! Se que han pasado [tiempo]. "
                    "Vi [algo relevante a su interes] y pense en nuestra conversacion. "
                    "[Compartir ese algo brevemente]. "
                    "Como has estado?"
                ),
                "timing_recomendado": (
                    "Si han pasado 3-7 dias, esta bien retomar. "
                    "Si mas de 2 semanas, probablemente mejor dejarlo."
                ),
                "riesgos": (
                    "Puede ignorarte otra vez. "
                    "No lo tomes personal - puede estar ocupada o no interesada."
                ),
                "indicadores_exito": [
                    "Ella responde con explicacion de por que no contesto antes",
                    "Ella retoma conversacion con energia"
                ]
            }
        else:
            sugerencia = {
                "sugerencia_accion": (
                    "Ella fue la ultima en escribir. RESPONDE ya! "
                    "No la dejes esperando."
                ),
                "mensaje_sugerido": (
                    "[Responde a lo que ella escribio + agrega algo nuevo para continuar]"
                ),
                "timing_recomendado": "AHORA - no la hagas esperar mas",
                "riesgos": "Alto riesgo de perderla si sigues sin responder.",
                "indicadores_exito": ["Respondes y continuan conversacion"]
            }

    return json.dumps(sugerencia, ensure_ascii=False, indent=2)


# Lista de todas las herramientas para facil import
COQUETEO_TOOLS = [
    analizar_compatibilidad,
    generar_icebreaker,
    predecir_respuesta,
    escalar_conversacion
]

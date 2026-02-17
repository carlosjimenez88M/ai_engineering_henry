"""
Personas Latino para ejemplos de coqueteo y matching.

Este modulo define 3 arquetipos distintos de perfiles Latino para demostrar
como los sistemas de prompting (CoT y ReAct) se adaptan a diferentes estilos
y contextos culturales.

Uso:
    from common.coqueteo_personas import (
        get_persona_romantico_clasico,
        get_persona_moderno_carismatico,
        get_persona_culto_misterioso
    )

    perfil = get_persona_romantico_clasico()
"""

from typing import TypedDict, List


class PersonaLatino(TypedDict):
    """Estructura de datos para un perfil Latino completo."""
    tipo_persona: str
    gustos: List[str]
    estilo: str
    contexto: str
    estrategias: List[str]
    pais_origen: str
    edad_aproximada: str
    red_flags: List[str]


def get_persona_romantico_clasico() -> PersonaLatino:
    """
    Galan latino clasico, poetico y caballeroso.

    Este arquetipo representa el estilo tradicional de cortejo latino:
    elegancia vintage, lenguaje florido pero sincero, referencias culturales
    clasicas (boleros, poesia, galanteria).

    Returns:
        PersonaLatino: Perfil completo del Romantico Clasico

    Example:
        >>> perfil = get_persona_romantico_clasico()
        >>> print(perfil["tipo_persona"])
        'galan latino clasico, poetico y caballeroso'
    """
    return PersonaLatino(
        tipo_persona="galan latino clasico, poetico y caballeroso",
        gustos=[
            "boleros de Los Panchos y Trio San Javier",
            "caminatas al atardecer por el malecon",
            "escribir cartas a mano con pluma fuente",
            "recitar poesia de Neruda, Benedetti y Sabines",
            "flores frescas (rosas rojas, no arreglos comerciales)",
            "restaurantes con musica en vivo (no cadenas)"
        ],
        estilo="romantico tradicional, lenguaje florido pero sincero, nunca invasivo",
        contexto=(
            "Quiere cautivar con elegancia vintage y respeto profundo. "
            "Busca conexion emocional genuina antes que atraccion superficial. "
            "Valora la paciencia y el cortejo progresivo."
        ),
        estrategias=[
            "metaforas poeticas sutiles (no cursi ni exagerado)",
            "referencias culturales latinas (musica, literatura, cine clasico)",
            "lenguaje corporal respetuoso (nunca invasivo ni posesivo)",
            "timing de cumplidos (gradual, no abrumar en primer mensaje)",
            "usar 'usted' inicialmente, transicionar a 'tu' con permiso",
            "invitaciones concretas pero romanticas (concierto, museo, lectura de poesia)"
        ],
        pais_origen="Mexico",
        edad_aproximada="35-45",
        red_flags=[
            "parecer desactualizado o fuera de contexto con generacion actual",
            "exceso de formalidad que crea distancia",
            "ser predecible (siempre flores rojas, siempre Neruda)",
            "confundir romance con posesividad o celos",
            "ignorar senales de que ella prefiere estilo mas casual"
        ]
    )


def get_persona_moderno_carismatico() -> PersonaLatino:
    """
    Latino urbano, carismatico y autentico.

    Este arquetipo representa el latino contemporaneo: adaptado a la cultura
    digital, bilingue, con humor inteligente y vulnerabilidad calibrada.
    Busca autenticidad sobre perfeccion.

    Returns:
        PersonaLatino: Perfil completo del Moderno Carismatico

    Example:
        >>> perfil = get_persona_moderno_carismatico()
        >>> print(perfil["pais_origen"])
        'Colombia'
    """
    return PersonaLatino(
        tipo_persona="latino urbano, carismatico y autentico",
        gustos=[
            "salsa en vivo los viernes (clubes especificos, no genericos)",
            "street art latinoamericano (grafiti con mensaje)",
            "cafes con wifi donde trabajar (nomada digital)",
            "reggaeton viejo (nostalgia de 2000s, no urbano generico actual)",
            "podcasts en espanol sobre emprendimiento y cultura",
            "fusion food (tacos coreanos, ceviche japones)"
        ],
        estilo="casual pero intencional, humor inteligente, nunca forzado",
        contexto=(
            "Match en app de citas. Quiere destacar en mar de perfiles genericos "
            "sin sonar desesperado ni try-hard. Busca conexion genuina pero sabe "
            "que el primer mensaje es critico. Bilingue natural (Spanglish)."
        ),
        estrategias=[
            "humor autoironico latino (reirse de uno mismo, no de otros)",
            "referencias pop culture bilingue (memes, series, musica actual)",
            "vulnerabilidad calibrada (autentico pero no debil ni dramatico)",
            "invitaciones especificas (no vagas tipo 'salir algun dia')",
            "usar Spanglish estrategicamente (crear intimidad cultural)",
            "preguntas abiertas sobre pasiones (no interrogatorio)",
            "emoji usage moderado (no spam, no corazones en primer mensaje)"
        ],
        pais_origen="Colombia",
        edad_aproximada="28-35",
        red_flags=[
            "tratar demasiado duro (parecer desesperado)",
            "usar cliches ('reina', 'mami', 'preciosa' en primer mensaje)",
            "ser generico (perfil podria ser de cualquier persona)",
            "code-switching forzado (Spanglish que no suena natural)",
            "hablar solo de si mismo sin hacer preguntas",
            "proponer salir demasiado rapido (antes de conexion basica)"
        ]
    )


def get_persona_culto_misterioso() -> PersonaLatino:
    """
    Intelectual latino con aire enigmatico.

    Este arquetipo representa el latino culto: selectivo, profundo, con
    referencias intelectuales y culturales. Busca conexion mental antes
    que fisica. Crea intriga mediante revelation gradual.

    Returns:
        PersonaLatino: Perfil completo del Culto Misterioso

    Example:
        >>> perfil = get_persona_culto_misterioso()
        >>> print(perfil["edad_aproximada"])
        '32-42'
    """
    return PersonaLatino(
        tipo_persona="intelectual latino con aire enigmatico",
        gustos=[
            "cine de autor latinoamericano (Inarritu, Cuaron, Martel)",
            "jazz experimental y fusion latina (no mainstream)",
            "librerias de viejo (buscar primeras ediciones)",
            "vino tinto en tertulias filosoficas",
            "fotografia analogica (preferencia por blanco y negro)",
            "literatura latinoamericana (Borges, Cortazar, Bolano)"
        ],
        estilo="profundo, selectivo, revela poco a poco, nunca pretencioso",
        contexto=(
            "Busca conexion intelectual antes que atraccion fisica inmediata. "
            "Es selectivo con quien invierte tiempo. Prefiere conversaciones "
            "sustanciales sobre small talk. Crea misterio intencionalmente."
        ),
        estrategias=[
            "preguntas filosoficas sutiles (no pretencioso ni pedante)",
            "silencios estrategicos (crear intriga, no responder inmediato)",
            "recomendaciones culturales como anzuelo (libros, peliculas, musica)",
            "crear misterio (no revelar todo en primer mensaje)",
            "referencias intelectuales accesibles (no oscuras ni elitistas)",
            "invitaciones culturales especificas (exposicion, obra teatro, lectura)",
            "escribir mensajes mas largos que promedio (densidad de ideas)"
        ],
        pais_origen="Argentina",
        edad_aproximada="32-42",
        red_flags=[
            "parecer snob o elitista (alejar en vez de atraer)",
            "ser demasiado serio (sin humor ni ligereza)",
            "intimidar con referencias oscuras",
            "asumir superioridad intelectual",
            "ignorar sus intereses si no son 'cultos'",
            "crear distancia emocional (frio, distante, inaccesible)"
        ]
    )


def get_all_personas() -> dict[str, PersonaLatino]:
    """
    Obtiene todas las personas Latino disponibles.

    Returns:
        dict: Diccionario con keys: 'romantico', 'moderno', 'culto'

    Example:
        >>> personas = get_all_personas()
        >>> for nombre, perfil in personas.items():
        ...     print(f"{nombre}: {perfil['pais_origen']}")
        romantico: Mexico
        moderno: Colombia
        culto: Argentina
    """
    return {
        "romantico": get_persona_romantico_clasico(),
        "moderno": get_persona_moderno_carismatico(),
        "culto": get_persona_culto_misterioso()
    }


# Ejemplos de perfiles de match (targets) para combinar con personas
def get_match_cientifica_aventurera() -> dict:
    """
    Perfil de match: cientifica con espiritu aventurero.

    Este es un perfil de ejemplo que puede ser usado como "match" para
    demostrar como cada persona Latino abordaria el mismo target.
    """
    return {
        "nombre": "Ana",
        "edad": 32,
        "profesion": "Neurocientifica",
        "intereses": [
            "escalada en roca los fines de semana",
            "documentales de naturaleza",
            "cocina fusion (experimenta con recetas)",
            "yoga y meditacion",
            "viajar a lugares remotos"
        ],
        "personalidad": "curiosa, independiente, valora autenticidad",
        "bio_app": (
            "Cientifica de dia, aventurera de fin de semana. "
            "Busco alguien que pueda hablar de neuroplasticidad "
            "y tambien armar una carpa bajo las estrellas."
        ),
        "lo_que_busca": "conexion intelectual + espiritu aventurero",
        "red_flags_para_ella": [
            "machismo disfrazado de caballerosidad",
            "falta de ambicion o pasion",
            "no respetar su independencia"
        ]
    }


def get_match_arquitecta_artistica() -> dict:
    """
    Perfil de match: arquitecta con sensibilidad artistica.

    Otro perfil de ejemplo para demostrar adaptacion de estrategias.
    """
    return {
        "nombre": "Sofia",
        "edad": 29,
        "profesion": "Arquitecta especializada en diseno sustentable",
        "intereses": [
            "exposiciones de arte contemporaneo",
            "fotografia urbana",
            "cafes especiales (coffee snob admitida)",
            "arquitectura brutalista",
            "musica electronica y techno"
        ],
        "personalidad": "creativa, perfeccionista, introvertida selectiva",
        "bio_app": (
            "Diseno espacios que respiran. "
            "Adicta al cafe, a las lineas limpias y a las conversaciones profundas. "
            "Si sabes la diferencia entre Bauhaus y Art Deco, ya tienes puntos."
        ),
        "lo_que_busca": "alguien con criterio estetico + profundidad",
        "red_flags_para_ella": [
            "falta de sensibilidad estetica",
            "conversaciones superficiales",
            "no valorar su tiempo (introvertida)"
        ]
    }

'''
Workflow for prompt chaining in AI engineering (Interactive Version).
Objetivo : Construir un marco referencial interactivo donde la IA 
           solicita contexto humano para refinar la estrategia.
Release Date : 2026-02-10
'''

import os
import argparse
import logging
import json
from dotenv import load_dotenv
from openai import OpenAI

#========================================#
# -----        logger Design       ----- #
#========================================#
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s")

logger = logging.getLogger()

#========================================#
# ----- load environment variables ----- #
#========================================#
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    logger.warning("No se encontró la variable OPENAI_API_KEY en el entorno.")

client = OpenAI(api_key=api_key)

#===========================================
#          Agent Configuration             #
#===========================================

def call_api(system_prompt, user_prompt, temp, model="gpt-4o-mini", json_mode=False):
    """
    Llama a la API. Si json_mode es True, fuerza la salida en formato JSON.
    """
    try:
        response_format = {"type": "json_object"} if json_mode else {"type": "text"}
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temp,
            response_format=response_format
        )
        return response.choices[0].message.content

    except Exception as e:
        logger.error(f"Critical API Error: {e}")
        return None

#======================================================
#     Definición de agentes especialistas  
#======================================================

def agente_entrevistador(topic):
    """
    Analiza el topic y genera preguntas clave para el usuario.
    Retorna una lista de preguntas.
    """
    system_prompt = """
    Eres un estratega de relaciones humanas. Tu objetivo es leer una descripción 
    y generar EXACTAMENTE 3 preguntas clave para entender mejor el contexto.
    
    Responde SIEMPRE en formato JSON:
    {
        "preguntas": ["pregunta 1", "pregunta 2", "pregunta 3"]
    }
    """
    user_prompt = f"El perfil inicial es: {topic}. ¿Qué necesito saber para proceder?"
    
    logger.info("Agente Entrevistador: Generando preguntas...")
    response_json = call_api(system_prompt, user_prompt, temp=0.7, json_mode=True)
    
    try:
        data = json.loads(response_json)
        return data['preguntas']
    except (json.JSONDecodeError, KeyError):
        logger.warning("Error parseando JSON, usando preguntas por defecto.")
        return ["¿Edad?", "¿Hobbies principales?", "¿Personalidad?"]


def agente_estrategia(contexto_completo):
    """
    Define la estrategia de comunicación basada en el contexto enriquecido.
    """
    system_prompt = """
    Eres un experto en comunicación estratégica.
    Analiza el perfil completo y define:
    1. Tono emocional (ej: formal, humorístico, directo).
    2. Puntos clave a abordar.
    3. Estructura del mensaje sugerida.
    """
    user_prompt = f"Perfil detallado:\n{contexto_completo}\n\nDefine la estrategia."
    
    logger.info("Agente Estrategia: Definiendo abordaje...")
    response = call_api(system_prompt, user_prompt, temp=0.5)
    return response


def agente_poeta(estrategia):
    """
    Genera un componente creativo/lírico basado en la estrategia.
    """
    system_prompt = """
    Eres un redactor creativo. Basado en la estrategia, crea una frase 
    o metáfora breve e impactante que sirva de gancho emocional.
    """
    user_prompt = f"Estrategia: {estrategia}. Genera el gancho creativo."
    
    logger.info("Agente Poeta: Creando contenido creativo...")
    response = call_api(system_prompt, user_prompt, temp=0.8)
    return response


def agente_redactor_final(contexto, estrategia, componente_creativo):
    """
    Ensambla el mensaje final.
    """
    system_prompt = """
    Eres un redactor profesional. Tu misión es redactar el mensaje final 
    integrando el contexto del usuario, la estrategia definida y el componente creativo.
    El mensaje debe parecer natural y humano.
    """
    user_prompt = f"""
    CONTEXTO: {contexto}
    ESTRATEGIA: {estrategia}
    CREATIVIDAD: {componente_creativo}
    
    Redacta el mensaje final.
    """
    logger.info("Agente Redactor: Ensamblando mensaje...")
    response = call_api(system_prompt, user_prompt, temp=0.7)
    return response


def agente_verificador(mensaje):
    """
    Evalúa la calidad del mensaje.
    """
    system_prompt = """
    Actúa como control de calidad. Evalúa el mensaje del 1 al 10 
    basado en claridad, respeto y efectividad.
    """
    user_prompt = f"Evalúa este mensaje: {mensaje}"
    
    logger.info("Agente Verificador: Auditando...")
    response = call_api(system_prompt, user_prompt, temp=0.2)
    return response

#=============================================================
#            Workflow Interactivo      
#=============================================================

def main(topic):
    logger.info("INICIO DEL WORKFLOW")
    
    # 1. Fase de descubrimiento
    print(f"\n[SISTEMA]: Analizando objetivo '{topic}'...")
    preguntas = agente_entrevistador(topic)
    
    # 2. Interacción Humana
    respuestas_usuario = []
    print("\n[SISTEMA]: Por favor responda las siguientes preguntas para mejorar el contexto:")
    
    for i, pregunta in enumerate(preguntas, 1):
        print(f"\n{i}. {pregunta}")
        try:
            respuesta = input("   >> Respuesta: ")
            respuestas_usuario.append(f"P: {pregunta} | R: {respuesta}")
        except KeyboardInterrupt:
            print("\n[SISTEMA]: Entrada cancelada por usuario.")
            return None
    
    # Contexto enriquecido
    contexto_enriquecido = f"Perfil base: {topic}\n" + "\n".join(respuestas_usuario)
    
    # 3. Estrategia
    estrategia = agente_estrategia(contexto_enriquecido)
    
    # 4. Creatividad
    poema = agente_poeta(estrategia)
    
    # 5. Redacción
    mensaje_final = agente_redactor_final(contexto_enriquecido, estrategia, poema)
    
    # 6. Verificación
    score = agente_verificador(mensaje_final)
    
    logger.info("Workflow finalizado correctamente")
    
    return {
        "estrategia": estrategia,
        "mensaje_final": mensaje_final,
        "calidad": score
    } 


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Workflow de Generación de Mensajes con IA")
    
    parser.add_argument(
        '-t', '--topic', 
        type=str, 
        required=True, 
        help='Descripción inicial del objetivo'
    )

    args = parser.parse_args()
    
    try:
        resultado = main(args.topic)
        
        if resultado:
            print("\n" + "="*60)
            print("REPORTE DE EJECUCION")
            print("="*60)
            
            print(f"\n[ESTRATEGIA]:\n{resultado['estrategia']}")
            print("-" * 30)
            print(f"\n[MENSAJE FINAL]:\n{resultado['mensaje_final']}")
            print("-" * 30)
            print(f"\n[CALIDAD]:\n{resultado['calidad']}")
            print("="*60)
            
    except Exception as e:
        logger.error(f"Error en la ejecución principal: {e}")
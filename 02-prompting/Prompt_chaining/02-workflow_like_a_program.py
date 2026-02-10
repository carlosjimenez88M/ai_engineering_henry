'''
Workflow for prompt chaining in AI engineering.
Objetivo : Construir un marco referencial en el cual se pueda desplegar 
           este tipo de arquitectura modular
Release Date : 2026-02-10
'''


#===================#
#     libraries     # 
#===================#

import os
import argparse  # <--- Librería para argumentos de terminal
import logging
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

def call_api(system_prompt, 
             user_prompt, 
             temp, 
             model="gpt-4o-mini"):
    """
    Realiza la llamada a la API de OpenAI con manejo de errores.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temp,
        )
        return response.choices[0].message.content

    except Exception as e:
        logger.warning(f"Fallo en la llamada a la API: {e}")
        return "Error: No se pudo generar contenido debido a una falla en la API."


#======================================================
#     Definición de agentes especialistas  
#======================================================

def agente_coqueton(topic):
    system_prompt = """
                   Eres un experto en coqueteo, muy latino y gracioso, eres una especie de combinación entre el 'Zorro' y 'Don Juan', vas a ayudar a encantar
                   a una persona basado en lo siguiente que debes preguntar:
                   # Descripción sobre la personalidad de la persona
                   # Gustos conocidos
                   # Qué cosas no le gustan 
                    """
    user_prompt = f"La persona a encantar es {topic} "
    logger.info("Agente Coquetón : Recibiendo información sobre la persona a encantar")
    
    response = call_api(system_prompt, user_prompt, temp=0.2) 
    
    logger.info("Agente Coquetón : Información procesada")
    return response


def agente_poeta(topic):
    system_prompt = """
                   Eres un poeta romántico, tu tarea es crear un poema de amor basado en la información que te voy a dar sobre una persona, 
                   debes usar un lenguaje muy romántico y apasionado, el poema debe ser corto pero muy impactante.
                    """
    user_prompt = f"La información sobre la persona es : {topic} "
    logger.info("Agente Poeta : Recibiendo información procesada por el agente coquetón")
    
    response = call_api(system_prompt, user_prompt, temp=0.2)
    
    logger.info("Agente Poeta : Poema generado")
    return response


def agente_redactor_de_mensaje(topic, poema):
    system_prompt = """
                   Eres un redactor de mensajes experto en amor, tu tarea es crear un mensaje de texto para conquistar a una persona, 
                   el mensaje debe ser corto pero muy impactante.
                    """
    user_prompt = f"La información sobre la persona es : {topic} , el poema que se ha generado es : {poema} "
    logger.info("Agente Redactor : Recibiendo info y poema")
    
    response = call_api(system_prompt, user_prompt, temp=0.2)
    
    logger.info("Agente Redactor de Mensaje : Mensaje generado")
    return response


def agente_verificador(mensaje):
    system_prompt = """
                   Vas a verificar que el mensaje sea respetuoso. Otorga un score de 1 a 10.
                    """
    user_prompt = f"El mensaje a evaluar es : {mensaje} "
    logger.info("Agente Verificador : Analizando el mensaje")
    
    response = call_api(system_prompt, user_prompt, temp=0.2)
    
    logger.info("Agente Verificador : Evaluación realizada")
    return response


#=============================================================
#            Workflow de los agentes especialistas.      
#=============================================================

def main(topic):
    logger.info(f"Workflow iniciado para el topic: {topic}")
    
    # Paso 1
    info_coqueton = agente_coqueton(topic)
    
    # Paso 2 (Si falla el anterior, este recibirá el mensaje de error, pero el flujo sigue)
    poema = agente_poeta(info_coqueton)
    
    # Paso 3
    mensaje = agente_redactor_de_mensaje(info_coqueton, poema)
    
    # Paso 4
    verificacion = agente_verificador(mensaje)
    
    logger.info("Workflow finalizado")
    
    return {
        "info_coqueton": info_coqueton,
        "poema": poema,
        "mensaje": mensaje,
        "verificacion": verificacion
    } 


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ejecuta el workflow de Agentes de IA para generar mensajes románticos.")
    parser.add_argument(
        '-t', '--topic', 
        type=str, 
        required=True, 
        help='Descripción de la persona o situación para el agente (e.g., "Le gusta el rock y el café")'
    )

    args = parser.parse_args()

    # Ejecución
    resultado = main(args.topic)
    
    # Impresión limpia del resultado
    print("\n" + "="*50)
    print("RESULTADO DEL WORKFLOW")
    print("="*50)
    for k, v in resultado.items():
        print(f"\n--- {k.upper()} ---\n{v}")
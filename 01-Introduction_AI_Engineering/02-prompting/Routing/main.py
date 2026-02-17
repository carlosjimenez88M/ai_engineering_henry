'''
Workflow with Routing Pattern for AI Engineering.
Objetivo: Implementar un 'Router' que decide dinámicamente qué flujo de trabajo
          ejecutar según la intención del usuario (Seducción, Disculpa, Casual).
Release Date: 2026-02-10
'''
#===================#
#     libraries     # 
#===================#

import os
import argparse
import logging
import json
from dotenv import load_dotenv
from openai import OpenAI

#========================================#
# -----        Configuración       ----- #
#========================================#
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s")

logger = logging.getLogger()

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#===========================================
#          Motor de LLM Genérico           #
#===========================================

def call_api(system_prompt, 
             user_prompt, temp=0.2, 
             json_mode=False):
    try:
        response_format = {"type": "json_object"} if json_mode else {"type": "text"}
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temp,
            response_format=response_format
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error en API: {e}")
        return None

#======================================================
#     COMPONENTE 1: EL ROUTER (El Cerebro)
#======================================================

def agente_router(topic):
    """
    Analiza la entrada y clasifica la intención en una de tres categorías.
    """
    system_prompt = """
    Eres un clasificador de intenciones. Tu única tarea es leer el input del usuario
    y categorizarlo en UNA de las siguientes rutas:
    
    1. "RECONCILIACION": Si el usuario quiere pedir perdón, arreglar una pelea o volver con un ex.
    2. "CASUAL": Si el usuario quiere proponer una salida tranquila, un café, algo sin presión o humorístico.
    3. "ROMANTICO": Si el usuario quiere declarar amor profundo, usar poemas o ser intenso.
    
    Responde estricamente en JSON: {"ruta": "NOMBRE_RUTA", "razon": "breve explicacion"}
    """
    
    logger.info(f"Router: Analizando intención de '{topic}'...")
    response = call_api(system_prompt, topic, temp=0.0, json_mode=True)
    
    try:
        data = json.loads(response)
        return data.get("ruta", "CASUAL") # Default a Casual si falla
    except:
        logger.error("Fallo en router, usando ruta por defecto.")
        return "CASUAL"

#======================================================
#     COMPONENTE 2: LOS ESPECIALISTAS (Las Ramas)
#======================================================

# --- RUTA A: RECONCILIACIÓN (Serio, empático) ---
def flujo_reconciliacion(topic):
    logger.info("--> Entrando en Flujo de Reconciliación")
    
    system_prompt = """
    Eres un mediador de conflictos experto y empático.
    Tu objetivo es redactar un mensaje para pedir disculpas o abrir el diálogo tras una pelea.
    REGLAS:
    - No uses chistes.
    - Asume responsabilidad (usa "Yo siento" en lugar de "Tú hiciste").
    - Sé breve y humilde.
    """
    mensaje = call_api(system_prompt, f"Contexto del conflicto: {topic}", temp=0.3)
    return mensaje

# --- RUTA B: CASUAL (Divertido, directo) ---
def flujo_casual(topic):
    logger.info("--> Entrando en Flujo Casual")
    
    system_prompt = """
    Eres un amigo 'cool' y relajado.
    Tu objetivo es escribir un mensaje para invitar a alguien a salir o romper el hielo.
    REGLAS:
    - Usa humor ligero.
    - Cero intensidad.
    - Debe parecer espontáneo.
    """
    mensaje = call_api(system_prompt, f"Contexto de la persona: {topic}", temp=0.8)
    return mensaje

# --- RUTA C: ROMÁNTICO (El flujo complejo original) ---
def flujo_romantico(topic):
    logger.info("--> Entrando en Flujo Romántico Intenso")
    
    # Paso 1: Generar Poema
    sys_poeta = "Eres un poeta apasionado. Escribe 2 versos impactantes sobre este tema."
    poema = call_api(sys_poeta, topic, temp=0.9)
    
    # Paso 2: Integrar en carta
    sys_carta = "Escribe una breve carta de amor que incluya estos versos."
    carta = call_api(sys_carta, f"Tema: {topic}. Versos: {poema}", temp=0.7)
    
    return carta

#=============================================================
#            Main Controller (Orquestador)      
#=============================================================

def main(topic):
    # 1. El Router decide el camino
    ruta_seleccionada = agente_router(topic)
    logger.info(f"Router decidió: {ruta_seleccionada}")
    
    resultado = ""
    
    # 2. Switch Case (Lógica de Enrutamiento)
    if ruta_seleccionada == "RECONCILIACION":
        resultado = flujo_reconciliacion(topic)
        
    elif ruta_seleccionada == "ROMANTICO":
        resultado = flujo_romantico(topic)
        
    elif ruta_seleccionada == "CASUAL":
        resultado = flujo_casual(topic)
        
    else:
        # Fallback
        logger.warning("Ruta desconocida, ejecutando flujo casual.")
        resultado = flujo_casual(topic)
        
    return {
        "ruta": ruta_seleccionada,
        "mensaje": resultado
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Message Generator con Routing Pattern")
    
    parser.add_argument(
        '-t', '--topic', 
        type=str, 
        required=True, 
        help='Situación o descripción (ej: "Peleamos por dinero" o "Quiero invitarla al cine")'
    )

    args = parser.parse_args()
    
    print(f"\n[INPUT]: {args.topic}\n")
    
    final_output = main(args.topic)
    
    print("-" * 50)
    print(f"ESTRATEGIA SELECCIONADA: {final_output['ruta']}")
    print("-" * 50)
    print(f"MENSAJE GENERADO:\n{final_output['mensaje']}")
    print("-" * 50)
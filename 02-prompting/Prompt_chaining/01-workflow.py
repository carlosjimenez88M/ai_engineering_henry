'''
Workflow for prompt chaining in AI engineering.
Objetivo : Construir un marco referencial en el cual se pueda desplegar 
           este tipo de arquitectura  modular
Release Date : 2026-02-10
'''

#######################################################################################
#     Componente o definición principal       
#
# Se debe dividir la tarea en componentes pequeños y en pasos que sean fáciles de 
# manejar y entender por parte del LLM
#
# El core de esta estrategia es :
#   La entrada de cada noda es la salida del anterior 
#   Es útil para controlar la calidad de las respuestas 
#   Se puede versionar cada paso , lo cual es útil para debug
#######################################################################################

#===================#
#     libraries     # 
#===================#

import os 
from dotenv import load_dotenv
from openai import OpenAI
import logging


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
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#===========================================
#          Agent Configuration             #
#===========================================


def call_api(system_prompt, 
             user_prompt, 
             temp , 
             model="gpt-4.1-mini"):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=temp,
    )
    return response.choices[0].message.content


#======================================================
#     Definición de agentes especialistas  
#======================================================


def agente_coqueton(topic):
    system_prompt = """
                   Eres un experto en coqueteo , muy latino y gracioso, eres una especie de combinación entre el 'Zorro' y 'Don Juan', vas a ayudar a encantar
                   a una persona basado en lo siguiente que debes preguntar :
                   # Descripción sobre la personalidad de la mi enamorada
                   # Gustos conocidos
                   # Qué cosas no le gustan 
                    """
    user_prompt = f"La persona a encantar es {topic} "
    logger.info("Agente Coquetón : Recibiendo información sobre la persona a encantar")
    response = call_api(system_prompt, 
                        user_prompt, 
                        temp=0.2)
    logger.info("Agente Coquetón : Información procesada")
    return response


def agente_poeta(topic):
    system_prompt = """
                   Eres un poeta romántico , tu tarea es crear un poema de amor basado en la información que te voy a dar sobre una persona, 
                   debes usar un lenguaje muy romántico y apasionado, el poema debe ser corto pero muy impactante, 
                   debe transmitir emociones profundas y sinceras, el objetivo es conquistar el corazón de esa persona a través de tus palabras.
                    """
    user_prompt = f"La información sobre la persona es : {topic} "
    logger.info("Agente Poeta : Recibiendo información procesada por el agente coquetón")
    response = call_api(system_prompt, 
                        user_prompt, 
                        temp=0.2)
    logger.info("Agente Poeta : Poema generado")
    return response


def quitale_cursileria(poema):
    system_prompt = """
                  Vas a recibir un poema, resulta que los poemas ya no se usan ni se leen con el ritmo que tienen
                  por lo tanto vas a cambiar la forma de como esta escrito para buscar frases impactantes
                  algo como : tienes unos labios cosmopolitas
                    """
    user_prompt = f"El poema a transformar es : {poema}"
    logger.info("Agente Quitale Cursileria : Recibiendo poema generado por el agente poeta")
    response = call_api(system_prompt, 
                        user_prompt, 
                        temp=0.5)
    logger.info("Agente Quitale Cursileria : Poema transformado")
    return response


def agente_redactor_de_mensaje(topic, poema):
    system_prompt = """
                   Eres un redactor de mensajes experto en amor, tu tarea es crear un mensaje de texto para conquistar a una persona, 
                   el mensaje debe ser corto pero muy impactante, debe transmitir emociones profundas y sinceras, el objetivo es conquistar el corazón de esa persona a través de tus palabras.
                    """
    user_prompt = f"La información sobre la persona es : {topic} , el poema que se ha generado es : {poema} "
    logger.info("Agente Redactor de Mensaje : Recibiendo información procesada por el agente coquetón y el poema generado por el agente poeta")
    response = call_api(system_prompt, 
                        user_prompt, 
                        temp=0.2)
    logger.info("Agente Redactor de Mensaje : Mensaje generado")
    return response



def agente_verificador(mensaje):
    system_prompt = """
                   Vas a verificar que el mensaje que se esta enviando es respetuoso y va acorde con el objetivo de conquistar a una persona, o sea no 
                   se desemboca en un mensaje ofensivo o irrespetuoso, tu tarea es evaluar el mensaje y decir si es adecuado o no, si no es adecuado debes sugerir cambios para que sea adecuado,
                   si es adecuado debes decir que el mensaje es adecuado y no necesita cambios, tu respuesta debe. Tambien otorgaras uin score de 1 a 10 sobre la calidad del mensaje
                    """
    user_prompt = f"El mensaje a evaluar es : {mensaje} "
    logger.info("Agente Verificador : Recibiendo mensaje generado por el agente redactor de mensaje")
    response = call_api(system_prompt, 
                        user_prompt, 
                        temp=0.2)
    logger.info("Agente Verificador : Evaluación realizada")
    return response



#=============================================================
#            Workflow de los agentes especialistas.      
#=============================================================

def main(topic):
    logger.info("Workflow iniciado")
    info_coqueton = agente_coqueton(topic)
    poema = agente_poeta(info_coqueton)
    se_realista = quitale_cursileria(poema)
    mensaje = agente_redactor_de_mensaje(info_coqueton, se_realista)
    verificacion = agente_verificador(mensaje)
    logger.info("Workflow finalizado")
    return {
        "info_coqueton": info_coqueton,
        "poema": poema,
        "se_realista": se_realista,
        "mensaje": mensaje,
        "verificacion": verificacion
    } 



if __name__ == "__main__":
    topic = "Una ingeniera de software que le gusta estudiar AI y le gusta el café , su hobbie es la ingenieria de contexto"
    resultado = main(topic)
    print(resultado)



'''
Workflow with LangGraph & LangSmith Integration.
Objetivo: Implementar un grafo de estado con trazabilidad completa 
          en LangSmith para depuracion y observabilidad.
Release Date: 2026-02-10
'''

#===================#
#     libraries     # 
#===================#
import os
import argparse
import logging
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv

#========================================#
# -----      Logger Configuration    ----#
#========================================#

class ColoredFormatter(logging.Formatter):
    # Codigos ANSI para colores en terminal (sin emojis)
    GREEN = "\x1b[32;20m"
    YELLOW = "\x1b[33;20m"
    RED = "\x1b[31;20m"
    RESET = "\x1b[0m"
    format_str = "%(asctime)s - %(levelname)s - %(message)s"

    FORMATS = {
        logging.INFO: GREEN + format_str + RESET,
        logging.WARNING: YELLOW + format_str + RESET,
        logging.ERROR: RED + format_str + RESET,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt='%H:%M:%S')
        return formatter.format(record)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setFormatter(ColoredFormatter())
logger.addHandler(ch)

#========================================#
# -----     Load Environment         ----#
#========================================#

load_dotenv()

# 1. Verificacion de OpenAI
if not os.getenv("OPENAI_API_KEY"):
    logger.error("Falta OPENAI_API_KEY. El script fallara.")

# 2. Verificacion de LangSmith
langchain_api_key = os.getenv("LANGCHAIN_API_KEY")
tracing_v2 = os.getenv("LANGCHAIN_TRACING_V2")

if langchain_api_key and tracing_v2 == "true":
    project_name = os.getenv("LANGCHAIN_PROJECT", "default")
    logger.info(f"[OK] LangSmith Activado | Proyecto: {project_name}")
    logger.info("Los trazas se enviaran a: https://smith.langchain.com")
else:
    logger.warning("[!] LangSmith NO esta configurado. No veras graficos en la web.")


# Inicializamos el modelo
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

#========================================#
# 1. Definir el Estado
#========================================#
class AgentState(TypedDict):
    topic: str
    category: str
    final_message: str

#========================================#
# 2. Nodos
#========================================#

def router_node(state: AgentState):
    topic = state["topic"]
    logger.info(f"[ROUTER] Analizando: {topic}")
    
    prompt = f"""
    Clasifica la intencion en una de estas categorias:
    - RECONCILIACION
    - CASUAL
    - ROMANTICO
    
    Responde SOLO con la categoria en mayusculas.
    Texto: {topic}
    """
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        category = response.content.strip().upper()
        
        # Validacion simple
        validas = ["RECONCILIACION", "CASUAL", "ROMANTICO"]
        if category not in validas:
            # Fallback seguro
            category = "CASUAL"
        
        logger.info(f"[ROUTER] Ruta seleccionada -> {category}")
        return {"category": category}
    except Exception as e:
        logger.error(f"Error en Router: {e}")
        return {"category": "CASUAL"}

def specialist_reconciliacion(state: AgentState):
    logger.info("[AGENT] Ejecutando especialista: Reconciliacion")
    res = llm.invoke(f"Escribe una disculpa sincera para: {state['topic']}")
    return {"final_message": res.content}

def specialist_casual(state: AgentState):
    logger.info("[AGENT] Ejecutando especialista: Casual")
    res = llm.invoke(f"Escribe una invitacion divertida para: {state['topic']}")
    return {"final_message": res.content}

def specialist_romantico(state: AgentState):
    logger.info("[AGENT] Ejecutando especialista: Romantico")
    res = llm.invoke(f"Escribe un poema de amor corto sobre: {state['topic']}")
    return {"final_message": res.content}

#========================================#
# 3. Logica de Enrutamiento
#========================================#

def route_decision(state: AgentState) -> Literal["node_reconciliacion", "node_casual", "node_romantico"]:
    mapping = {
        "RECONCILIACION": "node_reconciliacion",
        "CASUAL": "node_casual",
        "ROMANTICO": "node_romantico"
    }
    return mapping.get(state["category"], "node_casual")

#========================================#
# 4. Grafo
#========================================#

def build_graph():
    workflow = StateGraph(AgentState)

    # Nodos
    workflow.add_node("router", router_node)
    workflow.add_node("node_reconciliacion", specialist_reconciliacion)
    workflow.add_node("node_casual", specialist_casual)
    workflow.add_node("node_romantico", specialist_romantico)

    # Entrada
    workflow.set_entry_point("router")

    # Aristas condicionales
    workflow.add_conditional_edges(
        "router",
        route_decision,
        {
            "node_reconciliacion": "node_reconciliacion",
            "node_casual": "node_casual",
            "node_romantico": "node_romantico"
        }
    )

    # Salida
    workflow.add_edge("node_reconciliacion", END)
    workflow.add_edge("node_casual", END)
    workflow.add_edge("node_romantico", END)

    return workflow.compile()

#========================================#
# Main
#========================================#

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LangGraph + LangSmith Agent")
    parser.add_argument('-t', '--topic', type=str, required=True, help='Situacion')
    args = parser.parse_args()

    try:
        app = build_graph()
        
        print("-" * 50)
        print(f"INICIANDO PROCESO PARA: '{args.topic}'")
        print("-" * 50)

        # Ejecucion con trazabilidad automatica de LangSmith
        result = app.invoke({"topic": args.topic})

        print(f"CLASIFICACION: {result['category']}")
        print(f"RESPUESTA:\n{result['final_message']}")
        print("-" * 50)

    except Exception as e:
        logger.error(f"Error critico: {e}")

#python adv_main.py -t "Quiero decirle que la amo con locura"
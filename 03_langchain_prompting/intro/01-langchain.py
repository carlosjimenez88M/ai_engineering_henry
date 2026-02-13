"""
     Buscador especializado de criticas de cine
release date : 2026-02-12
"""

########################
# ---- libraries ----- #
########################

import os
import argparse
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

##################
# -- load env -- #
##################

load_dotenv()

#########################
# --- Support FUcntion
#########################


@tool
def search(query: str) -> str:
    """Busca información en internet sobre el query proporcionado."""
    print(f"Esto es lo que estoy buscando {query}")
    return "Buscando información relevante..."


########################
# --- Agent Design
########################

llm = ChatOpenAI(
    model="gpt-5.2", temperature=0.00003  # Entre mas dificil sea la division
)

tools = [search]


agent = create_agent(llm, tools)


##############################
# --- main program
##############################


def main():
    parser = argparse.ArgumentParser(
        description="Necesito que le pasen un topic para que esta cosa busque algo en internet"
    )

    parser.add_argument(
        "-q",
        "--question",
        type=str,
        default=None,
    )
    args = parser.parse_args()

    if not args.question:
        print("Error: Debes proporcionar una pregunta usando -q o --question")
        return

    question = args.question
    result = agent.invoke({"messages": [HumanMessage(content=question)]})
    final_answer = result["messages"][-1]
    print("==" * 64)
    print(final_answer.content)
    print("==" * 64)


if __name__ == "__main__":
    main()

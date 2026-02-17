"""ReAct LangChain Notebooks module."""
import importlib.util
import sys
from pathlib import Path

_current_dir = Path(__file__).parent

# Load 01_react_langchain_avanzado
_spec1 = importlib.util.spec_from_file_location(
    "react_langchain_avanzado",
    _current_dir / "01_react_langchain_avanzado.py"
)
react_langchain_avanzado = importlib.util.module_from_spec(_spec1)
sys.modules["ReAct_LangChain.Notebooks.react_langchain_avanzado"] = react_langchain_avanzado
_spec1.loader.exec_module(react_langchain_avanzado)

# Load 02_react_langgraph
_spec2 = importlib.util.spec_from_file_location(
    "react_langgraph_02",
    _current_dir / "02_react_langgraph.py"
)
react_langgraph_02 = importlib.util.module_from_spec(_spec2)
sys.modules["ReAct_LangChain.Notebooks.react_langgraph_02"] = react_langgraph_02
_spec2.loader.exec_module(react_langgraph_02)

__all__ = ["react_langchain_avanzado", "react_langgraph_02"]

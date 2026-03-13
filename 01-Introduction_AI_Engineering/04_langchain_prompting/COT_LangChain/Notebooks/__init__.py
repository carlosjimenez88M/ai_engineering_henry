"""
__init__.py

Objetivo del script: 
COT LangChain Notebooks module.

Copyright 2026 Henry Academy.
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import importlib.util
import sys
from pathlib import Path

_current_dir = Path(__file__).parent

# Load 01_cot_langchain_avanzado
_spec1 = importlib.util.spec_from_file_location(
    "cot_langchain_avanzado",
    _current_dir / "01_cot_langchain_avanzado.py"
)
cot_langchain_avanzado = importlib.util.module_from_spec(_spec1)
sys.modules["COT_LangChain.Notebooks.cot_langchain_avanzado"] = cot_langchain_avanzado
_spec1.loader.exec_module(cot_langchain_avanzado)

# Load 02_cot_langgraph
_spec2 = importlib.util.spec_from_file_location(
    "cot_langgraph_02",
    _current_dir / "02_cot_langgraph.py"
)
cot_langgraph_02 = importlib.util.module_from_spec(_spec2)
sys.modules["COT_LangChain.Notebooks.cot_langgraph_02"] = cot_langgraph_02
_spec2.loader.exec_module(cot_langgraph_02)

__all__ = ["cot_langchain_avanzado", "cot_langgraph_02"]

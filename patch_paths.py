"""
patch_paths.py

Objetivo del script: 
Script description goes here.

Copyright 2026 Henry Academy.
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import os

REPLACEMENTS = {
    # 01 module
    "01_introduction/02_ai_engineering": "01_introduction/02_ai_engineering",
    "01_introduction/01_python_software_engineering": "01_introduction/01_python_software_engineering",
    "01_introduction": "01_introduction",
    "02_prompting": "02_prompting",
    "05_rags": "05_rags",
    "00_python_extra_class": "00_00_python_extra_class",
    "01_prompt_introduction": "01_prompt_introduction",
    "02_prompt_chaining": "02_prompt_chaining",
    "03_routing": "03_routing",
    "04_cot/": "04_cot/",
    "05_react/": "05_react/",
    "00_common/": "00_00_common/",
    "00_tools/": "00_00_tools/",
    "03_routing/01_main.py": "03_routing/01_main.py",
    "03_routing/02_adv_main.py": "03_routing/02_adv_main.py",
    
    # 02 module
    "01_intro/": "01_01_intro/",
    "02_databases/": "02_02_databases/",
    "03_rag/": "03_rag/",
    "04_batman_vector_db_orchestration/": "04_04_batman_vector_db_orchestration/",
    "02_rag_tfidf.ipynb": "02_rag_tfidf.ipynb",
    "03_transformers.ipynb": "03_transformers.ipynb",
    "04_text_classification.ipynb": "04_text_classification.ipynb",
    "05_rags_vectorial_databases.ipynb": "05_rags_vectorial_databases.ipynb",
    "01_tokens.ipynb": "01_tokens.ipynb",
    
    # 03 module
    "02_langchain/": "02_02_langchain/",
    "03_multi_agent/": "03_multi_agent/",
    "04_production/": "04_04_production/",
    "05_llmops/": "05_llmops/",
    "00_data/": "00_00_data/",
    "99_tests/": "99_99_tests/",
    "01_que_es_un_agente.ipynb": "01_que_es_un_agente.ipynb",
    "02_workflows_vs_agentes.ipynb": "02_workflows_vs_agentes.ipynb",
    "03_costo_latencia_alucinacion.ipynb": "03_costo_latencia_alucinacion.ipynb",
    "01_tool_calling.ipynb": "01_tool_calling.ipynb",
    "02_routing_condicional.ipynb": "02_routing_condicional.ipynb",
    "03_validacion_salida.ipynb": "03_validacion_salida.ipynb",
    "04_rag_agentico.ipynb": "04_rag_agentico.ipynb",
    "05_flujo_agentico_completo.ipynb": "05_flujo_agentico_completo.ipynb",
    "01_orquestador_workers.ipynb": "01_orquestador_workers.ipynb",
    "02_handoffs.ipynb": "02_handoffs.ipynb",
    "03_resolucion_conflictos.ipynb": "03_resolucion_conflictos.ipynb",
    "01_timeouts_retries.ipynb": "01_timeouts_retries.ipynb",
    "02_fallback_guardrails.ipynb": "02_fallback_guardrails.ipynb",
    "03_presupuesto_costos.ipynb": "03_presupuesto_costos.ipynb",
    "04_alertas_calidad.ipynb": "04_alertas_calidad.ipynb",
}

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return
        
    new_content = content
    for old, new in REPLACEMENTS.items():
        new_content = new_content.replace(old, new)
        
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath}")

def main():
    base_dir = "/Users/carlosdaniel/Documents/Projects/Laborales/Henry/2026/01_introduction_ai_engineering/ai_engineering_henry"
    for root, dirs, files in os.walk(base_dir):
        if '.git' in root or '.venv' in root or '__pycache__' in root:
            continue
        for file in files:
            if file.endswith('.py') or file.endswith('.ipynb') or file.endswith('.toml') or file.endswith('.md') or file == 'Makefile':
                filepath = os.path.join(root, file)
                process_file(filepath)

if __name__ == "__main__":
    main()

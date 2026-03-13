"""
__init__.py

Objetivo del script: 
Multi-agent routing + RAG skeleton using LangChain.

Copyright 2026 Henry Academy.
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from .pipeline import MultiAgentService, build_multi_agent_pipeline, build_multi_agent_service

__all__ = ["MultiAgentService", "build_multi_agent_pipeline", "build_multi_agent_service"]

"""
synthesizer.py

Objetivo del script: 
Synthesizer node: produces the final CulturalResponse.

Copyright 2026 Henry Academy.
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import annotations

from typing import Any

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, SystemMessage

from cinematic_intelligence.models import CulturalResponse, DomainEnum
from cinematic_intelligence.state import CulturalState

SYNTHESIZER_SYSTEM_PROMPT = """You are the final response synthesizer for a Cultural Intelligence system.
Your role is to take the specialist's analysis and produce a clear, engaging, and well-structured final response.

Guidelines:
- Present information in a natural, conversational but knowledgeable tone
- Include specific titles, dates, and technical details when relevant
- Connect the analysis to broader cultural significance when appropriate
- Keep responses focused and avoid unnecessary repetition
- Write in the same language as the user's query"""


def build_synthesizer_node(llm: BaseChatModel):
    """Factory that returns a LangGraph node for response synthesis."""
    structured_llm = llm.with_structured_output(CulturalResponse)

    def synthesizer_node(state: CulturalState) -> dict[str, Any]:
        """Synthesize the specialist analysis into a final response."""
        messages = state["messages"]
        domain = state.get("domain", DomainEnum.GENERAL)
        domain_result = state.get("domain_result", {})
        original_query = messages[0].content if messages else ""

        context = f"""Domain: {domain}
Original query: {original_query}
Specialist analysis: {domain_result}"""

        try:
            response: CulturalResponse = structured_llm.invoke(
                [
                    SystemMessage(content=SYNTHESIZER_SYSTEM_PROMPT),
                    *messages,
                    AIMessage(content=context),
                ]
            )
            return {
                "final_response": response,
                "messages": [AIMessage(content=response.final_answer)],
            }
        except Exception:
            # Fallback: use last AI message as final answer
            last_ai_content = ""
            for msg in reversed(messages):
                if isinstance(msg, AIMessage):
                    last_ai_content = msg.content
                    break

            fallback = CulturalResponse(
                domain=domain or DomainEnum.GENERAL,
                query=original_query,
                final_answer=last_ai_content or "No response generated.",
            )
            return {"final_response": fallback}

    return synthesizer_node

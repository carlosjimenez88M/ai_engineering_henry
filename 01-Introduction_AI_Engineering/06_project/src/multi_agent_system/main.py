"""
main.py

Objetivo del script: 
CLI entrypoint for the multi-agent routing demo.

Copyright 2026 Henry Academy.
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import annotations

import argparse
import json

from .config import load_settings
from .pipeline import build_multi_agent_service



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run multi-agent intent routing + RAG")
    parser.add_argument("--query", required=True, help="User query to route")
    parser.add_argument("--conversation-id", default="cli-session", help="Optional conversation id")
    parser.add_argument(
        "--use-heuristic-router",
        action="store_true",
        help="Use keyword-based intent router instead of LLM classifier.",
    )
    parser.add_argument(
        "--hide-debug",
        action="store_true",
        help="Do not print debug metadata in output.",
    )
    return parser.parse_args()



def main() -> None:
    args = parse_args()
    settings = load_settings()
    service = build_multi_agent_service(settings, use_heuristic_router=args.use_heuristic_router)

    result = service.ask(args.query, conversation_id=args.conversation_id)
    payload = result.model_dump()
    if args.hide_debug:
        payload.pop("debug", None)
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

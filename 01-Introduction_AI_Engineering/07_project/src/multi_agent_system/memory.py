"""
memory.py

Objetivo del script: 
Lightweight in-memory conversation store.

This keeps recent user turns to help intent disambiguation.
Replace with Redis/Postgres in production.

Copyright 2026 Henry Academy.
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass, field


@dataclass
class InMemoryConversationStore:
    max_history_turns: int = 4
    _store: dict[str, deque[str]] = field(default_factory=lambda: defaultdict(deque))

    def append_user_turn(self, conversation_id: str, query: str) -> None:
        history = self._store[conversation_id]
        history.append(query.strip())
        while len(history) > self.max_history_turns:
            history.popleft()

    def get_history(self, conversation_id: str) -> list[str]:
        return list(self._store[conversation_id])

    def clear(self, conversation_id: str) -> None:
        if conversation_id in self._store:
            del self._store[conversation_id]

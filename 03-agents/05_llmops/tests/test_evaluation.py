"""
test_evaluation.py

Objetivo del script: 
Script description goes here.

Copyright 2026 Henry Academy.
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from __future__ import annotations

from llmops.evaluation import run_evaluation
from llmops.models import Prediction, TicketExample, UsageStats


def _ticket(ticket_id: str, route: str, priority: str) -> TicketExample:
    return TicketExample(
        id=ticket_id,
        customer_message="demo",
        expected_route=route,
        expected_priority=priority,
    )


def _prediction(ticket_id: str, route: str, priority: str) -> Prediction:
    return Prediction(
        ticket_id=ticket_id,
        route=route,
        priority=priority,
        answer_es="ok",
        model="gpt-5-mini",
        latency_ms=10.0,
        usage=UsageStats(input_tokens=10, output_tokens=10, total_tokens=20),
        raw_output="{}",
    )


def test_run_evaluation_without_judge() -> None:
    dataset = [_ticket("A", "billing", "P1"), _ticket("B", "technical", "P2")]
    predictions = [_prediction("A", "billing", "P1"), _prediction("B", "billing", "P2")]

    report = run_evaluation(
        dataset=dataset,
        predictions=predictions,
        model="gpt-5-mini",
        judge=None,
    )

    assert report.summary.total_tickets == 2
    assert report.summary.route_accuracy == 0.5
    assert report.summary.priority_accuracy == 1.0
    assert report.summary.avg_judge_score is None


class StubJudge:
    def score(self, ticket: TicketExample, prediction: Prediction):  # noqa: ANN201, ARG002
        class Result:
            score = 4
            rationale = "Buena respuesta"

        return Result()


def test_run_evaluation_with_stub_judge() -> None:
    dataset = [_ticket("A", "billing", "P1")]
    predictions = [_prediction("A", "billing", "P1")]

    report = run_evaluation(
        dataset=dataset,
        predictions=predictions,
        model="gpt-5-mini",
        judge=StubJudge(),
    )

    assert report.summary.total_tickets == 1
    assert report.summary.route_accuracy == 1.0
    assert report.summary.priority_accuracy == 1.0
    assert report.summary.avg_judge_score == 4.0

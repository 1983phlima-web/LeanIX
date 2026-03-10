import pytest

from app.domain.models import ClaimType, QueryAnswer, SourceRef, SourceType
from app.domain.policies import PolicyEngine, PolicyError


def test_policy_accepts_answer_with_sources() -> None:
    engine = PolicyEngine()
    answer = QueryAnswer(
        answer="ok",
        sources=[SourceRef(type=SourceType.LEANIX_FACTSHEET, id="1", name="App A")],
        confidence=0.9,
        claim_type=ClaimType.FACT,
    )
    validated = engine.validate_answer(answer)
    assert validated.answer == "ok"


def test_policy_rejects_answer_without_sources() -> None:
    engine = PolicyEngine()
    answer = QueryAnswer(answer="sem fontes", sources=[], confidence=0.9, claim_type=ClaimType.FACT)
    with pytest.raises(PolicyError):
        engine.validate_answer(answer)

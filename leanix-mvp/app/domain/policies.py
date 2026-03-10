from app.domain.models import ClaimType, QueryAnswer


class PolicyError(ValueError):
    pass


class PolicyEngine:
    def validate_answer(self, answer: QueryAnswer) -> QueryAnswer:
        if not answer.sources:
            raise PolicyError("Resposta sem fontes é bloqueada pela política.")
        if answer.claim_type == ClaimType.FACT and answer.confidence < 0.3:
            raise PolicyError("Confiança baixa demais para classificar a saída como fato.")
        return answer

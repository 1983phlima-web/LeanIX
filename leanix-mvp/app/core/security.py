from fastapi import HTTPException, status


def ensure_suggest_mode_allowed(is_enabled: bool) -> None:
    if not is_enabled:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Suggest mode está desabilitado por feature flag.",
        )

from __future__ import annotations


class UseCaseError(Exception):
    """Base error for application use-cases."""


class NotFoundError(UseCaseError):
    """Requested entity not found."""


class ForbiddenError(UseCaseError):
    """Operation is not allowed for current user/context."""


class ValidationError(UseCaseError):
    """Input data is invalid."""

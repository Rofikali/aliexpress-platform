from core.domains.accounts.adapters.outbound.persistence.repositories.user_repository import (
    UserRepository,
)


def forget_user(user_id):
    repo = UserRepository()
    user = repo.get(user_id)
    user.anonymize()
    repo.save(user)

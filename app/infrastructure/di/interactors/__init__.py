from .organization import OrganizationInteractorProvider


def get_interactor_providers():
    return [
        OrganizationInteractorProvider(),
    ]

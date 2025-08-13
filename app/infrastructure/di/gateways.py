from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.interfaces.adapters.organization import OrganizationGateway
from app.infrastructure.db.gateways.organization import OrganizationDbGateway


class GatewayProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def get_organization_gateway(
        self, session: AsyncSession,
    ) -> OrganizationGateway:
        return OrganizationDbGateway(session=session)

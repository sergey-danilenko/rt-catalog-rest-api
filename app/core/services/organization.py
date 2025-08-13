import logging

from app.core.exception.exception import OrganizationAlreadyExists
from app.core.interfaces.adapters.organization import OrganizationGateway
from app.core.interfaces.uow import UoW
from app.core.models import dto
from app.core.common.intearctor import Interactor, InputDTO, OutputDTO

logger = logging.getLogger(__name__)


class OrganizationInteractor(Interactor[InputDTO, OutputDTO]):
    def __init__(self, uow: UoW, db_gateway: OrganizationGateway) -> None:
        self.uow = uow
        self.db_gateway = db_gateway


class GetOrgById(OrganizationInteractor[int, dto.Organization]):
    async def __call__(self, organization_id: int) -> dto.Organization:
        org = await self.db_gateway.get_by_id(organization_id)
        await self.uow.commit()
        return org


class GetOrgByName(OrganizationInteractor[str, dto.Organization]):
    async def __call__(
        self, name: str,
    ) -> dto.Organization:
        org = await self.db_gateway.get_by_name(name)
        await self.uow.commit()
        return org


class GetAllByBuildingId(OrganizationInteractor[int, list[dto.Organization]]):
    async def __call__(
        self, building_id: int,
    ) -> list[dto.Organization]:
        organizations = await self.db_gateway.get_all_by_building_id(
            building_id=building_id,
        )
        await self.uow.commit()
        return organizations


class GetAllByBuildingAddress(
    OrganizationInteractor[dto.AddressFilter, list[dto.Organization]]
):
    async def __call__(
        self, query: dto.AddressFilter,
    ) -> list[dto.Organization]:
        organizations = await self.db_gateway.get_all_by_building_address(
            query=query,
        )
        await self.uow.commit()
        return organizations


class GetAllByRadius(
    OrganizationInteractor[dto.GeoRadiusQuery, list[dto.Organization]]
):
    async def __call__(
        self, query: dto.GeoRadiusQuery,
    ) -> list[dto.Organization]:
        organizations = await self.db_gateway.get_all_by_radius(
            query=query,
        )
        await self.uow.commit()
        return organizations


class GetAllByRect(
    OrganizationInteractor[dto.GeoRectQuery, list[dto.Organization]]
):
    async def __call__(
        self, query: dto.GeoRectQuery,
    ) -> list[dto.Organization]:
        organizations = await self.db_gateway.get_all_by_rect(
            query=query,
        )
        await self.uow.commit()
        return organizations


class GetAllByActivityName(OrganizationInteractor[str, list[dto.Organization]]):
    async def __call__(
        self, activity_name: str,
    ) -> list[dto.Organization]:
        organizations = await self.db_gateway.get_all_by_activity_name(
            activity_name=activity_name,
        )
        await self.uow.commit()
        return organizations


class GetAllByActivityTree(
    OrganizationInteractor[dto.OrgActivityQuery, list[dto.Organization]],
):
    async def __call__(
        self, query: dto.OrgActivityQuery,
    ) -> list[dto.Organization]:
        organizations = await self.db_gateway.get_all_by_activity_tree(
            activity_name=query.activity_name,
            depth=query.depth,
        )
        await self.uow.commit()
        return organizations


class AddOrganization(OrganizationInteractor[dto.OrgCreate, dto.Organization]):
    async def __call__(
        self, organization: dto.OrgCreate,
    ) -> dto.Organization:
        try:
            org = await self.db_gateway.add_organization(
                organization=organization,
            )
            await self.uow.commit()
            return org
        except OrganizationAlreadyExists as e:
            await self.uow.rollback()
            logger.error(f"{e.notify}: %s", e)


class UpdateOrganization(
    OrganizationInteractor[dto.Organization, dto.Organization]
):
    async def __call__(
        self, organization: dto.Organization,
    ) -> dto.Organization:
        org = await self.db_gateway.update_organization(
            organization=organization,
        )
        await self.uow.commit()
        return org


class DeleteOrganization(OrganizationInteractor[int, bool]):
    async def __call__(self, organization_id: int) -> bool:
        org = await self.db_gateway.delete_organization(
            organization_id=organization_id,
        )
        await self.uow.commit()
        return org

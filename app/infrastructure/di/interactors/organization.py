from dishka import Provider, Scope, provide

from app.core.interfaces.adapters.organization import OrganizationGateway
from app.core.interfaces.uow import UoW
from app.core.services.organization import (
    GetOrgById,
    GetOrgByName,
    GetAllByBuildingId,
    GetAllByBuildingAddress,
    GetAllByRadius,
    GetAllByRect,
    GetAllByActivityName,
    GetAllByActivityTree,
    AddOrganization,
    UpdateOrganization,
    DeleteOrganization,
)


class OrganizationInteractorProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_by_id(
        self, uow: UoW, db_gateway: OrganizationGateway,
    ) -> GetOrgById:
        return GetOrgById(uow=uow, db_gateway=db_gateway)

    @provide
    def get_by_name(
        self, uow: UoW, db_gateway: OrganizationGateway,
    ) -> GetOrgByName:
        return GetOrgByName(uow=uow, db_gateway=db_gateway)

    @provide
    def get_all_by_building_id(
        self, uow: UoW, db_gateway: OrganizationGateway,
    ) -> GetAllByBuildingId:
        return GetAllByBuildingId(uow=uow, db_gateway=db_gateway)

    @provide
    def get_all_by_building_address(
        self, uow: UoW, db_gateway: OrganizationGateway,
    ) -> GetAllByBuildingAddress:
        return GetAllByBuildingAddress(uow=uow, db_gateway=db_gateway)

    @provide
    def get_all_by_radius(
        self, uow: UoW, db_gateway: OrganizationGateway,
    ) -> GetAllByRadius:
        return GetAllByRadius(uow=uow, db_gateway=db_gateway)

    @provide
    def get_all_by_rect(
        self, uow: UoW, db_gateway: OrganizationGateway,
    ) -> GetAllByRect:
        return GetAllByRect(uow=uow, db_gateway=db_gateway)

    @provide
    def get_all_by_activity_name(
        self, uow: UoW, db_gateway: OrganizationGateway,
    ) -> GetAllByActivityName:
        return GetAllByActivityName(uow=uow, db_gateway=db_gateway)

    @provide
    def get_all_by_activity_tree(
        self, uow: UoW, db_gateway: OrganizationGateway,
    ) -> GetAllByActivityTree:
        return GetAllByActivityTree(uow=uow, db_gateway=db_gateway)

    @provide
    def add_organization(
        self, uow: UoW, db_gateway: OrganizationGateway,
    ) -> AddOrganization:
        return AddOrganization(uow=uow, db_gateway=db_gateway)

    @provide
    def update_organization(
        self, uow: UoW, db_gateway: OrganizationGateway,
    ) -> UpdateOrganization:
        return UpdateOrganization(uow=uow, db_gateway=db_gateway)

    @provide
    def delete_organization(
        self, uow: UoW, db_gateway: OrganizationGateway,
    ) -> DeleteOrganization:
        return DeleteOrganization(uow=uow, db_gateway=db_gateway)

from abc import abstractmethod
from typing import Protocol

from app.core.models import dto


class OrganizationGateway(Protocol):
    @abstractmethod
    async def get_by_id(
        self, organization_id: int,
    ) -> dto.Organization:
        raise NotImplementedError

    @abstractmethod
    async def get_by_name(self, name: str) -> dto.Organization:
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_building_id(
        self, building_id: int,
    ) -> list[dto.Organization]:
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_building_address(
        self, query: dto.AddressFilter,
    ) -> list[dto.Organization]:
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_radius(
        self, query: dto.GeoRadiusQuery,
    ) -> list[dto.Organization]:
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_rect(
        self, query: dto.GeoRectQuery,
    ) -> list[dto.Organization]:
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_activity_name(
        self, activity_name: str,
    ) -> list[dto.Organization]:
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_activity_tree(
        self, activity_name: str, depth: int = 3,
    ) -> list[dto.Organization]:
        raise NotImplementedError

    @abstractmethod
    async def add_organization(
        self, organization: dto.OrgCreate,
    ) -> dto.Organization:
        raise NotImplementedError

    @abstractmethod
    async def update_organization(
        self, organization: dto.Organization,
    ) -> dto.Organization:
        raise NotImplementedError

    @abstractmethod
    async def delete_organization(self, organization_id: int) -> bool:
        raise NotImplementedError

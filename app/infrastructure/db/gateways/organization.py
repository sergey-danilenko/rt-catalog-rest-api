from sqlalchemy import update, select, func, literal
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased, selectinload, joinedload

from app.core.exception.exception import OrganizationAlreadyExists
from app.core.interfaces.adapters.organization import OrganizationGateway
from app.core.models import dto
from app.core.utils.geo import bounding_box, EARTH_RADIUS_KM
from app.infrastructure.db.gateways.base import BaseGateway
from app.infrastructure.db import models


class OrganizationDbGateway(
    BaseGateway[models.Organization], OrganizationGateway
):
    def __init__(self, session: AsyncSession):
        super().__init__(models.Organization, session)

    async def get_by_id(self, organization_id: int) -> dto.Organization:
        options = [
            joinedload(models.Organization.building),
            selectinload(models.Organization.activities),
            selectinload(models.Organization.phones),

        ]
        if org := await self._get_by_id(organization_id, options):
            return org.to_dto()

    async def get_by_name(self, name: str) -> dto.Organization:
        stmt = (
            select(models.Organization)
            .where(models.Organization.name == name)
        )
        org = (await self.session.scalars(stmt)).one_or_none()
        if org:
            return org.to_dto()

    async def get_all_by_building_id(
        self, building_id: int,
    ) -> list[dto.Organization]:
        stmt = (
            select(models.Organization)
            .where(models.Organization.building_id == building_id)
        )
        res = (await self.session.scalars(stmt)).all()
        return [org.to_dto() for org in res]

    async def get_all_by_building_address(
        self, query: dto.AddressFilter,
    ) -> list[dto.Organization]:
        stmt = select(models.Organization).join(models.Building)
        if city := query.city:
            stmt = stmt.where(models.Building.city.ilike(f'{city}%'))
        if street := query.street:
            stmt = stmt.where(models.Building.street.ilike(f'{street}%'))
        if house := query.house:
            stmt = stmt.where(models.Building.house == house)
        if office := query.office:
            stmt = stmt.where(models.Organization.office == office)

        res = (await self.session.scalars(stmt)).all()
        return [org.to_dto() for org in res]

    async def get_all_by_radius(
        self, query: dto.GeoRadiusQuery,
    ) -> list[dto.Organization]:

        lat_min, lon_min, lat_max, lon_max = bounding_box(
            query.center_lat, query.center_lon, query.radius
        )
        dist = _haversine_distance(query)
        stmt = (
            select(models.Organization)
            .join(models.Building)
            .where(models.Building.lat.between(lat_min, lat_max))
            .where(models.Building.lon.between(lon_min, lon_max))
            .where(dist <= query.radius)
        )
        res = (await self.session.scalars(stmt)).all()
        return [org.to_dto() for org in res]

    async def get_all_by_rect(
        self, query: dto.GeoRectQuery,
    ) -> list[dto.Organization]:
        stmt = (
            select(models.Organization)
            .join(models.Building)
            .where(
                models.Building.lat.between(query.lat_min, query.lat_max),
                models.Building.lon.between(query.lon_min, query.lon_max),
            )
        )
        res = (await self.session.scalars(stmt)).all()
        return [org.to_dto() for org in res]

    async def get_all_by_activity_name(
        self, activity_name: str,
    ) -> list[dto.Organization]:
        stmt = (
            select(models.Organization)
            .join(models.Organization.activities)
            .where(models.Activity.name.ilike(activity_name))
        )
        res = (await self.session.scalars(stmt)).all()
        return [org.to_dto() for org in res]

    async def get_all_by_activity_tree(
        self, activity_name: str, depth: int = 3,
    ) -> list[dto.Organization]:

        activity_alias = aliased(models.Activity)

        base = (
            select(models.Activity.id, literal(1).label("depth"))
            .where(models.Activity.name.ilike(activity_name))
        )
        cte = base.cte(name="activity_tree", recursive=True)

        recursive = (
            select(activity_alias.id, (cte.c.depth + 1).label("depth"))
            .where(activity_alias.parent_id == cte.c.id)
            .where(cte.c.depth < depth)
        )

        cte = cte.union_all(recursive)
        stmt = (
            select(models.Organization)
            .join(models.Organization.activities)
            .where(models.Activity.id.in_(select(cte.c.id)))
            .distinct()
        )

        res = (await self.session.scalars(stmt)).all()
        return [org.to_dto() for org in res]

    async def add_organization(
        self, organization: dto.OrgCreate,
    ) -> dto.Organization:
        org = models.Organization(
            name=organization.name,
            inn=organization.inn,
            building_id=organization.building_id,
            office=organization.office,
            phones=[models.PhoneNumber(number=p) for p in organization.phones],
            org_activities=[
                models.OrgActivity(activity_id=a)
                for a in organization.activities
            ]
        )
        self.session.add(org)
        try:
            await self.session.flush()
            return org.to_dto()
        except IntegrityError as e:
            raise OrganizationAlreadyExists(
                name=organization.name,
                inn=organization.inn,
                building_id=organization.building_id,
                office=organization.office,
            ) from e

    async def update_organization(
        self, organization: dto.Organization,
    ) -> dto.Organization:
        values = {"name": organization.name}
        if building_id := organization.building_id:
            values["building_id"] = building_id
        if office := organization.office:
            values["office"] = office
        stmt = (
            update(models.Organization)
            .where(models.Organization.id == organization.id)
            .values(**values)
            .returning(models.Organization)
        )
        org = (await self.session.scalars(stmt)).one_or_none()
        await self._flush()
        if org:
            return org.to_dto()

    async def delete_organization(
        self, organization_id: int,
    ) -> bool:
        org = await self._get_by_id(organization_id)
        if org:
            await self.session.delete(org)
        return org is not None


def _haversine_distance(query: dto.GeoRadiusQuery):
    lat1 = func.radians(query.center_lat)
    lon1 = func.radians(query.center_lon)
    lat2 = func.radians(models.Building.lat)
    lon2 = func.radians(models.Building.lon)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        func.sin(dlat / 2) * func.sin(dlat / 2)
        + func.cos(lat1) * func.cos(lat2) * func.sin(dlon / 2)
        * func.sin(dlon / 2)
    )
    c = 2 * func.atan2(func.sqrt(a), func.sqrt(1 - a))

    return EARTH_RADIUS_KM * c

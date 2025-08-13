from typing import Annotated

from dishka.integrations.fastapi import inject, FromDishka
from fastapi import APIRouter, Query, Path, HTTPException, status

from app.api.docs.responses import (
    UNAUTHORIZED_ERROR, VALIDATION_ERROR, NOT_FOUND_ERROR,
)
from app.core.models import dto
from app.core.services.organization import (
    GetOrgById,
    GetOrgByName,
    GetAllByBuildingId,
    GetAllByBuildingAddress,
    GetAllByRadius,
    GetAllByRect,
    GetAllByActivityName,
    GetAllByActivityTree,
)
from app.core.utils.str_cleaner import StrNormalizer, AddressCleaner


@inject
async def organization_by_id(
    id_: Annotated[int, Path(alias="id", description="ID организации")],
    interactor: FromDishka[GetOrgById],
) -> dto.Organization:
    """Получить организацию по её ID."""
    org = await interactor(id_)
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )
    return org


@inject
async def organization_by_name(
    interactor: FromDishka[GetOrgByName],
    normalizer: FromDishka[StrNormalizer],
    name: str = Query(
        ...,
        description="Название организации (полное)"
    ),
) -> dto.Organization:
    """Получить организацию по названию."""
    org = await interactor(normalizer.full_clean(name))
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )
    return org


@inject
async def organizations_by_building_id(
    id_: Annotated[int, Path(alias="id", description="ID здания")],
    interactor: FromDishka[GetAllByBuildingId],
) -> list[dto.Organization]:
    """Список организаций в заданном здании."""
    return await interactor(id_)


@inject
async def organizations_by_building_address(
    interactor: FromDishka[GetAllByBuildingAddress],
    cleaner: FromDishka[AddressCleaner],
    city: str | None = Query(default=None, description="Город"),
    street: str | None = Query(default=None, description="Улица"),
    house: str | None = Query(default=None, description="Дом"),
    office: str | None = Query(default=None, description="Офис"),
) -> list[dto.Organization]:
    """Список организаций по адресу здания."""
    query = dto.AddressFilter(
        city=cleaner.full_clean(city),
        street=cleaner.full_clean(street),
        house=cleaner.full_clean(house),
        office=cleaner.full_clean(office),
    )
    return await interactor(query)


@inject
async def organizations_by_radius(
    interactor: FromDishka[GetAllByRadius],
    center_lat: float = Query(..., description="Широта центра"),
    center_lon: float = Query(..., description="Долгота центра"),
    radius: float = Query(..., description="Радиус поиска в километрах"),
) -> list[dto.Organization]:
    """Список организаций в радиусе от точки."""
    query = dto.GeoRadiusQuery(
        center_lat=center_lat, center_lon=center_lon, radius=radius,
    )
    return await interactor(query)


@inject
async def organizations_by_rect(
    interactor: FromDishka[GetAllByRect],
    lat_min: float = Query(..., description="Минимальная широта"),
    lat_max: float = Query(..., description="Максимальная широта"),
    lon_min: float = Query(..., description="Минимальная долгота"),
    lon_max: float = Query(..., description="Максимальная долгота"),
) -> list[dto.Organization]:
    """Список организаций в прямоугольной области."""
    query = dto.GeoRectQuery(
        lat_min=lat_min, lat_max=lat_max, lon_min=lon_min, lon_max=lon_max,
    )
    return await interactor(query)


@inject
async def organizations_by_activity(
    interactor: FromDishka[GetAllByActivityName],
    normalizer: FromDishka[StrNormalizer],
    activity_name: str = Query(..., description="Название вида деятельности"),
) -> list[dto.Organization]:
    """Список организаций по виду деятельности."""
    return await interactor(normalizer.full_clean(activity_name))


@inject
async def organizations_by_activity_tree(
    interactor: FromDishka[GetAllByActivityTree],
    normalizer: FromDishka[StrNormalizer],
    activity_name: str = Query(..., description="Название вида деятельности"),
    depth: int = Query(
        default=3,
        ge=1,
        le=3,
        description="Глубина вложенности (максимум 3)"
    ),
) -> list[dto.Organization]:
    """Список организаций по виду деятельности с учетом вложенности."""
    query = dto.OrgActivityQuery(
        activity_name=normalizer.full_clean(activity_name),
        depth=depth,
    )
    return await interactor(query)


def setup() -> APIRouter:
    router = APIRouter(
        prefix="/api/org/v0",
        tags=["Organizations"],
        responses={**UNAUTHORIZED_ERROR, **VALIDATION_ERROR}
    )
    router.add_api_route(
        "/search/by-name/",
        organization_by_name,
        methods=["GET"],
        summary="Поиск организации по названию",
        description="Возвращает организацию по её названию.",
        response_model=dto.Organization,
        responses={**NOT_FOUND_ERROR},
    )
    router.add_api_route(
        "/building/address/",
        organizations_by_building_address,
        methods=["GET"],
        summary="Список всех организаций находящихся в конкретном здании по адресу здания",
        response_model=list[dto.Organization],
    )
    router.add_api_route(
        "/building/by-radius/",
        organizations_by_radius,
        methods=["GET"],
        summary="Список организаций в радиусе, относительно указанной точки на карте",
        response_model=list[dto.Organization],
    )
    router.add_api_route(
        "/building/by-rect/",
        organizations_by_rect,
        methods=["GET"],
        summary="Список организаций в прямоугольной области, относительно указанной точки на карте",
        response_model=list[dto.Organization],
    )
    router.add_api_route(
        "/activity/",
        organizations_by_activity,
        methods=["GET"],
        summary="Список всех организаций, которые относятся к указанному виду деятельности",
        response_model=list[dto.Organization],
    )
    router.add_api_route(
        "/activity/tree/",
        organizations_by_activity_tree,
        methods=["GET"],
        summary="Поиск организаций по виду деятельности",
        description="""
        Например, поиск по виду деятельности «Еда», которая находится на первом 
        уровне дерева, и чтобы нашлись все организации, которые относятся 
        к видам деятельности, лежащим внутри. 
        Т.е. в результатах поиска должны отобразиться организации 
        с видом деятельности Еда, Мясная продукция, Молочная продукция.
        
        Уровень вложенности деятельностей ограничен 3 уровням
        """,
        response_model=list[dto.Organization],
    )
    router.add_api_route(
        "/building/{id}/",
        organizations_by_building_id,
        methods=["GET"],
        summary="Список всех организаций находящихся в конкретном здании по ID здания",
        response_model=list[dto.Organization],
    )
    router.add_api_route(
        "/{id}/",
        organization_by_id,
        methods=["GET"],
        summary="Вывод информации об организации по её идентификатору",
        description="Возвращает полную информацию об организации по её идентификатору.",
        response_model=dto.Organization,
        responses={**NOT_FOUND_ERROR},
    )

    return router

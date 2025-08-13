import asyncio
import json
import random
from collections import defaultdict
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSession

from app.common.config import Config, Paths
from app.common.config import load_config
from app.common.config import get_paths
from app.core.models import dto
from app.infrastructure.db.factory import create_engine, create_session_maker
from app.infrastructure.db import models

random.seed(42)

paths: Paths = get_paths()
config: Config = load_config(paths)

if t := config.db.type == "sqlite":
    from sqlalchemy.dialects.sqlite import insert
elif t == "postgresql":
    from sqlalchemy.dialects.postgresql import insert
elif t == "mysql":
    from sqlalchemy.dialects.mysql import insert


def get_data(path: Path) -> dict | list:
    with open(paths.app_dir / "test_data" / path, "r", encoding="utf-8") as file:
        return json.loads(file.read())


async def fill_phones(
    session: AsyncSession, data: dict, org_map: dict,
) -> None:
    phones_data = []
    for org in data:
        org_id = org_map[org["name"]]
        for phone in org["phones"]:
            phones_data.append(
                {"number": phone, "organization_id": org_id},
            )

    phone_stmt = (
        insert(models.PhoneNumber)
        .values(phones_data)
        .on_conflict_do_nothing(index_elements=[models.PhoneNumber.number])
    )

    await session.execute(phone_stmt)


def _build_act_levels(
    activities: list[dto.Activity],
) -> dict[int, list[list[int]]]:
    children = defaultdict(list)
    roots = []
    for a in activities:
        (roots if a.parent_id is None else children[a.parent_id]).append(a.id)

    def walk(root) -> list[list[int]]:
        levels = []
        frontier = [root]
        while frontier:
            levels.append(frontier)
            next_frontier = []
            for n in frontier:
                next_frontier.extend(children[n])
            frontier = next_frontier
        return levels

    return {r: walk(r) for r in roots}


async def fill_org_activities(
    session: AsyncSession,
    activities: list[dto.Activity],
    org_map: dict[str, int],
) -> None:
    levels = _build_act_levels(activities)
    levels_keys = list(levels.keys())
    links = []
    for org_id in org_map.values():
        root_id = random.choice(levels_keys)
        chosen_acts = random.choice(levels[root_id])
        for act_id in chosen_acts:
            links.append(
                {
                    "organization_id": org_id,
                    "activity_id": act_id,
                }
            )

    stmt = (
        insert(models.OrgActivity)
        .values(links)
        .on_conflict_do_nothing(
            index_elements=[
                models.OrgActivity.organization_id,
                models.OrgActivity.activity_id,
            ]
        )
    )
    await session.execute(stmt)


async def fill_organizations(
    session: AsyncSession,
    buildings: list[dto.Building],
    activities: list[dto.Activity],
) -> None:
    data = get_data(Path("organization.json"))

    stmt = insert(models.Organization).values(
        [
            {
                "name": org["name"],
                "inn": org["inn"],
                "office": org["office_number"],
                "building_id": random.choice(buildings).id,
            } for org in data
        ]
    )
    stmt = stmt.on_conflict_do_update(
        index_elements=(models.Organization.inn,),
        set_={"name": stmt.excluded.name}
    ).returning(models.Organization)

    saved_orgs = (await session.scalars(stmt)).all()
    org_map = {o.name: o.id for o in saved_orgs}

    await fill_phones(session, data, org_map)
    await fill_org_activities(session, activities, org_map)


async def fill_buildings(session: AsyncSession) -> list[dto.Building]:
    data = get_data(Path("building.json"))

    stmt = insert(models.Building).values(data)
    stmt = stmt.on_conflict_do_update(
        index_elements=(
            models.Building.city,
            models.Building.street,
            models.Building.house,
        ),
        set_={
            "lat": stmt.excluded.lat,
            "lon": stmt.excluded.lon,
        }
    ).returning(models.Building)

    saved_buildings = (await session.scalars(stmt)).all()
    return [b.to_dto() for b in saved_buildings]


async def fill_activities(session: AsyncSession) -> list[dto.Activity]:
    added_activities: list[models.Activity] = []

    async def create_activities(data: dict,
                                parent: models.Activity | None = None):
        for name, children in data.items():
            stmt = insert(models.Activity).values(
                [
                    {
                        "name": name,
                        "parent_id": parent.id if parent else None,
                    },
                ]
            )
            stmt = stmt.on_conflict_do_update(
                index_elements=[models.Activity.name],
                set_={"parent_id": stmt.excluded.parent_id}
            ).returning(models.Activity)

            saved_activity = (await session.scalars(stmt)).first()
            added_activities.append(saved_activity)
            if isinstance(children, list):
                for item in children:
                    await create_activities(item, parent=saved_activity)

    await create_activities(
        get_data(Path("activities.json"))
    )
    return [a.to_dto() for a in added_activities]


async def main():
    engine: AsyncEngine = create_engine(config.db, echo=True)
    pool: async_sessionmaker[AsyncSession] = create_session_maker(engine)

    async with pool() as session:
        activities = await fill_activities(session)
        buildings = await fill_buildings(session)
        await fill_organizations(session, buildings, activities)
        await session.commit()


if __name__ == "__main__":
    asyncio.run(main())

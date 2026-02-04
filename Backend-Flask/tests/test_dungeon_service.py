import pytest
from pytest_mock import MockFixture
from sqlalchemy import exc

from utils.customexceptions import DatabaseError, DataNotFoundError, ServiceException
from service.DungeonService import (
    get_dungeons_all,
    get_dungeon_by_id_or_name,
    del_dungeon_by_id_or_name,
    add_dungeon,
)


def test_get_dungeons_all(mocker: MockFixture):
    mock_get_all = mocker.patch(
        "service.DungeonService.get_all_dugeons_db",
        return_value=[(1, "Deadmines"), (2, "Shadowfang")],
    )

    data = get_dungeons_all()
    assert mock_get_all.called
    assert isinstance(data, list)
    assert data == [
        {"id": 1, "dungeon": "Deadmines"},
        {"id": 2, "dungeon": "Shadowfang"},
    ]


def test_get_dungeons_all_db_error(mocker: MockFixture):
    mocker.patch(
        "service.DungeonService.get_all_dugeons_db",
        side_effect=exc.SQLAlchemyError("boom"),
    )

    with pytest.raises(DatabaseError):
        get_dungeons_all()


def test_get_dungeon_by_id_found(mocker: MockFixture):
    mocker.patch(
        "service.DungeonService.db_get_dungeon_by_id", return_value=(1, "Deadmines")
    )

    result = get_dungeon_by_id_or_name(1)
    assert result == {"id": 1, "dungeon": "Deadmines"}


def test_get_dungeon_by_name_found(mocker: MockFixture):
    mocker.patch(
        "service.DungeonService.db_get_dungeon_by_name",
        return_value=(2, "Shadowfang"),
    )

    result = get_dungeon_by_id_or_name("Shadowfang")
    assert result == {"id": 2, "dungeon": "Shadowfang"}


def test_get_dungeon_not_found(mocker: MockFixture):
    mocker.patch("service.DungeonService.db_get_dungeon_by_name", return_value=None)

    with pytest.raises(DataNotFoundError) as e:
        get_dungeon_by_id_or_name("NonExistentDungeon")

    assert str(e.value) == "No data found for the provided input NonExistentDungeon"


def test_del_dungeon_by_id_success(mocker: MockFixture):
    mocker.patch("service.DungeonService.db_del_dungeon_by_id", return_value=1)

    result = del_dungeon_by_id_or_name(2)
    assert result == 1


def test_del_dungeon_by_name_success(mocker: MockFixture):
    mocker.patch("service.DungeonService.db_del_dungeon_by_name", return_value=1)

    result = del_dungeon_by_id_or_name("SomeDungeon")
    assert result == 1


def test_del_dungeon_not_found_converted_to_service_exception(mocker: MockFixture):
    mocker.patch("service.DungeonService.db_del_dungeon_by_id", return_value=0)

    with pytest.raises(ServiceException) as e:
        del_dungeon_by_id_or_name(99)

    assert str(e.value) == "Failed to delete dungeon"


def test_del_dungeon_unknown_not_deletable():
    with pytest.raises(ServiceException) as e:
        del_dungeon_by_id_or_name(1)

    assert str(e.value) == "the dungeon 'Unknown' is not deletable"


def test_add_dungeon_success(mocker: MockFixture):
    mocker.patch("service.DungeonService.post_new_dungeon_db", return_value=(5,))

    res = add_dungeon("NewDungeon")
    assert res == {"id": 5, "dungeon": "NewDungeon"}


def test_add_dungeon_integrity_error_raises_value_error(mocker: MockFixture):
    mocker.patch(
        "service.DungeonService.post_new_dungeon_db",
        side_effect=exc.IntegrityError("stmt", "params", BaseException("duplicate")),
    )

    with pytest.raises(ValueError):
        add_dungeon("DuplicateDungeon")


def test_add_dungeon_database_error_passthrough(mocker: MockFixture):
    mocker.patch(
        "service.DungeonService.post_new_dungeon_db",
        side_effect=DatabaseError("db fail"),
    )

    with pytest.raises(DatabaseError):
        add_dungeon("Any")


def test_add_dungeon_sqlalchemy_error_converted(mocker: MockFixture):
    mocker.patch(
        "service.DungeonService.post_new_dungeon_db",
        side_effect=exc.SQLAlchemyError("boom"),
    )

    with pytest.raises(DatabaseError):
        add_dungeon("Any")


def test_add_dungeon_general_exception_converted(mocker: MockFixture):
    mocker.patch(
        "service.DungeonService.post_new_dungeon_db",
        side_effect=Exception("bang"),
    )

    with pytest.raises(ServiceException):
        add_dungeon("Any")

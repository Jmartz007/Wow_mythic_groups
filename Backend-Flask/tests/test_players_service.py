import pytest
from pytest_mock import MockFixture
import sqlalchemy
import sqlalchemy.exc

from utils.customexceptions import DataNotFoundError, DatabaseError

from service.PlayersService import (
    del_char,
    delete_player_by_id_or_name,
    get_all_chars_from_player,
    get_player_by_name,
    process_data_to_frontend,
    process_player_data,
)


def test_get_player_by_name(mocker: MockFixture):
    mock_find_player = mocker.patch(
        "service.PlayersService.db_find_player_by_name", return_value=(1, "TestPlayer")
    )
    player_data = get_player_by_name("TestPlayer")
    assert mock_find_player.called

    assert player_data == {"id": 1, "player name": "TestPlayer"}


def test_get_player_by_name_not_found(mocker: MockFixture):
    mock_find_player = mocker.patch(
        "service.PlayersService.db_find_player_by_name", return_value=None
    )

    with pytest.raises(DataNotFoundError) as e:
        get_player_by_name("NonExistentPlayer")
    mock_find_player.assert_called_once()
    assert str(e.value) == "No data found for the provided input NonExistentPlayer"


def test_get_player_by_name_db_error(mocker: MockFixture):
    mock_find_player = mocker.patch(
        "service.PlayersService.db_find_player_by_name",
        side_effect=sqlalchemy.exc.SQLAlchemyError("Database error"),
    )

    with pytest.raises(DatabaseError) as e:
        get_player_by_name("TestPlayer")
    mock_find_player.assert_called_once()


def test_delete_player_by_id_or_name(mocker: MockFixture):
    mock_find_player_id = mocker.patch(
        "service.PlayersService.db_find_player_id", return_value=(1, "TestPlayer")
    )
    mock_delete_player = mocker.patch(
        "service.PlayersService.delete_player_from_db", return_value=1
    )

    result = delete_player_by_id_or_name(1)
    assert mock_find_player_id.called
    assert mock_delete_player.called
    assert result == 1


def test_delete_player_by_id_or_name_by_name(mocker: MockFixture):
    mock_delete_player = mocker.patch(
        "service.PlayersService.delete_player_from_db", return_value=1
    )

    result = delete_player_by_id_or_name("TestPlayer")
    assert mock_delete_player.called
    assert result == 1


def test_delete_player_by_id_or_name_invalid_id(mocker: MockFixture):
    with pytest.raises(TypeError) as e:
        delete_player_by_id_or_name(3.14)  # type: ignore[arg-type]
    assert str(e.value) == "incorrect type"


def test_delete_player_by_id_or_name_int_not_found(mocker: MockFixture):
    mock_find_player_id = mocker.patch(
        "service.PlayersService.db_find_player_id", return_value=(None, None)
    )

    with pytest.raises(DataNotFoundError) as e:
        delete_player_by_id_or_name(9999)
    mock_find_player_id.assert_called_once()
    assert str(e.value) == "No data found for the provided input 9999"


def test_delete_player_by_id_or_name_str_not_found(mocker: MockFixture):
    mock_delete_player = mocker.patch(
        "service.PlayersService.delete_player_from_db", return_value=0
    )

    with pytest.raises(DataNotFoundError) as e:
        delete_player_by_id_or_name("NonExistentPlayer")
    mock_delete_player.assert_called_once_with("NonExistentPlayer")
    assert str(e.value) == "No data found for the provided input NonExistentPlayer"


def test_delete_player_by_id_or_name_db_error(mocker: MockFixture):
    mock_find_player_id = mocker.patch(
        "service.PlayersService.db_find_player_id",
        return_value=(1, "TestPlayer"),
    )
    mock_delete_player = mocker.patch(
        "service.PlayersService.delete_player_from_db",
        side_effect=sqlalchemy.exc.SQLAlchemyError("Database error"),
    )

    with pytest.raises(DatabaseError):
        delete_player_by_id_or_name(1)
    mock_find_player_id.assert_called_once()
    mock_delete_player.assert_called_once()


def test_get_all_chars_from_player(mocker: MockFixture):
    mock_rows = [
        ("TestPlayer", "Char1", "Mage", "DPS", "ranged", "high", "Deadmines", 10, True),
        (
            "TestPlayer",
            "Char1",
            "Mage",
            "Healer",
            "ranged",
            "high",
            "Deadmines",
            10,
            True,
        ),
        (
            "TestPlayer",
            "Char2",
            "Warrior",
            "Tank",
            "melee",
            "medium",
            "Blackrock",
            5,
            False,
        ),
    ]
    mock_get_chars = mocker.patch(
        "service.PlayersService.db_get_character_for_player",
        return_value=mock_rows,
    )

    chars = get_all_chars_from_player("TestPlayer")
    assert mock_get_chars.called
    assert chars == [
        {
            "character name": "Char1",
            "class": "Mage",
            "skill": "high",
            "party role": ["DPS", "Healer"],
            "ranged": "ranged",
            "dungeon": "Deadmines",
            "key level": 10,
            "active": True,
        },
        {
            "character name": "Char2",
            "class": "Warrior",
            "skill": "medium",
            "party role": ["Tank"],
            "ranged": "melee",
            "dungeon": "Blackrock",
            "key level": 5,
            "active": False,
        },
    ]


def test_get_all_chars_from_player_not_found(mocker: MockFixture):
    mock_get_chars = mocker.patch(
        "service.PlayersService.db_get_character_for_player",
        return_value=[],
    )

    with pytest.raises(DataNotFoundError) as e:
        get_all_chars_from_player("NonExistentPlayer")
    mock_get_chars.assert_called_once()
    assert str(e.value) == "No data found for the provided input NonExistentPlayer"


def test_get_all_chars_from_player_db_error(mocker: MockFixture):
    mock_get_chars = mocker.patch(
        "service.PlayersService.db_get_character_for_player",
        side_effect=sqlalchemy.exc.SQLAlchemyError("Database error"),
    )

    with pytest.raises(DatabaseError) as e:
        get_all_chars_from_player("TestPlayer")
    mock_get_chars.assert_called_once()


def test_del_char(mocker: MockFixture):
    mock_delete_char = mocker.patch(
        "service.PlayersService.delete_char_from_db", return_value=1
    )

    result = del_char("TestCharacter")
    assert mock_delete_char.called
    assert result == 1


def test_del_char_db_error(mocker: MockFixture):
    mock_delete_char = mocker.patch(
        "service.PlayersService.delete_char_from_db",
        side_effect=sqlalchemy.exc.SQLAlchemyError("Database error"),
    )

    with pytest.raises(DatabaseError):
        del_char("TestCharacter")
    mock_delete_char.assert_called_once()


def test_process_player_data(mocker: MockFixture):
    incoming = {
        "playerName": "TestPlayer",
        "characterName": "TestChar",
        "className": "Mage",
        "dungeon": "Deadmines",
        "roles": {
            "Tank": {"enabled": True, "combatRole": "MainTank", "skill": "high"},
            "Healer": {"enabled": False, "combatRole": "OffHeal", "skill": "low"},
            "DPS": {"enabled": True, "combatRole": "DPSRole", "skill": "medium"},
        },
    }

    expected_new_player = {
        "player_name": "TestPlayer",
        "character_name": "TestChar",
        "class_name": "Mage",
        "dungeon": "Deadmines",
        "combat_roles": {
            "combat_role_Tank": "MainTank",
            "TankSkill": "high",
            "combat_role_DPS": "DPSRole",
            "DPSSkill": "medium",
        },
        "role": ["tank", "dps"],
    }
    mock_player_entry = mocker.patch(
        "service.PlayersService.player_entry",
        return_value=True,
    )

    result = process_player_data(incoming)
    mock_player_entry.assert_called_once()
    called_kwargs = dict(mock_player_entry.call_args.kwargs)  # Create a mutable copy

    # Compare combat_roles by comparing sorted items
    expected_combat_roles = expected_new_player.pop("combat_roles")
    called_combat_roles = called_kwargs.pop("combat_roles")
    assert sorted(called_combat_roles.items()) == sorted(expected_combat_roles.items())

    # Compare roles list by converting to sets
    expected_roles = set(expected_new_player.pop("role"))
    called_roles = set(called_kwargs.pop("role"))
    assert called_roles == expected_roles

    # Compare the rest of the dictionary
    assert called_kwargs == expected_new_player
    assert result is True


def test_process_player_data_db_error(mocker: MockFixture):
    incoming = {
        "playerName": "TestPlayer",
        "characterName": "TestChar",
        "className": "Mage",
        "dungeon": "Deadmines",
        "roles": {
            "Tank": {"enabled": True, "combatRole": "MainTank", "skill": "high"},
        },
    }

    mock_player_entry = mocker.patch(
        "service.PlayersService.player_entry",
        side_effect=DatabaseError("Database error"),
    )

    with pytest.raises(DatabaseError) as e:
        process_player_data(incoming)
    mock_player_entry.assert_called_once()
    assert str(e.value) == "Database error"


def test_process_data_to_frontend(mocker: MockFixture):
    player_entries = [(1, "Player1")]
    char_entries = [
        ("Player1", "Char1", "Mage", "ranged", "high", "Deadmines", 10, True),
        ("Player1", "Char2", "Warrior", "melee", "medium", "Nexus", 5, False),
    ]
    role_entries = [
        ("Char1", "DPS", "Char1", "high"),
        ("Char1", "Healer", "Char1", "low"),
        ("Char2", "Tank", "Char2", "medium"),
    ]

    mock_get_all = mocker.patch(
        "service.PlayersService.get_all_players",
        return_value=(player_entries, char_entries, role_entries),
    )

    # Test nested output (default)
    expected_nested = {
        "Player1": {
            "Char1": {
                "Class": "Mage",
                "Range": "ranged",
                "Skill Level": "high",
                "Dungeon": "Deadmines",
                "Key Level": 10,
                "is_active": True,
                "Roles": [
                    {"Type": "DPS", "Skill": "high"},
                    {"Type": "Healer", "Skill": "low"},
                ],
            },
            "Char2": {
                "Class": "Warrior",
                "Range": "melee",
                "Skill Level": "medium",
                "Dungeon": "Nexus",
                "Key Level": 5,
                "is_active": False,
                "Roles": [
                    {"Type": "Tank", "Skill": "medium"},
                ],
            },
        }
    }
    result_nested = process_data_to_frontend()
    assert result_nested == expected_nested

    # Test flattened output
    expected_flattened = [
        {
            "Player": "Player1",
            "Character": "Char1",
            "Class": "Mage",
            "Dungeon": "Deadmines",
            "Key Level": 10,
            "Range": "ranged",
            "Role Type": ["DPS", "Healer"],
            "Role Skill": ["high", "low"],
            "Skill Level": "high",
            "Is Active": True,
        },
        {
            "Player": "Player1",
            "Character": "Char2",
            "Class": "Warrior",
            "Dungeon": "Nexus",
            "Key Level": 5,
            "Range": "melee",
            "Role Type": ["Tank"],
            "Role Skill": ["medium"],
            "Skill Level": "medium",
            "Is Active": False,
        },
    ]
    result_flattened = process_data_to_frontend(flattened=True)
    assert result_flattened == expected_flattened
    assert mock_get_all.call_count == 2


def test_process_data_to_frontend_db_error(mocker: MockFixture):
    mock_get_all = mocker.patch(
        "service.PlayersService.get_all_players",
        side_effect=sqlalchemy.exc.SQLAlchemyError("Database error"),
    )

    with pytest.raises(DatabaseError) as e:
        process_data_to_frontend()
    mock_get_all.assert_called_once()
    assert str(e.value) == "A database error occurred"

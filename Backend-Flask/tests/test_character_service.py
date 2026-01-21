import pytest
from pytest_mock import MockFixture
from utils.customexceptions import (
    CharacterNotFoundError,
    ServiceException,
    DataNotFoundError,
)
from service.CharacterService import (
    get_character_data,
    delete_character_service,
    update_character_key,
)


test_character = (
    1,
    "TestCharacter",
    "priest",
    "value3",
    "healer",
    "ranged",
    "medium",
    "Deadmines",
    7,
)

character_name = "TestCharacter"


def test_get_character_data(mocker: MockFixture):
    character_name = "TestCharacter"
    mock_get_char_name = mocker.patch(
        "service.CharacterService.db_find_character_by_name",
        return_value=(1, "TestCharacter"),
    )

    mock_get_char_info = mocker.patch(
        "service.CharacterService.db_get_all_info_for_character",
        return_value=[test_character],
    )

    data = get_character_data(character_name)
    assert mock_get_char_name.called
    assert mock_get_char_info.called
    assert isinstance(data, list)

    assert data == [
        {
            "character_name": "TestCharacter",
            "class_name": "priest",
            "party_role": "healer",
            "role_range_name": "ranged",
            "role_skill": "medium",
            "dungeon_name": "Deadmines",
            "level": 7,
        }
    ]


def test_get_character_data_not_found(mocker: MockFixture):
    mock_get_char_name = mocker.patch(
        "service.CharacterService.db_find_character_by_name", return_value=None
    )
    mock_get_all_info = mocker.patch(
        "service.CharacterService.db_get_all_info_for_character", return_value=[]
    )

    with pytest.raises(CharacterNotFoundError) as e:
        get_character_data("NonExistentCharacter")
    mock_get_char_name.assert_called_once()
    mock_get_all_info.assert_not_called()
    assert str(e.value) == "Character not found: NonExistentCharacter"


def test_delete_character_service(mocker: MockFixture):
    character_name = "TestCharacter"
    mock_delete_char = mocker.patch(
        "service.CharacterService.delete_char_from_db", return_value=1
    )

    result = delete_character_service(character_name)
    assert mock_delete_char.called
    assert result is True


def test_delete_character_service_not_found(mocker: MockFixture):
    mock_delete_char = mocker.patch(
        "service.CharacterService.delete_char_from_db", return_value=0
    )

    result = delete_character_service("NonExistentCharacter")
    assert mock_delete_char.called
    assert result is False


def test_update_character_key(mocker: MockFixture):
    character_name = "TestCharacter"
    data = {"Dungeon": "NewDungeon", "Key Level": 10}

    mock_update_key = mocker.patch(
        "service.CharacterService.db_udpate_key_data", return_value=1
    )

    result = update_character_key(character_name, data)

    assert mock_update_key.called
    assert result == 1


def test_update_character_key_not_found(mocker: MockFixture):
    data = {"Dungeon": "NonExistentDungeon", "Key Level": 10}

    mock_update = mocker.patch(
        "service.CharacterService.db_udpate_key_data", return_value=0
    )

    with pytest.raises(DataNotFoundError) as e:
        update_character_key("TestCharacter", data)
    mock_update.assert_called_once()
    assert str(e.value) == "Character or dungeon not found None"


def test_update_character_key_no_data(mocker: MockFixture):
    data = {}

    mock_update = mocker.patch(
        "service.CharacterService.db_udpate_key_data", return_value=1
    )

    with pytest.raises(ServiceException) as e:
        update_character_key("TestCharacter", data)
    mock_update.assert_not_called()
    assert str(e.value) == "Missing data to update"


def test_update_character_key_invalid_level(mocker: MockFixture):
    data = {"Key Level": -5}
    mock_update = mocker.patch(
        "service.CharacterService.db_udpate_key_data", return_value=0
    )

    with pytest.raises(ServiceException) as e:
        update_character_key("TestCharacter", data)
    mock_update.assert_not_called()
    assert str(e.value) == "Invalid Key number. Must be integer greater than 0"


def test_update_character_key_invalid_int(mocker: MockFixture):
    data = {"Key Level": "invalid"}
    mock_update = mocker.patch(
        "service.CharacterService.db_udpate_key_data", return_value=0
    )

    with pytest.raises(ServiceException) as e:
        update_character_key("TestCharacter", data)
    mock_update.assert_not_called()
    assert str(e.value) == "Invalid Key Number. Must be integer"

from pytest_mock import MockFixture
from service.CharacterService import get_character_data


test_character = (
    "TestCharacter",
    "priest",
    "healer",
    "ranged",
    "medium",
    "Deadmines",
    7,
)


def test_get_character_data(mocker: MockFixture):
    mock_get_char_name = mocker.patch(
        "service.CharacterService.db_find_character_by_name"
    )
    mock_get_char_info = mocker.patch(
        "service.CharacterService.db_get_all_info_for_character"
    )
    character_name = "TestCharacter"
    mock_get_char_name.return_value = (1, 42, "TestCharacter")
    mock_get_char_info.return_value = test_character

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

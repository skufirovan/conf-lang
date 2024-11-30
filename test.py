import pytest
import tempfile
import os
from main import parse_toml, is_valid_name, evaluate_expression, convert_to_custom_config, save_config

# Тестовые данные
toml_content = """# Comment 1
First_value = 10
Second_value = 20
Array = [1, 2, 3, 4]
# Comment 2
Expression_value = "^First_value + ^Second_value"
"""

expected_comments = [
    "Comment 1",
    None,
    None,
    None,
    "Comment 2",
    None
]

expected_output = """\
! Comment 1
First_value: 10;
Second_value: 20;
Array: array(1, 2, 3, 4);
! Comment 2
Expression_value: 30;
"""

@pytest.fixture
def create_toml_file():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".toml") as tmp:
        tmp.write(toml_content.encode('utf-8'))
        tmp_path = tmp.name
    yield tmp_path
    os.remove(tmp_path)

@pytest.fixture
def create_output_file():
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = tmp.name
    yield tmp_path
    os.remove(tmp_path)

def test_parse_toml(create_toml_file):
    parsed_data, comments = parse_toml(create_toml_file)
    assert parsed_data["First_value"] == 10
    assert parsed_data["Second_value"] == 20
    assert parsed_data["Array"] == [1, 2, 3, 4]
    assert parsed_data["Expression_value"] == "^First_value + ^Second_value"
    assert comments == expected_comments

def test_is_valid_name():
    assert is_valid_name("A") is True
    assert is_valid_name("_validName123") is True
    assert is_valid_name("1invalid") is False
    assert is_valid_name("invalid-name") is False

def test_evaluate_expression():
    constants = {"first_value": 10, "second_value": 20}
    result = evaluate_expression("^first_value + ^second_value", constants)
    assert result == 30

    with pytest.raises(ValueError):
        evaluate_expression("^undefined + 10", constants)

def test_convert_to_custom_config():
    data = {
        "First_value": 10,
        "Second_value": 20,
        "Array": [1, 2, 3, 4],
        "Expression_value": "^First_value + ^Second_value"
    }
    comments = expected_comments
    result = convert_to_custom_config(data, comments)
    assert result.strip() == expected_output.strip()

def test_save_config(create_output_file):
    test_content = "test content"
    save_config(create_output_file, test_content)
    with open(create_output_file, 'r') as file:
        assert file.read() == test_content

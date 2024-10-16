import subprocess


def test_extract():
    """Tests the extract function"""
    result = subprocess.run(
        ["python", "main.py", "extract"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.returncode == 0, "Extract command failed"
    assert "Extracting data..." in result.stdout


def test_transform_load():
    """Tests the transform and load function"""
    result = subprocess.run(
        ["python", "main.py", "transform_load"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.returncode == 0, "Transform and load command failed"
    assert "Transforming data..." in result.stdout


def test_query():
    """Tests the complex SQL"""
    result = subprocess.run(
        ["python", "main.py", "query_nutrition"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.returncode == 0, "SQL queries failed"
    assert "Querying data..." in result.stdout


if __name__ == "__main__":
    test_extract()
    test_transform_load()
    test_query()

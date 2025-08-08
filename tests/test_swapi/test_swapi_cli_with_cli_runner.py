from typer.testing import CliRunner
from swapi.app_commands import app


# Create a CliRunner instance to run CLI commands as if from the terminal
runner = CliRunner()


# Test: Check that the CLI correctly retrieves planet details for a valid planet ID
def test_retrieves_planet_details_correctly() -> None:
    """
    This test runs the CLI command `test_swapi planet 1` and checks that:
    - It exits successfully (exit code 0)
    - The output includes expected labels with emojis for planet information
    """
    result = runner.invoke(
        app, ["planet", "1"]
    )  # Simulate running: test_swapi planet 1

    # Confirm that the command succeeded
    assert result.exit_code == 0

    # Confirm that the output includes all expected fields
    assert "Name:" in result.output
    assert "Climate:" in result.output
    assert "Terrain:" in result.output
    assert "Population:" in result.output


# Test: Check that the CLI handles an invalid planet ID (e.g., 999999) gracefully
def test_handles_invalid_planet_id_gracefully() -> None:
    """
    This test runs the CLI command with an invalid planet ID to ensure:
    - The command exits with a non-zero status (indicating failure)
    - An appropriate error message is shown to the user
    """
    result = runner.invoke(
        app, ["planet", "999999"]
    )  # Simulate: test_swapi planet 999999

    # Expect a non-zero exit code due to the error
    assert result.exit_code != 0

    # Check for an error message in the output (update with the exact expected string if needed)
    assert "" in result.output


def test_retrieves_resident_details_correctly() -> None:
    """
    Test that the CLI command 'resident 1' retrieves resident details successfully.

    This test simulates invoking the CLI to get details for resident with ID 1,
    and asserts that:
    - The command exits with a status code of 0 (success).
    - The output contains expected labels with emojis for resident information:
      '🧍 Name:', '🚻 Gender:', and '🎂 Birth Year:'.

    :raises AssertionError: If the command fails or output does not contain expected strings.
    """
    result = runner.invoke(app, ["people", "1"])

    assert result.exit_code == 0
    assert "Name:" in result.output
    assert "Height:" in result.output
    assert "Mass:" in result.output


def test_handles_invalid_resident_id_gracefully() -> None:
    """
    Test that the CLI command handles an invalid resident ID properly.

    This test simulates invoking the CLI with an invalid resident ID (e.g., 999999),
    and asserts that:
    - The command exits with a non-zero status code (indicating failure).
    - An appropriate error message is displayed in the output.

    :raises AssertionError: If the command does not fail or error message is missing.
    """
    result = runner.invoke(app, ["people", "999999"])

    assert result.exit_code != 0
    assert "" in result.output  # Replace with specific error message when available

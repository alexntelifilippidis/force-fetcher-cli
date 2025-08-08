import requests
import typer
from colorama import Fore, init

from swapi.logger import get_logger

# Initialize colorama for colored terminal output
init(autoreset=True)

app = typer.Typer(
    help="Swapi CLI: Query Star Wars people, planets, and starships using https://swapi.info/"
)

BASE_URL = "https://swapi.info/api"
logger = None  # Will be initialized in the callback


@app.callback()
def main(
    debug: bool = typer.Option(False, "--debug", help="Enable debug logging"),
) -> None:
    """
    CLI entry point. Initializes the logger.

    :param debug: Enable debug logging, defaults to False
    """
    global logger
    logger = get_logger(__name__, debug=debug)


def fetch_data(endpoint: str, id: int) -> dict[str, object]:
    """
    Fetch data from the SWAPI API for a given endpoint and ID.

    :param endpoint: API endpoint to query (e.g., "people", "planets")
    :param id: ID of the resource to retrieve
    :return: Parsed JSON response from the API
    :rtype: dict
    :raises typer.Exit: If the request fails
    """
    url = f"{BASE_URL}/{endpoint}/{id}/"
    logger.debug(f"Fetching URL: {url}")  # type: ignore[union-attr]
    response = requests.get(url=url, timeout=30)
    success_status = 200
    if response.status_code == success_status:
        logger.debug(f"Successfully fetched {endpoint} id={id}")  # type: ignore[union-attr]
        return response.json()  # type: ignore[no-any-return]
    else:
        logger.error(  # type: ignore[union-attr]
            f"Error fetching {endpoint} id={id}: {response.status_code} - {response.reason}"
        )
        typer.secho(
            f"Error: {response.status_code} - {response.reason}", fg=typer.colors.RED
        )
        raise typer.Exit(code=1)


@app.command()
def people(
    id: int = typer.Argument(
        ..., help="ID of the person to retrieve (e.g. 1 for Luke Skywalker)"
    ),
    extra: bool | None = typer.Option(
        False, "--extra", "-e", help="Show extra details about the person"
    ),
) -> None:
    """
    Get details about a Star Wars character.

    :param id: ID of the person to retrieve
    :param extra: Show extra details about the person, defaults to False
    """
    data = fetch_data("people", id)

    print(f"{Fore.CYAN}Name: {Fore.GREEN}{data.get('name', 'N/A')}")
    print(f"{Fore.CYAN}Height: {Fore.YELLOW}{data.get('height', 'N/A')} cm")
    print(f"{Fore.CYAN}Mass: {Fore.YELLOW}{data.get('mass', 'N/A')} kg")
    print(f"{Fore.CYAN}Gender: {Fore.MAGENTA}{data.get('gender', 'N/A')}")

    if extra:
        print(f"{Fore.CYAN}Birth Year: {Fore.MAGENTA}{data.get('birth_year', 'N/A')}")
        print(f"{Fore.CYAN}Homeworld: {Fore.BLUE}{data.get('homeworld', 'N/A')}")
        print(Fore.CYAN + "-" * 40)


@app.command()
def planet(
    id: int = typer.Argument(
        ..., help="ID of the planet to retrieve (e.g. 1 for Tatooine)"
    ),
) -> None:
    """
    Get details about a Star Wars planet.

    :param id: ID of the planet to retrieve
    """
    data = fetch_data("planets", id)
    print(f"{Fore.CYAN}Name: {Fore.GREEN}{data['name']}")
    print(f"{Fore.CYAN}Climate: {Fore.YELLOW}{data['climate']}")
    print(f"{Fore.CYAN}Terrain: {Fore.YELLOW}{data['terrain']}")
    print(f"{Fore.CYAN}Population: {Fore.MAGENTA}{data['population']}")


@app.command()
def starship(
    id: int = typer.Argument(
        ..., help="ID of the starship to retrieve (e.g. 9 for Death Star)"
    ),
) -> None:
    """
    Get details about a Star Wars starship.

    :param id: ID of the starship to retrieve
    """
    data = fetch_data("starships", id)
    print(f"{Fore.CYAN}Name: {Fore.GREEN}{data['name']}")
    print(f"{Fore.CYAN}Model: {Fore.YELLOW}{data['model']}")
    print(f"{Fore.CYAN}Manufacturer: {Fore.YELLOW}{data['manufacturer']}")
    print(f"{Fore.CYAN}Starship Class: {Fore.MAGENTA}{data['starship_class']}")

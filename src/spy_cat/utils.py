import aiohttp
from difflib import get_close_matches

from src.settings import BREEDS_API


async def validate_cat_breed(query: str) -> list[str] or str:
    """
    Finds the 3 best-matching cat breeds based on a query.

    :param query: The query string to match breeds against.
    :return: A list of 3 best-matching breed names.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(BREEDS_API) as response:
            if response.status == 200:
                data = await response.json()
                fetched_breeds = [item['name'] for item in data if 'name' in item]

                if query in fetched_breeds:
                    return query
                best_matches = get_close_matches(query, fetched_breeds, n=3)
                return best_matches
            else:
                raise ValueError(f"API request failed with status code {response.status}")

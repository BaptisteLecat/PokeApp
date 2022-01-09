# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = pokemon_listed_from_dict(json.loads(json_string))

from typing import Any, List, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class Result:
    name: str
    url: str

    def __init__(self, name: str, url: str) -> None:
        self.name = name
        self.url = url

    @staticmethod
    def from_dict(obj: Any) -> 'Result':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        url = from_str(obj.get("url"))
        return Result(name, url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["url"] = from_str(self.url)
        return result


class PokemonListed:
    count: int
    next: str
    previous: str
    results: List[Result]

    def __init__(self, count: int, next: str, previous: str, results: List[Result]) -> None:
        self.count = count
        self.next = next
        self.previous = previous
        self.results = results

    @staticmethod
    def from_dict(obj: Any) -> 'PokemonListed':
        assert isinstance(obj, dict)
        count = from_int(obj.get("count"))
        next = None if (obj.get("next") == None) else from_str(obj.get("next"))
        previous = None if (obj.get("previous") == None) else from_str(obj.get("previous"))
        results = from_list(Result.from_dict, obj.get("results"))
        return PokemonListed(count, next, previous, results)

    def to_dict(self) -> dict:
        result: dict = {}
        result["count"] = from_int(self.count)
        result["next"] = from_str(self.next)
        result["previous"] = from_str(self.previous)
        result["results"] = from_list(
            lambda x: to_class(Result, x), self.results)
        return result


def pokemon_listed_from_dict(s: Any) -> PokemonListed:
    return PokemonListed.from_dict(s)


def pokemon_listed_to_dict(x: PokemonListed) -> Any:
    return to_class(PokemonListed, x)

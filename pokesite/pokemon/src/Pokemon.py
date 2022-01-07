# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = pokemon_from_dict(json.loads(json_string))

from typing import Any, List, TypeVar, Type, cast, Callable


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


class Species:
    name: str
    url: str

    def __init__(self, name: str, url: str) -> None:
        self.name = name
        self.url = url

    @staticmethod
    def from_dict(obj: Any) -> 'Species':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        url = from_str(obj.get("url"))
        return Species(name, url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["url"] = from_str(self.url)
        return result


class Ability:
    is_hidden: bool
    slot: int
    ability: Species

    def __init__(self, is_hidden: bool, slot: int, ability: Species) -> None:
        self.is_hidden = is_hidden
        self.slot = slot
        self.ability = ability

    @staticmethod
    def from_dict(obj: Any) -> 'Ability':
        assert isinstance(obj, dict)
        is_hidden = from_bool(obj.get("is_hidden"))
        slot = from_int(obj.get("slot"))
        ability = Species.from_dict(obj.get("ability"))
        return Ability(is_hidden, slot, ability)

    def to_dict(self) -> dict:
        result: dict = {}
        result["is_hidden"] = from_bool(self.is_hidden)
        result["slot"] = from_int(self.slot)
        result["ability"] = to_class(Species, self.ability)
        return result


class GameIndex:
    game_index: int
    version: Species

    def __init__(self, game_index: int, version: Species) -> None:
        self.game_index = game_index
        self.version = version

    @staticmethod
    def from_dict(obj: Any) -> 'GameIndex':
        assert isinstance(obj, dict)
        game_index = from_int(obj.get("game_index"))
        version = Species.from_dict(obj.get("version"))
        return GameIndex(game_index, version)

    def to_dict(self) -> dict:
        result: dict = {}
        result["game_index"] = from_int(self.game_index)
        result["version"] = to_class(Species, self.version)
        return result


class VersionGroupDetail:
    level_learned_at: int
    version_group: Species
    move_learn_method: Species

    def __init__(self, level_learned_at: int, version_group: Species, move_learn_method: Species) -> None:
        self.level_learned_at = level_learned_at
        self.version_group = version_group
        self.move_learn_method = move_learn_method

    @staticmethod
    def from_dict(obj: Any) -> 'VersionGroupDetail':
        assert isinstance(obj, dict)
        level_learned_at = from_int(obj.get("level_learned_at"))
        version_group = Species.from_dict(obj.get("version_group"))
        move_learn_method = Species.from_dict(obj.get("move_learn_method"))
        return VersionGroupDetail(level_learned_at, version_group, move_learn_method)

    def to_dict(self) -> dict:
        result: dict = {}
        result["level_learned_at"] = from_int(self.level_learned_at)
        result["version_group"] = to_class(Species, self.version_group)
        result["move_learn_method"] = to_class(Species, self.move_learn_method)
        return result


class Move:
    move: Species
    version_group_details: List[VersionGroupDetail]

    def __init__(self, move: Species, version_group_details: List[VersionGroupDetail]) -> None:
        self.move = move
        self.version_group_details = version_group_details

    @staticmethod
    def from_dict(obj: Any) -> 'Move':
        assert isinstance(obj, dict)
        move = Species.from_dict(obj.get("move"))
        version_group_details = from_list(
            VersionGroupDetail.from_dict, obj.get("version_group_details"))
        return Move(move, version_group_details)

    def to_dict(self) -> dict:
        result: dict = {}
        result["move"] = to_class(Species, self.move)
        result["version_group_details"] = from_list(lambda x: to_class(
            VersionGroupDetail, x), self.version_group_details)
        return result


class Sprites:
    back_default: str

    def __init__(self, back_default: str) -> None:
        self.back_default = back_default

    @staticmethod
    def from_dict(obj: Any) -> 'Sprites':
        assert isinstance(obj, dict)
        back_default = from_str(obj.get("back_default"))
        return Sprites(back_default)

    def to_dict(self) -> dict:
        result: dict = {}
        result["back_default"] = from_str(self.back_default)
        return result


class Stat:
    base_stat: int
    effort: int
    stat: Species

    def __init__(self, base_stat: int, effort: int, stat: Species) -> None:
        self.base_stat = base_stat
        self.effort = effort
        self.stat = stat

    @staticmethod
    def from_dict(obj: Any) -> 'Stat':
        assert isinstance(obj, dict)
        base_stat = from_int(obj.get("base_stat"))
        effort = from_int(obj.get("effort"))
        stat = Species.from_dict(obj.get("stat"))
        return Stat(base_stat, effort, stat)

    def to_dict(self) -> dict:
        result: dict = {}
        result["base_stat"] = from_int(self.base_stat)
        result["effort"] = from_int(self.effort)
        result["stat"] = to_class(Species, self.stat)
        return result


class TypeElement:
    slot: int
    type: Species

    def __init__(self, slot: int, type: Species) -> None:
        self.slot = slot
        self.type = type

    @staticmethod
    def from_dict(obj: Any) -> 'TypeElement':
        assert isinstance(obj, dict)
        slot = from_int(obj.get("slot"))
        type = Species.from_dict(obj.get("type"))
        return TypeElement(slot, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["slot"] = from_int(self.slot)
        result["type"] = to_class(Species, self.type)
        return result


class Pokemon:
    id: int
    name: str
    base_experience: int
    height: int
    is_default: bool
    order: int
    weight: int
    abilities: List[Ability]
    forms: List[Species]
    game_indices: List[GameIndex]
    location_area_encounters: str
    moves: List[Move]
    species: Species
    sprites: Sprites
    stats: List[Stat]
    types: List[TypeElement]

    def __init__(self, id: int, name: str, base_experience: int, height: int, is_default: bool, order: int, weight: int, abilities: List[Ability], forms: List[Species], game_indices: List[GameIndex], location_area_encounters: str, moves: List[Move], species: Species, sprites: Sprites, stats: List[Stat], types: List[TypeElement]) -> None:
        self.id = id
        self.name = name
        self.base_experience = base_experience
        self.height = height
        self.is_default = is_default
        self.order = order
        self.weight = weight
        self.abilities = abilities
        self.forms = forms
        self.game_indices = game_indices
        self.location_area_encounters = location_area_encounters
        self.moves = moves
        self.species = species
        self.sprites = sprites
        self.stats = stats
        self.types = types

    @staticmethod
    def from_dict(obj: Any) -> 'Pokemon':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        name = from_str(obj.get("name"))
        base_experience = from_int(obj.get("base_experience"))
        height = from_int(obj.get("height"))
        is_default = from_bool(obj.get("is_default"))
        order = from_int(obj.get("order"))
        weight = from_int(obj.get("weight"))
        abilities = from_list(Ability.from_dict, obj.get("abilities"))
        forms = from_list(Species.from_dict, obj.get("forms"))
        game_indices = from_list(GameIndex.from_dict, obj.get("game_indices"))
        location_area_encounters = from_str(
            obj.get("location_area_encounters"))
        moves = from_list(Move.from_dict, obj.get("moves"))
        species = Species.from_dict(obj.get("species"))
        sprites = Sprites.from_dict(obj.get("sprites"))
        stats = from_list(Stat.from_dict, obj.get("stats"))
        types = from_list(TypeElement.from_dict, obj.get("types"))
        return Pokemon(id, name, base_experience, height, is_default, order, weight, abilities, forms, game_indices, location_area_encounters, moves, species, sprites, stats, types)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        result["name"] = from_str(self.name)
        result["base_experience"] = from_int(self.base_experience)
        result["height"] = from_int(self.height)
        result["is_default"] = from_bool(self.is_default)
        result["order"] = from_int(self.order)
        result["weight"] = from_int(self.weight)
        result["abilities"] = from_list(
            lambda x: to_class(Ability, x), self.abilities)
        result["forms"] = from_list(lambda x: to_class(Species, x), self.forms)
        result["game_indices"] = from_list(
            lambda x: to_class(GameIndex, x), self.game_indices)
        result["location_area_encounters"] = from_str(
            self.location_area_encounters)
        result["moves"] = from_list(lambda x: to_class(Move, x), self.moves)
        result["species"] = to_class(Species, self.species)
        result["sprites"] = to_class(Sprites, self.sprites)
        result["stats"] = from_list(lambda x: to_class(Stat, x), self.stats)
        result["types"] = from_list(
            lambda x: to_class(TypeElement, x), self.types)
        return result


def pokemon_from_dict(s: Any) -> Pokemon:
    return Pokemon.from_dict(s)


def pokemon_to_dict(x: Pokemon) -> Any:
    return to_class(Pokemon, x)

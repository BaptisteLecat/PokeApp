# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = move_complete_from_dict(json.loads(json_string))

from typing import Any, List, TypeVar, Type, cast, Callable


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


class DamageClass:
    name: str
    url: str

    def __init__(self, name: str, url: str) -> None:
        self.name = name
        self.url = url

    @staticmethod
    def from_dict(obj: Any) -> 'DamageClass':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        url = from_str(obj.get("url"))
        return DamageClass(name, url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["url"] = from_str(self.url)
        return result


class EffectEntry:
    effect: str
    short_effect: str
    language: DamageClass

    def __init__(self, effect: str, short_effect: str, language: DamageClass) -> None:
        self.effect = effect
        self.short_effect = short_effect
        self.language = language

    @staticmethod
    def from_dict(obj: Any) -> 'EffectEntry':
        assert isinstance(obj, dict)
        effect = from_str(obj.get("effect"))
        short_effect = from_str(obj.get("short_effect"))
        language = DamageClass.from_dict(obj.get("language"))
        return EffectEntry(effect, short_effect, language)

    def to_dict(self) -> dict:
        result: dict = {}
        result["effect"] = from_str(self.effect)
        result["short_effect"] = from_str(self.short_effect)
        result["language"] = to_class(DamageClass, self.language)
        return result


class Meta:
    ailment: DamageClass
    category: DamageClass
    drain: int
    healing: int
    crit_rate: int
    ailment_chance: int
    flinch_chance: int
    stat_chance: int

    def __init__(self, ailment: DamageClass, category: DamageClass, drain: int, healing: int, crit_rate: int, ailment_chance: int, flinch_chance: int, stat_chance: int) -> None:
        self.ailment = ailment
        self.category = category
        self.drain = drain
        self.healing = healing
        self.crit_rate = crit_rate
        self.ailment_chance = ailment_chance
        self.flinch_chance = flinch_chance
        self.stat_chance = stat_chance

    @staticmethod
    def from_dict(obj: Any) -> 'Meta':
        assert isinstance(obj, dict)
        ailment = DamageClass.from_dict(obj.get("ailment"))
        category = DamageClass.from_dict(obj.get("category"))
        drain = from_int(obj.get("drain"))
        healing = from_int(obj.get("healing"))
        crit_rate = from_int(obj.get("crit_rate"))
        ailment_chance = from_int(obj.get("ailment_chance"))
        flinch_chance = from_int(obj.get("flinch_chance"))
        stat_chance = from_int(obj.get("stat_chance"))
        return Meta(ailment, category, drain, healing, crit_rate, ailment_chance, flinch_chance, stat_chance)

    def to_dict(self) -> dict:
        result: dict = {}
        result["ailment"] = to_class(DamageClass, self.ailment)
        result["category"] = to_class(DamageClass, self.category)
        result["drain"] = from_int(self.drain)
        result["healing"] = from_int(self.healing)
        result["crit_rate"] = from_int(self.crit_rate)
        result["ailment_chance"] = from_int(self.ailment_chance)
        result["flinch_chance"] = from_int(self.flinch_chance)
        result["stat_chance"] = from_int(self.stat_chance)
        return result


class Name:
    name: str
    language: DamageClass

    def __init__(self, name: str, language: DamageClass) -> None:
        self.name = name
        self.language = language

    @staticmethod
    def from_dict(obj: Any) -> 'Name':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        language = DamageClass.from_dict(obj.get("language"))
        return Name(name, language)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["language"] = to_class(DamageClass, self.language)
        return result


class MoveComplete:
    id: int
    name: str
    accuracy: int
    pp: int
    priority: int
    power: int
    damage_class: DamageClass
    effect_entries: List[EffectEntry]
    effect_changes: List[Any]
    meta: Meta
    names: List[Name]
    past_values: List[Any]
    stat_changes: List[Any]
    target: DamageClass
    type: DamageClass

    def __init__(self, id: int, name: str, accuracy: int, pp: int, priority: int, power: int, damage_class: DamageClass, effect_entries: List[EffectEntry], effect_changes: List[Any], meta: Meta, names: List[Name], past_values: List[Any], stat_changes: List[Any], target: DamageClass, type: DamageClass) -> None:
        self.id = id
        self.name = name
        self.accuracy = accuracy
        self.pp = pp
        self.priority = priority
        self.power = power
        self.damage_class = damage_class
        self.effect_entries = effect_entries
        self.effect_changes = effect_changes
        self.meta = meta
        self.names = names
        self.past_values = past_values
        self.stat_changes = stat_changes
        self.target = target
        self.type = type

    @staticmethod
    def from_dict(obj: Any) -> 'MoveComplete':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        name = from_str(obj.get("name"))
        accuracy = 0 if (obj.get("accuracy") == None) else from_int(obj.get("accuracy"))
        pp = from_int(obj.get("pp"))
        priority = from_int(obj.get("priority"))
        power = 0 if (obj.get("power") ==
                      None) else from_int(obj.get("power"))
        damage_class = DamageClass.from_dict(obj.get("damage_class"))
        effect_entries = from_list(
            EffectEntry.from_dict, obj.get("effect_entries"))
        effect_changes = from_list(lambda x: x, obj.get("effect_changes"))
        meta = Meta.from_dict(obj.get("meta"))
        names = from_list(Name.from_dict, obj.get("names"))
        past_values = from_list(lambda x: x, obj.get("past_values"))
        stat_changes = from_list(lambda x: x, obj.get("stat_changes"))
        target = DamageClass.from_dict(obj.get("target"))
        type = DamageClass.from_dict(obj.get("type"))
        return MoveComplete(id, name, accuracy, pp, priority, power, damage_class, effect_entries, effect_changes, meta, names, past_values, stat_changes, target, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        result["name"] = from_str(self.name)
        result["accuracy"] = from_int(self.accuracy)
        result["pp"] = from_int(self.pp)
        result["priority"] = from_int(self.priority)
        result["power"] = from_int(self.power)
        result["damage_class"] = to_class(DamageClass, self.damage_class)
        result["effect_entries"] = from_list(
            lambda x: to_class(EffectEntry, x), self.effect_entries)
        result["effect_changes"] = from_list(lambda x: x, self.effect_changes)
        result["meta"] = to_class(Meta, self.meta)
        result["names"] = from_list(lambda x: to_class(Name, x), self.names)
        result["past_values"] = from_list(lambda x: x, self.past_values)
        result["stat_changes"] = from_list(lambda x: x, self.stat_changes)
        result["target"] = to_class(DamageClass, self.target)
        result["type"] = to_class(DamageClass, self.type)
        return result


def move_complete_from_dict(s: Any) -> MoveComplete:
    return MoveComplete.from_dict(s)


def move_complete_to_dict(x: MoveComplete) -> Any:
    return to_class(MoveComplete, x)

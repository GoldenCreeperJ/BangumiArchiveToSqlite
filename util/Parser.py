# This file is modified from the source code of below link, and only keep the minimum code to parse the Infobox.
# https://github.com/bangumi/wiki-parser-py/blob/99525731e4c1de658186a180ff40b9b7da655905/src/bgm_tv_wiki/__init__.py

from __future__ import annotations
import dataclasses


@dataclasses.dataclass(slots=True, kw_only=True)
class Wiki:
    @dataclasses.dataclass(slots=True, frozen=True, kw_only=True)
    class Field:
        key: str
        value: str | tuple[Wiki.Field, ...] = ""

        def __iter__(self):
            yield self.key, self.value

    __fields: tuple[Field, ...] = dataclasses.field(default_factory=tuple)

    def __init__(self, s: str):
        s = "\n".join(s.splitlines()).strip()
        if not s:
            return

        fields: dict[str, str | tuple[Wiki.Field, ...]] = \
            {"wiki_type": s[9:min(s.find(c) for c in "\n}")].strip()}

        item_container: list[Wiki.Field] = []
        duplicated_keys: set[str] = set()
        current_key: str = ""

        for line in s.splitlines()[1:-1]:
            line = line.strip()

            if not line:
                continue

            if line[0] == "|":
                current_key = ""

                # Read line without leading '|' as key value pair, spaces are trimmed.
                key, value = tuple(map(str.strip, line[1:].partition("=")[::2]))

                if not value:
                    continue
                elif value == "{":
                    current_key = key
                    continue

                f = Wiki.Field(key=key, value=value)

            elif line == "}":
                v = [x for x in item_container if x.key or x.value]
                item_container = []
                if not v:
                    continue
                f = Wiki.Field(key=current_key, value=tuple(v))
            else:
                # Read whole line as an array item, spaces are trimmed.
                key, value = tuple(map(str.strip, line[1:-1].partition("|")[::2])) \
                    if '|' in line[1:-1] else ("", line[1:-1].strip())
                item_container.append(Wiki.Field(key=key, value=value))
                continue

            if f.key in duplicated_keys:
                continue
            if f.key not in fields:
                fields[f.key] = f.value
            elif f.value:
                if not fields[f.key]:
                    fields[f.key] = f.value
                elif fields[f.key] != f.value:
                    duplicated_keys.add(f.key)

        self.__fields = tuple(Wiki.Field(key=key, value=value) for key, value in fields.items())

    def __iter__(self):
        for field in self.__fields:
            if isinstance(field.value, tuple):
                value = [dict(item) for item in field.value]
            else:
                value = field.value
            yield field.key, value

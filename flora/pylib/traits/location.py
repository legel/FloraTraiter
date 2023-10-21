from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language
from spacy import registry
from traiter.pylib import const as t_const
from traiter.pylib import term_util as tu
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add
from traiter.pylib.traits import terms as t_terms
from traiter.pylib.traits.base import Base


@dataclass
class Location(Base):
    # Class vars ----------
    location_ents: ClassVar[list[str]] = ["location"]

    location_csv: ClassVar[Path] = (
        Path(__file__).parent / "terms" / "location_terms.csv"
    )
    units_csv: ClassVar[Path] = Path(t_terms.__file__).parent / "unit_length_terms.csv"
    all_csvs: ClassVar[list[Path]] = [location_csv, units_csv]

    replace: ClassVar[dict[str, str]] = tu.term_data(location_csv, "replace")
    overwrite: ClassVar[list[str]] = (
        ["part", "subpart"] + tu.get_labels(location_csv) + tu.get_labels(units_csv)
    )
    # ---------------------

    location: str = None
    type: str = None

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="location_terms", path=cls.all_csvs)
        add.trait_pipe(
            nlp,
            name="location_patterns",
            compiler=cls.location_patterns(),
            overwrite=cls.overwrite,
        )
        add.cleanup_pipe(nlp, name="part_location_cleanup")

    @classmethod
    def location_patterns(cls):
        decoder = {
            "9.9": {"TEXT": {"REGEX": t_const.FLOAT_TOKEN_RE}},
            "-/to": {"LOWER": {"IN": t_const.DASH + ["to", "_"]}},
            "adj": {"POS": "ADJ"},
            "cm": {"ENT_TYPE": {"IN": ["metric_length", "imperial_length"]}},
            "joined": {"ENT_TYPE": "joined"},
            "leader": {"ENT_TYPE": "location_leader"},
            "location": {"ENT_TYPE": "location"},
            "missing": {"ENT_TYPE": "missing"},
            "of": {"LOWER": "of"},
            "part": {"ENT_TYPE": "part"},
            "prep": {"POS": {"IN": ["ADP", "CCONJ"]}},
            "subpart": {"ENT_TYPE": "subpart"},
        }
        return [
            Compiler(
                label="part_as_location",
                id="location",
                on_match="part_as_location_match",
                decoder=decoder,
                keep="location",
                patterns=[
                    "missing? joined?  leader prep? part",
                    "missing? location leader       part",
                    "                  leader       part prep? missing? joined",
                ],
            ),
            Compiler(
                label="subpart_as_location",
                id="location",
                on_match="subpart_as_location_match",
                decoder=decoder,
                keep="location",
                patterns=[
                    "missing? joined?  leader subpart",
                    "missing? joined?  leader subpart of adj? subpart",
                    "missing? location leader subpart",
                    "missing? location leader subpart of adj? subpart",
                ],
            ),
            Compiler(
                label="part_as_distance",
                id="location",
                on_match="part_as_distance_match",
                keep="location",
                decoder=decoder,
                patterns=[
                    "missing? joined?  leader prep? part prep? 9.9 -/to* 9.9? cm",
                    "missing? location leader prep? part prep? 9.9 -/to* 9.9? cm",
                ],
            ),
            Compiler(
                label="part_location",
                id="location",
                on_match="part_location_match",
                keep="location",
                decoder=decoder,
                patterns=[
                    "location+",
                ],
            ),
        ]

    @classmethod
    def loc(cls, ent):
        return " ".join([cls.replace.get(t.lower_, t.lower_) for t in ent])

    @classmethod
    def part_as_distance_match(cls, ent):
        return cls.from_ent(ent, type="part_as_distance", location=cls.loc(ent))

    @classmethod
    def part_as_location_match(cls, ent):
        return cls.from_ent(ent, type="part_as_location", location=cls.loc(ent))

    @classmethod
    def subpart_as_location_match(cls, ent):
        return cls.from_ent(ent, type="subpart_as_location", location=cls.loc(ent))

    @classmethod
    def part_location_match(cls, ent):
        return cls.from_ent(ent, type="part_location", location=cls.loc(ent))


@registry.misc("part_as_distance_match")
def part_as_distance_match(ent):
    return Location.part_as_distance_match(ent)


@registry.misc("part_as_location_match")
def part_as_location_match(ent):
    return Location.part_as_location_match(ent)


@registry.misc("subpart_as_location_match")
def subpart_as_location_match(ent):
    return Location.subpart_as_location_match(ent)


@registry.misc("part_location_match")
def part_location_match(ent):
    return Location.part_location_match(ent)

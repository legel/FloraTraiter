from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language, registry

from flora.pylib.trait_util import clean_trait
from traiter.traiter.pylib import const as t_const
from traiter.traiter.pylib import term_util
from traiter.traiter.pylib.darwin_core import DarwinCore
from traiter.traiter.pylib.pattern_compiler import Compiler
from traiter.traiter.pylib.pipes import add

from .linkable import Linkable


@dataclass(eq=False)
class Odor(Linkable):
    # Class vars ----------
    odor_csv: ClassVar[Path] = Path(__file__).parent / "terms" / "odor_terms.csv"
    replace: ClassVar[dict[str, str]] = term_util.term_data(odor_csv, "replace")
    # ---------------------

    odor: str = None

    def to_dwc(self, dwc) -> DarwinCore:
        return dwc.add_dyn(**{self.key: self.odor})

    @property
    def key(self) -> str:
        return self.key_builder("odor")

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="odor_terms", path=cls.odor_csv)
        add.trait_pipe(
            nlp,
            name="odor_patterns",
            compiler=cls.odor_patterns(),
            overwrite=["odor"],
        )
        add.cleanup_pipe(nlp, name="odor_cleanup")

    @classmethod
    def odor_patterns(cls):
        decoder = {
            "(": {"TEXT": {"IN": t_const.OPEN}},
            ")": {"TEXT": {"IN": t_const.CLOSE}},
            "odor": {"ENT_TYPE": "odor"},
        }
        return [
            Compiler(
                label="odor",
                on_match="odor_match",
                keep="odor",
                decoder=decoder,
                patterns=[
                    "  odor ",
                    "( odor )",
                ],
            ),
        ]

    @classmethod
    def odor_match(cls, ent):
        return cls.from_ent(ent, odor=clean_trait(ent, cls.replace))


@registry.misc("odor_match")
def odor_match(ent):
    return Odor.odor_match(ent)

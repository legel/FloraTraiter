from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from spacy import Language
from spacy import registry
from traiter.pylib import const as t_const
from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add

from ..trait_util import clean_trait
from .linkable import Linkable


@dataclass
class Woodiness(Linkable):
    # Class vars ----------
    woodiness_csv: ClassVar[Path] = (
        Path(__file__).parent / "terms" / "woodiness_terms.csv"
    )
    replace: ClassVar[dict[str, str]] = term_util.term_data(woodiness_csv, "replace")
    # ---------------------

    woodiness: str = None

    def to_dwc(self, dwc, ent):
        dwc.new_rec()
        key = self.dwc_key("woodiness")
        dwc.add_dyn(**{key: self.woodiness})
        self.add_loc(dwc, "woodiness")

    @classmethod
    def pipe(cls, nlp: Language):
        add.term_pipe(nlp, name="woodiness_terms", path=cls.woodiness_csv)
        add.trait_pipe(
            nlp,
            name="woodiness_patterns",
            compiler=cls.woodiness_patterns(),
            overwrite=["woodiness"],
        )
        add.cleanup_pipe(nlp, name="woodiness_cleanup")

    @classmethod
    def woodiness_patterns(cls):
        decoder = {
            "(": {"TEXT": {"IN": t_const.OPEN}},
            ")": {"TEXT": {"IN": t_const.CLOSE}},
            "woodiness": {"ENT_TYPE": "woodiness"},
        }
        return [
            Compiler(
                label="woodiness",
                on_match="woodiness_match",
                keep="woodiness",
                decoder=decoder,
                patterns=[
                    "  woodiness ",
                    "( woodiness )",
                ],
            ),
        ]

    @classmethod
    def woodiness_match(cls, ent):
        return cls.from_ent(ent, woodiness=clean_trait(ent, cls.replace))


@registry.misc("woodiness_match")
def woodiness_match(ent):
    return Woodiness.woodiness_match(ent)

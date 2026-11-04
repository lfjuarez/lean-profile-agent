"""Lexical retrieval (BM25) over knowledge-base sections, one index per language.

No embeddings on purpose: the knowledge base is a few dozen sections, so a deterministic
lexical index is cheap, debuggable and testable. Query terms are case- and accent-folded and
lightly stemmed; document titles and the suggested questions of each document are indexed
together with the section body so that natural questions land on the right section.
"""

from __future__ import annotations

import math
import re
import unicodedata
from collections import Counter
from dataclasses import dataclass

from .kb import Chunk, KnowledgeBase

_WORD = re.compile(r"[a-z0-9]+")

STOPWORDS_EN = frozenset(
    """a an and or of to in on for with is are was were be been being do does did done you
    your yours i me my we our it its this that these those what which who whom how when where
    why can could would should will shall have has had having about tell please any some there
    as at by from up out if than then so not no yes also into like much many per one ones
    want know get give got more most other such own same just only very s t re ve ll d
    the best""".split()
)
STOPWORDS_ES = frozenset(
    """de la el los las un una unos unas y o u que en con por para es sos son soy tu tus su
    sus mi mis me te se lo le les del al a e como cual cuales cuanto cuanta cuantos cuantas
    donde cuando hay ha han hace haces hace hacer tiene tienes tengo tenes puedo puede puedes
    podes podrias podria sobre mas muy ya si no ni este esta esto estos estas ese esa eso esos
    esas contame decime contar dime cuentame quiero saber quisiera querria gustaria algo algun
    alguna algunos algunas otro otra otros otras ser estar fue era eres sea sean nos vos usted
    ustedes ellos ellas el ella yo hasta desde entre sin pero aunque porque cuales cual
    tambien""".split()
)
STOPWORDS = STOPWORDS_EN | STOPWORDS_ES

_ES_MARKERS = frozenset(
    """que cual cuales cuanto cuanta como donde cuando tenes tienes sos tu tus sus hacés haces
    trabajas trabajás podes podés ofreces ofrecés cuesta cuestan tarifa tarifas servicios
    experiencia certificaciones contacto disponibilidad formacion habilidades el la los las
    de del con por para es son una unos unas al se te me""".split()
)
_EN_MARKERS = frozenset(
    """the you your what which how do does are is can have with about tell rates services
    experience certifications contact availability where when who why and for of in on
    hold work offer build cost much""".split()
)


# Words visitors use that the documents phrase differently. Keys and values are tokens
# (folded and stemmed), so "¿Dónde vivís?" reaches the section that says "Vive en".
_LOCATION = ("ubicacion", "vive", "location", "based", "argentina")
_EDUCATION = ("formacion", "maestria", "education", "degree", "universidad")
_RATES = ("tarifa", "rate", "price", "usd")
_CURRENT = ("actualidad", "actual", "present", "current")
_AI = ("ia", "ai", "agente", "agent", "llm")
_EMPLOYMENT = (
    "freelance",
    "contrato",
    "contract",
    "hora",
    "hour",
    "disponibilidad",
    "availability",
)
_LEAD = ("liderazgo", "lidero", "leadership", "led", "equipo", "team")
_MENTOR = ("mentoria", "mentoring", "transferencia", "transfer", "capacitacion", "training")
_CODE = ("python", "lenguaje", "language", "typescript", "sql")
_HIRE = ("diferencia", "different", "differentiator")
SYNONYMS: dict[str, tuple[str, ...]] = {
    **{
        w: _LOCATION
        for w in (
            "reside",
            "residi",
            "residencia",
            "vivi",
            "vivo",
            "vive",
            "vivir",
            "ubicado",
            "ubicada",
            "radicado",
            "radicada",
            "localidad",
            "ciudad",
            "pais",
            "nacionalidad",
            "live",
            "living",
            "located",
            "location",
            "based",
            "city",
            "country",
            "nationality",
            "from",
        )
    },
    **{
        w: _EDUCATION
        for w in (
            "estudiaste",
            "estudio",
            "estudie",
            "estudia",
            "titulo",
            "carrera",
            "universidad",
            "educacion",
            "study",
            "studied",
            "studie",
            "education",
            "university",
            "college",
            "degree",
        )
    },
    **{
        w: _RATES
        for w in (
            "precio",
            "cobra",
            "cobrar",
            "cobras",
            "salario",
            "salarial",
            "sueldo",
            "pretension",
            "pretende",
            "honorario",
            "price",
            "pricing",
            "charge",
            "salary",
            "compensation",
            "expectation",
            "fee",
            "cost",
        )
    },
    **{
        w: _CURRENT for w in ("actualmente", "hoy", "ahora", "currently", "now", "today", "current")
    },
    **{
        w: _AI
        for w in ("inteligencia", "artificial", "ia", "ai", "llm", "genai", "agente", "agent")
    },
    **{
        w: _EMPLOYMENT
        for w in (
            "full",
            "fulltime",
            "employment",
            "empleo",
            "dependencia",
            "permanente",
            "permanent",
            "jornada",
            "part",
            "parttime",
        )
    },
    **{
        w: _LEAD
        for w in (
            "liderando",
            "liderar",
            "lidera",
            "lider",
            "leading",
            "lead",
            "leader",
            "manage",
            "managing",
            "manager",
            "gestionar",
        )
    },
    **{
        w: _MENTOR
        for w in (
            "mentor",
            "mentorea",
            "mentoring",
            "coach",
            "coaching",
            "junior",
            "ensenar",
            "ensenas",
            "teach",
            "onboard",
            "onboarding",
        )
    },
    **{
        w: _CODE
        for w in (
            "programar",
            "programa",
            "programacion",
            "code",
            "coding",
            "programming",
            "developer",
            "desarrollar",
        )
    },
    **{w: _HIRE for w in ("contratarte", "contratar", "hire", "hiring", "elegirte", "choose")},
    "remota": ("remoto",),
    "remotamente": ("remoto",),
    "remotely": ("remote",),
    "prioriza": ("prioriza", "priority", "prioridad"),
    "prioritize": ("priority", "prioritize"),
    "cliente": ("cliente", "stakeholder"),
    "client": ("client", "stakeholder"),
}


def expand(terms: list[str]) -> list[str]:
    out = list(terms)
    for t in terms:
        out.extend(x for x in SYNONYMS.get(t, ()) if x not in out)
    return out


def fold(text: str) -> str:
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()


# Plain-language complaints and "how is it built" phrasings map to the words the documents use.
SYNONYMS.update(
    {
        **{
            w: ("lenta", "rendimiento", "capacidad", "performance", "slow")
            for w in ("lento", "lenta", "lentitud", "slow", "sluggish")
        },
        **{
            w: ("licencia", "costo", "license", "cost", "spend")
            for w in ("caro", "cara", "costoso", "costosa", "expensive", "pricey")
        },
        **{
            w: ("stack", "fastapi", "funciona", "works", "built")
            for w in (
                "construido",
                "construida",
                "hecho",
                "hecha",
                "desarrollado",
                "armado",
                "built",
            )
        },
        **{
            w: ("ia", "ai", "agente", "agent", "agentes", "llm", "mcp")
            for w in ("inteligencia", "artificial", "intelligence")
        },
    }
)


def _stem(token: str) -> str:
    if len(token) > 5 and token.endswith("es"):
        return token[:-2]
    if len(token) > 4 and token.endswith("s"):
        return token[:-1]
    return token


def tokenize(text: str) -> list[str]:
    """Lowercase, accent-fold, drop stopwords and single characters, light plural stemming."""
    return [_stem(t) for t in _WORD.findall(fold(text)) if len(t) > 1 and t not in STOPWORDS]


def detect_lang(text: str, default: str = "en") -> str:
    words = _WORD.findall(fold(text))
    es = sum(w in _ES_MARKERS for w in words) + text.count("¿") * 2 + text.count("¡") * 2
    en = sum(w in _EN_MARKERS for w in words)
    if es > en:
        return "es"
    if en > es:
        return "en"
    return default


@dataclass(frozen=True)
class Hit:
    chunk: Chunk
    score: float
    matched: frozenset[str]


class Index:
    """BM25 index over the chunks of one knowledge base."""

    k1 = 1.5
    b = 0.75
    score_floor = 1.0
    coverage_floor = 0.5

    def __init__(self, kb: KnowledgeBase) -> None:
        self.kb = kb
        self.chunks = kb.chunks
        self._tf: list[Counter[str]] = []
        self._len: list[int] = []
        df: Counter[str] = Counter()
        for chunk in self.chunks:
            tokens = self._chunk_tokens(chunk)
            counts = Counter(tokens)
            self._tf.append(counts)
            self._len.append(len(tokens))
            df.update(counts.keys())
        n = len(self.chunks)
        self._avg_len = (sum(self._len) / n) if n else 1.0
        self._idf = {t: math.log(1 + (n - d + 0.5) / (d + 0.5)) for t, d in df.items()}

    @staticmethod
    def _chunk_tokens(chunk: Chunk) -> list[str]:
        titles = tokenize(chunk.doc_title) + tokenize(chunk.section_title)
        questions = [t for q in chunk.questions for t in tokenize(q)]
        return titles * 2 + questions + tokenize(chunk.text)

    def search(self, query: str, k: int = 6) -> list[Hit]:
        terms = expand(tokenize(query))
        if not terms:
            return []
        hits: list[Hit] = []
        for i, chunk in enumerate(self.chunks):
            tf = self._tf[i]
            score = 0.0
            matched: set[str] = set()
            norm = self.k1 * (1 - self.b + self.b * self._len[i] / self._avg_len)
            for term in set(terms):
                f = tf.get(term)
                if not f:
                    continue
                matched.add(term)
                score += self._idf[term] * (f * (self.k1 + 1)) / (f + norm)
            if score > 0:
                hits.append(Hit(chunk=chunk, score=score, matched=frozenset(matched)))
        hits.sort(key=lambda h: (-h.score, h.chunk.id))
        return hits[:k]

    def is_answerable(self, hits: list[Hit], query: str | None = None) -> bool:
        """True when the hits plausibly contain the answer; used to skip the model call."""
        if not hits or hits[0].score < self.score_floor:
            return False
        if not query:
            return True
        # each original term counts as covered when it, or one of its synonyms, matched
        matched = {t for h in hits for t in h.matched}
        # words the documents never use ("sabés", "describe") neither help nor hurt coverage
        terms = [
            t
            for t in tokenize(query)
            if t in self._idf or set(SYNONYMS.get(t, ())) & self._idf.keys()
        ]
        if not terms:
            return False
        covered = [t for t in terms if t in matched or matched & set(SYNONYMS.get(t, ()))]
        return len(covered) / len(terms) >= self.coverage_floor

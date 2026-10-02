"""kata07-howd-i-do - How'd I Do? - Quiz scoring system

Score a quiz: model questions and answers, support several question types,
partial credit, weighted and bonus questions, and produce a report.

Source: http://codekata.com/kata/kata07-howd-i-do/

Architecture: DDD + CQRS + Repository, in-memory state only.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Protocol

# =============================================================================
# Value Objects
# =============================================================================

DEFAULT_GRADING_SCALE: dict[str, float] = {
    "A": 0.90,
    "B": 0.80,
    "C": 0.70,
    "D": 0.60,
    "F": 0.00,
}


class QuestionType(Enum):
    """The kind of question asked."""

    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    SHORT_ANSWER = "short_answer"
    NUMERIC_RANGE = "numeric_range"
    BONUS = "bonus"

    @property
    def is_bonus(self) -> bool:
        return self is QuestionType.BONUS


class GradingScale(Enum):
    """How a percentage is turned into a grade."""

    PERCENTAGE = "percentage"
    LETTER = "letter"
    GPA = "gpa"


# Type of a normalized correct answer. ``range`` is the interval form used by
# numeric questions, where the bound order carries the (low, high) meaning.
type AnswerValue = str | float | range


def _normalize(value: object, case_sensitive: bool = True) -> str:
    """Canonical string form of an answer, for comparison purposes."""
    text = str(value).strip()
    return text if case_sensitive else text.lower()


# =============================================================================
# Domain Entities
# =============================================================================

@dataclass
class Question:
    """A single question with its answer key and scoring rules."""

    text: str
    correct_answer: AnswerValue
    type: QuestionType = QuestionType.SHORT_ANSWER
    points: float = 1.0
    case_sensitive: bool = True
    credit_threshold: float = 0.6
    bonus_points: float = 1.0

    def __post_init__(self) -> None:
        if not self.text:
            raise ValueError("Question text cannot be empty")
        if self.points <= 0:
            raise ValueError("Question points must be positive")
        if not 0 <= self.credit_threshold <= 1:
            raise ValueError("credit_threshold must be between 0 and 1")

    @property
    def worth(self) -> float:
        """Points a fully correct answer earns (including bonus points)."""
        total = self.points
        if self.type.is_bonus:
            total += self.bonus_points
        return total

    def evaluate(self, answer: object) -> float:
        """Fraction of this question the given answer earns, 0.0 - 1.0."""
        if answer is None:
            return 0.0

        if self.type is QuestionType.MULTIPLE_CHOICE or self.type is QuestionType.TRUE_FALSE:
            exact = _normalize(self.correct_answer, False)
            return 1.0 if _normalize(answer, False) == exact else 0.0

        if self.type is QuestionType.SHORT_ANSWER or self.type is QuestionType.BONUS:
            given = _normalize(answer, self.case_sensitive)
            expected = _normalize(self.correct_answer, self.case_sensitive)
            if given == expected:
                return 1.0
            if expected in given and len(given) > len(expected):
                # A longer answer that contains the key earns partial credit.
                return round(self.credit_threshold, 4)
            return 0.0

        # NUMERIC_RANGE: credit scales with how deep inside the interval the
        # answer lands; outside the interval earns nothing.
        correct = self.correct_answer
        if not isinstance(correct, range) or isinstance(answer, bool):
            return 0.0
        try:
            value = float(answer)  # type: ignore[arg-type]
        except (TypeError, ValueError):
            return 0.0

        low = float(correct.start)
        high = float(correct.stop)
        if not low <= value <= high or high == low:
            return 0.0
        # An interval narrower than one unit has no room for graded closeness;
        # anything inside is simply accepted.
        if high - low <= 1.0:
            return 1.0
        midpoint = (low + high) / 2
        half = (high - low) / 2
        closeness = 1.0 - abs(value - midpoint) / half
        return round(self.credit_threshold + (1 - self.credit_threshold) * closeness, 4)


@dataclass(frozen=True)
class Answer:
    """A student's response to a question."""

    question_text: str
    value: str


@dataclass(frozen=True)
class QuestionResult:
    """The outcome of marking one question."""

    question_text: str
    given: str
    expected: str
    points: float
    possible: float
    reason: str

    @property
    def correct(self) -> bool:
        return self.possible > 0 and self.points == self.possible

    @property
    def partial(self) -> bool:
        return 0 < self.points < self.possible


@dataclass(frozen=True)
class ScoreReport:
    """Aggregate result of marking a whole quiz."""

    results: tuple[QuestionResult, ...] = ()
    raw_points: float = 0.0
    base_points: float = 0.0
    total_points: float = 0.0
    unanswered: tuple[str, ...] = ()

    @property
    def correct_count(self) -> int:
        return sum(1 for r in self.results if r.correct)

    @property
    def partial_count(self) -> int:
        return sum(1 for r in self.results if r.partial)

    @property
    def incorrect_count(self) -> int:
        """Answered questions that earned nothing."""
        return sum(
            1
            for r in self.results
            if not r.correct and not r.partial and r.given != ""
        )

    @property
    def wrong_questions(self) -> list[str]:
        """Questions that did not earn full marks, in quiz order."""
        return [r.question_text for r in self.results if not r.correct]

    @property
    def percentage(self) -> float:
        """Score as a percentage of the non-bonus quiz total, capped at 100."""
        if self.base_points <= 0:
            return 0.0
        return min(100.0, round(100.0 * self.total_points / self.base_points, 2))

    def letter_grade(self, scale: dict[str, float] | None = None) -> str:
        """Letter grade, by default on the standard 90/80/70/60 scale."""
        table = scale if scale is not None else DEFAULT_GRADING_SCALE
        percentage = self.percentage
        for grade, floor in sorted(table.items(), key=lambda item: -item[1]):
            if percentage >= floor * 100:
                return grade
        return "F"

    def gpa(self, scale: dict[str, float] | None = None) -> float:
        """Grade point average on a 4.0 scale."""
        table = scale if scale is not None else DEFAULT_GRADING_SCALE
        grade = self.letter_grade(table)
        return {"A": 4.0, "B": 3.0, "C": 2.0, "D": 1.0, "F": 0.0}.get(grade, 0.0)

    def grade(self, scale: GradingScale = GradingScale.PERCENTAGE) -> float | str:
        """The score expressed in a particular grading scale."""
        if scale is GradingScale.LETTER:
            return self.letter_grade()
        if scale is GradingScale.GPA:
            return self.gpa()
        return self.percentage

    def summary(self) -> str:
        """One-line, human-readable report."""
        return (
            f"Score: {self.total_points:g}/{self.base_points:g} "
            f"({self.percentage:g}%) - {self.letter_grade()}"
        )

    def report(self) -> str:
        """Multi-line report: totals plus every question not fully correct."""
        lines = [self.summary()]
        if self.unanswered:
            lines.append(f"Unanswered: {', '.join(self.unanswered)}")
        if not self.wrong_questions and self.results:
            lines.append("All questions answered correctly.")
        for result in self.results:
            if result.correct:
                continue
            lines.append(
                f"  {result.question_text}: {result.points:g}/{result.possible:g}"
                f" - {result.reason}"
            )
        return "\n".join(lines)


# =============================================================================
# Domain Service
# =============================================================================

class QuizService:
    """Marks answers against a question key and aggregates the result."""

    def grade(self, questions: list[Question], answers: dict[str, str]) -> ScoreReport:
        results: list[QuestionResult] = []
        unanswered: list[str] = []
        raw = 0.0
        base = 0.0

        for question in questions:
            given = answers.get(question.text)
            if given is None:
                unanswered.append(question.text)
                fraction = 0.0
            else:
                fraction = question.evaluate(given)

            earned = question.points * fraction
            if question.type.is_bonus:
                raw += earned + question.bonus_points * fraction
            else:
                raw += earned
                base += question.points

            expected = _describe(question.correct_answer)
            results.append(
                QuestionResult(
                    question_text=question.text,
                    given="" if given is None else str(given),
                    expected=expected,
                    points=round(earned + _bonus_credit(question, fraction), 4),
                    possible=question.worth,
                    reason=_reason(question, given, fraction),
                )
            )

        return ScoreReport(
            results=tuple(results),
            raw_points=round(raw, 4),
            base_points=round(base, 4),
            total_points=round(raw, 4),
            unanswered=tuple(unanswered),
        )


def _bonus_credit(question: Question, fraction: float) -> float:
    """Bonus points earned, zero for ordinary questions."""
    if not question.type.is_bonus:
        return 0.0
    return question.bonus_points * fraction


def _describe(correct: AnswerValue) -> str:
    if isinstance(correct, range):
        return f"{correct.start}-{correct.stop}"
    return str(correct)


def _reason(question: Question, given: object, fraction: float) -> str:
    if given is None:
        return "not answered"
    if fraction >= 1.0:
        return "correct"
    if fraction > 0:
        return "partial credit"
    return "incorrect"


# =============================================================================
# Repository
# =============================================================================

class QuizRepository(Protocol):
    """Storage abstraction for quizzes (in-memory only)."""

    def save(self, quiz: Quiz) -> None: ...

    def get(self, name: str) -> Quiz | None: ...

    def all(self) -> list[Quiz]: ...

    def __len__(self) -> int: ...


class InMemoryQuizRepository:
    """In-memory dictionary-backed quiz store."""

    def __init__(self) -> None:
        self._quizzes: dict[str, Quiz] = {}

    def save(self, quiz: Quiz) -> None:
        self._quizzes[quiz.name] = quiz

    def get(self, name: str) -> Quiz | None:
        return self._quizzes.get(name)

    def all(self) -> list[Quiz]:
        return list(self._quizzes.values())

    def __len__(self) -> int:
        return len(self._quizzes)


# =============================================================================
# CQRS
# =============================================================================

@dataclass
class AddQuestionCommand:
    quiz_name: str
    question: Question


@dataclass
class ScoreQuizCommand:
    quiz_name: str
    answers: dict[str, str] = field(default_factory=dict)


@dataclass
class ReportQuery:
    quiz_name: str
    answers: dict[str, str] = field(default_factory=dict)


@dataclass
class GradeQuery:
    quiz_name: str
    answers: dict[str, str] = field(default_factory=dict)
    scale: GradingScale = GradingScale.PERCENTAGE


class QuizCommandHandler:
    """Write side: build and score quizzes."""

    def __init__(self, service: QuizService, repository: QuizRepository):
        self._service = service
        self._repository = repository

    def handle_add_question(self, cmd: AddQuestionCommand) -> Question:
        quiz = self._repository.get(cmd.quiz_name)
        if quiz is None:
            quiz = Quiz(name=cmd.quiz_name)
            self._repository.save(quiz)
        quiz.add(cmd.question)
        return cmd.question

    def handle_score(self, cmd: ScoreQuizCommand) -> ScoreReport:
        quiz = self._repository.get(cmd.quiz_name)
        if quiz is None:
            return ScoreReport()
        return self._service.grade(quiz.questions, cmd.answers)


class QuizQueryHandler:
    """Read side: reports and grades for a stored quiz."""

    def __init__(self, service: QuizService, repository: QuizRepository):
        self._service = service
        self._repository = repository

    def handle_report(self, query: ReportQuery) -> ScoreReport:
        quiz = self._repository.get(query.quiz_name)
        if quiz is None:
            return ScoreReport()
        return self._service.grade(quiz.questions, query.answers)

    def handle_grade(self, query: GradeQuery) -> float | str:
        return self.handle_report(
            ReportQuery(query.quiz_name, dict(query.answers))
        ).grade(query.scale)


# =============================================================================
# Aggregate + Facade
# =============================================================================

class Quiz:
    """Aggregate root: an ordered collection of questions."""

    def __init__(self, name: str = "quiz") -> None:
        self.name = name
        self._questions: list[Question] = []

    @property
    def questions(self) -> list[Question]:
        return list(self._questions)

    def __len__(self) -> int:
        return len(self._questions)

    def add_question(
        self,
        text: str,
        correct_answer: object,
        type: str | QuestionType | None = None,
        points: float = 1.0,
        case_insensitive: bool = False,
        **options: Any,
    ) -> Question:
        """Add a question; by default the ``type`` follows the answer shape."""
        question_type = _resolve_type(type, correct_answer, case_insensitive)
        question = Question(
            text=text,
            correct_answer=_coerce_answer(correct_answer, question_type),
            type=question_type,
            points=points,
            case_sensitive=not case_insensitive,
            **options,
        )
        self._questions.append(question)
        return question

    def add(self, question: Question) -> Question:
        """Append an already-built Question to this quiz."""
        self._questions.append(question)
        return question

    def score(self, answers: dict[str, str]) -> ScoreReport:
        """Mark the given answers against this quiz's key."""
        return QuizService().grade(self._questions, answers)


class HowdIDo:
    """Main facade for quiz scoring, with CQRS wiring over an in-memory store."""

    _service: QuizService
    _repository: InMemoryQuizRepository
    _command_handler: QuizCommandHandler
    _query_handler: QuizQueryHandler

    def __init__(self, name: str = "quiz") -> None:
        self.name = name
        self._service = QuizService()
        self._repository = InMemoryQuizRepository()
        self._command_handler = QuizCommandHandler(self._service, self._repository)
        self._query_handler = QuizQueryHandler(self._service, self._repository)
        self._session = Quiz(name=name)
        self._repository.save(self._session)

    # Commands
    def add_question(self, *args: Any, **kwargs: Any) -> Question:
        return self._session.add_question(*args, **kwargs)

    def add(self, question: Question) -> Question:
        """Append an already-built Question to the session quiz."""
        return self._session.add(question)

    def score(self, answers: dict[str, str]) -> ScoreReport:
        return self._command_handler.handle_score(
            ScoreQuizCommand(quiz_name=self.name, answers=answers)
        )

    # Queries
    def report(self, answers: dict[str, str]) -> str:
        return self._query_handler.handle_report(
            ReportQuery(quiz_name=self.name, answers=answers)
        ).report()

    def grade(
        self, answers: dict[str, str], scale: GradingScale = GradingScale.PERCENTAGE
    ) -> float | str:
        return self._query_handler.handle_grade(
            GradeQuery(quiz_name=self.name, answers=answers, scale=scale)
        )

    def score_quiz(self, answers: list[str], key: list[str]) -> int:
        """Positional interface: answers against a key, count full marks."""
        session = Quiz()
        for text, expected in zip(key, answers, strict=False):
            session.add_question(text, expected)
        pairs = zip(session.questions, answers, strict=False)
        report = session.score({q.text: a for q, a in pairs})
        return report.correct_count


def _resolve_type(
    type_spec: str | QuestionType | None, answer: object, case_insensitive: bool = False
) -> QuestionType:
    if isinstance(type_spec, QuestionType):
        return type_spec
    aliases = {
        "multiple_choice": QuestionType.MULTIPLE_CHOICE,
        "choice": QuestionType.MULTIPLE_CHOICE,
        "mc": QuestionType.MULTIPLE_CHOICE,
        "true_false": QuestionType.TRUE_FALSE,
        "truefalse": QuestionType.TRUE_FALSE,
        "bool": QuestionType.TRUE_FALSE,
        "short": QuestionType.SHORT_ANSWER,
        "short_answer": QuestionType.SHORT_ANSWER,
        "text": QuestionType.SHORT_ANSWER,
        "numeric": QuestionType.NUMERIC_RANGE,
        "numeric_range": QuestionType.NUMERIC_RANGE,
        "range": QuestionType.NUMERIC_RANGE,
        "bonus": QuestionType.BONUS,
    }
    if isinstance(type_spec, str) and type_spec in aliases:
        return aliases[type_spec]
    # No usable type spelling: fall back to the answer's own shape.
    if isinstance(answer, range):
        return QuestionType.NUMERIC_RANGE
    if isinstance(answer, bool):
        return QuestionType.TRUE_FALSE
    if isinstance(answer, str):
        return QuestionType.SHORT_ANSWER
    # Booleans are never numeric ranges, so a bare ``True`` means true/false.
    # Anything else has no numeric bound, so case sensitivity is the only
    # signal left to distinguish a text answer from a true/false one.
    return QuestionType.TRUE_FALSE if case_insensitive else QuestionType.SHORT_ANSWER


def _coerce_answer(answer: object, question_type: QuestionType) -> AnswerValue:
    if isinstance(answer, range):
        return answer
    if question_type is QuestionType.NUMERIC_RANGE:
        try:
            return float(str(answer))
        except ValueError:
            return str(answer)
    return str(answer)


# =============================================================================
# Functional interface
# =============================================================================

def score_quiz(
    answers: list[str], key: list[str], case_sensitive: bool = True
) -> int:
    """Number of answers matching the key position-for-position."""
    short = min(len(answers), len(key))
    return sum(
        1
        for a, k in zip(answers[:short], key[:short], strict=False)
        if _normalize(a, case_sensitive) == _normalize(k, case_sensitive)
    )


def score_percentage(
    answers: list[str], key: list[str], case_sensitive: bool = True
) -> float:
    """Percentage of the key answered correctly (0.0 when the key is empty)."""
    if not key:
        return 0.0
    return round(100.0 * score_quiz(answers, key, case_sensitive) / len(key), 2)


def letter_grade(percentage: float) -> str:
    """Standard letter grade for a percentage."""
    for grade, floor in sorted(
        DEFAULT_GRADING_SCALE.items(), key=lambda item: -item[1]
    ):
        if percentage >= floor * 100:
            return grade
    return "F"


def build_quiz(questions: list[dict[str, Any]]) -> Quiz:
    """Build a quiz from plain dictionaries (used by the demo)."""
    quiz = Quiz(name="built")
    for spec in questions:
        quiz.add_question(
            text=spec["text"],
            correct_answer=spec.get("answer", ""),
            type=spec.get("type", QuestionType.SHORT_ANSWER),
            points=float(spec.get("points", 1.0)),
            case_insensitive=bool(spec.get("case_insensitive", False)),
        )
    return quiz


# =============================================================================
# Example Usage & Demo
# =============================================================================

if __name__ == "__main__":
    print("=== Kata07: How'd I Do? - Demo ===\n")

    # 1. The README example.
    quiz = Quiz()
    quiz.add_question("What is 2+2?", "4", type="short")
    quiz.add_question("Capital of France?", "Paris", type="short", case_insensitive=True)
    report = quiz.score({"What is 2+2?": "4", "Capital of France?": "paris"})
    print(f"README example: {report.summary()}")

    # 2. A richer quiz covering every question type.
    engine = HowdIDo(name="mixed")
    engine.add_question("Sky colour?", "blue", type="choice")
    engine.add_question("2+2=4?", True, type="true_false")
    engine.add_question("Capital of France?", "Paris", case_insensitive=True)
    engine.add_question("Mass of Earth (kg)", range(5_972, 5_974), type="numeric")
    engine.add_question("Name a planet", "Mars", type="bonus")

    answers = {
        "Sky colour?": "blue",
        "2+2=4?": "True",
        "Capital of France?": "Paris, the capital",
        "Mass of Earth (kg)": "5972.2",
        "Name a planet": "Mars",
    }
    print(engine.report(answers))
    print(f"Letter grade: {engine.grade(answers, GradingScale.LETTER)}")
    print(f"GPA:          {engine.grade(answers, GradingScale.GPA)}")

    # 3. The functional positional interface.
    key = ["4", "Paris", "Saturn"]
    given = ["4", "paris", "Jupiter"]
    print(f"\nPositional score (case-sensitive): {score_quiz(given, key)}/3")
    print(f"Positional score (case-insensitive): {score_quiz(given, key, False)}/3")
    print(f"Percentage: {score_percentage(given, key)}%")

    # 4. An unanswered question is reported, not silently ignored.
    partial = engine.score({"Sky colour?": "blue"})
    print(f"\nPartial attempt: {partial.summary()}")
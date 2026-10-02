"""Tests for kata07-howd-i-do."""

from kata07_howd_i_do import (
    DEFAULT_GRADING_SCALE,
    GradingScale,
    HowdIDo,
    InMemoryQuizRepository,
    Question,
    QuestionType,
    Quiz,
    QuizService,
    ScoreReport,
    build_quiz,
    letter_grade,
    score_percentage,
    score_quiz,
)


class TestHowdIDo:
    """Test cases for kata07-howd-i-do."""

    def test_basic_case(self):
        """Score the README example."""
        quiz = Quiz()
        quiz.add_question("What is 2+2?", "4", type="short")
        quiz.add_question(
            "Capital of France?", "Paris", type="short", case_insensitive=True
        )

        report = quiz.score({"What is 2+2?": "4", "Capital of France?": "paris"})

        assert report.correct_count == 2
        assert report.wrong_questions == []
        assert report.summary() == "Score: 2/2 (100%) - A"

    def test_edge_cases(self):
        """Empty quizzes, unanswered and unexpected answers."""
        empty = Quiz()
        assert empty.score({}).percentage == 0.0

        quiz = Quiz()
        quiz.add_question("One?", "1")

        # Unanswered questions are reported rather than silently skipped.
        report = quiz.score({})
        assert report.correct_count == 0
        assert report.unanswered == ("One?",)
        assert "not answered" in report.report()

        # Answers for questions that do not exist are ignored.
        assert quiz.score({"One?": "1", "Ghost?": "boo"}).percentage == 100.0

    def test_tdd_progression(self):
        """Grow from exact match to typed questions, partial credit and grades."""
        # Step 1: multiple choice is an exact match.
        quiz = Quiz()
        quiz.add_question("Sky colour?", "blue", type="choice")
        assert quiz.score({"Sky colour?": "blue"}).correct_count == 1
        assert quiz.score({"Sky colour?": "Blue"}).correct_count == 1
        assert quiz.score({"Sky colour?": "green"}).correct_count == 0

        # Step 2: short answers respect case sensitivity by default.
        quiz = Quiz()
        quiz.add_question("Capital of France?", "Paris")
        assert quiz.score({"Capital of France?": "paris"}).correct_count == 0
        assert quiz.score({"Capital of France?": "Paris"}).correct_count == 1

        # Step 3: a longer answer containing the key earns partial credit.
        close = quiz.score({"Capital of France?": "Paris, the capital"})
        assert close.partial_count == 1
        assert 0 < close.total_points < 1

        # Step 4: weighted questions move the needle more.
        weighted = Quiz()
        weighted.add_question("Hard?", "yes", points=3)
        weighted.add_question("Easy?", "yes")
        assert weighted.score({"Hard?": "yes", "Easy?": "no"}).percentage == 75.0

        # Step 5: grades summarise the score.
        assert weighted.score({"Hard?": "yes", "Easy?": "yes"}).letter_grade() == "A"
        assert weighted.score({"Hard?": "no", "Easy?": "no"}).letter_grade() == "F"


class TestQuestionTypes:
    """Each question type marks answers the way a teacher would."""

    def test_true_false_accepts_common_spellings(self):
        question = Question("2+2=4?", True, QuestionType.TRUE_FALSE)

        assert question.evaluate("true") == 1.0
        assert question.evaluate("True") == 1.0
        assert question.evaluate("false") == 0.0

    def test_multiple_choice_is_exact_but_case_insensitive(self):
        question = Question("Sky colour?", "Blue", QuestionType.MULTIPLE_CHOICE)

        assert question.evaluate("blue") == 1.0
        assert question.evaluate("BLUE") == 1.0
        assert question.evaluate("green") == 0.0

    def test_short_answer_contains_the_key_gets_partial_credit(self):
        question = Question("Capital of France?", "Paris", QuestionType.SHORT_ANSWER)

        assert question.evaluate("Paris") == 1.0
        assert question.evaluate("Paris, the capital") == question.credit_threshold
        assert question.evaluate("London") == 0.0

    def test_numeric_range_credits_closeness(self):
        question = Question(
            "Mass of Earth (kg)", range(5_972, 5_973), QuestionType.NUMERIC_RANGE
        )

        assert question.evaluate("5972.5") == 1.0
        assert question.evaluate("5972") == 1.0
        assert question.evaluate("6000") == 0.0
        # A closed interval has a single midpoint, so distance earns partial
        # credit rather than a flat full mark.
        closed = Question(
            "Penguin weight (kg)", range(30, 40), QuestionType.NUMERIC_RANGE
        )
        assert closed.evaluate("35") == 1.0
        assert 0.0 < closed.evaluate("32") < 1.0
        assert closed.evaluate("10") == 0.0
        assert question.evaluate("not a number") == 0.0

    def test_bonus_question_adds_its_bonus_points(self):
        question = Question("Name a planet", "Mars", QuestionType.BONUS, points=1.0)

        assert question.worth == 2.0
        assert question.evaluate("Mars") == 1.0

    def test_type_defaults_from_the_answer_shape(self):
        session = Quiz()
        assert session.add_question("A?", "a").type is QuestionType.SHORT_ANSWER
        assert session.add_question("B?", range(1, 3)).type is QuestionType.NUMERIC_RANGE
        assert session.add_question("C?", True).type is QuestionType.TRUE_FALSE

    def test_question_rejects_invalid_configuration(self):
        for build in (
            lambda: Question("", "a"),
            lambda: Question("A?", "a", points=0),
            lambda: Question("A?", "a", credit_threshold=1.5),
        ):
            try:
                build()
            except ValueError:
                pass
            else:
                raise AssertionError("invalid Question should raise ValueError")


class TestScoringRules:
    """Weighting, bonus points, partial credit and unanswered questions."""

    def test_weighted_questions_contribute_proportionally(self):
        quiz = Quiz()
        quiz.add_question("Hard?", "yes", points=3)
        quiz.add_question("Easy?", "yes")

        report = quiz.score({"Hard?": "yes", "Easy?": "no"})

        assert report.total_points == 3.0
        assert report.percentage == 75.0

    def test_bonus_points_can_lift_the_score_above_the_base_total(self):
        quiz = Quiz()
        quiz.add_question("Q1?", "a", points=1)
        quiz.add_question("Q2?", "b", points=1)
        quiz.add_question("Bonus?", "c", type="bonus", bonus_points=2)

        report = quiz.score({"Q1?": "a", "Q2?": "b", "Bonus?": "c"})

        assert report.base_points == 2.0
        assert report.total_points == 5.0
        # A perfect paper never reports more than 100%.
        assert report.percentage == 100.0

    def test_partial_credit_is_reflected_in_points_and_report(self):
        quiz = Quiz()
        quiz.add_question("Capital of France?", "Paris")

        report = quiz.score({"Capital of France?": "Paris is the capital"})

        assert report.partial_count == 1
        assert report.correct_count == 0
        assert report.wrong_questions == ["Capital of France?"]
        assert "partial credit" in report.report()

    def test_report_lists_every_question_not_fully_correct(self):
        quiz = Quiz()
        quiz.add_question("Right?", "yes")
        quiz.add_question("Wrong?", "yes")
        quiz.add_question("Skipped?", "yes")

        report = quiz.score({"Right?": "yes", "Wrong?": "no"})

        assert report.correct_count == 1
        assert report.incorrect_count == 1
        assert report.unanswered == ("Skipped?",)
        assert report.wrong_questions == ["Wrong?", "Skipped?"]

        text = report.report()
        assert "Wrong?" in text
        assert "Skipped?" in text
        assert "Right?" not in text

    def test_report_says_when_everything_is_right(self):
        quiz = Quiz()
        quiz.add_question("Q?", "a")

        report = quiz.score({"Q?": "a"})

        assert report.unanswered == ()
        assert "All questions answered correctly." in report.report()


class TestGradingScales:
    """Percentage, letter and GPA views of the same score."""

    def test_percentage_letter_and_gpa_agree(self):
        quiz = Quiz()
        for i in range(10):
            quiz.add_question(f"Q{i}?", "a")

        answers = {f"Q{i}?": ("a" if i < 9 else "b") for i in range(10)}
        report = quiz.score(answers)

        assert report.percentage == 90.0
        assert report.letter_grade() == "A"
        assert report.gpa() == 4.0
        assert report.grade(GradingScale.PERCENTAGE) == 90.0
        assert report.grade(GradingScale.LETTER) == "A"
        assert report.grade(GradingScale.GPA) == 4.0

    def test_letter_grade_boundaries(self):
        assert letter_grade(100) == "A"
        assert letter_grade(90) == "A"
        assert letter_grade(89.99) == "B"
        assert letter_grade(70) == "C"
        assert letter_grade(69.99) == "D"
        assert letter_grade(59.99) == "F"

    def test_custom_grading_scale_is_honoured(self):
        strict = {"A": 0.95, "F": 0.0}
        quiz = Quiz()
        for i in range(10):
            quiz.add_question(f"Q{i}?", "a")
        report = quiz.score({f"Q{i}?": ("a" if i < 9 else "b") for i in range(10)})

        assert report.percentage == 90.0
        assert report.letter_grade(strict) == "F"
        assert report.letter_grade(DEFAULT_GRADING_SCALE) == "A"

    def test_empty_score_grades_as_zero(self):
        report = QuizService().grade([], {})

        assert report.percentage == 0.0
        assert report.letter_grade() == "F"
        assert report.gpa() == 0.0


class TestArchitecture:
    """DDD / CQRS / Repository wiring."""

    def test_questions_are_stored_in_the_repository(self):
        engine = HowdIDo(name="stored")
        engine.add_question("Q1?", "a")
        engine.add_question("Q2?", "b")

        repository = InMemoryQuizRepository()
        assert len(repository) == 0  # a fresh repository is independent

        stored = engine._repository.get("stored")
        assert stored is not None
        assert len(stored) == 2

    def test_score_command_grades_the_stored_quiz(self):
        engine = HowdIDo(name="cmd")
        engine.add_question("Q1?", "a")
        engine.add_question("Q2?", "b")

        report = engine.score({"Q1?": "a", "Q2?": "c"})

        assert report.correct_count == 1
        assert report.percentage == 50.0

    def test_query_reports_and_grades_the_stored_quiz(self):
        engine = HowdIDo(name="query")
        engine.add_question("Q1?", "a")

        assert engine.score({"Q1?": "a"}).correct_count == 1
        assert engine.grade({"Q1?": "a"}, GradingScale.LETTER) == "A"
        assert "Q1?" in engine.report({"Q1?": "b"})

    def test_scoring_an_unknown_quiz_is_empty(self):
        report = HowdIDo(name="known").score({"Q1?": "a"})

        assert report.results == ()
        assert report.percentage == 0.0

    def test_service_is_shared_by_both_handlers(self):
        engine = HowdIDo(name="shared")
        engine.add_question("Q1?", "Paris", case_insensitive=True)

        assert engine.score({"Q1?": "paris"}).correct_count == 1

    def test_quizzes_are_independent(self):
        first = HowdIDo(name="first")
        second = HowdIDo(name="second")
        first.add_question("Q1?", "a")
        second.add_question("Q1?", "b")

        assert first.score({"Q1?": "a"}).correct_count == 1
        assert second.score({"Q1?": "a"}).correct_count == 0


class TestFunctionalInterface:
    """Module-level helpers mirror the facade."""

    def test_positional_score_quiz(self):
        key = ["4", "Paris", "Saturn"]

        assert score_quiz(["4", "Paris", "Saturn"], key) == 3
        assert score_quiz(["4", "paris", "Jupiter"], key) == 1
        assert score_quiz(["4", "paris", "Jupiter"], key, case_sensitive=False) == 2

    def test_score_quiz_tolerates_short_and_long_answers(self):
        key = ["a", "b", "c"]

        assert score_quiz(["a", "b"], key) == 2
        assert score_quiz(["a", "b", "c", "d"], key) == 3
        assert score_quiz([], key) == 0

    def test_score_percentage(self):
        assert score_percentage(["a", "b", "c", "d"], ["a", "b", "c", "x"]) == 75.0
        assert score_percentage([], []) == 0.0

    def test_build_quiz_from_plain_dictionaries(self):
        quiz = build_quiz(
            [
                {"text": "Q1?", "answer": "a"},
                {"text": "Q2?", "answer": "b", "points": 2.0},
            ]
        )

        assert len(quiz) == 2
        report = quiz.score({"Q1?": "a", "Q2?": "x"})
        assert report.total_points == 1.0
        assert report.percentage == 33.33

    def test_report_is_a_string_for_an_unused_quiz(self):
        report = ScoreReport()

        assert report.summary() == "Score: 0/0 (0%) - F"
        assert report.report() == "Score: 0/0 (0%) - F"
        assert report.results == ()


class TestQuizScale:
    """Behaves on a large, repetitive quiz."""

    def test_scores_a_large_quiz(self):
        quiz = Quiz()
        total = 500
        for i in range(total):
            quiz.add_question(f"Q{i}?", "yes")

        answers = {f"Q{i}?": ("yes" if i % 2 == 0 else "no") for i in range(total)}
        report = quiz.score(answers)

        assert report.correct_count == total // 2
        assert report.incorrect_count == total // 2
        assert report.percentage == 50.0
        assert len(report.wrong_questions) == total // 2

    def test_weighting_a_large_quiz_is_additive(self):
        quiz = Quiz()
        for i in range(100):
            quiz.add_question(f"Q{i}?", "yes", points=float(i + 1))

        report = quiz.score({})
        assert report.unanswered == tuple(f"Q{i}?" for i in range(100))
        assert report.total_points == 0.0
        assert report.percentage == 0.0
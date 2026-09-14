"""Tests for the prompt builder module."""

from prompts.prompts import (
    build_summary_prompt,
    build_quiz_prompt,
    build_explain_prompt,
    build_improve_prompt,
)

SAMPLE_NOTES = (
    "Photosynthesis is the process by which green plants and some other "
    "organisms use sunlight to synthesize foods from carbon dioxide and water. "
    "It generally involves the green pigment chlorophyll and generates oxygen "
    "as a byproduct."
)


class TestBuildSummaryPrompt:
    """Test suite for build_summary_prompt()."""

    def test_returns_string(self):
        result = build_summary_prompt(SAMPLE_NOTES)
        assert isinstance(result, str)

    def test_contains_student_notes(self):
        result = build_summary_prompt(SAMPLE_NOTES)
        assert SAMPLE_NOTES in result

    def test_contains_role_instruction(self):
        result = build_summary_prompt(SAMPLE_NOTES)
        assert "academic assistant" in result.lower()

    def test_asks_for_summary_format(self):
        result = build_summary_prompt(SAMPLE_NOTES)
        prompt_lower = result.lower()
        assert "bullet" in prompt_lower or "heading" in prompt_lower

    def test_asks_for_key_concepts(self):
        result = build_summary_prompt(SAMPLE_NOTES)
        assert "key concept" in result.lower()


class TestBuildQuizPrompt:
    """Test suite for build_quiz_prompt()."""

    def test_returns_string(self):
        result = build_quiz_prompt(SAMPLE_NOTES)
        assert isinstance(result, str)

    def test_contains_student_notes(self):
        result = build_quiz_prompt(SAMPLE_NOTES)
        assert SAMPLE_NOTES in result

    def test_default_question_count(self):
        result = build_quiz_prompt(SAMPLE_NOTES)
        assert "5" in result

    def test_custom_question_count(self):
        result = build_quiz_prompt(SAMPLE_NOTES, num_questions=8)
        assert "8" in result

    def test_specifies_mcq_format(self):
        result = build_quiz_prompt(SAMPLE_NOTES)
        prompt_lower = result.lower()
        assert "multiple-choice" in prompt_lower or "mcq" in prompt_lower

    def test_asks_for_answer_key(self):
        result = build_quiz_prompt(SAMPLE_NOTES)
        assert "Answer Key" in result

    def test_specifies_four_options(self):
        result = build_quiz_prompt(SAMPLE_NOTES)
        assert "A)" in result and "B)" in result and "C)" in result and "D)" in result


class TestBuildExplainPrompt:
    """Test suite for build_explain_prompt()."""

    def test_returns_string(self):
        result = build_explain_prompt("recursion")
        assert isinstance(result, str)

    def test_contains_concept(self):
        result = build_explain_prompt("recursion in programming")
        assert "recursion in programming" in result

    def test_asks_for_analogy(self):
        result = build_explain_prompt("recursion")
        assert "analogy" in result.lower() or "example" in result.lower()

    def test_asks_for_simple_language(self):
        result = build_explain_prompt("recursion")
        assert "simple" in result.lower()

    def test_asks_for_key_points(self):
        result = build_explain_prompt("recursion")
        assert "key point" in result.lower() or "remember" in result.lower()


class TestBuildImprovePrompt:
    """Test suite for build_improve_prompt()."""

    def test_returns_string(self):
        result = build_improve_prompt("my answer text here is long enough")
        assert isinstance(result, str)

    def test_contains_answer(self):
        answer = "Photosynthesis converts sunlight to energy."
        result = build_improve_prompt(answer)
        assert answer in result

    def test_without_question(self):
        result = build_improve_prompt("my answer text here")
        assert "Original Question" not in result

    def test_with_question(self):
        result = build_improve_prompt("my answer", "What is photosynthesis?")
        assert "Original Question" in result
        assert "What is photosynthesis?" in result

    def test_empty_question_treated_as_no_question(self):
        result = build_improve_prompt("my answer", "   ")
        assert "Original Question" not in result

    def test_preserves_student_ideas(self):
        result = build_improve_prompt("my answer")
        assert "preserve" in result.lower() or "original" in result.lower()

    def test_asks_for_tips(self):
        result = build_improve_prompt("my answer")
        assert "tip" in result.lower() or "improved" in result.lower()

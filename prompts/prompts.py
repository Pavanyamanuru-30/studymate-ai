def build_summary_prompt(notes: str) -> str:
    """
    Build a structured prompt for summarizing student lecture notes.

    The prompt instructs the LLM to produce a clear, organized summary
    with headings, bullet points, and highlighted key concepts.
    """
    return f"""You are a helpful academic assistant. A student has shared their lecture notes below.

Your task:
- Summarize the notes in a clear, structured format.
- Use bullet points and headings where appropriate.
- Highlight key concepts, definitions, and important details.
- Keep the summary concise but comprehensive.
- Use simple language that a student can quickly revise from.

---

**Student's Lecture Notes:**

{notes}

---

**Structured Summary:**"""


def build_quiz_prompt(notes: str, num_questions: int = 5) -> str:
    """
    Build a structured prompt for generating a quiz from student notes.

    The prompt instructs the LLM to create multiple-choice questions
    with answers and brief explanations.
    """
    return f"""You are a helpful academic assistant and quiz master. A student has shared their lecture notes below.

Your task:
- Generate exactly {num_questions} multiple-choice questions (MCQs) based on the notes.
- Each question should test understanding of a key concept from the notes.
- Provide 4 options (A, B, C, D) for each question.
- After all questions, provide an **Answer Key** with the correct answer and a one-line explanation for each.

Use this format for each question:

**Q1.** [Question text]
- A) [Option A]
- B) [Option B]
- C) [Option C]
- D) [Option D]

After all questions, add:

---

**Answer Key:**
1. [Correct letter] — [Brief explanation]
2. [Correct letter] — [Brief explanation]
...

---

**Student's Lecture Notes:**

{notes}

---

**Quiz:**"""


def build_explain_prompt(concept: str) -> str:
    """
    Build a structured prompt for explaining a concept to a student.

    The prompt instructs the LLM to break down a topic in simple,
    student-friendly language with examples and analogies.
    """
    return f"""You are a patient, knowledgeable tutor. A student wants to understand a concept.

Your task:
- Explain the concept in simple, clear language that a student can easily understand.
- Start with a one-line definition.
- Then provide a more detailed explanation broken into logical parts.
- Use a real-world analogy or relatable example to make it intuitive.
- Mention 2-3 key points the student should remember.
- If relevant, briefly note why this concept matters or where it's applied.

---

**Concept to explain:**

{concept}

---

**Explanation:**"""


def build_improve_prompt(answer: str, question: str = "") -> str:
    """
    Build a structured prompt for improving a student's written answer.

    The prompt instructs the LLM to enhance the answer's clarity,
    structure, accuracy, and academic tone while preserving the student's
    original ideas.
    """
    context = ""
    if question.strip():
        context = f"""**Original Question:**

{question}

"""

    return f"""You are an academic writing coach. A student has written an answer and wants to improve it.

Your task:
- Improve the answer for clarity, structure, completeness, and academic tone.
- Preserve the student's original ideas — don't change the meaning.
- Fix any grammatical or factual errors.
- Add structure with paragraphs or bullet points if needed.
- At the end, provide 2-3 brief tips on what was improved and why.

---

{context}**Student's Original Answer:**

{answer}

---

**Improved Answer:**"""

def build_rag_prompt(query: str, context: str) -> str:
    """
    Build a structured prompt for grounded document Q&A.
    """
    return f"""You are a helpful, accurate study assistant. 
Your task is to answer the student's question based strictly on the provided document context.

# INSTRUCTIONS:
1. Answer the question using ONLY the provided context below.
2. If the context does not contain the answer, politely state: "I cannot find the answer to this in the provided document." Do not guess or use outside knowledge.
3. Be concise, clear, and professional.

# DOCUMENT CONTEXT:
---
{context}
---

# STUDENT QUESTION:
---
{query}
---"""

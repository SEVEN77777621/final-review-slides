# Mock-exam generation

Generate a mock exam only when the user requests it or assessment sources provide enough evidence. Evidence priority for format and emphasis is: explicit Revision/syllabus statements, past exams, quizzes/assignments, then lecture examples. Label unsupported timing, marks, or format choices as simulation assumptions.

Build `mock-exam-blueprint.md` first. Map every planned question to concept IDs, evidence, type, difficulty, marks, and source range. Prefer new questions and meaningful variants; do not reproduce source questions verbatim unless requested and permitted.

Use a course-appropriate mix such as single-choice, definitions, comparisons, calculations, derivations, applications, protocol traces, security analysis, attacks, or repairs. Distractors must reflect plausible misconceptions. A single-choice question must have exactly one best answer.

Keep the question paper free of solutions and revealing citations. In the separate solutions document give the model answer, reasoning or working, marking points, common errors, difficulty, assessed concept IDs, and citations. Verify calculations, formulas, protocol sequences, and every claimed answer against source evidence.

Before passing, check: all questions are answerable from supplied course material; topic and difficulty distribution match the blueprint; explicit Revision priorities are represented; no unsupported content appears; choice keys are unique; total marks add correctly; answers do not leak into the question paper; and citations resolve to supporting pages.

## Carriers

The question paper and the solution booklet each ship in three carriers: PDF (LaTeX), Word `.docx` via `scripts/color_docx.py`, and a self-contained HTML per `references/html-color-review.md`.

- The question paper (in every carrier) stays free of solutions, marking points, and citations that reveal answers.
- The solution booklet carries the model answer, reasoning/working, marking points, common errors, difficulty, assessed concept IDs, and citations.
- HTML mock-exam files reuse the template CSS: questions as list/`.kv` items, options as plain lines, and the answer key plus reasoning in a `.tip`/`.warn`-style block. Keep the question file and solution file separate.
- Distractor plausibility, single-best-answer uniqueness, mark totals, and answer/paper separation are checked the same way across every carrier.

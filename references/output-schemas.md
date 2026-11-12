# Output schemas

## Color coding

Apply the five-color scheme defined in SKILL.md: blue `concept`, green `number`, orange `mechanism`, red `trap`, yellow `conclusion`. PDFs use `assets/color-style.tex`; Word `.docx` handouts use `scripts/color_docx.py`; HTML handouts use `assets/review-template.html` per `references/html-color-review.md`. Traps go in red boxes, conclusions and mnemonics in yellow boxes, causal mechanisms in orange boxes; key figures and metrics go in green number badges. Keep the same color-to-category mapping across every artifact.

## final-review

1. Course and source scope
2. Assessment evidence and Revision/Review priorities
3. Course map derived from `course-map.json` (Mermaid rendering or PDF-native fallback)
4. Chapters in strict lecture order
5. Per-chapter recap and source references
6. Cross-lecture dependency index

Each chapter follows the source sequence. For substantive concepts use supported fields: definition/original wording, intuition, purpose, mechanism or derivation, assumptions, boundary conditions, example/application, failure or attack mode, distinctions, assessment links, and citations. End with a recap. `comprehensive` is the default depth; headings or one-line mentions do not count as explanation.

## review-html

One self-contained `.html` quick-review handout (CSS/JS inlined, no framework). Structure:

1. Hero: title, scope subtitle, five-color legend chips.
2. Sticky capsule nav: anchor links to sections; every `href="#sN"` resolves to a unique `<section id="sN">`.
3. One card per source section: numbered head, collapsible body, left color bar by main kind; use blocks, kv pairs, tags, number badges, warn/tip boxes, flow chain, comparison table, and formula block as needed.
4. Footer: source note and collapse hint.

Content order, citations, and coverage status match the PDF/Word artifacts; the HTML presentation adds no unverified claims. Layout parameters, component classes, responsive rules, and screenshot QA are specified in `references/html-color-review.md`.

## mock-exam

The question paper contains instructions, time/marks only when evidenced or clearly labeled as simulated, questions, and no solutions or source citations that reveal answers. The separate solution paper contains for each question: model answer, working/reasoning, marking points, common errors, difficulty, assessed concept IDs, and tight source citations.

`mock-exam-blueprint.md` records evidence, assumptions, topic/type/difficulty/marks matrix, coverage, answerability checks, single-choice uniqueness checks, total-mark arithmetic, and final verdict.

Both the question paper and the solution booklet ship in PDF, editable `.docx`, and self-contained HTML; all carriers reuse the same five-color mapping, and the paper never leaks answers or revealing citations.

## quick-reference

Use compact tables organized for lookup. Suggested columns:

`item | definition/formula | symbols | assumptions/conditions | when to use | common trap | source`

For non-mathematical courses replace formulas with frameworks, cases, vocabulary, dates, arguments, or comparison criteria.

## mistakes-and-distinctions

Suggested sections:

- easily confused concept pairs
- invalid shortcuts and boundary conditions
- notation and terminology traps
- diagram/table interpretation errors
- recurring mistakes evidenced by assignments or assessments

Suggested columns:

`confusion | incorrect belief | correct distinction | diagnostic cue | counterexample | source`

## coverage-report

Include:

- source inventory and resolved order
- missing/duplicate/ambiguous source findings
- Revision/Review topics and where covered
- page/slide ledger summary by file and lecture
- visual-inspection counts and findings
- exclusions with reasons
- unresolved uncertainties
- citation spot-check results
- build and visual-QA results for each PDF
- HTML handout structure, responsive, and segmented-screenshot QA results when produced
- `.docx` handout build and open/parse check results when produced
- build-preflight result, selected backend, template mode, missing dependencies, and fallback attempts
- resolved language and depth modes
- mock-exam blueprint and validation results when applicable
- map renderer used and fallback reason when applicable
- final gate table with PASS/PARTIAL/FAIL and evidence

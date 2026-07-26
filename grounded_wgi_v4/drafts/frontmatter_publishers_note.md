<!-- model=claude-fable-5 (Claude Max subagent), stage=3 apparatus, date=2026-07-25 -->

# Publisher's Note to the Second Revised Edition

## What This Book Is — and Is Not

This volume is an **experimental, fully AI-generated assessment** in the style of an Intergovernmental Panel on Climate Change (IPCC) Working Group I report. It is **not an IPCC product**. It has no connection to, endorsement from, or review by the IPCC, the World Meteorological Organization, the United Nations Environment Programme, or any of the scientists who author genuine assessment reports. It is not peer-reviewed science. No claim in this book should be relied upon for policy, investment, safety, or academic purposes without independent verification against the primary literature.

We say this on the first page, in plain language, because radical transparency about machine generation is the founding principle of the Variant Earths imprint. Every chapter of this book was written by a large language model — Anthropic's Claude Fable 5 — operating inside a documented, reproducible pipeline whose every step is described in the Production Notes at the back of this volume and in our public repository.

Why publish such a thing at all? Because the question of what AI systems can and cannot do with the scientific literature is one of the most consequential open questions of this decade, and it deserves published, inspectable evidence rather than anecdote. A full-length assessment volume — with its calibrated language, its cross-chapter structure, its thousands of factual commitments — is among the most demanding nonfiction forms that exist. We publish these experiments so that readers, researchers, and critics can examine exactly what a frontier model produces under controlled, disclosed conditions.

## What Changed in the Second Revised Edition

The first edition of this volume (2026, ISBN 9781608887866) was what we now call a **parametric** build: the model wrote every chapter from its internal knowledge. Its citations were emitted during writing and checked only for internal consistency — never against the actual literature. That method produces fluent, often insightful assessment prose, but it inherits the well-known weakness of parametric generation: references that are plausible rather than verified.

This Second Revised Edition inverts the entire production order. It is a **source-first, grounded** build:

1. **Research came first.** Before a single sentence was drafted, we harvested a verified source database from OpenAlex, the open scholarly index: **1,506 unique, real, DOI-bearing works** (2,275 chapter-tagged source entries) published in the post-AR6 window, 2021–2026. Every entry in the database resolves to a locatable publication.

2. **Writing was constrained.** Each chapter's drafting agent received a numbered list of the top eighty most-cited works harvested for that chapter and was bound by a strict rule: cite *only* from the allowed list. If a claim could not be supported by an allowed source, the model was required to state it without a citation or omit it — never to recall a reference from memory, however famous.

3. **Every citation was machine-verified.** After drafting, an independent verification program matched every in-text author–year citation in every chapter against the source database, and every reference-list DOI against the harvested records. The build could not proceed with a single failure. The result across all ten chapters: **zero unverifiable citations and zero unknown DOIs.**

The consequence, visible throughout this edition, is a different texture of assessment. The grounded model makes *fewer, better-anchored* claims. Where its allowed sources are thin, it says less, or says it in an honest uncited assessment voice, rather than manufacturing support. We regard the contrast between the two editions — same model family, parametric versus grounded — as the most instructive artifact the Variant Earths program has yet produced, and we have preserved the first edition precisely so the two can be compared page against page.

## Why This Contrast Matters

Publishers, educators, and readers are being asked to absorb a rapidly growing volume of AI-assisted nonfiction. The uncomfortable truth is that most of it is parametric, and parametric text wears its confidence uniformly, whether or not the underlying knowledge is real. The grounded method demonstrated here is slower and stricter, and it visibly changes what the machine is willing to assert. If AI-generated nonfiction is to earn a place on serious shelves, we believe pipelines of this kind — research first, constrained writing, machine-verified citation — are the minimum standard, and we publish this edition as a working demonstration of that standard, limitations included.

Those limitations are real and are catalogued candidly in the Production Notes: automated harvesting admits some off-topic highly-cited works into the source pools, which reduced citation density in the affected chapters; the verification tooling imposes formatting constraints of its own; and no machine process substitutes for expert human review, which this book has not had.

## Edition History

- **First edition** (2026): parametric build, v3 pipeline. ISBN 9781608887866.
- **Second Revised Edition** (2026): source-first grounded build, v4 pipeline; all ten chapters redrafted against a verified source database; Summary for Policymakers and Technical Summary newly synthesized from the grounded chapters. ISBN 9798259506800.

## A Note on Rights

This book is **© 2026 Fred Zimmerman / Nimble Books LLC.** Although its text was generated by an AI system, it exists only because a human directed, constrained, edited, and took responsibility for its creation; the publisher claims copyright in the work on that basis.

Genuine IPCC assessment reports are themselves **copyrighted** works (© IPCC, published by Cambridge University Press) — they are **not** in the public domain. This volume neither reproduces nor derives its text from any IPCC report. It imitates only the *format and register* of a Working Group assessment; its substance is synthesized from a separately assembled corpus of independently published, openly indexed scholarly articles. "AR7" and "Working Group I" name the target format, nothing more.

— **Variant Earths**, an imprint of Nimble Books LLC

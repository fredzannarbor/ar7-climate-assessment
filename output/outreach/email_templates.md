# Email templates (critique-seeking)

Replace `{{NAME}}`, `{{GROUP}}`, `{{SPECIFIC_HOOK}}`, and the recipient address before sending.
All three keep the same spine: humble, non-IPCC, "please critique," small ask.

---

## Tier A — community

**Subject:** A small open experiment on LLMs + scientific synthesis — would value your community's critique

Hi {{NAME}} / {{GROUP}} organizers,

I run a tiny independent AI lab and recently did a small, fully reproducible experiment I
think your community might find worth picking apart. I gave seven LLMs the same task —
draft assessment-style scientific text in the *format* of an IPCC Working Group II report —
and then fact-checked and scored every chapter.

Two findings stood out: (1) the most verbose model was the *least* factually reliable
(~2.8× more flagged issues than a shorter, higher-scoring one), and (2) without prompt
enforcement, citation grounding was uniformly weak across all models.

Two things I want to be clear about up front: this is **not affiliated with or endorsed by
the IPCC**, and it's **not** a proposal to automate climate assessment — it's a measurement
of model behavior, with all the usual caveats (single LLM judge, no human-expert validation,
Nov-2025 model snapshot). I'd genuinely value critique of the method, and pointers to
related work.

Everything's open: https://github.com/fredzannarbor/ar7-climate-assessment
One-page brief and a short methods note are in the repo.

Is this something worth sharing with your list / at the workshop? Happy to write it up in
whatever form is most useful — or to just be told what I got wrong.

Thanks,
Fred Zimmerman
AI Lab for Book-Lovers, Nimble Books LLC

---

## Tier B — methods researcher

**Subject:** Verbosity vs. factuality in long-form LLM synthesis — a small reproducible probe + a request

Hi {{NAME}},

Your work on {{SPECIFIC_HOOK}} is part of why I'm writing. I ran a small, reproducible
experiment giving seven LLMs an IPCC-WGII-style drafting task and scoring the output, and
the cleanest result is one I suspect you'll have opinions about: on matched chapters, the
wordiest model drew ~2.8× more fact-check issues than a more concise model that scored
slightly higher — a "specificity paradox" where more concrete claims mean more chances to
be wrong. Citation grounding was also uniformly weak unless forced.

Caveats I'm not hiding from: a single LLM judge (I cite the self-preference/verbosity-bias
literature in the note), no human-expert validation, and a Nov-2025 model snapshot. It's a
measurement of behavior, not a claim about climate science, and it is not affiliated with
the IPCC.

I'd value your critique on two things specifically: (a) whether the single-judge design
fatally confounds the length finding, and (b) whether you know of prior work isolating
verbosity from factuality in long-form generation.

Methods note + code: https://github.com/fredzannarbor/ar7-climate-assessment

No pressure at all — even a one-line "this is confounded because X" would be useful.

Best,
Fred Zimmerman

---

## Tier C — journalist

**Subject:** Tip: the wordiest AI was the wrongest — small open experiment on LLMs + science

Hi {{NAME}},

Quick, low-key tip in case it's useful — and I'm leading with the caveats because they
matter. I ran a small independent experiment giving seven AI models the same task: draft
text in the *format* of an IPCC climate assessment. I then fact-checked everything. The
counter-intuitive result: the model that wrote the most made about 2.8× more factual errors
than a shorter one. And unless forced, none of them cited sources well — they produced
authoritative-sounding text untethered to anything checkable.

Important framing, because I don't want this misread: it is **not affiliated with the IPCC**,
**not** a claim that AI should write assessments, the output was never validated by a climate
scientist, and the scoring was done by another AI. It's a cautionary measurement, not a
breakthrough.

If the "more words, more errors / fluent but ungrounded" angle is interesting for an
AI-reliability story, everything is open and reproducible here:
https://github.com/fredzannarbor/ar7-climate-assessment

Happy to walk through the method or connect you with sharper critics of it.

Thanks,
Fred Zimmerman, Nimble Books LLC

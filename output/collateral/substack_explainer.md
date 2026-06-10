# Substack explainer

**Working title:** I asked seven AIs to write a climate assessment. The wordiest one was the wrongest.

---

There's a quiet assumption baked into a lot of "AI for science" enthusiasm: that if a
model writes more — more detail, more pages, more citations-that-look-like-citations —
it's doing more useful work. Last November I ran a small experiment that pokes a hole in
that assumption.

The setup was simple. I took the published author outline for an IPCC Working Group II
climate assessment and handed it, unchanged, to seven different large language models —
GPT-5, Gemini, Grok, Claude, Mixtral, Qwen, DeepSeek. Same prompt, same task: draft the
report. Then I scored every chapter two ways — overall quality, and a fact-check pass
that flagged errors as minor, major, or critical.

A quick, loud caveat before the fun part: **this is not a plan to replace the IPCC, and
I'm not claiming AI should write climate assessments.** The real assessment process is
slow, expert-run, and accountable precisely because the stakes are enormous. My experiment
measures how models *behave* on a hard task. Nothing here was checked by a climate
scientist, and the scores were assigned by another AI. So: interesting signal, not gospel.
And it's not affiliated with or endorsed by the IPCC.

## The finding

Here's the part I didn't expect. On the full run, the model that wrote the *most* —
about 160,000 words — got flagged with **roughly 2.8× more factual issues** than a model
that wrote less (about 141,000 words) and scored slightly *higher* overall.

More words. More mistakes. Not more reliability.

I think of it as a *specificity paradox*. Longer prose means more concrete claims —
specific dates, specific magnitudes, specific "in 2031, X will happen" assertions — and
every one of those is another chance to be confidently, precisely wrong. The shorter model
hedged less and committed to fewer falsifiable specifics, so it tripped fewer wires.

(The shortest model, for the record, failed the opposite way: it was too thin to assess.
There's a sweet spot, and "maximum verbosity" is past it.)

## The other finding, which worried me more

Unless I explicitly forced them to cite sources, *none* of the models cited well. They all
produced fluent, well-organized, official-sounding text — text that pattern-matches to
"authoritative scientific document" — while being largely untethered to anything you could
go check. That's the dangerous failure mode: not gibberish, but polished plausibility with
no roots.

## Why I'm sharing it

"More text = better" is a tempting shortcut when you're wiring up an AI research pipeline,
and it's wrong in a way that's easy to miss because the wrong output *looks* great. This
little experiment is a caution flag. I've open-sourced all the prompts, the scoring code,
and the rubric so you can re-run it, argue with it, swap in a better evaluator, or have an
actual domain expert grade the output (please do — I'd love that).

Code and methods write-up: https://github.com/fredzannarbor/ar7-climate-assessment

---

*From the AI Lab for Book-Lovers. If you build with LLMs, the takeaway is small and
practical: stop rewarding length. Reward what survives a fact-check.*

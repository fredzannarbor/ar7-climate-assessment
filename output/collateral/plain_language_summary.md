# Plain-language summary

**What we did.** We gave seven AI chatbots the same assignment: draft a long climate
report in the format of an IPCC assessment. Then we measured how they did — how good
the writing was, and how many facts they got wrong.

**The headline.** *The model that wrote the most was not the model that wrote the best.*
In fact, the most long-winded model made about **2.8× more factual errors** than a
shorter, more careful one — while scoring slightly worse overall. More words bought
more mistakes, not more reliability.

**The other lesson.** Unless we forced them to, none of the models cited their sources
well. They produced confident, polished, official-sounding text that wasn't actually
tied to real references. That's exactly the kind of thing that looks trustworthy and
isn't.

**What this is NOT.** This is not a tool for replacing the IPCC, and we're not claiming
AI should write climate assessments. It's a measurement experiment about how these
models behave on a hard task. None of the AI text was checked by a climate scientist,
and the scores were assigned by another AI — so read everything as "interesting signal,"
not "proven fact." It is not affiliated with or endorsed by the IPCC.

**Why share it.** "More text = better" is a tempting shortcut in AI pipelines. Our small,
fully reproducible experiment is a caution against it. All the prompts and code are open
so anyone can re-run, disagree, or improve on it.

Repo: https://github.com/fredzannarbor/ar7-climate-assessment

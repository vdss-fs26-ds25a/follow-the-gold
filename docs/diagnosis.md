---
title: "Diagnosis — Current State vs. Scrollytelling Target"
date: 2026-05-26
status: Phase 1 deliverable (review before Phase 2 starts)
---

# TL;DR

The current `deployment/app.py` is a **five-chapter dashboard with a chrome-themed skin**, not a scrollytelling piece. It has:

- A persistent sidebar (Year Range slider, Highlight Country dropdown) — the single most dashboard-defining UI element. Scrollytelling has **no sidebar**: the user scrolls, the story drives the state.
- Interactive widgets *inside* each chapter (radio buttons, multiselects, a year slider for the scatter) that ask the reader to do exploratory work. Scrollytelling does the exploratory work for the reader and *reveals* a result.
- Five charts arranged by **chart type variety** (choropleth, time series, scatter, grouped bar, share line, metric cards) rather than by narrative beats. The Quarto Charta still promises a Sankey for Chapter 4 — it does not exist in code. Doc and app drifted apart.
- Insight boxes that **state the question, hedge the answer, then change the subject**. There is no protagonist, no rising tension, no reveal, no ending sentence the reader leaves with.
- A "verdict" chapter that concludes "evidence broadly consistent with gold's safe-haven role" while the same app shows a Headline-CPI-vs-imports correlation labelled "Very Weak". The story contradicts itself.

On top of that, several charts present a **misleading picture** because of data-coverage gaps the project documents but does not honour visually (see §4). The combined effect is: a reader who scrolls through cannot answer the question on the title bar — *Is Gold Really the Safe Haven?* — except to shrug and say "kind of".

The good news: the underlying data does support a real story. It just isn't the story currently being told.

---

# 1. Requirements check against the Bewertungsraster

The instructor rubric (`Bewertungsraster Visualisierungsprojekt-3.pdf`) awards **20 points** across the criteria below. Verdict per row is mine, not the instructor's; quotes are verbatim from the rubric.

| # | Rubric item | Max | Current state | Verdict |
|---|---|---|---|---|
| 1 | "Präsentationsstil" | 2 | Not yet — presentation hasn't happened. Slides only planned in `project_charta.qmd` Phase 6. | Pending |
| 2 | "Formulierung der Projektziele und Erfolgskriterien" | 2 | Charta lists 5 RQs and a "Success Criteria" table (≥4 chart types, ≥2 interactions, ≥3 chapters, etc.). The criteria are **formal/quantitative** ("≥ 4 chart types"). None of them measure whether the visualisation *tells a story*. | **Weak.** Criteria measure ingredients, not whether the dish tastes like anything. |
| 3 | "Beschreibung der Zielgruppe(n)/Personas" | 2 | Two personas (Lena, 24, finance-curious student; Thomas, 52, financial advisor) — JTBD-style, well-written, plausible. | **OK.** This part is genuinely solid. |
| 4 | "Auswahl und Begründung / Konzipierung der Visualisierungselemente … Konsistenz mit Projektzielen und Bedürfnissen der Zielgruppe(n)" | 5 | Choropleth/scatter/bar/line/metric-cards. Justification in the Charta is brief ("we chose log scale because skew") and reads as *"we used variety because the rubric mentions ≥4 chart types"*. None of the charts are designed for **Lena's pains** ("can't tell neutral analysis from gold-seller marketing"). The Sankey promised to Thomas in the Charta doesn't exist. | **Weak — biggest risk area.** The 5 charts are not concepted *for* the personas; they are concepted *around* the data. |
| 5 | "Umsetzung und Verständlichkeit der Visualisierungselemente" | 5 | Charts render and are tooltip-clean. But the **scatter plot's headline number ("Correlation 0.12") directly contradicts the chapter's takeaway**. The time-series shows a clean jump 2016→2017 that is a *dataset switch artefact*, not a real economic event — and is not flagged on the chart. Türkiye appears twice in the choropleth (`Turkey` and mojibake `TÃ¼rkiye`). | **Below ceiling.** Verständlichkeit is the lever that costs the most points right now. |
| 6 | "Nachvollziehbarkeit und Reproduzierbarkeit des Codes" | 2 | `uv sync` + `streamlit run` works. `build_dataset.py` is one clean script. Repo is tidy after the recent restructure (commit `c8e360d`). | **OK.** |
| 7 | "Vollständigkeit von Project Charta und Data Report" | 2 | Charta is complete (with personas, plan, risks). Data report is detailed and honest about quality issues. **However:** the `viz_design_report.qmd` and `evaluation.qmd` are still the **template stubs** — placeholder sections, no project content. These two files alone could cost ≥1 point unless they are filled in (note: the assignment text says only Charta + Data Report are required, but the rubric line says "Project Charta and Data Report" — these two are safe). | **Charta + Data Report OK; the other docs are stubs and the README will need to follow whatever the app actually does.** |
| 8 | *Zusatzpunkt:* "Komplexität Datensatz" | +1 | Two real APIs joined (UN Comtrade Plus + Kaggle legacy + World Bank inflation), 192 k rows, schema decisions documented. | **Likely yes.** |
| 9 | *Zusatzpunkt:* "Umsetzung (Animationen, Bereitstellung, etc.)" | +1 | Deployed on Streamlit Cloud, GitHub Pages live. No animations / no scrollytelling polish. | **Half — deployment yes, animations no.** |

**Where the points bleed today: rows 4 (concepting) and 5 (implementation clarity).** That is the 10-point block we can actually move with this refactor. Row 7's stub documents are a free 1-point fix.

---

# 2. The scrollytelling gap

## What scrollytelling is (and what this app isn't)

A working definition, after Segel & Heer's *Narrative Visualization* (IEEE TVCG 2010) and Bostock's NYT pieces: the user **scrolls**, and at fixed points in their scroll the **visual state changes to reveal the next step of an argument the author is making**. The visual is not a panel for the user to query; it is a paragraph the user is reading. Author-driven, with reader-driven moments only where they add to the argument (Segel & Heer call this the *Martini Glass* structure: narrow start, narrow finish, wider exploration in the middle).

The current app is the opposite of that:

| Scrollytelling cue | Current app |
|---|---|
| **No sidebar.** The reader's controls are scroll-wheel and (optionally) one in-line interaction per beat. | Persistent sidebar with two global filters that **invalidate every chart's caption when changed**. |
| **State changes are bound to scroll.** Reaching paragraph 3 swaps the highlight; reaching paragraph 4 zooms in. | State changes are bound to widget clicks. Some widgets (e.g. `flow_type` Export in the Switzerland chapter) silently break the chart because Switzerland has no export rows in our dataset. |
| **One evolving visual is normal**. A choropleth that highlights different countries across beats often beats five charts. | Each chapter introduces a brand-new chart with new axes. The reader re-orients five times in ten paragraphs. |
| **Charts are annotated where the prose is making the point.** Arrows, callouts, labels on the chart itself. | Vertical dashed lines for "2008 Crisis", "COVID-19", "Inflation Wave" — but the 2008 line points to a global line whose pre-2017 values are missing for most reporters and the chart doesn't flag this. |
| **Greying-out** is the default emphasis tool. Everything not in this beat fades. | Every country is the same chrome-gold colour at all times. |
| **End on a sentence.** The last beat closes the argument. | Last beat is three more metric cards and a hedged paragraph that says, paraphrasing, *"sort of, but also not — more research needed"*. |

## How big is the gap?

Big. Removing the sidebar and inlining the controls would be a 30-minute change but would also unmask that **the chapters have no story sequence**. Each currently stands alone. You can read them in any order and lose nothing. That's a dashboard property, not a story property.

---

# 3. The narrative gap

The Charta states the project's central question as **"Is Gold Really the Safe Haven?"** and lists five research questions underneath. None of those five are a question whose answer would *change anyone's mind*:

> Where does gold flow during high-inflation periods?
> Do high-inflation countries import more gold?
> Is gold special, or do silver and platinum show the same patterns?
> What role does Switzerland play?
> Which type of inflation has the strongest link to gold trade?

These are **analyst questions**, not story questions. They have the form "tell me about X". A story question has the form "I bet you X — but watch what actually happens." Compare:

- "Do high-inflation countries import more gold?" → answer is yes/no/it depends. Reader nods, moves on.
- "When inflation hit in 2022, did the world actually buy more gold — or is that just what we tell ourselves?" → reader is now *in the experiment with you*.

### Protagonist?

There isn't one. The current app has five subjects (the world map, the global time series, the inflation scatter, the three metals, Switzerland) and no organising character. Switzerland appears in Chapter 4 as a curiosity rather than as the story's main character.

The data itself nominates two candidate protagonists:

1. **Switzerland.** ~20 % of global gold imports by value 2017–2024, peaked at 22 % in 2020 (COVID), drives a refining flow no other small country comes near. It is, however, **not visible at all in the pre-2017 panel** of our dataset — so a Swiss-protagonist arc has to either start in 2017 or pull pre-2017 evidence from a third source (the research notes' "70 % refining" number is from articles, not from our CSVs).
2. **China.** Gold imports doubled 2021 → 2022 ($39 B → $85 B), the same year Russia was sanctioned and central-bank gold buying hit a 70-year record. This is *exactly* the kind of "I bet you X but watch what happens" moment a story needs. It is also a much harder story for a finance-curious Swiss student persona to feel close to.

### Tension?

Zero. The Charta and the app's title both pose the safe-haven question and then **never genuinely entertain "no"**. The data offers a genuine "no": Venezuela (CPI 201 %) imported $0 of gold in 2022; Sudan (139 %) imported $251 M; Zimbabwe (105 %) imported $77 M. **The countries that supposedly need gold most don't buy it.** Meanwhile Switzerland, with 2.8 % CPI, imported $106 B. That's a tension worth a chapter. The current app shows it as a weak scatter correlation and moves on.

### Reveal?

None. Chapter 5 reads as a summary, not as an arrival. There is no moment of "oh — *that's* what was going on". The "Switzerland is a refining hub" line is offered as factoid, not as the answer to a setup planted three chapters earlier.

### Conclusion?

Hedged. "Evidence broadly consistent with gold's safe-haven role during periods of economic uncertainty." That sentence is true of essentially any dataset; it commits to nothing. A reader cannot retell it. A reader **needs to be able to retell it.**

---

# 4. The insight gap — what the data actually says vs. what the app says

This is the section the team should read most carefully. Several current charts present misleading framing because the dataset has a structural break at 2017 that is documented in the data report but not enforced in the visuals.

## 4.1 The dataset has two halves, and they are not comparable

`data/build_dataset.py` joins (1988–2016 Kaggle redistribution of UN Comtrade) with (2017–2024 UN Comtrade Plus extract). The two halves use different harmonisation revisions and **the older half is missing entire major reporters** for Gold:

```
Pre-2017 Gold imports (USD bn, from the joined CSV):
  Switzerland: NaN for every year before 2017
  USA, UK, UAE: NaN for every year before 2017
  China: 0.2–0.3 bn (implausibly low — clearly a coverage artefact, not a real flow)
  India: present and plausible (17–55 bn)
```

The global "Gold Import Value Over Time" chart (Chapter 2) therefore shows a clean jump from $151 B (2016) to $340 B (2017) **driven by reporting coverage, not by global flows.** The chart annotates this with a vertical line at "2008 Crisis" — and the pre-crisis values are a misleading aggregate of whichever reporters happened to be in the Kaggle dump.

**Implication for the refactor:** drawing global-aggregate trade-flow lines spanning 1988–2024 is dishonest given this data. Either (i) restrict the story to 2017–2024 where the panel is complete, or (ii) show the time series only for a single reporter with consistent coverage (India qualifies; the EU does in aggregate; few others do).

## 4.2 The Switzerland chapter is built on a dataset that starts 2017

The current Chapter 4 line chart annotates "2008", "COVID 2020" and "Inflation Wave 2022" as vertical dashed lines on a Swiss time series — but the **earliest Swiss data point in this dataset is 2017**. The "2008" annotation is on a chart whose 2008 value is missing. A reader who hovers gets nothing; a reader who doesn't hover assumes something happened in 2008 they can verify here.

Additionally, Switzerland has **zero Export rows** in the dataset, so the radio button "Flow Type: Export / Both" silently produces empty or misleading plots.

## 4.3 The scatter undermines the framing

Chapter 2's scatter (Headline CPI vs. log gold imports, 2022 default) computes a correlation of about 0.12 and labels it "Very Weak". The data backs this:

```
2022 — top inflation countries and their gold imports (USD M):
  Venezuela     CPI 201%   imports     $0
  Lebanon       CPI 189%   imports $1,118
  Sudan         CPI 139%   imports   $252
  Zimbabwe      CPI 105%   imports    $77
  Argentina     CPI  72%   imports     $3
  …
  Switzerland   CPI   2.8% imports $105,900
```

The framing "inflation drives gold imports" is **disconfirmed at exactly the moment of highest interest** — the 2022 inflation wave. The chart shows this honestly; the prose around it does not draw the obvious conclusion. *That conclusion is itself the most interesting thing in the project.* If high-inflation citizens aren't buying gold, then **who is** — and that question is the story's natural pivot to Switzerland-as-refining-hub and to central-bank purchases.

## 4.4 The "70 % Swiss refining share" number isn't in the data

The opening hero card reads `70 %  Swiss Refining Share`. This is a real figure from Aisosa's and Thiveja's research notes (sourced to the Substack / World Gold Council pieces). It is **not derivable from any CSV in the repo**. That is fine to cite — but it needs to be cited *as an external fact*, with a source link visible next to the number, not stamped under the headline. Right now a reader cannot tell which numbers come from "our data" and which from "an article we read".

## 4.5 The "Türkiye" / "Turkey" duplicate

The processed CSV contains both `Turkey` and the mojibake `TÃ¼rkiye` (UTF-8 mis-decoded as Latin-1). Both are aggregated separately in the choropleth and the bar charts. Not a story-killer, but the kind of detail that costs row-5 ("Verständlichkeit") points instantly when an instructor spots it.

---

# 5. What this means for the refactor

The recommendation, to be confirmed in Phase 2, is roughly this:

1. **Reframe the central question** away from the analyst question ("is gold an inflation hedge?") toward a story question that the data can actually win or lose ("when inflation hit in 2022, did the world buy more gold — and *who* exactly?").
2. **Pick a protagonist.** Switzerland is the natural one for the persona Lena, and we now know from the data that the Swiss panel is clean from 2017–2024 — squarely covering the COVID and 2022 inflation moments. China is the harder, more surprising protagonist, and the data also supports it.
3. **Cut the 1988–2016 panel from the visible story.** Use it once, in an early "the world before" beat if at all, with full coverage caveats. Build the main arc on 2017–2024 where the data is honest.
4. **Replace the sidebar with scroll-bound state changes.** No global year slider. No global country dropdown. One in-line interaction per beat, at most.
5. **Cut chapters down to beats. Each beat is: one paragraph + one chart that exists because of the paragraph.** Resist keeping all five current charts; the Sankey and the grouped-metal bar are the easiest cuts unless we find a beat that *needs* them.
6. **Annotate the charts on the chart.** Russia/Ukraine Feb 2022, Fed pivot, COVID March 2020, Gold ATH 2024 — written *on* the line, not as dashed vertical floaters.
7. **End on a sentence.** One specific number and one specific country. Something like: *"In 2022, the world bought a record \$541 B of gold. Almost a fifth of it went through Switzerland."*

Phase 2 (`docs/narrative_design.md`) will turn this into a concrete five-beat outline with the protagonist named, the beats wired, and the cuts marked. Phase 3 implements it. Phase 4 brings the Quarto docs into line.

---

# 6. Open decisions for the user before Phase 2 starts

1. **Protagonist:** Switzerland (familiar, persona-aligned, clean Swiss panel 2017–2024) or **China** (genuinely surprising — gold imports doubled in 2022, plausibly the story's natural reveal)? Or both, with Switzerland as our entry-camera and China as the second-half pivot?
2. **Time scope:** restrict the visible story to **2017–2024** (clean, honest, post the dataset break) or keep a single early-history beat using India / a curated subset?
3. **What to cut:** the Sankey is already cut from the code; do we also cut the gold-vs-silver-vs-platinum comparison if it doesn't fit the new arc, or keep it as a single sanity-check beat ("is this just a precious-metals thing, or is gold genuinely different?")?
4. **Conclusion line:** are we comfortable concluding "gold's safe-haven story is a Swiss-refinery and central-bank story, not a consumer-inflation story"? That is what the data actually supports. The Charta currently hedges away from a sharp conclusion; the rubric (row 4: *Konsistenz mit Projektzielen und Bedürfnissen der Zielgruppe(n)*) will reward sharpness.

Phase 2 will not start until the user weighs in on these.

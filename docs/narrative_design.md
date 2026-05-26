---
title: "Narrative Design — Follow the Gold"
date: 2026-05-26
status: Phase 2 deliverable (review before Phase 3 implementation)
supersedes: parts of project_charta.qmd (driving question + visualisation concept)
---

# Decisions taken in Phase 1 review

User confirmed on 2026-05-26:

- **Protagonist:** China.
- **Time scope:** 2017–2024 only. The 1988–2016 panel is cut from the visible story (it goes into the Data Report as honest disclosure, not into the app).
- **Cuts:** *"Everything on streamlit is shit — create it newly."* The existing `deployment/app.py` is treated as a write-off; the new app is built from scratch.
- **Conclusion:** sharp, committed position. No hedging.

---

# 1. The driving question

> **The advice has always been: "when inflation hits, buy gold." So when inflation actually hit in 2022 — the worst wave in 40 years — who bought the gold?**

That phrasing matters. It is not "is gold an inflation hedge?" (an analyst question that gets a yes / no / it depends shrug). It is a **whodunit**. The reader is invited to predict an answer — the high-inflation countries, presumably — and the data is going to disagree with that prediction.

The reveal: **it wasn't consumers in high-inflation countries. It was China. And China didn't buy gold because of inflation — China bought gold because the United States had just demonstrated, by freezing Russia's reserves, that the dollar is no longer politically neutral.**

That one sentence is what the reader leaves with.

---

# 2. The protagonist — and why China

Switzerland was the safer, more persona-aligned pick (Lena is Swiss; refining is a "home" angle). We rejected it because the surprise-per-paragraph ratio is lower. The Swiss story is essentially *"big number stays big number"* — Switzerland imports ~20 % of global gold every year, with a COVID bump and a steady high since. That is a fact, not a story.

China is sharper because three things line up *in the same year*, 2022, in our data:

| | 2021 | 2022 | Δ |
|---|---|---|---|
| China gold imports (USD bn) | 39.4 | **85.3** | **+116 %** |
| Headline CPI (China) | 0.9 % | 2.0 % | basically flat |
| (External, cited fact) Global central-bank gold purchases (tons) | 450 | **1,136** | **70-year record** |
| (External, cited fact) Russia central-bank reserves frozen by G7 | — | Feb 2022 | event |

China's gold imports doubled in the year that inflation peaked **and** the year that Russia got sanctioned. The Charta-era story said "this is the inflation hedge in action". The data, plus published central-bank purchase numbers, says **no — this is the post-sanctions central-bank de-dollarisation move, dressed up as an inflation story.**

That conclusion is defensible from our CSVs *combined with* the World Gold Council figures Aisosa and Thiveja already pulled. It is a real claim the project can stand behind in the presentation.

### What Switzerland still does in the arc

Switzerland is **not** the protagonist but it is **the establishing shot**. Switzerland is how the reader first orients to the map: "this small country handles a fifth of the world's gold". Then we move on. Switzerland comes back briefly at the end to close the loop ("the refinery doesn't care who's buying — it just refines").

---

# 3. The beat-by-beat outline

Five beats. Each beat is **one paragraph of prose + exactly one visual that exists because of that paragraph**. No widgets unless they serve the beat. The reader scrolls; the story moves.

The visual language: dark background, single gold accent colour (kept from the existing CSS — that part of the current app is fine), greyed-out non-focus elements, on-chart text labels, no legends unless unavoidable.

---

## Beat 1 — "Buy gold."

**Prose direction.** Set the cliché up to be broken. Two sentences max.

> *Every time inflation rises, the advice is the same: buy gold. In 2022, inflation hit its highest level in forty years — and gold importers worldwide spent a record \$541 billion bringing it across borders.*

**Visual.** Single line chart: global gold imports, 2017–2024. Greyed everywhere except 2022, which is the highlighted point. Annotation on the chart: **"\$541 B in 2022 — the year inflation peaked."** No axis decoration beyond what's needed. No sidebar, no widget.

**What the reader feels.** *Of course gold went up — that's the rule.* The reader thinks the story is over before it began. (This is the setup. We're about to take it back.)

**Source for the visual.** `precious_metals_trade_1988_2024.csv`, filtered to `metal_group == "Gold"` and `flow == "Import"`, summed by year, 2017–2024 only.

---

## Beat 2 — "But not in Caracas."

**Prose direction.** Disconfirm the consumer story, hard.

> *Here's the problem. In Venezuela, where inflation hit 201 % in 2022, gold imports were effectively zero. Zimbabwe, with 105 % inflation, imported \$77 million. Lebanon, 189 % — \$1.1 billion. None of these countries is on the list of large gold importers. The countries that the safe-haven story says should be buying gold the hardest are not buying it at all.*

**Visual.** A dot plot or annotated horizontal bar, **2022 only**, comparing 8–10 hand-picked countries: Venezuela, Lebanon, Sudan, Zimbabwe, Argentina, Iran on the high-inflation side; Switzerland, China, India, UAE on the low-inflation side. Two encodings:
- horizontal position = 2022 Headline CPI
- bar length = 2022 gold imports (log scale)

The visual punchline: **the bars don't track the inflation positions.** The high-inflation countries have invisible bars; the low-inflation countries have huge ones. Label every country on the chart itself.

**What the reader feels.** *Wait. So who actually bought it?* This is the story's first inflection point. The "buy gold" rule has just been broken at exactly the moment of maximum interest.

**Source.** Same CSV, year 2022, joined to `Headline CPI`. Curate the list of 10 countries by hand (filtering down from the scatter we already have to the ones that *make the point* clearly). No interactive year slider.

**Caveat to ship on-chart.** A small note: *Trade flows are not the same as private investment in gold ETFs or jewellery. We are measuring physical imports across borders.* That is the right caveat to have, and it should be visible.

---

## Beat 3 — "Then who?"

**Prose direction.** Show who *did* buy gold in 2022, and let the reader notice what those countries have in common (most have *low* inflation).

> *So who imported the \$541 billion of gold the world bought in 2022? At the top of the list: Switzerland, China, the UAE, the UK, India. Five countries took roughly two-thirds of the total. Four of the five had inflation rates of 5 % or below.*

**Visual.** Horizontal bar chart, top 8 importers in 2022 by USD value. Coloured by Headline CPI (a divergent or sequential ramp — pick a colourblind-safe palette, e.g. ColorBrewer YlOrRd). Switzerland and China are emphasised; the rest are the supporting cast.

**What the reader feels.** *These are the buyers? Most of them barely have inflation.* The story is now openly broken — and the reader is on the hook for the next answer.

**Source.** Same CSV, 2022, top 10 by `trade_value_usd`.

**Open question for implementation.** Whether to *also* show a choropleth at this beat. Probably no — a choropleth gives the same information less sharply than a ranked bar, and we don't need both. Save the map for Beat 4 where it pulls weight.

---

## Beat 4 — "China doubled down."

**Prose direction.** The reveal. China's gold imports doubled in 2022. Frame it in the political moment, not the inflation moment.

> *China's gold imports in 2021: \$39 billion. In 2022, the year inflation peaked: \$85 billion. A doubling, in one year. That same February, Russia invaded Ukraine — and the United States, the EU, and Japan froze about \$300 billion of Russia's foreign reserves. The signal to every other central bank was unambiguous: dollar reserves can be switched off. In 2022, central banks worldwide bought 1,136 tons of gold — the most since 1950.*

**Visual.** China's gold imports, 2017–2024, as a stepped bar or thick line. 2022 highlighted. Three annotations placed on the chart itself:

- **2020 H1** — *COVID. Imports collapse to \$9 B.*
- **2022 Feb 24** — *Russia invasion. G7 freezes Russian reserves.*
- **2022** — *Imports double. China central bank gold buying highest in 25 years.*

The 1,136-tons-of-central-bank-purchases number does **not** come from our CSVs — it comes from the World Gold Council figures Aisosa and Thiveja already cited in `summaries/aisosa_research.md`. It must be visibly cited *on the chart*, not silently dropped in. The chart shows trade flows; the citation shows the central-bank context.

**What the reader feels.** *Oh. This isn't about inflation. This is about Russia.*

**Source.** CSV for the China line. World Gold Council 2022 Annual Gold Demand Report and Aisosa's research notes for the central-bank number.

---

## Beat 5 — "Gold's safe-haven story isn't about inflation."

**Prose direction.** Land the position. One sentence. One number.

> *The "buy gold during inflation" story is a story about consumers. The 2022 data isn't. In 2022, the people in Caracas and Harare didn't buy gold; the central banks in Beijing, Abu Dhabi, and Ankara did. Gold's safe-haven role is alive — it's just no longer the citizen's safe haven against inflation. It's the sovereign's safe haven against the dollar.*

**Visual.** A small "recap" composite: three numbers stacked vertically.

- **+116 %** — *China's gold imports, 2021 → 2022*
- **\$0** — *Gold imported by Venezuela in 2022 (CPI 201 %)*
- **1,136 t** — *Central-bank gold purchases worldwide in 2022 — most since 1950*

No new chart. The third number is the external (cited) one; the first two come from our CSV. Closing source line at the bottom of the beat with the citations spelled out.

**What the reader feels.** They have the answer. They can re-tell it to a friend tomorrow. Specifically: they can say *"China doubled its gold imports the year Russia got sanctioned"* — and that is a single sentence that survives Persona Lena's "talk about it with friends" job.

---

# 4. What gets cut from the current app

- **Sidebar.** Entire sidebar removed. No global year-range slider. No global country highlighter.
- **Chapter 1 choropleth.** Removed. Beat 3 will use a ranked bar instead. (A map for the sake of having a map is exactly the kind of "look at the data" visual we are trying to leave behind.)
- **Chapter 2 time series + scatter.** Reworked: time series becomes Beat 1; scatter is replaced by the curated Beat 2 comparison.
- **Chapter 3 gold-vs-silver-vs-platinum.** Cut entirely. The three-metals comparison was a "for completeness" beat that does not serve the China arc. If we are asked for a 6th beat later, it could come back as a sanity-check inset, but it is not load-bearing.
- **Chapter 4 Swiss connection.** Cut as a chapter. Switzerland is briefly mentioned in Beat 3 ("Switzerland is the world's gold refinery") but does not get its own act.
- **Chapter 5 verdict metric cards.** Cut. Replaced by the three-number recap in Beat 5.
- **All in-chart widgets.** No `st.radio`, no `st.slider`, no `st.multiselect` *inside* the narrative. The story drives state, not the reader.

Net effect: the app shrinks from ~490 lines and 5 charts to a target of ~250 lines and 4 charts + one number stack, with no sidebar.

---

# 5. What new analysis / data work is needed

Most of the story works from `data/processed/precious_metals_trade_1988_2024.csv`. The following are new or changed:

1. **Restrict the visible data to 2017–2024** at load time. The pre-2017 rows stay in the CSV (the Data Report documents them) but the app filters them out before any chart is drawn. One-line change.
2. **Fix the `Turkey` / `TÃ¼rkiye` duplicate.** UTF-8 / Latin-1 mojibake in the joined CSV. Either (i) fix at the build step in `data/build_dataset.py` (preferred — `encoding="utf-8"` everywhere), or (ii) post-process in the app with a single `replace` call. Both rows must merge before Beat 2 / Beat 3 charts are drawn.
3. **Hand-curate Beat 2's country list.** A constant in the app: 10 named countries (5 high-inflation, 5 low-inflation), each with a one-word annotation. Not a `head(10)` slice — picked for the story.
4. **Add inline citations to external numbers.** Specifically the 1,136 tons (World Gold Council 2022 Annual Gold Demand Report, via Aisosa) and the ~70 % refining share if it appears at all (Substack source via Thiveja). These citations live in the app prose, not just in the Data Report.
5. **No new data sources are required.** We do not need to add gold price, ETF flow, or central-bank reserve data — the central-bank context is cited textually from Aisosa's research notes, which is honest and within scope.

---

# 6. How this maps back to the Bewertungsraster

| Rubric row | Lever this design pulls |
|---|---|
| Row 3 — Personas | Lena's "talk about it with friends" job is now achievable — the reader leaves with one transferrable sentence. Thomas's "neutral, data-backed evidence" need is met by the curated Beat 2 + cited central-bank context. |
| Row 4 — Konzipierung / Konsistenz | Every beat exists for a documented reason in this file. The Charta will be updated to point here so the rubric reviewer can trace beat → persona need → visual. |
| Row 5 — Verständlichkeit | On-chart labels, no surprising widgets, no global filter that invalidates the chapter's caption. The 2016 → 2017 dataset-break artefact is removed by scoping to 2017–2024. The Türkiye encoding bug is removed. |
| Row 7 — Vollständigkeit | `viz_design_report.qmd` and `evaluation.qmd` get filled in to reference this narrative + Segel & Heer's narrative-visualisation typology. |
| Zusatzpunkt — Umsetzung | The scrollytelling-via-Streamlit pattern (long single-page layout, scroll-bound emphasis, in-chart annotations) is the implementation novelty. We do not need scrollama.js or a custom React component to earn this point; the discipline of zero-widget, scroll-driven progression is the deliverable. |

---

# 7. Open implementation choices (decided in Phase 3)

These are intentionally left for the implementation step, not the design step. They are flagged here so they don't get forgotten:

- Should Beat 4 use a bar chart or a thick-line chart for China 2017–2024? (Lean: bar, because the year is the unit and "doubled" reads better as bar height.)
- Should Beat 3's ranked bar be coloured by CPI (sequential ramp) or just by `country == "China"` (single highlight)? (Lean: by CPI, to let the reader *see* that most top importers are low-CPI without us having to say it.)
- Beat 5's three-number block: stacked vertically, or in a row of three? (Lean: stacked, because vertical scroll matches the reading rhythm.)
- Whether to add a 6th, very short "method note" beat at the very end ("how we measured this") or fold it into the in-chart caveats. (Lean: fold into caveats.)

---

# 8. What we are explicitly *not* doing

- No price prediction.
- No investment advice.
- No "interactive explorer" mode after the verdict. The reader can scroll back up.
- No tabs, no navigation menu, no chapter index — scroll is the only navigation.
- No D3 / scrollama.js dependency unless Streamlit's vertical layout fails us; the design as written can be built with plain Streamlit + Plotly.

Phase 3 starts on user approval of this design.

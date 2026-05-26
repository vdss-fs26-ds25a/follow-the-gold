<h1>
<p align="center">
  <br> Global Precious Metals Trade and Inflation
  <p align="center">
  <a href="https://follow-the-gold-vdss.streamlit.app/"><img src="https://img.shields.io/badge/Live_App-Streamlit-red?logo=streamlit" alt="Live App"></a>
  <a href="https://vdss-fs26-ds25a.github.io/follow-the-gold/"><img src="https://img.shields.io/badge/Documentation-GitHub_Pages-blue?logo=github" alt="Documentation"></a>
</p>
</p>
</h1>


A single-page scrollytelling narrative answering one question: **when inflation hit in 2022, the worst wave in forty years, who actually bought the gold?**

The intuitive answer is "consumers in high-inflation countries". The country-level data, joining UN Comtrade gold-import flows with the World Bank Global Inflation Database, says otherwise: Venezuela (CPI 201 %) imported essentially zero; Zimbabwe (CPI 105 %) imported $77 M; meanwhile Switzerland, China, the UAE, the UK, and India (all low-inflation economies) took roughly two-thirds of global gold imports between them. **China's imports doubled in 2022**, the same year the G7 froze Russia's foreign reserves and the World Gold Council recorded the highest central-bank gold purchases since 1950.

The app walks a reader through this argument in five beats:

1. **Buy gold.** The cliché and the $541 B global figure for 2022.
2. **But not in Caracas.** The high-inflation countries did not buy.
3. **Then who?** Top-eight 2022 importers, coloured by inflation rate.
4. **China doubled down.** The reveal: China's gold imports, 2017–2024, framed against the Russia/Ukraine reserve freeze.
5. **The verdict.** Gold's safe-haven role is alive, but it is now the sovereign's hedge against the dollar, not the citizen's hedge against inflation.

Full driving question, persona analysis, success criteria, and beat-by-beat visualisation rationale are documented in [`docs/project_charta.qmd`](docs/project_charta.qmd). Data sources, catalogues, build steps, and quality findings are in [`docs/data_report.qmd`](docs/data_report.qmd).


## Data Sources

| Dataset | Source | Coverage |
|---|---|---|
| UN Global Commodity Trade Statistics | Kaggle (filtered to HS codes 7106–7112) | 1988–2016, ~10,000–50,000 rows after filtering |
| World Bank Global Inflation Database | Ha, Kose & Ohnsorge (2023) | 1970–2025, 209 countries × 6 inflation types |


## Project Structure

```
follow-the-gold/
├── data/              # Raw inputs + processed CSV used by the app
│   ├── raw/
│   ├── processed/
│   ├── build_dataset.py
│   └── country_mapping.py
├── deployment/        # Streamlit app (app.py + requirements.txt)
├── src/               # Shared utilities
└── docs/              # Quarto documentation (submitted artefacts)
    ├── project_charta.qmd
    ├── data_report.qmd
    └── summaries/     # Background research notes (not rendered to the site)
```


## Setup

**Requirements:** [uv](https://docs.astral.sh/uv/getting-started/installation/), [Quarto](https://quarto.org/docs/get-started/)

```bash
# Clone the repo and install dependencies
uv sync

# Run the Streamlit app
uv run streamlit run deployment/app.py

# Preview the documentation website
cd docs && uv run quarto preview
```

To add or remove packages:
```bash
uv add <package>
uv remove <package>
```


## Documentation (Quarto)

Source files are in `docs/`. To build and deploy:

```bash
cd docs
uv run quarto render    # builds to docs/build/, updates docs/_freeze
```

The documentation is deployed to GitHub Pages via GitHub Actions on every push to `main`. Python computations are cached in `docs/_freeze` (checked in), so the Actions runner does not need Python.

**Initial setup (once):** Go to **Settings > Pages** in the GitHub repo and set the source to **GitHub Actions**.


## Team

| Name | Role | Contact |
|---|---|---|
| Valentin Schwarz | Data Engineering: pipeline, repo structure | vschwarz@ik.me |
| Aisosa Omokaro | App Infrastructure: inflation data, Streamlit deployment | aisosashina@gmail.com |
| Thiveja Thirukumar | Documentation: research, data report, project charter | thiveja.thirukumar@gmail.com |


## License

See [LICENSE](LICENSE).

# SpaceX Falcon 9 Launch Analysis

An end-to-end data analysis project exploring historical SpaceX Falcon 9 launches and the factors associated with first-stage landing success. The project combines **Python, SQL, data collection, exploratory analysis, visualisation, geospatial analysis, and introductory machine learning**.

> **Portfolio focus:** Demonstrate how raw operational data can be collected, cleaned, explored, visualised, and translated into findings that support a business decision.

## Business question

First-stage booster recovery is central to rocket reusability. This project investigates whether historical launch characteristics—such as launch site, payload mass, orbit, flight number, and booster configuration—are associated with landing outcomes.

The practical question is: **What patterns in historical launches could help a launch provider understand and estimate the likelihood of a successful first-stage landing?**

This is an exploratory portfolio analysis, not an operational launch-safety system or a validated cost-pricing model.

## What the project covers

| Stage | Work completed | Tools |
|---|---|---|
| Data collection | Retrieve launch information from the SpaceX API | Python, requests, pandas |
| Web data collection | Extract launch records from a web table | Python, BeautifulSoup, pandas |
| Data preparation | Clean and transform records; prepare a modelling dataset | pandas |
| Exploratory analysis | Explore launch outcomes, payloads, launch sites, orbits, and time trends | pandas, Matplotlib, Seaborn |
| SQL analysis | Query the launch dataset to answer analytical questions | SQL, Jupyter |
| Geospatial analysis | Map launch locations and explore site geography | Folium |
| Interactive dashboard | Filter launch records by site and payload range | Plotly, Dash |
| Predictive analysis | Compare classification models for landing-success prediction | scikit-learn |
| Communication | Summarise the approach and findings in a final presentation/report | Jupyter, PowerPoint, PDF |

## Findings from the current analysis

The existing notebooks report several patterns worth investigating further:

- **Launch site matters:** the exploratory notebook reports different landing-success rates across launch sites.
- **Outcomes vary by orbit:** the observed success rates differ by orbit category. Some categories have relatively few records, so apparent 100% success rates should not be treated as conclusive.
- **Launch history provides context:** the notebook describes an upward trend in landing success over the period covered by the dataset.
- **Payload and flight number are useful exploratory variables:** the visual analysis examines how they relate to landing outcomes, although these relationships should not be interpreted as proof of causation.

### Model evaluation status (OLD)

The machine-learning notebook has been updated to load the committed datasets, split the data before fitting the scaler, remove the deprecated decision-tree `max_features='auto'` option, and compare models using precision, recall, F1-score, and confusion matrices alongside accuracy.

The notebook's old execution outputs were cleared because the preprocessing workflow changed; the earlier saved metrics should not be treated as results from the revised workflow. Re-run the notebook from top to bottom to generate fresh, reproducible results before quoting model performance in an application or interview.


### Model Evaluation (NEW)

Four classification models were evaluated to explore whether historical launch characteristics could help classify first-stage landing outcomes.

| Model | Test Accuracy | Precision | Recall | F1-Score |
|---|---:|---:|---:|---:|
| Logistic Regression | 77.8% | 78.6% | 91.7% | 84.6% |
| Support Vector Machine | 77.8% | 78.6% | 91.7% | 84.6% |
| Decision Tree | 77.8% | 83.3% | 83.3% | 83.3% |
| K-Nearest Neighbours | 77.8% | 75.0% | 100.0% | 85.7% |

The Decision Tree achieved the highest mean cross-validation accuracy at approximately **90.4%**. However, all four models achieved the same accuracy on the held-out test set.

**How to interpret these results:** The K-Nearest Neighbours model achieved the highest recall and F1-score in the reported test results, while the Decision Tree had the highest precision among the four models. The appropriate model depends on the relative importance of missed successful landings versus incorrect positive classifications.

**Important limitation:** The test set contains only 18 launches. A single prediction therefore has a substantial effect on the reported metrics. The cross-validation result is encouraging but does not establish that the model will generalise to new launches. These models are exploratory and should not be used for operational launch decisions.

The analysis compares model performance using accuracy, precision, recall, F1-score and confusion matrices rather than relying on accuracy alone.

## Repository guide

### Notebooks
- [Data collection using the SpaceX API](Data%20Collection%20API.ipynb)
- [Data collection with web scraping](Data%20Collection%20with%20Web%20Scraping.ipynb)
- [Data wrangling](Data%20Wrangling.ipynb)
- [Exploratory analysis and visualisation](EDA%20with%20Data%20Visualization.ipynb)
- [SQL analysis notebook](EDA%20with%20SQL.ipynb)
- [Standalone SQLite analysis queries](sql/analysis_queries.sql)
- [Interactive mapping with Folium](Interactive%20Visual%20Analytics%20with%20Folium.ipynb)
- [Machine-learning model comparison](Machine%20Learning%20Prediction.ipynb)
- [Notebook dependencies](requirements-notebooks.txt)

### Data and reporting
- [Prepared launch dataset](dataset_part_2.csv)
- [Model features](dataset_part_3.csv)
- [Web-scraped launch records](spacex_web_scraped.csv)
- [Final presentation](Apllied%20Data%20Science%20Capstone%20Final%20Presentation.pptx)
- [Project report](Winning%20Space%20Race%20with%20Data%20Science.pdf)

### Dashboard
The interactive dashboard source is in [app.py](app.py). It reads the committed `dataset_part_2.csv` file and uses current Dash imports.

## Run the dashboard locally

Use Python 3.10 or newer if possible.

1. Clone this repository and enter the project folder.
2. Install the dependencies listed in `requirements.txt`.
3. Run `python app.py`.
4. Open the local URL printed in your terminal.

The dashboard uses the prepared launch dataset in this repository. Notebook dependencies may vary by notebook, and some original course notebooks may contain cloud-service setup cells that require adaptation to run in a local environment.

### Run the standalone SQL queries

The queries in [`sql/analysis_queries.sql`](sql/analysis_queries.sql) use SQLite syntax. Import `dataset_part_2.csv` into a local SQLite database as a table named `launches`, preserving the column headers, then run the queries. They cover launch-site and orbit success rates, yearly trends, payload comparisons, booster flight counts, and basic data-quality checks.

## Tools and skills demonstrated

- **Python:** pandas, data preparation, exploratory analysis
- **SQL:** filtering, aggregation, grouping, and analytical queries
- **Visualisation:** Matplotlib, Seaborn, Plotly
- **Dashboarding:** Plotly Dash
- **Geospatial analysis:** Folium
- **Machine learning:** scikit-learn, classification, cross-validation, hyperparameter search
- **Communication:** documenting assumptions, explaining findings, and noting limitations

## Limitations and next steps

- The modelling dataset is small, and the saved test set contains only 18 records.
- Historical associations do not establish causation and should not be used alone for operational decisions.
- Model evaluation should include precision, recall, F1-score, confusion-matrix counts, and checks for class imbalance.
- The notebook workflow should be made reproducible with consistent local paths, dependency versions, and clear data provenance.
- The dashboard and its filters should be tested against the repository's committed dataset.

## Project context

This repository builds on the IBM Data Science Professional Certificate Applied Data Science Capstone learning workflow. The notebooks include course-provided instructional material; this README summarises the project and its saved outputs for portfolio review. Further improvements should focus on reproducibility, independent interpretation, and clearly evidenced business insights.

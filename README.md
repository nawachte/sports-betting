# sports-betting
A comprehensive exploration of NFL data, featuring exploratory data analysis (EDA), predictive modeling, and machine learning applications. This repository includes projects focused on over/under predictions, arbitrage opportunities, and other analytics-driven insights, utilizing Python, pandas, scikit-learn, and more. 

1. NFLScoreModel.ipynb
This notebook is the core of the project, implementing the predictive model for over/under scores in NFL games. It uses the cleaned dataset to train and test a machine learning model, optimizing for predictive accuracy.
Primary Focus: Building and testing machine learning models.
Key Features: Model training, evaluation, and performance metrics.

2. NFL_analysis_and_EDA.ipynb
This notebook focuses on data cleaning and exploratory data analysis (EDA) for the NFL dataset. It lays the groundwork for understanding patterns and trends in the data, providing valuable insights for feature engineering and modeling.
Primary Focus: Data cleaning and initial analysis.
Key Features: Preparing the dataset for model development and visualization.

3. NFLoverunder.ipynb
This notebook provides calculation functions and aggregates multiple methods of estimating the total score for NFL games. It leverages the Mean Absolute Error (MAE) calculated during the analysis and EDA phase to fine-tune predictions. These aggregated predictions are used to inform over/under betting decisions.
Primary Focus: Utility functions for betting decisions.
Key Features: Aggregation of multiple scoring prediction methods.
Use of MAE metrics to weigh prediction confidence.
Structured data management for team matchups and over/under odds.

4. arbitrage.py
This script identifies arbitrage opportunities in sports betting by analyzing moneyline odds from different sportsbooks. It calculates potential risk-free profit by comparing odds from multiple bookmakers and determining optimal bet distributions. The results are automatically compiled and sent via email, ensuring timely alerts for profitable betting scenarios.
Primary Focus: Identifying and executing arbitrage betting opportunities.
Key Features: Calculation of arbitrage opportunities using moneyline odds.
Automated email notifications for detected opportunities.

5. helper.py
This module handles data retrieval from sports betting APIs, fetching current moneyline odds for NFL and NBA games. It processes JSON responses, extracts relevant odds from selected sportsbooks, and formats them into a structured dataset for further calculations. Additionally, it includes functions for handling different response types, ensuring seamless data integration into the arbitrage algorithm.
Primary Focus: Fetching and structuring sports betting data.
Key Features: API integration for retrieving live sports betting odds.
Filtering and structuring data from selected sportsbooks.
Handling of JSON and HTML responses for seamless data processing.

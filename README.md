# COVID-19 Vaccination and Cases Analysis  
An Analysis of Vaccination Impact on COVID-19 Cases  

## 1. Overview  
This repository contains the analysis and visualizations of a dataset exploring the relationship between COVID-19 vaccinations and case numbers across different regions. By analyzing temporal patterns and performing lag-based correlations, this project seeks to understand whether vaccination efforts have had a delayed impact on reducing COVID-19 cases.  

The hypothesis explored in this analysis is:  
> "Vaccination efforts have a delayed effect on reducing COVID-19 cases, with variations based on regional factors and reporting accuracy."  

## 2. Project Structure  
The repository is organized as follows:  

- **`.circleci/`**: Configuration files for CircleCI integration to automate testing and ensure code reliability.  
- **`data/`**: Contains raw datasets:  
  - `daily-covid-19-vaccine-doses.csv`: Vaccination data.  
  - `daily-new-confirmed-covid-19-cases.csv`: COVID-19 case data.  
- **`visualisations/`**: Stores all visualizations generated during the analysis.  
- **`main.py`**: Core script to process data, perform analysis, and generate visualizations.  
- **`models.py`**: Contains functions for lag analysis and regression models.  
- **`datafunction.py`**: Functions for data preprocessing, cleaning, and merging datasets.  
- **`tests.py`**: Test scripts to ensure correctness of data functions and models.  
- **`requirements.txt`**: Specifies Python dependencies required for the project.  
- **`README.md`**: Project documentation.  

## 3. Dataset  
The datasets used for this analysis are sourced from the **World Health Organization (WHO)**:  
- **Vaccination data**: Records daily doses administered worldwide.  
- **Case data**: Tracks daily new confirmed COVID-19 cases globally.  

### Pre-processing:  
- Datasets were cleaned, columns were renamed for merging, and missing values were handled using interpolation.  
- Time-series data alignment ensured comparability.  

The final datasets include information on:  
- Regional vaccine administration and case counts.  
- Temporal trends from January 2021 to mid-2024.  

## 4. How to Run  
To run the analysis and generate visualizations locally:  

1. Clone the repository:  
    ```bash
    git clone https://github.com/FarhanU001N/DAT5902FinalProject
    cd DAT5902FinalProject 

2. Install the required dependencies from 'requrements.txt':
    ```bash
    pip install -r requirements.txt

4. Run the data analysis script - 'data_analysis.py':
   ```bash
   python main.py

6. To execute the test suite:
    ```bash
    unitests tests.py

7. View the visualisations:

   Navigate inside the 'visualisations/' folder to do so.

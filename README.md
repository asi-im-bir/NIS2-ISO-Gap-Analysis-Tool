That's the most crucial step for presenting your project\! A well-structured **`README.md`** file tells the complete story of your project, highlighting your technical skills and the business value of the solution for the Information Security Engineer role.

Here is the complete content for your `README.md` file. Copy this, create the file in your project's root directory (`nis2-iso-gap-tool`), and then commit and push it to GitHub.

-----

# 🛡️ Automated NIS2 / ISO 27001 Control Gap Analysis Tool

## Project Summary

This project demonstrates the creation of a powerful, automated governance tool designed to streamline the continuous compliance requirements for the modern Security Office.

The tool uses **Python (Pandas)** to process disparate compliance data (YAML controls, CSV mappings) and generate a quantitative **Gap Analysis Report** and a visualization dataset for **Tableau**. This system replaces messy, manual spreadsheet tracking with objective, data-driven risk prioritization—a critical function for ensuring compliance with mandates like **NIS2** and **ISO/IEC 27001**.

## Key Technical Achievements (What I Built)

This solution integrates multiple tools and demonstrates skills in core data engineering and security automation:

1.  **Cross-Framework Mapping Engine:** Implemented logic to merge operational controls (from YAML) against requirements from **two distinct standards** (NIS2 Article 21 and ISO 27001 Annex A), establishing a single source of compliance truth.
2.  **Quantitative Risk Scoring:** Developed a custom algorithm to calculate **Maximum Control Coverage** and assign a categorical **Risk Priority** (Critical, High, Medium) based on combining the requirement's inherent **Risk Weight** with the calculated implementation score.
3.  **End-to-End Automation Pipeline:** Created a scripted pipeline that handles data ingestion, transformation, and professional reporting (PDF output via **Pandoc/MiKTeX**), preparing results for both audit review and executive dashboards.
4.  **Tool Integration:** Successfully integrated Python with external binary dependencies (**Pandoc**) and professional BI platforms (**Tableau**) for high-impact reporting.

-----

## 🛠️ Project Structure

The project is designed with clear separation of code, data, and outputs:

```
nis2-iso-gap-tool/
├── src/
│   ├── analysis_engine.py    # Core logic: data merging, coverage, and risk calculation.
│   └── main.py               # Execution file: calls analysis and generates reports (PDF/CSV).
├── data/
│   ├── implemented_controls.yaml # Operational controls and effectiveness scores.
│   ├── standards_requirements.csv # List of all ISO/NIS2 requirements and their Risk Weights.
│   └── control_mapping.csv        # The cross-walk matrix (Control ID -> Requirement ID).
├── output/                     # Location for generated reports (.pdf, .csv).
└── requirements.txt
```

-----

## 🚀 Getting Started

### Prerequisites

1.  **Python 3.x**
2.  **Pandoc:** The core document conversion utility (must be installed on your system PATH).
3.  **MiKTeX:** A LaTeX distribution (required by Pandoc to render high-quality PDF files).

### Installation

Navigate to the root directory and install the necessary Python libraries:

```bash
pip install -r requirements.txt
```

### Execution

Run the main script to process the data, generate the analysis, and export the reports:

```bash
python src/main.py
```

-----

## 📊 Outputs and Visualization

The script generates two critical outputs in the `/output` folder:

1.  **`Gap_Analysis_Data_YYYYMMDD.csv`:** The final, clean, and scored data source, ready to be connected directly to Tableau.
2.  **`Gap_Analysis_Report_YYYYMMDD.pdf`:** The formal, prioritized audit summary.

### Interactive Compliance Dashboard

[Link to your Interactive Version on Tableau Public]

\<iframe
src="[PASTE YOUR TABLEAU PUBLIC EMBED URL HERE]"
width="100%"
height="800px"
frameborder="0"\>
\</iframe\>

-----

## ✅ Technical Challenges Solved

| Challenge Area | Description |
| :--- | :--- |
| **Dependency Management** | Successfully configured the Python environment to integrate with external binaries (Pandoc) and resolve dependency conflicts (`PyYAML`, `tabulate`). |
| **PDF Generation** | Overcame the complex **`pdflatex not found`** error by correctly identifying and installing the MiKTeX LaTeX compiler, ensuring high-quality, professional PDF output. |
| **Data Integrity** | Resolved input file parsing errors by establishing rigorous file path handling and ensuring the final Pandas DataFrame consistently included all necessary columns for external reporting. |

-----

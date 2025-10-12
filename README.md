#  Information Management Project — Health (COVID) Data Pipeline Framework

---

##  Team Members
- **Chioma Agoh**  
- **Kindness Harbor**  
- **Julian Tubel**  
- **Yonael Zeamann**

---

##  Roles
| Role | Member |
|------|---------|
| **Project Coordinator** | Yonael Zeamann |
| **Documentation Manager** | Chioma Agoh |
| **Liaison** | Kindness Harbor |
| **Quality Assurance** | Julian Tubel |

---

##  Communication
- **Platform:** GroupMe (team group established)  
- **Regular Meeting:** Tuesdays at **3:00 PM ET**

---

##  Conflict Resolution Strategy
1. Practice active listening to understand member concerns.  
2. Seek compromise and constructive trade-offs.  
3. If needed, request neutral mediation (e.g., TA involvement).  
4. Clarify expectations and responsibilities early to avoid misunderstandings.

---

##  Project Overview
**Title:** Health Data Pipeline Framework  
**Domain:** Research Data Management (Public Health)  
**Goal:**  
Build a modular function library and data pipeline that loads, cleans, validates, transforms, and summarizes disease case data — enabling faster insights and decision-making.

---

##  Problem Statement
Public-health teams often struggle to:

- Combine case data from multiple sources and formats (CSV, JSON, XML).  
- Validate reported case counts for accuracy and consistency.  
- Clean and standardize messy inputs (missing values, wrong dates, inconsistent names).  
- Transform raw data into visual summaries for reports.  
- Organize outputs for multiple research projects.

---

##  Project Features & Scope

###  Core (Must-Have)
- **Data Import:** Read CSV, JSON, and XML files.  
- **Validation & Cleaning:** Check for missing/invalid entries and fix simple errors.  
- **Transformations:** Aggregate by date, location, or age group.  
- **Basic Visualizations:**  
  - Line charts for case counts  
  - Bar charts for locations  
- **Automated Reports:** Generate summary tables and charts for each dataset.  
- **Configuration Options:** Allow users to select which steps to execute (e.g., cleaning, charting, reporting).

###  Nice-to-Have (Future Enhancements)
- Export cleaned datasets to new files.  
- Additional chart types (heatmaps, stacked bars).  
- Support for live data ingestion from APIs.  
- Save user preferences for repeated analyses.  
- Generate email or PDF reports automatically.

---

##  Growth & Complexity Roadmap

### **Phase 1 — Basics**
- Load one public-health dataset.  
- Clean and validate the data.  
- Produce a simple line chart showing case counts over time.  

### **Phase 2 — Expansion**
- Support multiple datasets and more complex aggregations.  
- Add moving averages or weekly incidence calculations.  

### **Phase 3 — Interface**
- Add a simple CLI or UI to select pipeline steps.  
- Enable dataset export and optional report automation.  

---

##  Next Steps
- Finalize function list and file layout (`utils.py`, `validation.py`, `cleaning.py`, etc.).  
- Assign development tasks and peer review responsibilities.  
- Prepare an example dataset and demonstration script (`examples/demo_script.py`).  
- Document AI assistance and individual learning (per course AI Collaboration Guidelines).  

---

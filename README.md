# Information Management Project — Health (COVID) Data Pipeline Framework

---

## Team Members
- **Chioma Agoh**  
- **Kindness Harbor**  
- **Julian Tubel**  
- **Yonael Zeamann**

---

## Roles
| Role | Member |
|------|---------|
| **Project Coordinator** | Yonael Zeamann |
| **Documentation Manager** | Chioma Agoh |
| **Liaison** | Kindness Harbor |
| **Quality Assurance** | Julian Tubel |

---

## Communication
- **Platform:** GroupMe (team group established)  
- **Regular Meeting:** Tuesdays at **3:00 PM ET**

---

## Conflict Resolution Strategy
1. Practice active listening to understand member concerns.  
2. Seek compromise and constructive trade-offs.  
3. If needed, request neutral mediation (e.g., TA involvement).  
4. Clarify expectations and responsibilities early to avoid misunderstandings.

---

## Project Overview
**Title:** Health Data Pipeline Framework  
**Domain:** Research Data Management (Public Health)  
**Goal:**  
Build a modular function library and data pipeline that loads, cleans, validates, transforms, and summarizes disease case data — enabling faster insights and decision-making.

---

## Problem Statement
Public-health teams often struggle to:

- Combine case data from multiple sources and formats (CSV, JSON, XML).  
- Validate reported case counts for accuracy and consistency.  
- Clean and standardize messy inputs (missing values, wrong dates, inconsistent names).  
- Transform raw data into visual summaries for reports.  
- Organize outputs for multiple research projects.

---

## Project Features & Scope

### Core (Must-Have)
- **Data Import:** Read CSV, JSON, and XML files.  
- **Validation & Cleaning:** Check for missing/invalid entries and fix simple errors.  
- **Transformations:** Aggregate by date, location, or age group.  
- **Basic Visualizations:**  
  - Line charts for case counts  
  - Bar charts for locations  
- **Automated Reports:** Generate summary tables and charts for each dataset.  
- **Configuration Options:** Allow users to select which steps to execute (e.g., cleaning, charting, reporting).

### Nice-to-Have (Future Enhancements)
- Export cleaned datasets to new files.  
- Additional chart types (heatmaps, stacked bars).  
- Support for live data ingestion from APIs.  
- Save user preferences for repeated analyses.  
- Generate email or PDF reports automatically.

---

## Growth & Complexity Roadmap

### **Phase 1 — Basics**
- Load one public-health dataset.  
- Clean and validate the data.  
- Produce a simple line chart showing case counts over time.  

### **Phase 2 — Object-Oriented Implementation (Completed)**
Part 2 introduced a **complete OOP structure** to replace the original function-only design.  
This update focused on applying **encapsulation, validation, and modular class design** across the pipeline system.

**Key Improvements**
- Converted major functions into object-oriented components.  
- Added constructors (`__init__`) with built-in validation for key attributes.  
- Used private attributes with property methods to manage access and integrity.  
- Integrated cleaning and summarization logic from Project 1 into organized class methods.  
- Improved documentation with class and method-level docstrings.  
- Established a foundation for future inheritance and polymorphism.

These updates made the codebase more readable, reusable, and easier to maintain — preparing the system for the advanced OOP concepts in Project 3.

---

### **Phase 3 — Advanced OOP (In Progress)**
The next stage will extend the current classes using **inheritance, polymorphism, and composition** to create a more flexible and scalable framework.

**Planned Goals**
- Introduce base and derived class hierarchies for dataset types.  
- Implement abstract base classes to define shared interfaces.  
- Demonstrate polymorphism with methods that behave differently across subclasses.  
- Use composition to represent “has-a” relationships between pipeline components.  
- Expand testing and documentation for class hierarchies and dynamic behavior.

---

## Next Steps
- Finalize inheritance hierarchy and abstract class design.  
- Implement polymorphic methods for specialized dataset handling.  
- Add composition relationships between system components.  
- Continue updating documentation and usage examples.  
- Prepare UML-style diagrams for the final submission.

---

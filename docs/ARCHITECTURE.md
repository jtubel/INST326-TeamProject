# Health Data Pipeline - Architecture Diagram

## Complete System Architecture

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                          ABSTRACT BASE LAYER                            │
│                     (Defines Interface Contracts)                       │
│                                                                         │
│  [JULIAN'S MODULE]                [KINDNESS'S MODULE]                   │
│  ┌─────────────────────┐          ┌───────────────────────────────┐     │
│  │   AbstractDataset   │          │       AbstractAnalyzer        │     │
│  ├─────────────────────┤          ├───────────────────────────────┤     │
│  │ @abstractmethod     │          │ @abstractmethod               │     │
│  │ + load_data()       │          │ + calculate_trends()          │     │
│  │ + validate_format() │          │ + detect_anomalies()          │     │
│  └──────────▲──────────┘          └──────────────▲────────────────┘     │
│             │                                    │                      │
│             │ inherits                           │ inherits             │
│             │                                    │                      │
├─────────────┼────────────────────────────────────┼──────────────────────┤
│             │                                    │                      │
│  CONCRETE IMPLEMENTATION LAYER                   │                      │
│                                                  │                      │
│  ┌──────────┴──────┐  ┌────────────────┐  ┌──────┴───────────────┐      │
│  │   CSVDataset    │  │  JSONDataset   │  │    TrendAnalyzer     │      │
│  ├─────────────────┤  ├────────────────┤  ├──────────────────────┤      │
│  │ load_data()     │  │ load_data()    │  │ calculate_trends()   │      │
│  │  → csv lib      │  │  → json lib    │  │  → statistical logic │      │
│  └──────────┬──────┘  └───────┬────────┘  └──────────────────────┘      │
│             │ creates         │ creates              │ used by          │
│             ▼                 ▼                      ▼                  │
└─────────────────────────────────────────────────────────────────────────┘
              │                 │                      │
              │ contains        │ contains             │
              ▼                 ▼                      │
┌─────────────────────────────────────────────────────────────────────────┐
│                        COMPOSITION LAYER                                │
│               (Data Objects & System Coordination)                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                            CaseRecord                             │  │
│  │                     (Fundamental Data Unit)                       │  │
│  ├───────────────────────────────────────────────────────────────────┤  │
│  │ + date, location, cases                                           │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│              ▲                                    ▲                     │
│              │ managed by                         │ used by             │
│              │                                    │                     │
│  ┌───────────┴────────────────────────────────────┴──────────────────┐  │
│  │                        [YONAEL'S MODULE]                          │  │
│  │                         PipelineManager                           │  │
│  │                    (System Controller/Coordinator)                │  │
│  ├───────────────────────────────────────────────────────────────────┤  │
│  │ + datasets: List[AbstractDataset]  ◄────── HAS-MANY datasets      │  │
│  │ + analyzers: List[AbstractAnalyzer] ◄───── HAS-MANY analyzers     │  │
│  │                                                                   │  │
│  │ + add_dataset(source)                                             │  │
│  │ + run_full_analysis()                                             │  │
│  └─────────────────────────────────┬─────────────────────────────────┘  │
│                                    │                                    │
│                                    │ generates data for                 │
│                                    ▼                                    │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                        [CHIOMA'S MODULE]                          │  │
│  │                           AlertReport                             │  │
│  ├───────────────────────────────────────────────────────────────────┤  │
│  │ + threshold_level                                                 │  │
│  │ + recipients_list                                                 │  │
│  │                                                                   │  │
│  │ + generate_alert(analysis_results)                                │  │
│  │ + save_report_to_file()                                           │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

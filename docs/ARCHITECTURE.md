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
│  │                        [CHIOMA'S MODULE]                          │  │
│  │                         PipelineManager                           │  │
│  │                    (System Controller/Coordinator)                │  │
│  ├───────────────────────────────────────────────────────────────────┤  │
│  │ + datasets: List[AbstractDataset]  ◄────── HAS-MANY datasets      │  │
│  │ + analyzers: List[AbstractAnalyzer] ◄───── HAS-MANY analyzers     │  │
│  │                                                                   │  │
│  │ + add_dataset(source)                                             │  │
│  │ + run_full_analysis()                                             │  │
│  │ + save_session_state()             ◄────── PROJ 4: PERSISTENCE    │  │
│  │ + load_session_state()             ◄────── PROJ 4: PERSISTENCE    │  │
│  └─────────────────────────────────┬─────────────────────────────────┘  │
│                                    │                                    │
│                                    │ generates data for                 │
│                                    ▼                                    │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                        [YONAEL'S MODULE]                          │  │
│  │                        ForecastingAnalyzer                        │  │
│  │                      (Advanced Predictions)                       │  │
│  ├───────────────────────────────────────────────────────────────────┤  │
│  │ + predict_future_cases()                                          │  │
│  │ + generate_growth_metrics()                                       │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

Key Relationships
INHERITANCE (is-a)
CSVDataset IS-A AbstractDataset

JSONDataset IS-A AbstractDataset

TrendAnalyzer IS-A AbstractAnalyzer (Proposed Interface)

DailyStats IS-A CaseRecord (Future extension)

COMPOSITION (has-a / has-many)
PipelineManager HAS-MANY datasets

PipelineManager HAS-MANY analyzers

PipelineManager HAS-A AlertReport (generator)

AbstractDataset HAS-MANY CaseRecords

TrendAnalyzer USES CaseRecords (dependency)

POLYMORPHISM (same method, different behavior)
All datasets implement load_data() differently:

CSVDataset: Uses csv.DictReader to parse comma-separated rows.

JSONDataset: Uses json.load to parse hierarchical objects.

All analyzers implement analyze() differently:

TrendAnalyzer: Calculates moving averages and linear regression.

AnomalyDetector: (Future) Identifies statistical outliers > 2 standard deviations.

Data Flow Example
1. User creates PipelineManager
   └─→ Manager initializes empty lists for datasets and analyzers

2. User adds data sources
   └─→ Manager.add_dataset("florida_data.csv")
       └─→ Instantiates CSVDataset
   └─→ Manager.add_dataset("newyork_data.json")
       └─→ Instantiates JSONDataset

3. User triggers data load
   └─→ Manager loops through datasets calling .load_data()
       └─→ POLYMORPHISM: Correct parsing logic executes per file type
       └─→ COMPOSITION: Each dataset fills its own list of CaseRecords

4. User requests analysis
   └─→ Manager passes records to TrendAnalyzer
       └─→ Analyzer calculates peaks and averages

5. System generates output
   └─→ Manager passes stats to AlertReport
       └─→ AlertReport checks thresholds (e.g., >5000 cases)
       └─→ Generates warning text file or console log
Why This Architecture Works
Abstract Layer Benefits
✓ Enforces consistent interfaces: If a team member adds an XMLDataset, they are forced to implement load_data. ✓ Cannot instantiate incomplete classes: Prevents runtime errors from uninitialized data handlers. ✓ Clear contracts for implementers: Defines exactly what methods are required for the pipeline to function.

Concrete Layer Benefits
✓ Code reuse through inheritance: Shared logic (like get_record_count) is written once in the parent class. ✓ Specialized behavior per type: Parsing logic is isolated; CSV bugs don't break JSON loading. ✓ Polymorphic method calls: The PipelineManager doesn't need if file == 'csv' statements. ✓ Easy to extend: New analyzers or data types can be added without changing the Manager code.

Composition Layer Benefits
✓ Flexible object relationships: We can swap out different Analysis modules without breaking the Data modules. ✓ No artificial inheritance hierarchies: A Dataset is a container for records, not a child of a record. ✓ Clear separation of concerns: Data loading , Analysis, and Reporting are distinct.

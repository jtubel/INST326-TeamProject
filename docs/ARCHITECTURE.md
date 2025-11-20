# Health Data Pipeline - System Architecture

## Complete System Architecture

                         ABSTRACT BASE LAYER
                    (Defines Interface Contracts)
                                  |
    +-----------------------------+------------------------------+
    |                      AbstractDataset                       |
    |               (inherits from Python ABC)                   |
    +------------------------------------------------------------+
    | + source_path                                              |
    | + _data (List of Records)  <--- HAS-MANY CaseRecords       |
    |                                                            |
    | @abstractmethod                                            |
    | + load_data()                                              |
    | + validate_format()                                        |
    |                                                            |
    | + get_all_records()                                        |
    +-----------------------------+------------------------------+
                                  |
                                  |
                   INHERITANCE & POLYMORPHISM LAYER
            (Concrete implementations of the Abstract Base)
                                  |
          +-----------------------+-----------------------+
          |                                               |
          v                                               v
+-----------------------+                       +-----------------------+
|      CSVDataset       |                       |      JSONDataset      |
+-----------------------+                       +-----------------------+
| + load_data()         |                       | + load_data()         |
|   -> Uses csv.reader  |                       |   -> Uses json.load   |
|                       |                       |                       |
| + validate_format()   |                       | + validate_format()   |
|   -> Check .csv ext   |                       |   -> Check .json ext  |
+-----------------------+                       +-----------------------+
          |                                               |
          | creates instances of                          | creates instances of
          v                                               v
+------------------------------------------------------------------------+
|                            COMPOSITION LAYER                           |
|                          (The Data Component)                          |
+------------------------------------------------------------------------+
|                                                                        |
|                              CaseRecord                                |
|                                                                        |
|   + date: str                                                          |
|   + location: str                                                      |
|   + cases: int                                                         |
|                                                                        |
|   (This class is simple and holds no logic. It is "owned"              |
|    by the Dataset classes via a list.)                                 |
+------------------------------------------------------------------------+


## Key Relationships

### INHERITANCE (is-a)
* CSVDataset **IS-A** AbstractDataset
* JSONDataset **IS-A** AbstractDataset

### COMPOSITION (has-a)
* AbstractDataset **HAS-MANY** CaseRecords
    * *Rationale:* A dataset is a container. It isn't a type of record, it *owns* a list of records.
* CSVDataset/JSONDataset **CREATES** CaseRecords
    * *Rationale:* The loading methods read raw text and convert it into CaseRecord objects.

### POLYMORPHISM (Same method, different behavior)
* **Method:** `load_data()`
    * In **CSVDataset**: Opens file as text, splits by commas, parses rows.
    * In **JSONDataset**: Opens file as object, parses key-value pairs.
* **Method:** `validate_format()`
    * In **CSVDataset**: Checks for comma delimiters and .csv extension.
    * In **JSONDataset**: Checks for brackets and .json extension.


## Data Flow Example

1. User starts the program
   |
   +-> User provides a filename: "data/florida.csv"

2. Program initializes specific class
   |
   +-> Instantiates CSVDataset("data/florida.csv")

3. Program calls load_data() [Polymorphism]
   |
   +-> The System calls generic .load_data()
       |
       +-> CSVDataset specific version runs
       +-> Opens file -> Reads Row
       +-> Creates CaseRecord object
       +-> Appends to self._data list

4. User requests analysis
   |
   +-> generic_dataset.get_all_records()
       |
       +-> Returns list of [CaseRecord, CaseRecord, ...]
       +-> Works exactly the same regardless of if source was CSV or JSON


## Design Pattern Summary

| Pattern | Component | Why we used it |
| :--- | :--- | :--- |
| **Abstract Base Class** | AbstractDataset | To force all future datasets to implement `load_data`. |
| **Inheritance** | CSV/JSONDataset | To share the `_data` list and `get_all_records` logic. |
| **Polymorphism** | load_data() | To allow the main system to ignore file format details. |
| **Composition** | CaseRecord | To separate "Data Storage" (Dataset) from "Data Unit" (Record). |

import xml.etree.ElementTree as ET
from case_data_manager import AbstractDataset, CaseRecord

class XMLDataset(AbstractDataset):
    """
    Specialized dataset for XML files.
    """

    def load_data(self) -> None:
        """
        Polymorphic implementation: Uses xml.etree to parse data.
        """
        try:
            tree = ET.parse(self.source_path)
            root = tree.getroot()
            
            # Assuming XML structure: <root><record><date>...</date></record>...</root>
            for child in root:
                # Extract text safely
                date = child.find('date').text if child.find('date') is not None else 'Unknown'
                loc = child.find('location').text if child.find('location') is not None else 'Unknown'
                cases_str = child.find('cases').text if child.find('cases') is not None else '0'
                
                # Create the shared CaseRecord object
                record = CaseRecord(date, loc, int(cases_str))
                self._data.append(record)
                
            print(f"Successfully loaded {len(self._data)} records from XML.")
            
        except ET.ParseError:
            print(f"Failed to parse XML file: {self.source_path}")
        except Exception as e:
            print(f"Error loading XML: {e}")

    def validate_format(self) -> bool:
        """Checks if file ends with .xml."""
        return self.source_path.lower().endswith('.xml')

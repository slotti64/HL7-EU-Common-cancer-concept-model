# HL7 EU Common Cancer Model
## Concept Model and Glossary for Common Cancer Model Project

The initial OWL 2 model was generated from [European Cancer Common Conceptual Model v2](https://confluence.hl7.org/download/attachments/281282385/CancerLogicalModel_20250414_Rev.png?version=1&modificationDate=1744961792994&api=v2) with Claude's LLM support. 
This OWL model was imported into MacDraw UML 2024x with the Cameo Concept Model plugin. The imported model was revised, integrated, and extended with the [glossary](https://confluence.hl7.org/spaces/HEU/pages/281282385/Cancer+Common+Model+Project+Edition+1)  
From this UML model, a set of arifacts was generated: 

* [EuropeanCancerModel-v02.rdf](https://github.com/slotti64/HL7-EU-Common-cancer-concept-model/blob/main/EuropeanCancerModel-v02.rdf) (revised OWL 2 model)
* [EuropeanCancerModel-v02.html](https://github.com/slotti64/HL7-EU-Common-cancer-concept-model/blob/main/EuropeanCancerModel-v02.html) (Natural Language Web Glossary)
* [Cancer Model Glossary-v02.xlsx](https://github.com/slotti64/HL7-EU-Common-cancer-concept-model/blob/main/Cancer%20Model%20Glossary-v02.xlsx) (Excel Glossary)

A Python program ([owl2plantuml_v17.py](https://github.com/slotti64/HL7-EU-Common-cancer-concept-model/tree/main/OWL2PlantUML/)) was created (with Claude) to transform the OWL2 file into PlantUML: 

* [EUCM-v02.puml](https://github.com/slotti64/HL7-EU-Common-cancer-concept-model/blob/main/EUCM-v02.puml)

The model, currently in an early stage, aims to support automated mapping from concepts to resources using a combined model-driven and LLM approach. 

An experimental generate  mapping to FHIR Resource and Profile is [here](https://github.com/slotti64/HL7-EU-Common-cancer-concept-model/blob/main/TEST%20LLM/EUCM%20mapping%20FHIR%20Resources-05-04-2025.docx).

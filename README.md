# HL7 EU Common Cancer Model
## Concept Model and Glossary for Common Cancer Model Project

The initial OWL 2 model was generated from [European Cancer Common Conceptual Model v2](https://confluence.hl7.org/download/attachments/281282385/CancerLogicalModel_20250414_Rev.png?version=1&modificationDate=1744961792994&api=v2) with Claude's LLM support. 
The Cameo Concept Model plugin imported this OWL model into MacDraw UML 2024x. The imported model was revised, integrated, and extended with the [glossary](https://confluence.hl7.org/spaces/HEU/pages/281282385/Cancer+Common+Model+Project+Edition+1)  
From this UML model, a set of artifacts was generated: 

* [EuropeanCancerModel-v02.rdf](https://github.com/slotti64/HL7-EU-Common-cancer-concept-model/blob/main/EuropeanCancerModel-v02.rdf) (revised OWL 2 model)
* [EuropeanCancerModel-v02.html](https://github.com/slotti64/HL7-EU-Common-cancer-concept-model/blob/main/EuropeanCancerModel-v02.html) (Natural Language Web Glossary)
* [Cancer Model Glossary-v02.xlsx](https://github.com/slotti64/HL7-EU-Common-cancer-concept-model/blob/main/Cancer%20Model%20Glossary-v02.xlsx) (Excel Glossary)

A Python program ([owl2plantuml_v17.py](https://github.com/slotti64/HL7-EU-Common-cancer-concept-model/tree/main/OWL2PlantUML/)) was created (with Claude) to transform the OWL2 file into PlantUML: 

* [EUCM-v02.puml](https://github.com/slotti64/HL7-EU-Common-cancer-concept-model/blob/main/EUCM-v02.puml)

Using a combined model-driven and LLM approach, the work, currently in an early stage, aims to support:
* formalization of the conceptual model and alignment
* support the HL7 Tooling
* an automated mapping from concepts to FHIR resources 

An experimental mapping (generated with Claude 3.7) to the FHIR Resource and Profile is [here](https://github.com/slotti64/HL7-EU-Common-cancer-concept-model/blob/main/TEST%20LLM/EUCM%20mapping%20FHIR%20Resources-05-04-2025.docx).

Madrid May 2025 WGM Presentation is [here](https://github.com/slotti64/HL7-EU-Common-cancer-concept-model/blob/main/Presentations/Common%20Cancer%20Model%20-%20Madrid%20WGM%20Presentation.pptx) 
(This work must be aligned with the result of WGM Discussion)

![Curent Formal Common Cancer Concept model](https://github.com/slotti64/HL7-EU-Common-cancer-concept-model/blob/main/RevisedEuropeanCancerConceptModel_in_UML-v02.jpg)

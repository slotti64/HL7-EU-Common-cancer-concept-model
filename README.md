# HL7 EU Common Cancer Model
## Formal Concept Model and Glossary 

The initial OWL 2 model was generated from [European Cancer Common Conceptual Model v2](https://confluence.hl7.org/download/attachments/281282385/CancerLogicalModel_20250414_Rev.png?version=1&modificationDate=1744961792994&api=v2) with Claude's LLM support. 
The Cameo Concept Model plugin imported this OWL model into MacDraw UML 2024x. The model was revised, integrated, and extended with the existing glossary before a set of artifacts was generated.

## Generated Artifacts

From this UML model, the following artifacts were produced:

* [EuropeanCancerModel-v02.rdf](https://github.com/slotti64/HL7-EU-Common-cancer-concept-model/blob/main/EuropeanCancerModel-v02.rdf) - Revised OWL 2 model
* [EuropeanCancerModel-v02.html](https://github.com/slotti64/HL7-EU-Common-cancer-concept-model/blob/main/EuropeanCancerModel-v02.html) - Natural Language Web Glossary
* [Cancer Model Glossary-v02.xlsx](https://github.com/slotti64/HL7-EU-Common-cancer-concept-model/blob/main/Cancer%20Model%20Glossary-v02.xlsx) - Excel Glossary 

## Transformation to PlantUML

A Python program ([owl2plantuml_v17.py](https://github.com/slotti64/HL7-EU-Common-cancer-concept-model/tree/main/OWL2PlantUML/)) was developed (with 'Vibe Coding' approach using Claude LLM) to transform the OWL2 file into PlantUML:

* [EUCM-v02.puml](https://github.com/slotti64/HL7-EU-Common-cancer-concept-model/blob/main/EUCM-v02.puml)

## Objectives

Using a combined model-driven and LLM approach, this work, currently in its early stages, aims to support (*at minimum*):

* Formalization and consolidation of the discussed Concept Model
* Integration  with the HL7 Tools
* Mapping from concepts to FHIR resources
* And future developments beyond these initial goals

An experimental mapping (generated with Claude 3.7) to FHIR Resource and Profile is [here](https://github.com/slotti64/HL7-EU-Common-cancer-concept-model/blob/main/TEST%20LLM/EUCM%20mapping%20FHIR%20Resources-05-04-2025.docx).

The presentation for the Madrid Working Group Meeting (May 2025) can be accessed [here](https://github.com/slotti64/HL7-EU-Common-cancer-concept-model/blob/main/Presentations/Common%20Cancer%20Model%20-%20Madrid%20WGM%20Presentation.pptx) 

(_This work must be aligned with the result of the May WGM Discussion_)

![Curent Formal Common Cancer Concept model](https://github.com/slotti64/HL7-EU-Common-cancer-concept-model/blob/main/RevisedEuropeanCancerConceptModel_in_UML-v02.jpg)

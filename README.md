# HL7 EU Common Cancer Model

## Formal concept model (ontology)
### Overview

The HL7 EU Common Cancer Model provides a formal ontological representation of cancer-related concepts, designed to support interoperability and semantic consistency across European healthcare information systems and seeks to establish a set of data elements that not only support research and analytics but also inform the definition of minimum requirements for primary data capture. 
This model formalizes the conceptual discussions within the HL7 Europe community into a machine-readable OWL 2 ontology.

The initial OWL 2 model was generated from the [European Cancer Common Conceptual Model v2](https://confluence.hl7.org/download/attachments/281282385/CancerLogicalModel_20250414_Rev.png?version=1&modificationDate=1744961792994&api=v2), developed with the assistance of Claude 3.7 Sonnet (Anthropic). The Cameo Concept Modeler plugin was then used to import the OWL model into MagicDraw UML 2024x and extended. Subsequent discussions following the Madrid Working Group Meeting led to the current release (version 2.1). The new model has been verified and revidsed with the assistance of Claude 4.5 Opus (Anthropic).

For comprehensive information about the overall project, please refer to the [HL7 EU Confluence project page](https://confluence.hl7.org/x/UQfEE).

### Generated Artifacts

The following artifacts have been produced from the UML model:

The [EuropeanCancerModel-v02.rdf](https://github.com/slotti64/HL7-EU-Common-cancer-concept-model/blob/main/EuropeanCancerModel-v02.rdf) file contains the revised OWL 2 ontology in RDF/XML serialization format. A human-readable Natural Language Web Glossary is available in [EuropeanCancerModel-v02.html](https://github.com/slotti64/HL7-EU-Common-cancer-concept-model/blob/main/EuropeanCancerModel-v02.html). For tabular reference, the [Cancer Model Glossary-v02.xlsx](https://github.com/slotti64/HL7-EU-Common-cancer-concept-model/blob/main/Cancer%20Model%20Glossary-v02.xlsx) provides the glossary in spreadsheet format.

### OWL to PlantUML Transformation

A Python utility ([owl2plantuml_v17.py](https://github.com/slotti64/HL7-EU-Common-cancer-concept-model/tree/main/OWL2PlantUML/)) has been developed to transform OWL 2 ontologies into PlantUML diagrams, enabling automated generation of visual representations from the formal model. This tool was developed using an LLM-assisted coding approach with Claude 3.7.

### Project Objectives

This initiative employs a combined model-driven and LLM-assisted approach to achieve several key objectives. The primary goals include the formalization and consolidation of the discussed Concept Model, integration with the HL7 tooling ecosystem, and systematic mapping from ontological concepts to FHIR resources. The framework is designed to accommodate future developments beyond these initial goals.

An experimental mapping to FHIR Resources and Profiles, generated with Claude 3.7, is available [here](https://github.com/slotti64/HL7-EU-Common-cancer-concept-model/blob/main/TEST%20LLM/EUCM%20mapping%20FHIR%20Resources-05-04-2025.docx).

### Documentation

The presentation delivered at the Madrid Working Group Meeting (May 2025) can be accessed [here](https://github.com/slotti64/HL7-EU-Common-cancer-concept-model/blob/main/Presentations/Common%20Cancer%20Model%20-%20Madrid%20WGM%20Presentation.pptx).

### Current Model Diagram

![HL7 EU Common Cancer Concept Model - UML Diagram v2](https://github.com/slotti64/HL7-EU-Common-cancer-concept-model/blob/main/HL7EU-CommonCancerModel-full-v2.1.jpg)

---

**Status**: This work is currently a draft under discussion within the HL7 EU community.

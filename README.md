# HL7 EU Common Cancer Model

## Formal concept model (ontology)
### Overview

The HL7 EU Common Cancer Model provides a formal ontological representation of cancer-related concepts, designed to support interoperability and semantic consistency across European healthcare information systems, and seeks to establish a set of data elements that not only support research and analytics but also inform the definition of minimum requirements for primary data capture. 
This model formalizes the conceptual discussions within the HL7 Europe community into a machine-readable OWL 2 ontology.

The initial OWL 2 model was generated from the [European Cancer Common Conceptual Model v2](https://confluence.hl7.org/download/attachments/281282385/CancerLogicalModel_20250414_Rev.png?version=1&modificationDate=1744961792994&api=v2), developed with the assistance of Claude 3.7 Sonnet (Anthropic). The Cameo Concept Modeler plugin was then used to import the OWL model into MagicDraw UML 2024x and extend it. Subsequent discussions following the Madrid Working Group Meeting led to the current release (version 2.1). The current updated model is based on the new version [European Cancer Common Conceptual Model v2.1](https://confluence.hl7.org/download/attachments/281282385/CancerConceptuallModel_20251126.png?version=1&modificationDate=1764164637839&api=v2), has been verified and revised with the assistance of Claude 4.5 Opus (Anthropic).

For comprehensive information about the overall project, please refer to the [HL7 EU Confluence project page](https://confluence.hl7.org/x/UQfEE).

### Project Objectives

This initiative employs a combined model-driven and LLM-assisted approach to achieve several key objectives. 
The primary goals include the formalization and consolidation of the discussed Concept Model, integration with the HL7 tooling ecosystem, and systematic mapping from ontological concepts to FHIR resources. 

Moreover, Ontologies are increasingly recognized as a key complement to Large Language Models (LLM), enabling more structured and semantically grounded GenAI applications. This synergy offers particular promises. As an example, enhancing data analysis through Retrieval-Augmented Generation (RAG) techniques. 

The underlying objective is to investigate the reciprocal relationship between artificial intelligence and healthcare standards—exploring not only how AI technologies can support and enhance standards development, but also how formal standards and ontological frameworks can improve AI reliability and precision.

### Generated Artifacts

The following artifacts have been produced from the UML model:

Ontology:
- [EuropeanCancerModel-v02.rdf](https://github.com/slotti64/HL7-EU-Common-cancer-concept-model/blob/main/OWL/CommonCancerModel-v2.1.rdf) current ontology in RDF/XML serialization format.
- [EuropeanCancerModel-v02.jsonld](https://github.com/slotti64/HL7-EU-Common-cancer-concept-model/blob/main/OWL/CommonCancerModel-v2.1.jsonld) current ontology in JSON-LD serialization format.
- [EuropeanCancerModel-v02.ofn](https://github.com/slotti64/HL7-EU-Common-cancer-concept-model/blob/main/OWL/CommonCancerModel-v2.1.ofn) current ontology in OWL Functional serialization format.
- [EuropeanCancerModel-v02.ttl](https://github.com/slotti64/HL7-EU-Common-cancer-concept-model/blob/main/OWL/CommonCancerModel-v2.1.ttl) current ontology in turtle serialization format.

Models
- [HL7CommonCancerModelV2.1.mdzip](https://github.com/slotti64/HL7-EU-Common-cancer-concept-model/blob/main/ModelMagicDraw/HL7CommonCancerModelV2.1.mdzip) ontology model in MagicDraw Cameo Concept Modeler.
- [ModelEclipseUML](https://github.com/slotti64/HL7-EU-Common-cancer-concept-model/blob/main/ModelEclipseUML/) the directory includes the Eclipse UML files to import the model in OSS tools as Papyrus UML (shortly we'll release the imported Papyrus Model).

### OWL to PlantUML Transformation

A Python utility ([owl2plantuml_v17.py](https://github.com/slotti64/HL7-EU-Common-cancer-concept-model/tree/main/OWL2PlantUML/)) has been developed to transform OWL 2 ontologies into PlantUML diagrams, enabling automated generation of visual representations from the formal model. This tool was developed using an LLM-assisted coding approach with Claude 3.7.

### Documentation

The presentation delivered at the Madrid Working Group Meeting (May 2025) can be accessed [here](https://github.com/slotti64/HL7-EU-Common-cancer-concept-model/blob/main/Presentations/Common%20Cancer%20Model%20-%20Madrid%20WGM%20Presentation.pptx).

### Current Model Diagram

![HL7 EU Common Cancer Concept Model - UML Diagram v2](https://github.com/slotti64/HL7-EU-Common-cancer-concept-model/blob/main/HL7EU-CommonCancerModel-full-v2.1.jpg)

---

**Status**: This work is currently a draft under discussion within the HL7 EU community.

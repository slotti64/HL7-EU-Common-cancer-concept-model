#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import re
import xml.etree.ElementTree as ET
from urllib.parse import urlparse

def parse_namespaces(root):
    """Estrae i namespace dal documento OWL"""
    namespaces = {}
    for key, value in root.attrib.items():
        if key.startswith('{http://www.w3.org/XML/1998/namespace}') or key.startswith('xmlns:'):
            prefix = key.split(':')[-1]
            namespaces[prefix] = value
    
    # Aggiungi anche i namespace standard
    if 'rdf' not in namespaces:
        namespaces['rdf'] = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
    if 'rdfs' not in namespaces:
        namespaces['rdfs'] = 'http://www.w3.org/2000/01/rdf-schema#'
    if 'owl' not in namespaces:
        namespaces['owl'] = 'http://www.w3.org/2002/07/owl#'
    if 'xsd' not in namespaces:
        namespaces['xsd'] = 'http://www.w3.org/2001/XMLSchema#'
    
    return namespaces

def get_local_name(uri):
    """Estrae il nome locale da un URI"""
    if uri is None:
        return "Unknown"
    
    # Se è una lista, prende il primo elemento non vuoto
    if isinstance(uri, list):
        for item in uri:
            if item:
                uri = item
                break
    
    # Converte a stringa se non lo è già
    uri = str(uri)
    
    # Rimuovi eventuali namespace bracket
    uri = uri.replace('{', '').replace('}', '')
    
    # Prova a estrarre il frammento dopo # o l'ultimo segmento del percorso
    fragment = urlparse(uri).fragment
    if fragment:
        return fragment
    
    # Se non c'è un frammento, prendi l'ultimo segmento del percorso
    path = urlparse(uri).path
    if path:
        return os.path.basename(path)
    
    # Se ancora non funziona, cerca l'ultimo segmento dopo # o /
    match = re.search(r'[#/]([^#/]+)$', uri)
    if match:
        return match.group(1)
    
    return uri

def normalize_value(value):
    """Normalizza un valore che potrebbe essere una lista o un altro tipo di dato"""
    if value is None:
        return None
    
    # Se è una lista, prende il primo elemento non vuoto
    if isinstance(value, list):
        for item in value:
            if item:
                return normalize_value(item)
        return None
    
    # Altrimenti, restituisce il valore come stringa
    return str(value)

def extract_enumerations(root, namespaces):
    """Estrae le enumerazioni dal documento OWL"""
    enumerations = []
    
    # Definisci i namespace per la ricerca
    ns = {
        'rdf': namespaces.get('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'),
        'rdfs': namespaces.get('rdfs', 'http://www.w3.org/2000/01/rdf-schema#'),
        'owl': namespaces.get('owl', 'http://www.w3.org/2002/07/owl#')
    }
    
    # Cerca tutti gli elementi che potrebbero contenere enumerazioni
    for desc in root.findall('.//rdf:Description', ns):
        enum_id = desc.get(f'{{{ns["rdf"]}}}about')
        if not enum_id:
            continue
        
        # Cerca solo gli elementi che hanno owl:equivalentClass con owl:oneOf
        equiv_class = desc.find('./owl:equivalentClass/rdfs:Datatype/owl:oneOf', ns)
        if equiv_class is None:
            continue
        
        enum_name = get_local_name(enum_id)
        enum_values = []
        
        # Estrai valori da una lista RDF
        current_node = equiv_class.find('./rdf:Description', ns)
        while current_node is not None:
            rdf_first = current_node.find('./rdf:first', ns)
            if rdf_first is not None and rdf_first.text:
                enum_values.append(rdf_first.text)
            
            # Vai al prossimo elemento nella lista RDF
            rdf_rest = current_node.find('./rdf:rest', ns)
            if rdf_rest is None:
                break
                
            rest_resource = rdf_rest.get(f'{{{ns["rdf"]}}}resource')
            if rest_resource == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#nil':
                break
                
            current_node = rdf_rest.find('./rdf:Description', ns)
        
        # Estrai annotazioni
        comment = desc.find('./rdfs:comment', ns)
        comment_text = comment.text if comment is not None else ""
        
        if enum_values:
            enumerations.append({
                'name': enum_name,
                'values': enum_values,
                'comment': comment_text
            })
    
    return enumerations

def extract_classes(root, namespaces):
    """Estrae le classi dall'ontologia"""
    classes = []
    equivalent_classes = []  # Lista per memorizzare le classi equivalenti
    
    # Definisci i namespace per la ricerca
    ns = {
        'rdf': namespaces.get('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'),
        'rdfs': namespaces.get('rdfs', 'http://www.w3.org/2000/01/rdf-schema#'),
        'owl': namespaces.get('owl', 'http://www.w3.org/2002/07/owl#')
    }
    
    # Cerca tutte le classi (in diversi formati OWL)
    class_elements = []
    
    # Aggiungi classi in formato OWL/XML e RDF/XML
    class_elements.extend(root.findall('.//owl:Class', ns))
    class_elements.extend(root.findall('.//rdfs:Class', ns))
    
    # Raccogli i nomi delle classi già aggiunte per evitare duplicati
    added_classes = set()
    
    # Estrai informazioni da ogni classe trovata
    for cls in class_elements:
        class_id = cls.get(f'{{{ns["rdf"]}}}about') or cls.get(f'{{{ns["rdf"]}}}ID')
        if not class_id:
            continue
            
        class_name = get_local_name(class_id)
        if class_name in added_classes:
            continue
            
        added_classes.add(class_name)
        
        class_info = {
            'name': class_name,
            'annotations': extract_annotations(cls, ns),
            'subClassOf': [],  # Lista di superclassi
            'equivalentTo': []  # Lista di classi equivalenti
        }
        
        # Cerca relazioni subClassOf esplicite
        for subclass_rel in cls.findall('./rdfs:subClassOf', ns):
            resource = subclass_rel.get(f'{{{ns["rdf"]}}}resource')
            if resource:
                parent_class = get_local_name(resource)
                if parent_class and parent_class not in class_info['subClassOf']:
                    class_info['subClassOf'].append(parent_class)
            else:
                # Cerca classi annidate in subClassOf
                nested_classes = subclass_rel.findall('./owl:Class', ns)
                if nested_classes:
                    for nested in nested_classes:
                        nested_id = nested.get(f'{{{ns["rdf"]}}}about') or nested.get('IRI')
                        if nested_id:
                            parent_class = get_local_name(nested_id)
                            if parent_class and parent_class not in class_info['subClassOf']:
                                class_info['subClassOf'].append(parent_class)
        
        # Cerca classi equivalenti
        for equivClass in cls.findall('./owl:equivalentClass', ns):
            resource = equivClass.get(f'{{{ns["rdf"]}}}resource')
            if resource:
                equiv_name = get_local_name(resource)
                if equiv_name and equiv_name not in class_info['equivalentTo']:
                    class_info['equivalentTo'].append(equiv_name)
            else:
                # Cerca classi annidate in equivalentClass
                nested_classes = equivClass.findall('./owl:Class', ns)
                if nested_classes:
                    for nested in nested_classes:
                        nested_id = nested.get(f'{{{ns["rdf"]}}}about') or nested.get('IRI')
                        if nested_id:
                            equiv_name = get_local_name(nested_id)
                            if equiv_name and equiv_name not in class_info['equivalentTo']:
                                class_info['equivalentTo'].append(equiv_name)
        
        classes.append(class_info)
    
    # Cerca dichiarazioni di SubClassOf dirette
    for subClassOf in root.findall('.//owl:SubClassOf', ns):
        sub_cls = None
        super_cls = None
        
        # Trova la sottoclasse
        sub_class_elem = subClassOf.find('./owl:Class', ns)
        if sub_class_elem is not None:
            sub_cls = get_local_name(sub_class_elem.get('IRI') or sub_class_elem.get(f'{{{ns["rdf"]}}}about'))
        
        # Trova la superclasse
        super_class_elem = subClassOf.find('./owl:Class[2]', ns)
        if super_class_elem is not None:
            super_cls = get_local_name(super_class_elem.get('IRI') or super_class_elem.get(f'{{{ns["rdf"]}}}about'))
        
        if sub_cls and super_cls:
            # Aggiorna una classe esistente o aggiungi una nuova
            existing_class = next((c for c in classes if c['name'] == sub_cls), None)
            if existing_class:
                if super_cls not in existing_class['subClassOf']:
                    existing_class['subClassOf'].append(super_cls)
            else:
                classes.append({
                    'name': sub_cls,
                    'subClassOf': [super_cls],
                    'annotations': [],
                    'equivalentTo': []
                })
    
    # Cerca anche relazioni di sottoclasse espresse in formato RDF/RDFS
    for subclass_stmt in root.findall('.//*[@rdf:type="http://www.w3.org/2000/01/rdf-schema#subClassOf"]', ns):
        sub_cls = get_local_name(subclass_stmt.get(f'{{{ns["rdf"]}}}subject'))
        super_cls = get_local_name(subclass_stmt.get(f'{{{ns["rdf"]}}}object'))
        
        if sub_cls and super_cls:
            existing_class = next((c for c in classes if c['name'] == sub_cls), None)
            if existing_class:
                if super_cls not in existing_class['subClassOf']:
                    existing_class['subClassOf'].append(super_cls)
            else:
                classes.append({
                    'name': sub_cls,
                    'subClassOf': [super_cls],
                    'annotations': [],
                    'equivalentTo': []
                })
    
    # Cerca dichiarazioni dirette di EquivalentClasses
    for equivClasses in root.findall('.//owl:EquivalentClasses', ns):
        class_names = []
        
        # Estrai tutti i nomi delle classi equivalenti
        for cls_elem in equivClasses.findall('./owl:Class', ns):
            class_name = get_local_name(cls_elem.get('IRI') or cls_elem.get(f'{{{ns["rdf"]}}}about'))
            if class_name:
                class_names.append(class_name)
        
        # Se abbiamo almeno due classi equivalenti
        if len(class_names) >= 2:
            equivalent_classes.append(class_names)
    
    # Aggiorna le classi con le equivalenze trovate
    for equiv_group in equivalent_classes:
        for i, class_name in enumerate(equiv_group):
            for j in range(len(equiv_group)):
                if i != j:  # Evita di rendere una classe equivalente a se stessa
                    # Trova la classe e aggiorna le sue equivalenze
                    existing_class = next((c for c in classes if c['name'] == class_name), None)
                    if existing_class:
                        if equiv_group[j] not in existing_class['equivalentTo']:
                            existing_class['equivalentTo'].append(equiv_group[j])
                    else:
                        # Se la classe non esiste ancora, creala
                        classes.append({
                            'name': class_name,
                            'annotations': [],
                            'subClassOf': [],
                            'equivalentTo': [equiv_group[j]]
                        })
    
    return classes

def extract_annotations(element, ns):
    """Estrae le annotazioni da un elemento"""
    annotations = []
    
    # Estrai le annotazioni esplicite
    for annot in element.findall('./owl:Annotation', ns):
        prop = annot.find('./owl:AnnotationProperty', ns)
        prop_name = get_local_name(prop.get('IRI') if prop is not None else None)
        
        literal = annot.find('./owl:Literal', ns)
        value = literal.text if literal is not None else None
        
        if prop_name and value:
            annotations.append({
                'property': normalize_value(prop_name),
                'value': normalize_value(value)
            })
    
    # Estrai anche le annotazioni RDF/XML
    
    #for label in element.findall(f'./rdfs:label', ns):
    #    annotations.append({
    #        'property': 'label',
    #        'value': normalize_value(label.text)
    #    })
    
    for comment in element.findall(f'./rdfs:comment', ns):
        annotations.append({
            'property': 'comment',
            'value': normalize_value(comment.text)
        })
    
    return annotations

def extract_properties(root, namespaces):
    """Estrae le proprietà dell'ontologia"""
    properties = []
    
    # Definisci i namespace per la ricerca
    ns = {
        'rdf': namespaces.get('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'),
        'rdfs': namespaces.get('rdfs', 'http://www.w3.org/2000/01/rdf-schema#'),
        'owl': namespaces.get('owl', 'http://www.w3.org/2002/07/owl#')
    }
    
    # Cerca ObjectProperty
    for prop in root.findall('.//owl:ObjectProperty', ns):
        prop_info = {
            'name': normalize_value(get_local_name(prop.get(f'{{{ns["rdf"]}}}about') or prop.get(f'{{{ns["rdf"]}}}ID'))),
            'type': 'ObjectProperty',
            'domain': None,
            'range': None,
            'annotations': extract_annotations(prop, ns)
        }
        
        # Estrai dominio
        domains = []
        for domain in prop.findall(f'./rdfs:domain', ns):
            # Controlla se il dominio è una risorsa diretta
            resource = domain.get(f'{{{ns["rdf"]}}}resource')
            if resource:
                domains.append(normalize_value(get_local_name(resource)))
            else:
                # Cerca classi annidate (ad esempio in unionOf)
                union_of = domain.find(f'./owl:Class/owl:unionOf', ns)
                if union_of is not None:
                    # Estrai tutte le classi nella raccolta unionOf
                    for desc in domain.findall(f'.//rdf:Description', ns):
                        resource = desc.get(f'{{{ns["rdf"]}}}about')
                        if resource:
                            domains.append(normalize_value(get_local_name(resource)))
        
        # Estrai range
        ranges = []
        for range_elem in prop.findall(f'./rdfs:range', ns):
            resource = range_elem.get(f'{{{ns["rdf"]}}}resource')
            if resource:
                ranges.append(normalize_value(get_local_name(resource)))
        
        # Se abbiamo trovato domini multipli, creiamo una proprietà per ciascun dominio
        if domains:
            for domain in domains:
                # Copia l'info di base della proprietà
                domain_prop_info = prop_info.copy()
                domain_prop_info['domain'] = domain
                
                # Usa il primo range trovato o None
                domain_prop_info['range'] = ranges[0] if ranges else None
                
                properties.append(domain_prop_info)
        else:
            # Se non abbiamo trovato domini, aggiungi comunque la proprietà con dominio None
            prop_info['range'] = ranges[0] if ranges else None
            properties.append(prop_info)
    
    # Cerca DataProperty
    for prop in root.findall('.//owl:DatatypeProperty', ns):
        prop_info = {
            'name': normalize_value(get_local_name(prop.get(f'{{{ns["rdf"]}}}about') or prop.get(f'{{{ns["rdf"]}}}ID'))),
            'type': 'DataProperty',
            'domain': None,
            'range': None,
            'annotations': extract_annotations(prop, ns)
        }
        
        # Estrai dominio
        for domain in prop.findall(f'./rdfs:domain', ns):
            prop_info['domain'] = normalize_value(get_local_name(domain.get(f'{{{ns["rdf"]}}}resource')))
        
        # Estrai range
        for range_elem in prop.findall(f'./rdfs:range', ns):
            prop_info['range'] = normalize_value(get_local_name(range_elem.get(f'{{{ns["rdf"]}}}resource')))
        
        properties.append(prop_info)
    
    # Cerca anche proprietà dati in formato RDF/RDFS
    for prop in root.findall('.//*[@rdf:type="http://www.w3.org/2002/07/owl#DatatypeProperty"]', ns):
        prop_name = normalize_value(get_local_name(prop.get(f'{{{ns["rdf"]}}}about')))
        if prop_name:
            prop_info = {
                'name': prop_name,
                'type': 'DataProperty',
                'domain': None,
                'range': None,
                'annotations': []
            }
            
            # Cerca dichiarazioni di dominio e range separate
            for stmt in root.findall(f'.//*[@rdf:subject="{prop.get(f"{{{ns["rdf"]}}}about")}"]', ns):
                pred = stmt.get(f'{{{ns["rdf"]}}}predicate')
                obj = stmt.get(f'{{{ns["rdf"]}}}object')
                
                if pred == f'{{{ns["rdfs"]}}}domain':
                    prop_info['domain'] = normalize_value(get_local_name(obj))
                elif pred == f'{{{ns["rdfs"]}}}range':
                    prop_info['range'] = normalize_value(get_local_name(obj))
            
            properties.append(prop_info)
    
    # Cerca anche dichiarazioni di dominio e range dirette
    for domain_decl in root.findall('.//owl:ObjectPropertyDomain', ns):
        prop_elem = domain_decl.find('./owl:ObjectProperty', ns)
        class_elem = domain_decl.find('./owl:Class', ns)
        
        if prop_elem is not None and class_elem is not None:
            prop_name = normalize_value(get_local_name(prop_elem.get('IRI')))
            domain_class = normalize_value(get_local_name(class_elem.get('IRI')))
            
            # Aggiorna una proprietà esistente o aggiungi una nuova
            existing_prop = next((p for p in properties if p['name'] == prop_name), None)
            if existing_prop:
                existing_prop['domain'] = domain_class
            else:
                properties.append({
                    'name': prop_name,
                    'type': 'ObjectProperty',
                    'domain': domain_class,
                    'range': None,
                    'annotations': []
                })
    
    for range_decl in root.findall('.//owl:ObjectPropertyRange', ns):
        prop_elem = range_decl.find('./owl:ObjectProperty', ns)
        class_elem = range_decl.find('./owl:Class', ns)
        
        if prop_elem is not None and class_elem is not None:
            prop_name = normalize_value(get_local_name(prop_elem.get('IRI')))
            range_class = normalize_value(get_local_name(class_elem.get('IRI')))
            
            # Aggiorna una proprietà esistente o aggiungi una nuova
            existing_prop = next((p for p in properties if p['name'] == prop_name), None)
            if existing_prop:
                existing_prop['range'] = range_class
            else:
                properties.append({
                    'name': prop_name,
                    'type': 'ObjectProperty',
                    'domain': None,
                    'range': range_class,
                    'annotations': []
                })
    
    # Estrai anche le proprietà di tipo attributo (per diagramma PlantUML)
    for cls in root.findall('.//owl:Class', ns) + root.findall('.//rdfs:Class', ns):
        class_id = cls.get(f'{{{ns["rdf"]}}}about') or cls.get(f'{{{ns["rdf"]}}}ID')
        if not class_id:
            continue
            
        class_name = normalize_value(get_local_name(class_id))
        
        # Cerca attributi definiti direttamente nella classe
        for property_elem in cls.findall('./owl:hasKey/owl:DataProperty', ns):
            prop_name = normalize_value(get_local_name(property_elem.get('IRI')))
            if prop_name:
                properties.append({
                    'name': prop_name,
                    'type': 'DataProperty',
                    'domain': class_name,
                    'range': 'String',  # Default range se non specificato
                    'annotations': []
                })
    
    return properties

def extract_enum_references(properties):
    """Estrae i riferimenti alle enumerazioni dalle proprietà"""
    enum_references = []
    
    for prop in properties:
        if prop['type'] == 'DataProperty' and prop['domain'] and prop['range']:
            # Cerca i range che potrebbero essere enumerazioni
            # Tipicamente i nomi terminano con 'Type'
            range_name = normalize_value(prop['range'])
            if range_name.endswith('Type'):
                enum_references.append({
                    'from': normalize_value(prop['domain']),
                    'to': range_name,
                    'property': normalize_value(prop['name'])
                })
    
    return enum_references

def extract_relations(classes, properties):
    """Estrae le relazioni tra le classi basate sulle proprietà oggetto"""
    relations = []
    
    # Le relazioni provengono dalle ObjectProperty con dominio e range specificati
    for prop in properties:
        if prop['type'] == 'ObjectProperty' and prop['domain'] and prop['range']:
            # Non includere relazioni con dominio "Unknown"
            domain = normalize_value(prop['domain'])
            if domain and domain != "Unknown":
                relations.append({
                    'from': domain,
                    'to': normalize_value(prop['range']),
                    'name': normalize_value(prop['name']),
                    'type': '-->'
                })
    
    # Aggiungi anche le relazioni di sottoclasse
    for cls in classes:
        for superclass in cls.get('subClassOf', []):
            if superclass:  # Verifica che non sia None o vuoto
                # Normalizza il valore della superclasse
                superclass_str = normalize_value(superclass)
                if superclass_str and superclass_str != "Unknown":
                    relations.append({
                        'from': superclass_str,
                        'to': normalize_value(cls['name']),
                        'name': 'subClassOf',
                        'type': '<|--'
                    })
        
        # Aggiungi le relazioni di equivalenza
        for equiv_class in cls.get('equivalentTo', []):
            equiv_class_str = normalize_value(equiv_class)
            if equiv_class_str and equiv_class_str != "Unknown":
                relations.append({
                    'from': normalize_value(cls['name']),
                    'to': equiv_class_str,
                    'name': 'equivalentTo',
                    'type': '..'  # Una linea punteggiata per equivalenza
                })
    
    # Rimuovi duplicati delle relazioni di equivalenza
    # (poiché se A equivale a B, abbiamo aggiunto sia A--B che B--A)
    unique_relations = []
    equiv_pairs = set()
    
    for rel in relations:
        if rel['name'] == 'equivalentTo':
            # Ordina i nomi per creare una chiave univoca indipendente dall'ordine
            pair = tuple(sorted([rel['from'], rel['to']]))
            if pair not in equiv_pairs and "Unknown" not in pair:
                equiv_pairs.add(pair)
                unique_relations.append(rel)
        else:
            # Assicurati che nessuna estremità della relazione sia "Unknown"
            if rel['from'] != "Unknown" and rel['to'] != "Unknown":
                unique_relations.append(rel)
    
    return unique_relations

def generate_plantuml(classes, properties, relations, enumerations, enum_references):
    """Genera il diagramma PlantUML dall'ontologia"""
    plantuml = '@startuml\n\n'
    plantuml += '!theme vibrant\n\n'
    plantuml += 'title EU Cancer Ontology Model\n\n'
    
    # Definisci legenda
    plantuml += 'legend\n'
    plantuml += '  |= Tipo di relazione |= Significato |\n'
    plantuml += '  | A <|-- B | B è sottoclasse di A |\n'
    plantuml += '  | A --> B | A ha una relazione con B |\n'
    plantuml += '  | A .. B : equivalentTo | A è equivalente a B |\n'
    plantuml += '  | A --> B : type | A utilizza l\'enumerazione B |\n'
    plantuml += 'endlegend\n\n'
    
    # Aggiungi le definizioni delle enumerazioni
    for enum in enumerations:
        plantuml += f'enum "{enum["name"]}" {{\n'
        
        # Aggiungi i valori dell'enumerazione
        for value in enum['values']:
            plantuml += f'  {value}\n'
        
        # Aggiungi commento se presente
        if enum['comment']:
            plantuml += '\n  .. comment ..\n'
            comment = enum['comment']
            if len(comment) > 50:
                comment = comment[:47] + '...'
            plantuml += f'  {comment}\n'
        
        plantuml += '}\n\n'
    
    # Raggruppa le proprietà dati per classe di dominio
    class_attributes = {}
    
    for prop in properties:
        if prop['type'] == 'DataProperty' and prop['domain']:
            domain = normalize_value(prop['domain'])
            if domain and domain != "Unknown":
                range_type = normalize_value(prop['range']) if prop['range'] else 'String'
                prop_name = normalize_value(prop['name'])
                
                if domain not in class_attributes:
                    class_attributes[domain] = []
                
                class_attributes[domain].append({
                    'name': prop_name,
                    'type': range_type
                })
    
    # Aggiungi classi con i loro attributi
    for cls in classes:
        # Assicurati che il nome della classe sia una stringa
        class_name = normalize_value(cls["name"])
        
        plantuml += f'class "{class_name}" {{\n'
        
        # Aggiungi attributi (proprietà dati)
        if class_name in class_attributes:
            for attr in class_attributes[class_name]:
                plantuml += f'  +{attr["type"]} {attr["name"]}\n'
        
        # Aggiungi una riga vuota se ci sono sia attributi che annotazioni
        if class_name in class_attributes and cls['annotations']:
            plantuml += '\n'
        
        # Aggiungi annotazioni come note
        for annotation in cls['annotations']:
            prop_name = normalize_value(annotation["property"])
            plantuml += f'  .. {prop_name} ..\n'
            
            # Pulisci il valore dell'annotazione per il formato PlantUML
            value = normalize_value(annotation['value'])
            if value and len(value) > 50:
                value = value[:47] + '...'
            plantuml += f'  {value}\n'
        
        plantuml += '}\n\n'
    
    # Aggiungi relazioni
    for relation in relations:
        if relation['from'] and relation['to']:
            # Normalizza i valori
            from_class = normalize_value(relation['from'])
            to_class = normalize_value(relation['to'])
            rel_type = relation['type']
            rel_name = relation['name']
            
            if rel_type == '<|--':
                # Relazione di ereditarietà
                plantuml += f'"{from_class}" {rel_type} "{to_class}"\n'
            elif rel_name == 'equivalentTo':
                # Relazione di equivalenza con stile specifico
                plantuml += f'"{from_class}" .. "{to_class}" : {rel_name}\n'
            else:
                # Relazione normale
                plantuml += f'"{from_class}" {rel_type} "{to_class}" : {rel_name}\n'
    
    # Aggiungi relazioni con le enumerazioni
    for ref in enum_references:
        from_class = normalize_value(ref['from'])
        to_enum = normalize_value(ref['to'])
        prop_name = normalize_value(ref['property'])
        
        # Verifica che l'enumerazione esista
        if any(enum['name'] == to_enum for enum in enumerations):
            plantuml += f'"{from_class}" --> "{to_enum}" : {prop_name}\n'
    
    plantuml += '@enduml'
    
    return plantuml

def convert_owl2plantuml(input_file, output_file):
    """Converte un file OWL in formato PlantUML"""
    try:
        # Parsa il file OWL
        tree = ET.parse(input_file)
        root = tree.getroot()
        
        # Estrai i namespace
        namespaces = parse_namespaces(root)
        
        # Estrai gli elementi dell'ontologia
        classes = extract_classes(root, namespaces)
        properties = extract_properties(root, namespaces)
        enumerations = extract_enumerations(root, namespaces)
        enum_references = extract_enum_references(properties)
        relations = extract_relations(classes, properties)
        
        # Genera il PlantUML
        plantuml_content = generate_plantuml(classes, properties, relations, enumerations, enum_references)
        
        # Scrivi il risultato su file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(plantuml_content)
        
        print(f"File PlantUML generato con successo: {output_file}")
        
    except Exception as e:
        print(f"Errore durante la conversione: {e}")
        raise

def main():
    """Funzione principale"""
    parser = argparse.ArgumentParser(description='Converti un file OWL in diagramma PlantUML')
    parser.add_argument('input', help='File OWL di input')
    parser.add_argument('output', help='File PlantUML di output')
    
    args = parser.parse_args()
    
    convert_owl2plantuml(args.input, args.output)

if __name__ == '__main__':
    main()
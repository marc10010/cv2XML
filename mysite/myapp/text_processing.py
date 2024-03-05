import xml.etree.ElementTree as ET
import xml.dom.minidom
import re
from . import interface

# Genera el XML con los campos generados por la IA
def generate_xml(person_data):
    root = ET.Element("personas")
    persona = ET.SubElement(root, "persona")
    for key, value in person_data.items():
        if isinstance(value, list) and value:
            container_element = ET.SubElement(persona, key)
            for item in value:
                if key == 'idiomas':
                   # Omite el primer elemento si es "Idiomas:"
                    if item.startswith("Idiomas:"):
                        continue
                    idioma = item.lstrip('- ')
                    ET.SubElement(container_element, 'idioma').text = idioma
                elif key == 'titulaciones':
                    # Omite el primer elemento si es "Titulaciones:"
                    if item.startswith("Titulaciones:"):
                        continue
                    titulacion = item.lstrip('- ')
                    ET.SubElement(container_element, 'titulacion').text = titulacion
                elif key == 'experiencias':
                    # Omite el primer elemento si es "Experiencias:"
                    if item.startswith("Experiencias:"):
                        continue
                    experiencia = item.lstrip('- ')
                    ET.SubElement(container_element, 'experiencia').text = experiencia
                elif key == 'referencias':
                    # Omite el primer elemento si es Referencias:"
                    if item.startswith("Referencias:"):
                        continue
                    referencia = item.lstrip('- ')
                    ET.SubElement(container_element, 'referencia').text = referencia
        else:
            ET.SubElement(persona, key).text = value

    rough_string = ET.tostring(root, 'unicode')
    reparsed = xml.dom.minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")



#Extrae los campos 
def extract_field(text, field_name):
    pattern = re.compile(rf"{field_name}\s*:\s*(.*)")
    match = pattern.search(text)
    return match.group(1).strip() if match else ""

#Extrae una lista de campos 
def extract_list(text, list_name):
    # Primero encuentra la posición donde comienza la lista
    start_index = text.find(f"{list_name}:")
    if start_index == -1:
        return []
    # Inicializa el end_index al final del texto por defecto
    end_index = len(text)
    # Encuentra el final de la lista (puede ser el inicio de otro campo o el final del texto)
    temp_index = text.find("\n", start_index + 1)
    while temp_index != -1:
        if text[temp_index + 1] == '-':
            temp_index = text.find("\n", temp_index + 1)
        else:
            end_index = temp_index
            break

    # Extrae la porción de texto que contiene la lista
    list_text = text[start_index:end_index]

    # Divide en elementos individuales
    return [line.strip() for line in list_text.split('\n') if line.strip()]

# Pasa el  texto generado con la IA a futuros tags XML
def parse_ai_response(ai_text):
    person_data = {
        "nombre": extract_field(ai_text, "Nombre"),
        "apellidos": extract_field(ai_text, "Apellidos"),
        "nombre_completo": extract_field(ai_text, "Nombre Completo"),
        "descripcion": extract_field(ai_text, "Descripción"),
        "subcategoria": extract_field(ai_text, "Subcategoría"),
        "ciudad": extract_field(ai_text, "Ciudad"),
        "telefono": extract_field(ai_text, "Teléfono"),
        "email": extract_field(ai_text, "Email"),
        "idiomas": extract_list(ai_text, "Idiomas"),
        "titulaciones": extract_list(ai_text, "Titulaciones"),
        "experiencias": extract_list(ai_text, "Experiencias"),
        "referencias": extract_list(ai_text, "Referencias")
    }
     # Imprimir el diccionario para depuración
    print("Datos Extraídos para XML:")
    print(person_data)

    return person_data

def update_xml_output(xml_text):
    interface.text_xml_output.delete('1.0', 'end')
    interface.text_xml_output.insert('1.0', xml_text)

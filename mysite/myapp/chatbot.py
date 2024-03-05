from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from . import (config, text_processing, interface)

# Prompt y interacción con la IA
def my_chatbot(language, freeform_text):
    prompt_text = (f"Por favor, extrae y resume la siguiente información del documento en {language}: "
                  "nombre, apellidos, descripción, ciudad, teléfono, correo electrónico, idiomas, títulos académicos y experiencias laborales. "
                  "En el caso de que no encuentres una descripción para el campo Descripción, podrias crear una breve a partir de la información?"
                  "Haz especial hincapié en extraer las titulaciones y experiencias que encuentres en el texto del currículum. "
                  "También recuerda rellenar todos los campos como email y nombre completo, no te dejes ninguno vacío a no ser que no encuentres la información, en ese caso dejalo vacío."
                  "En cuanto a los idiomas listamelos en listas que los elementos empiezen por -,  las experiencias, las titulaciones y las referencias también."
                  "Recuerda añadir tambien a las referencias un guion - delante de cada una para poder procesarlas"
                  "En cambio las Referencias quiero que dentro de cada una añadas esta estructura: - persona_que_referencia|lugar|contacto"
                  "y respetas esa estructura para listar las referencias, las personas que no tengan lo dejas vacio."
                  "Tambien existe el campo Subcategoría, que puede ser una de estas: Capitán/a, Marinero/a, Azafato/a,"
                  "Ingeniero/a, Chef, Limpieza, Instrutor/a, Asistencia y Otro. Debes elegir una de estas. Si es patrón pondras Capitán/a."
                  "El telefono tiene que estar en este formato +XX XXX XXX XXX."
                  "Este es el documento a procesar.\n\n{freeform_text}\n\n"
                  "Nombre: \n"
                  "Apellidos: \n"
                  "Nombre Completo: \n"
                  "Descripción: \n"
                  "Subcategoría: \n"
                  "Ciudad: \n"
                  "Teléfono: \n"
                  "Email: \n"
                  "Idiomas: \n"
                  "Titulaciones: \n"
                  "Experiencias: \n"
                  "Referencias:")

    prompt = PromptTemplate(
        input_variables=["language", "freeform_text"],
        template=prompt_text
    )

    bedrock_chain = LLMChain(llm=config.llm, prompt=prompt)
    response = bedrock_chain.invoke({'language': language, 'freeform_text': freeform_text})

    # Imprime el texto procesado por la IA en la consola
    print("Texto Procesado por la IA:")
    print(response['text'])

    structured_response = text_processing.parse_ai_response(response['text'])
    xml_output = text_processing.generate_xml(structured_response)
    return xml_output

#  Proceso IA
def process_with_ai():
    freeform_text = config.textOnDocument
    interface.label_frase1.config(text="")
    if freeform_text:
        xml_result = my_chatbot(config.language, freeform_text)
        # Actualiza la GUI con el XML generado
        text_processing.update_xml_output(xml_result)
        interface.label_frase1.config(text="TRABAJO FINALIZADO")

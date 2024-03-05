import os
from botocore.exceptions import NoCredentialsError
import time
from . import interface, chatbot, config
import threading

def wait_for_textract_job_completion(s3_file_path):
    
    # Llama a Textract para analizar un documento
    response = config.textract_client.start_document_text_detection(
        DocumentLocation={'S3Object': {'Bucket': os.getenv('BUCKET_NAME'),
                                        'Name': s3_file_path}}
    )

    # Obtiene el JobId para verificar el estado más tarde
    job_id = response['JobId']
    print(f'JobId: {job_id}')
    interface.label_frase1.config(text="Se está extrayendo el texto.")
    # Espera a que el trabajo de Textract termine
    while True:
        response = config.textract_client.get_document_text_detection(JobId=job_id)
        status = response['JobStatus']

        if status in ['SUCCEEDED', 'FAILED', 'PARTIAL_SUCCESS']:
            break  # El trabajo ha terminado
        elif status == 'IN_PROGRESS':
            print("Extrayendo texto...")
            time.sleep(3)  
        else:
            raise ValueError(f"Estado de trabajo no reconocido: {status}")

    # Imprime el texto extraído directamente
    for item in response.get('Blocks', []):
        if item['BlockType'] == 'LINE':
            config.textOnDocument += item["Text"]

    # Actualiza la GUI con el texto extraído
    interface.update_extracted_text(config.textOnDocument)
    
    # Empieza a procesar la Ia una vez acabado el trabajo de textract
    threading.Thread(target=chatbot.process_with_ai).start()
    
    config.textOnDocument = ""
    
    print ("----La IA está realizando correctamente su tarea de extraer información----")
    
    interface.label_frase1.config(text="Se está realizando la generación del XML.")

#Carga el documento en el bucket AWS
def upload_to_s3(local_file_path, bucket_name, s3_file_path):
    try:
        # Sube el archivo al bucket de S3
        config.s3.upload_file(local_file_path, bucket_name, s3_file_path)

        print(f'Archivo subido correctamente a {bucket_name}/{s3_file_path}')
        return True
    except FileNotFoundError:
        print(f'Error: El archivo {local_file_path} no se encontró')
        return False
    except NoCredentialsError:
        print('Error: Credenciales no disponibles')
        return False

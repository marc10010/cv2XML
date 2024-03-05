import os
from tkinter import Tk, Label, Entry, Button, filedialog,Text,Scrollbar
from . import aws_interaction
import threading

# Pide el PATH
def browse_file(entry_file_path):
    clear_text_widgets()
    filename = filedialog.askopenfilename()
    entry_file_path.delete(0, 'end')
    entry_file_path.insert(0, filename)

# Procesa el documento
def validate_document(entry_file_path):
    if not os.path.exists(entry_file_path):
        print("El archivo no existe.")
        return
    bucket_name = os.getenv('BUCKET_NAME')
    s3_file_path = 'Script_uploaded/' + os.path.basename(entry_file_path)

    # Subir el archivo al S3 y luego iniciar el proceso en un hilo separado
    if aws_interaction.upload_to_s3(entry_file_path, bucket_name, s3_file_path):
        threading.Thread(target=lambda: aws_interaction.wait_for_textract_job_completion(s3_file_path)).start()

# Actualiza el texto de los widgets GUI
def update_extracted_text(text):
    text_extracted.delete('1.0', 'end')
    text_extracted.insert('1.0', text)

def update_xml_output(xml_text):
    text_xml_output.delete('1.0', 'end')
    text_xml_output.insert('1.0', xml_text)   

# Limpia el texto de los widgets GUI 
def clear_text_widgets():
    text_extracted.delete('1.0', 'end') 
    text_xml_output.delete('1.0', 'end')    
       
# Configuración de la interfaz gráfica
# Colores
color_fondo = "#ADD8E6"  # Azul celeste 
color_fondo_texto = "#E0FFFF"  # Azul celeste claro 
color_boton = "#00008B"  # Azul oscuro 

# Configuración de la interfaz gráfica
root = Tk()
root.title("Currículum a XML")
root.configure(bg=color_fondo)

# Etiqueta y entrada para el archivo
label_file_path = Label(root, text="Ruta del Archivo:", bg=color_fondo)
label_file_path.grid(row=0, column=0, padx=10, pady=10)
entry_file_path = Entry(root,bg=color_fondo_texto)
entry_file_path.grid(row=0, column=1, padx=10, pady=10)

# Botón para buscar el archivo
button_browse = Button(root, text="Buscar Archivo", command=lambda: browse_file(entry_file_path), bg=color_boton, fg='white', activebackground=color_boton)
button_browse.grid(row=0, column=2, padx=10, pady=10)

# Área de texto para mostrar el texto extraído
label_extracted_text = Label(root, text="Texto Extraído:", bg=color_fondo)
label_extracted_text.grid(row=2, column=0, padx=10, pady=10)
text_extracted = Text(root, height=10, width=50, bg=color_fondo_texto)
text_extracted.grid(row=2, column=1, columnspan=2, padx=10, pady=10)
scroll_extracted = Scrollbar(root, command=text_extracted.yview)
scroll_extracted.grid(row=2, column=3, sticky='nsew')
text_extracted['yscrollcommand'] = scroll_extracted.set

# Área de texto para mostrar el XML generado
label_xml_output = Label(root, text="Salida XML:", bg=color_fondo)
label_xml_output.grid(row=3, column=0, padx=10, pady=10)
text_xml_output = Text(root, height=10, width=50, bg=color_fondo_texto)
text_xml_output.grid(row=3, column=1, columnspan=2, padx=10, pady=10)
scroll_xml = Scrollbar(root, command=text_xml_output.yview)
scroll_xml.grid(row=3, column=3, sticky='nsew')
text_xml_output['yscrollcommand'] = scroll_xml.set

# Botón para procesar el documento
button_validate = Button(root, text="Procesar Documento", command=lambda: 
                         validate_document(entry_file_path), bg=color_boton, fg='white', activebackground=color_boton)
button_validate.grid(row=1, column=0, columnspan=3, pady=20)

label_frase1 = Label(root, text="", bg=color_fondo)
label_frase1.grid(row=5, column=0, columnspan=3, padx=10, pady=10)


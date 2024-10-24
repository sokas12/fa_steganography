import os
from PIL import Image
import stepic
import base64
import mimetypes

mime_extension_map = {
    'image/png': 'png',
    'application/pdf': 'pdf',
    'audio/mpeg': 'mp3',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',
    'text/plain': 'txt'
}

def hide_text_in_image(image_path, output_image_path, text_to_hide):
    img = Image.open(image_path)
    text_to_hide_bytes = text_to_hide.encode('utf-8')
    encoded_image = None
    try:
        encoded_image = stepic.encode(img, text_to_hide_bytes)
        print(f'Data hidden in {output_image_path} successfully')
    except:
        print("Data is too large for the image")
        exit(1)

    if encoded_image:
        encoded_image.save(output_image_path, 'PNG')

def read_hidden_text_image(image_path):
    decoded_text = ""
    if os.path.exists(image_path):
        img = Image.open(image_path)
        decoded_text = stepic.decode(img)
    else:
        print("Image path does not exist")
    return decoded_text

def hide_file_in_image(image_path, output_image_path, file_to_hide):
    data = base64_encode_with_mime(file_to_hide)
    hide_text_in_image(image_path, output_image_path, data)

def read_hidden_file_from_image(image_path):
    data = read_hidden_text_image(image_path)
    if data:
        base64_decode_file(data)

def base64_encode_with_mime(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    print(mime_type)
    if mime_type is None:
        raise ValueError("Cannot determine MIME type of the file.")
    
    file_extension = mime_extension_map.get(mime_type, 'bin')
    file_extension_len = str(len(file_extension))
    with open(file_path, "rb") as file:
        encoded_data = base64.b64encode(file.read()).decode('utf-8')
        return file_extension_len + file_extension + encoded_data

def base64_decode_file(encoded_string):
    file_extension_len = int(encoded_string[0]) + 1
    file_extension = encoded_string[1:file_extension_len]
    file_data = encoded_string[file_extension_len:]
    decoded_data = base64.b64decode(file_data)

    output_file_path = f'found_hidden_file.{file_extension}'

    with open(output_file_path, 'wb') as output_file:
        output_file.write(decoded_data)

    print(f"Hidden file saved as {output_file_path}")

#input obrazek pro encode dat
input_image_path = "image.png"

#encoded obrazek se skrytymi daty
output_image_path = "output_image.png"

#schovani stringu
string_to_hide = "neskutecne tajny textik"
hide_text_in_image(input_image_path, output_image_path, string_to_hide)

#precteni schovaneho string
hidden_text = read_hidden_text_image(output_image_path) 
print(hidden_text) 

#testovaci soubory
image_to_hide_path = "test.png" 
mp3_to_hide_path = "test.mp3"
pdf_to_hide_path = "test.pdf"
docx_to_hide_path = "test.docx"
text_to_hide_path = "test.txt"

#encoding
hide_file_in_image(input_image_path, output_image_path, pdf_to_hide_path)

#decoding
read_hidden_file_from_image(output_image_path) 

#pri snaze ulozit 1000 znaku do 50x50 obrazku, dostaneme error message
image50x50 = "test.png" 
too_long_string_to_hide = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum. N"
hide_text_in_image(image50x50, output_image_path, too_long_string_to_hide)
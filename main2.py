import convertapi
import os


convertapi.api_secret = 'zJxLOvfcsVOzUHE2'


def converting(file_to_convert, file_type_to, file_type_from, user_name):  # converting file; returning path to new file
    filename = os.path.abspath(file_to_convert)  #thinking that its a filename, so getting file path

    # filepath = r''

    result = convertapi.convert(file_type_to, {'File': f'{filename}'}, from_format=file_type_from)
    result.file.save(f'{user_name}.{file_type_to}')  # saving new file with the result

    return rf"{os.path.abspath(f'{user_name}.{file_type_to}')}"



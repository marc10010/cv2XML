import os
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from . import interface


@api_view(["GET"])
def getBucketPath(request):
    return Response({"message": "This is the bucketPath"}, status=status.HTTP_200_OK)


@api_view(["POST"])
def uploadFile(request):

    uploaded_file = request.FILES['myFile']

    if uploaded_file:

        _, file_extension = os.path.splitext(uploaded_file.name)
        file_extension = file_extension.lower()

        if file_extension not in ['.pdf', '.jpg', '.jpeg', '.png', '.gif']:
            return Response({"message": "File format not supported"}, status=status.HTTP_400_BAD_REQUEST)

        current_directory = os.getcwd()
        file_path = os.path.join(current_directory, uploaded_file.name)

        with open(file_path, 'wb+') as new_file:
            for chunk in uploaded_file.chunks():
                new_file.write(chunk)

        if file_extension == '.pdf':
            interface.validate_document(file_path)
            return Response({"message": "PDF uploaded and validated"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Image uploaded successfully"}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "No file received"}, status=status.HTTP_400_BAD_REQUEST)


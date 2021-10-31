import os
import requests 
API_KEY = "ammusravya1930@gmail.com_dd814ccb7ba74c5ca22840a422291853b7a5"
BASE_URL = "https://api.pdf.co/v1"
SourceFile = ".\\sample.pdf"
Pages = ""
Password = ""
DestinationFile = ".\\result.xml"


def main(args = None):
    uploadedFileUrl = uploadFile(SourceFile)
    if (uploadedFileUrl != None):
        convertPdfToXml(uploadedFileUrl, DestinationFile)


def convertPdfToXml(uploadedFileUrl, destinationFile):
    """Converts PDF To XML using PDF.co Web API"""
    parameters = {}
    parameters["name"] = os.path.basename(destinationFile)
    parameters["password"] = Password
    parameters["pages"] = Pages
    parameters["url"] = uploadedFileUrl
    url = "{}/pdf/convert/to/xml".format(BASE_URL)
    response = requests.post(url, data=parameters, headers={ "x-api-key": API_KEY })
    if (response.status_code == 200):
        json = response.json()

        if json["error"] == False:
            resultFileUrl = json["url"]            
            r = requests.get(resultFileUrl, stream=True)
            if (r.status_code == 200):
                with open(destinationFile, 'wb') as file:
                    for chunk in r:
                        file.write(chunk)
                print(f"Result file saved as \"{destinationFile}\" file.")
            else:
                print(f"Request error: {response.status_code} {response.reason}")
        else:
            print(json["message"])
    else:
        print(f"Request error: {response.status_code} {response.reason}")


def uploadFile(fileName):
    """Uploads file to the cloud"""
    url = "{}/file/upload/get-presigned-url?contenttype=application/octet-stream&name={}".format(
        BASE_URL, os.path.basename(fileName))
    
    response = requests.get(url, headers={ "x-api-key": API_KEY })
    if (response.status_code == 200):
        json = response.json()
        
        if json["error"] == False:
            uploadUrl = json["presignedUrl"]
            uploadedFileUrl = json["url"]
            with open(fileName, 'rb') as file:
                requests.put(uploadUrl, data=file, headers={ "x-api-key": API_KEY, "content-type": "application/octet-stream" })

            return uploadedFileUrl
        else:
            print(json["message"])    
    else:
        print(f"Request error: {response.status_code} {response.reason}")

    return None


if _name_ == '_main_':
    main()
 
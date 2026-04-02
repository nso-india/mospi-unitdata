import requests
import os
from typing import List, Dict, Any


def listDatasets(pageNo=1) -> List[Dict[str, Any]]:
  
    try:
  
     response = requests.get("https://microdata.gov.in/NADA/index.php/api/listdatasets?page="+str(pageNo),headers=None)

     data = response.json()

     return data
    
    except Exception as e: 
      print('Error while downloading the data:',e)
       
     
    return None 


def getDatasets(folderPath, apiKey):

    page = 1
    errorFlag = False

    while True:

        data = listDatasets(page)

        if data is None:
            print('Error occurred while downloading the data!')
            errorFlag = True
            break

        rows = data["result"]["rows"]

        indexed_data = [
            {**item, "index": i}
            for i, item in enumerate(rows, start=1)
        ]

        for item in indexed_data:
            print(item["id"] + ":" + item["title"])

        total = int(data["result"]["total"])
        limit = int(data["result"]["limit"])

        pages = total // limit + (1 if total % limit else 0)

        user_input = input(
            f"Total pages:{pages}, Page:{page} of {pages},\n"
            "Enter Survey index number (put n to Navigate to Next Page): "
        )

       
        if user_input.strip().lower() == 'n':
            page = page + 1           
        
            if page > pages:
                print("No more Pages left to browse the data.")
                break
            else:
                continue

        else:
            if errorFlag == False:
              idno = None
              if user_input.isdigit():

                for item in indexed_data:
                  if item["id"] == user_input:
                    idno = item["idno"]

                if idno is not None:

                    url = "https://microdata.gov.in/NADA/index.php/api/datasets/" + idno + "/fileslist"

                    headers = {
                        "Host": "microdata.gov.in",
                        "X-API-KEY": apiKey
                    }

                    response = requests.get(url, headers=headers)

                    data = response.json()

                    folder = folderPath

                    for item1 in data["files"]:

                        url = "https://microdata.gov.in/NADA/index.php/api/fileslist/download/" + idno + "/" + item1["base64"]

                        response = requests.get(url, headers=headers)

                        filename = os.path.join(folder, item1["name"])

                        with open(filename, "wb") as f:
                            f.write(response.content)
                            print(filename + ":Downloaded successfully!")
                    break
                else:
                    print('No such index Exists to download the Data. Kindly check and try again!')
                    break
        
              else:
               print("Invalid Index no.")
               break
      
            else:
             print('Error occurred while downloading the data!')
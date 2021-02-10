import requests
import os
import pprint
import json


# Load subjects' name and url
subjects = json.load(open("subjects.json"))

selectedSubjects = []

# User selects the subjects to download
for subject in subjects:
    print("Seleccionar " + subject["name"] + " (S/n)")
    selection = input()

    if selection == "S" or selection == "s":
        selectedSubjects.append(subject)

    print()
    print()

# User selects if the solutions will also be downloaded
print("¿Descargar también las soluciones?: (S/n)")
selection = input()

solutions = False

if selection == "S" or selection == "s":
    solutions = True

# Years from download the exam
years = []

for x in range(2000, 2020):
    years.append(str(x))

errors404 = []

for subject in selectedSubjects:
    # Create subject's folder if not exists
    try:
        os.mkdir(subject["name"])
    except FileExistsError:
        pass

    for year in years:
        # Download July and September exams
        url = "https://dl.selepdf.com/exams/catalunya/pau_" + subject["url"] + year[2:] + "jl.pdf"

        print("Descargando examen de " + subject["name"] + " de junio del año " + year)

        file = requests.get(url)

        if file.status_code == 404:
            errors404.append("Examen de julio del año " + year + " de " + subject["name"])

        open(subject["name"] + "/" + subject["name"] + " " + year + " Julio.pdf", "wb").write(file.content)

        url = "https://dl.selepdf.com/exams/catalunya/pau_" + subject["url"] + year[2:] + "sl.pdf"

        print("Descargando examen de " + subject["name"] + " de septiembre del año " + year)

        file = requests.get(url)

        if file.status_code == 404:
            errors404.append("Examen de septiembre del año " + year + " de " + subject["name"])

        open(subject["name"] + "/" + subject["name"] + " " + year + " Septiembre.pdf", "wb").write(file.content)

        if solutions == True:
            # Download July and September solutions
            url = "https://dl.selepdf.com/exams/catalunya/pau_" + subject["url"] + year[2:] + "jp.pdf"

            print("Descargando soluciones de " + subject["name"] + " de junio del año " + year)

            file = requests.get(url)

            if file.status_code == 404:
                errors404.append("Soluciones de julio del año " + year + " de " + subject["name"])

            open(subject["name"] + "/" + subject["name"] + " " + year + " Julio (soluciones).pdf", "wb").write(file.content)

            url = "https://dl.selepdf.com/exams/catalunya/pau_" + subject["url"] + year[2:] + "sp.pdf"

            print("Descargando soluciones de " + subject["name"] + " de septiembre del año " + year)

            file = requests.get(url)

            if file.status_code == 404:
                errors404.append("Soluciones de septiembre del año " + year + " de " + subject["name"])

            open(subject["name"] + "/" + subject["name"] + " " + year + " Septiembre (soluciones).pdf", "wb").write(file.content)

print("Archivos no encontrados:")
pprint.pprint(errors404)

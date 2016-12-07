from lib import read_file_geolocalizacion as fichero

def main():
    file_save_text = "geolocation_"
    pathIsFileSave = "Geolocation/"
    pathIsFileJSON = "json/"

    fichero.create_file(file_save_text, pathIsFileSave,  pathIsFileJSON)


if __name__ == "__main__":
    main()

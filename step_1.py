from lib import read_file as fichero

def main():
    file_save_text = "save_bag_text_week_"
    file_bag_of_words = "bag_of_words_"
    pathIsFileSave = "Save_Bag_of_Word/"
    pathIsFileBag = "Bag_of_Word/"
    pathIsFileJSON = "json/"
    fichero.create_file(file_save_text, file_bag_of_words, pathIsFileSave, pathIsFileBag, pathIsFileJSON)

if __name__ == "__main__":
    main()

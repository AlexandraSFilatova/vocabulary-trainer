# vocabulary-trainer
The project is under active development.
This code works with .csv files FROM A LOCAL DIRECTORY(thus, this code will not work in such environments as Colab without any modifications)
Files with words from the folder "Content" contain a following structure: Date add, Word, Translation, Date of the last training, Training status, Number of training.


Date add - date when a word was added

Word - word in English

Translation - word in native language (the current set is Russian)

Date of the last training - Date of the last training

Training status - L means "learned", T means "need to train"

Number of training - Number of training. Default number MUST BE 0.

To run code you must have Python 3 on your Windows PC (MacOS,Linux not tested yet). You can just run "start.cmd" or run code from "vocabulary_trainer" with a program like VS Code through the opening directory (a function os.getcwd() will get a correct folder path only in this opening way).
All other files and folders also should be downloaded to your PC (requirements.txt, Content etc.). You can add a new file with words, which has appropriate structure as described above, in the folder "Content".
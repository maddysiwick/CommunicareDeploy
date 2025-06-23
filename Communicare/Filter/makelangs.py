from .models import Language

class langs:
    def populate():
        file=open('Filter/langs.txt',encoding="utf8")
        languages=file.readlines()

        for i in languages:
            name=i.split()[1]
            print(name)
        print('madelangs')

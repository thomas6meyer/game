"""
Character identification information
"""

import nomen
import nome
import numpy as np

__ranks__ = ('Boy', 'Man at Arms', 'Sergeant', 'Bachelor', 'Master at Arms')

__key__ = 0

group = set([tuple, list, set])

class ID:
    def __init__(self, name = '', ID='', rank='Boy', title ='Commoner', nationality=''):
        """
        name: empty string = pick at random according to nationality
        ID: auto-increment, unique
        rank: used to indicate a generic skill level.
            no experience = Boy
            novice or page = Man at Arms
            initiate or squire = Sergeant
            journeyman or knight = Bachelor
            master or banneret knight = Master
        title: tuple, list, or set = group of specific values. {"Patrician", "Knight"}
        nationality: empty string = pick at random according to demographics
        """
        global __key__

        assert rank in __ranks__
        self.rank = rank

        if nationality == '': # none given, so pick randomly
            if np.random.randint(1, 100) <= 5:
                self.nationality = "Galic"
            else:
                self.nationality = "Roman"
        else:
            self.nationality = nationality

        if name == '': # none given, so pick randomly
            if self.nationality == 'Roman':
                self.name = nomen.randomPleb()
            elif self.nationality == 'Galic':
                self.name = nome.randomNome()
            else:
                print "Unknown nationality:", nationality
                assert False
        else:
            self.name = name

        isPatrician = False
        if isinstance(title, str):
            self.titles = {title}
            if title == "Patrician":
                isPatrician = True
        elif type(title) in group:
            self.titles = list(title)
            if "Patrician" in title:
                isPatrician = True

        if isPatrician:
            self.name = nomen.randomPatrician()

        if ID == '':
            self.ID = __key__
            __key__ += 1
        else:
            self.ID = ID

    def uniqueID(self):
        return self.name + '_' + str(self.ID)

if __name__ == '__main__':
    for i in range(5):
        id = ID(title=set(["Procounsel", "Patrician"]))
        print id.name, id.nationality, id.id
    for i in range(5):
        id = ID(title="Patrician")
        print id.name, id.nationality, id.id
    for i in range(5):
        id = ID(nationality="Galic")
        print id.name, id.nationality,  id.id

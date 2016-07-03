

import os
import csv
import numpy as np
import character as pc
from PC_ID import __ranks__ as allRanks

def import_IH(fn, innate_db):
    with open(fn, 'rb') as fh:
        reader = csv.reader(fh)
        # postion 7 is empty iff this character is at the School
        IH_records = filter(lambda row: row[8] == '' and row[3] in allRanks, reader)

    db = {}
    for rec in IH_records:
        thisPC = pc.Character(name=rec[1], my_id=rec[0], rank=rec[3], title=tuple(rec[4:7]), nationality=rec[7])
        db[thisPC.ID.ID] = thisPC
    for IH in IH_db:
        thisPC = IH_db[IH]
        thisPC.addInnate(innate_db[thisPC.ID.ID])

    return db

def import_innates(fn):
    with open(fn, 'rb') as fh:
        reader = csv.reader(fh)
        records = [row for row in reader]

    records = records[1:] # skip column names
    IDs = set(np.transpose(records)[0])

    innates_db = {}
    for s in IDs:
        innates_db[s] = {}

    for r in records:
        innates_db[r[0]][r[1]] = [float(v) for v in r[2:]]
    return innates_db

def import_skills(fn):
    with open(fn, 'rb') as fh:
        reader = csv.reader(fh)
        records = [row for row in reader]
    records = records[1:]  # skip column names
    skills = set(np.transpose(records)[0])
    skills_db = {}
    for s in skills:
        skills_db[s] = []
    for r in records:
        skills_db[r[0]].append([r[1], float(r[2])])
    return skills_db

def import_styles(fn):
    with open(fn, 'rb') as fh:
        reader = csv.reader(fh)
        records = [row for row in reader]
    records = records[1:]  # skip column names
    styles = set(np.transpose(records)[0]) # unique set of style names
    styles_db = {}
    for s in styles:
        styles_db[s] = {}
    for r in records:
        styles_db[r[0]][r[1]] = r[2:7]

    return styles_db

if __name__ == '__main__':
    assert os.path.exists(r'C:\Users\caHt\Documents\MyPython\tournament\db')
    os.chdir(r'C:\Users\caHt\Documents\MyPython\tournament\db')

    innate_db = import_innates('Character_Innates  .csv')
    styles_db = import_styles('STYLE_SKILL_COMPLEXITY.csv')
    skills_db = import_skills('skills_innates.csv')

    IH_db = import_IH('Iron Helm.csv', innate_db) # create Contestants

    for IH in IH_db:
        thisPC = IH_db[IH]
        thisPC.addRandomExperience()
        print thisPC.ID.rank, thisPC.ID.name
        for style in thisPC.experience:
            ep = thisPC.experience[style]
            if ep > 1:
                print '\t', style, 'ep: {0:0.2f}'.format(ep), ' == ', '{0:0.2f}'.format(thisPC.EpToLevel(ep)), ' level'


    iWantToOverwriteTheExperienceDatabase = False
    if iWantToOverwriteTheExperienceDatabase:
        with open('ep.csv', 'wb') as fh:
            writer = csv.writer(fh, delimiter=',')
            writer.writerow(["ID", 'Name', 'Style', 'EP'])

            for IH in IH_db:
                    thisPC = IH_db[IH]
                    thisPC.addRandomExperience()
                    ID = thisPC.ID.ID
                    nm = thisPC.ID.name
                    for style in thisPC.experience:
                        ep = thisPC.experience[style]
                        writer.writerow([ID, nm, style, ep])
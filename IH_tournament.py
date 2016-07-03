
import numpy as np
import os
import character as pc
import db

def match(stillGoing, names, pc_db, style, ndx, logFile=None):
    if ndx == len(stillGoing)-1:
        ## I got a "by"
        if not logFile is None:
            logFile.write('\t' + names[stillGoing[ndx]] + ' got a by\n')
        return stillGoing[ndx], None
    else:
        pc1 = pc_db[names[stillGoing[ndx]]]
        pc2 = pc_db[names[stillGoing[ndx + 1]]]
        result = pc1.fight(pc2, style, logFile)
        if result:
            print pc1.ID.name, ' beat ', pc2.ID.name
            return pc1, pc2
        else:
            print pc2.ID.name, ' beat ', pc1.ID.name
            return pc2, pc1

def boysTourneyEvent(style, pc_db, logFile = None, date=None):
    assert style in pc.__defaultStyles__
    logging = not logFile is None
    if date is None:
        date = '1 January 1014'
    num_npc = len(pc_db)
    names = pc_db.keys()

    if logging:
        logFile.write("Boy's tourney in {0} on {1}\n".format(style, date))

    stillGoing = range(num_npc)
    victors = []
    round = 1
    while len(stillGoing) > 1:
        print "Round", round, "has", len(stillGoing), "contestants:", stillGoing
        if log:
            logFile.write("Round {0} has {1} matches\n".format(round, len(stillGoing)/2))
        winners = []
        losers  = []
        for c in range(0, len(stillGoing), 2):
            winner, loser = match(stillGoing, names, pc_db, style, c, logFile)
            winners.append(winner)
            if loser == None:
                print winner, "gets a 'by'"
            else:
                losers.append(loser)
        victors.append(winners)
        print "defeated:", losers
        print "winners:", winners
        stillGoing = winners
        ##
        ## The last fighter gets a by if there's an odd number of fighters
        ## so swap him to another place so it's not always to same fighter
        if len(winners) > 2:
            swap = np.random.randint(0, len(winners)-2)
            newlast = stillGoing[swap]
            stillGoing[swap] = stillGoing[-1]
            stillGoing[-1] = newlast
        round += 1

    for round, victor in enumerate(victors):
        print round+1
        for v in victor:
            print npc[v].ID.name, npc[v].ability[style]
    if log:
        logFile.close()
    return None

def IH_Full_Tourney(num_npc, skill, pcList=[], log=False):
    logFile = None
    if log:
        os.chdir(r'C:\Users\thm02004.UCONN\Documents\Python Projects and Stuff\tournament')
        logFile = open("logFile.txt", 'w')
        logFile.write(skill+"\nNumber contestants: {0}\n".format(num_npc))
    ## put together the pairs. First round enforces that belts don't fight other belts.
    ## second round and higher, it's luck of the draw.
    ## start by creating a list of all the belts

    nameList = ('Boy', 'M@A', 'Sgt', 'Bach', 'Mstr')

    belts = pcList ## start the list of belts with the PCs
    for rank in range(1, len(num_npc)): ## skip zero b/c that's the dog meat
        for n in range(num_npc[rank]):
            belts.append( Contestant(name='', skill=skill, rank=ranks[rank]) )
    np.random.shuffle(belts)

    ## shuffle the belts between the dog meat
    npc = []
    for n in range(num_npc[0]): # position zero holds the dog meat. alternate with belts
        npc.append( Contestant(name='', skill=skill, rank=ranks[0]) )
        if n < len(belts):
            npc.append(belts[n])

    ## there might be fewer dog meat than belts so add the rest of the belts
    if num_npc[0] < len(belts):
        npc.extend(belts[n+1:])

    stillGoing = range(len(npc))
    victors = []
    rnd = 1
    while len(stillGoing) > 1:
        print "Round", rnd, "has", len(stillGoing), "contestants:", stillGoing
        if log:
            logFile.write("Round {0} has {1} matches\n".format(rnd, len(stillGoing)/2))
        winners = []
        losers  = []
        for c in range(0, len(stillGoing), 2):
            winner, loser = match(stillGoing, npc, skill, c, logFile)
            winners.append(winner)
            if loser == None:
                print winner, "gets a 'by'"
            else:
                losers.append(loser)
        victors.append(winners)
        print "defeated:", losers
        print "winners:", winners
        stillGoing = winners
        ##
        ## The last fighter gets a by if there's an odd number of fighters
        ## so swap him to another place so it's not always to same fighter
        if len(winners) > 2:
            swap = np.random.randint(0, len(winners)-2)
            newlast = stillGoing[swap]
            stillGoing[swap] = stillGoing[-1]
            stillGoing[-1] = newlast
        rnd += 1

    for rnd, victor in enumerate(victors):
        print rnd+1
        for v in victor:
            print npc[v].ID.name, npc[v].innate, npc[v].level[skill]
    if log:
        logFile.close()
    return None

if __name__ == '__main__':
    assert os.path.exists(r'C:\Users\caHt\Documents\MyPython\tournament\db')
    os.chdir(r'C:\Users\caHt\Documents\MyPython\tournament\db')

    innate_db = db.import_innates('Character_Innates.csv')
    styles_db = db.import_styles('STYLE_SKILL_COMPLEXITY.csv')
    skills_db = db.import_skills('skills_innates.csv')

    IH_db = db.import_IH('Iron Helm.csv', innate_db)  # create Contestants

    log = True
    if log:
        os.chdir(r'C:\Users\caHt\Documents\MyPython\tournament')
        logFile = open("logFile.txt", 'w')
    else:
        logFile = None

    boysTourneyEvent("Bow", pc_db=IH_db, logFile=logFile)

    # IH_Full_Tourney([511, 50, 15, 5], "Polearm", pcList=[Rutillias], log=True)


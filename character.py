
import numpy as np
import PC_ID
from PC_ID import __ranks__ as allRanks
import game_utilities as util

__BoyStyles__          = [['General','required'], ['Bow','required'], ['Polearm','required'], ['Chivalric','required'], ['Boxing','required']]
__ManAtArmsStyles__    =  __BoyStyles__ + [['Karatejutsu','optional'], ['Florentine','optional'], ['Kenjutsu','optional'], ['Riding','required']]
__SergeantStyles__     = __ManAtArmsStyles__ + [['Aikijutsu','optional'], ['Great Weapon','optional'], ['Naginata','optional'], ['Staff','optional']]
__BachelorStyles__     = __SergeantStyles__ + [['Thrown Blade','optional']]
__MasterAtArmsStyles__ = __BachelorStyles__

__defaultStyles__ = {
    'Boy': __BoyStyles__,
    'Man at Arms': __ManAtArmsStyles__,
    'Sergeant': __SergeantStyles__,
    'Bachelor': __BachelorStyles__,
    'Master at Arms': __MasterAtArmsStyles__
}
__allStyles__ = set()
for rank in allRanks:
    for style, req in __defaultStyles__[rank]:
        __allStyles__.add(style)

__defaultLevel__  = {'Boy': 0.0, 'Man at Arms': 3.0, 'Sergeant': 6.0, 'Bachelor': 8.0, 'Master at Arms': 10.0}
__defaultInnate__ = {'Boy': 0.0, 'Man at Arms': 1.0, 'Sergeant': 2.0, 'Bachelor': 3.0, 'Master at Arms': 4.0}

class Character:
    def __init__(self, name = '', my_id='', rank='Boy', title='Commoner', nationality=''):
        """
        Generate a contestant randomly
        Inputs:
            name: str = this contestant's name.
            my_id: a unique identifier. If left default, the system generates it automatically
            title:
                str = gives title
                list of str = titles
            nationality: str = name of a nationality. If left default, generated
                randomly to reflect Angleterrian demographics
        """
        self.ID = PC_ID.ID(name, my_id, rank, title, nationality)
        self.innates = {}  # dictionary key=innateNm : [current, max, derivative]
        self.experience = {}
        for style in __allStyles__:
            self.experience[style] = 1.0

    def addInnate(self, innateDict):
        """
        Inputs:
            innateDict: dictionary = value from innate_db for this character
        """
        self.innates = innateDict
        return None

    def addRandomExperience(self, myRank=None):
        # This creates the experience database at random but in a way that
        # is sensible according to <myRank>. EP is added one rank at a time
        # to honor the notion that this PC has a history
        if myRank is None:
            myRank = self.ID.rank
        notDone = True
        rNdx = 0 # current rank

        while notDone:
            rank = allRanks[rNdx]
            prOptional =  len(filter(lambda l: 'optional' in l, __defaultStyles__[rank]))
            if prOptional > 0:
                prOptional = 1.0 / float(prOptional)
            # else it's already zero

            # don't let ep be negative
            ep = self.rankToEP(rank) * util.xrand(__defaultInnate__[rank]/1.5 + 1)

            # my specialties are some from the previous rank plus some from this rank
            myStyles  = []
            for style, required in __defaultStyles__[rank]:
                if required or self.experience[style] > 1:
                    if util.rrand(0, 1.0) > prOptional :
                        myStyles.append(style)
                else: # optional
                    if util.rrand(0, 1.0) < prOptional:
                        myStyles.append(style)

            epPerSpec = ep / len(myStyles)

            while ep > 0:
                for s in myStyles:
                    contribution = util.xrand(epPerSpec)
                    self.experience[s] += contribution
                    ep -= contribution
                    if ep < 0:
                        break
            notDone = allRanks[rNdx] != myRank
            rNdx += 1
        return None

    def rankToEP(self, rank):
        return self.levelToEP(__defaultLevel__[rank])

    def levelToEP(self, lvl):
        return 10.0 * 2**lvl

    def EpToLevel(self, ep):
        return np.log2(0.1 * ep)

    def ability(self, skills_db, style):
        # how well I can perform a skill in a style
        result = 0.0
        for innate_list in skills_db[style]:
            innate, weight = innate_list
            result += self.innates[innate][0] * weight
        return result

    def prof(self, style):
        """
        Returns a float == innate + level
        """
        thisInnate, thisLevel, ep = self.ability[style]
        return thisInnate + thisLevel

    def pool(self, style):
        """
        Returns float = number of cards per turn
        """
        return 1.4 * np.exp(self.prof(style) / 1.5)

    def fight(self, other, style, logFile=None):
        myPool = myProf = self.pool(style)
        otherPool = otherProf = other.pool(style)

        res = 0.0
        while abs(res) < 3.0:
            nCards = int(myPool)
            pull = util.drawCards(nCards)
            res += pull
            myPool = myPool - nCards + myProf # number of cards available next round
            other.ability[style][2] += pull # ep is sum of cards drawn against me

            nCards = int(otherPool)
            pull = util.drawCards(nCards)
            res -= pull
            otherPool = otherPool - nCards + otherProf
            self.ability[style][2] += pull

        i_won = res > 0
        if logFile is not None:
            if i_won:
                winner_name = self.ID.name
                winner_prof = myProf
                loser_name = other.ID.name
                loser_prof = otherProf
            else:
                winner_name = other.ID.name
                winner_prof = otherProf
                loser_name = self.ID.name
                loser_prof = myProf

            logFile.write('\t' + winner_name + ' ({0:0.2f})'.format(winner_prof) + ' beat ' + loser_name + ' ({0:0.2f})\n'.format(loser_prof) )
        return i_won

if __name__ == '__main__':
    f1 = Character()
    f2 = Character()

    skill = 'test'
    f1.addSkill(skill)
    f2.addSkill(skill)
    print f1.ability[skill]
    print f2.ability[skill]

    print f1.skills()
    print f1.prof(skill)
    print f1.pool(skill)

    print f1.fight(f2, skill)
    print f1.ability[skill]
    print f2.ability[skill]
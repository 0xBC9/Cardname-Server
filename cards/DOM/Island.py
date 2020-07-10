from enumeratedTypes import * 
from combatFunctions import * 
from gameElements import * 
from gameActions import * 
from abilities import * 

class Island(Card):
    def __init__(self, game, player):
        super(Island, self).__init__(game, player)

        c1 = (False, ((tap, self)))

        e1 = Effect(self)
        e1.effect = [[addMana, self.controller, Color.BLUE, 1]]
        e1.rulesText = "T: Add U."

        a1 = ActivatedAbility(game, c1, e1, {Zone.FIELD}, True)

        self.characteristics[Layer.BASE] = ("Island", 0, 0, [a1], {Supertype.BASIC, Type.LAND, Subtype.ISLAND}, {Color.COLORLESS})

        self.updateCharacteristics()
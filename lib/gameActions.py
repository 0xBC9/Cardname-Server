from time import sleep
from enumeratedTypes import *


def play(game, card):
    pass


def playLand(game, card, player):
    evaluate(game, moveToZone, card, Zone.FIELD, None)


def cast(game, card):
    evaluate(game, moveToZone, card, Zone.STACK, 0)


def activateAbility(game, effect):
    if effect.sourceAbility.isManaAbility:
        game.resolve(effect)
    else:
        game.push(effect)


def loseLife(game, source, player, amountToLose):
    """Set the life total for selected player to (current life - the amount to lose)

    Args:
        game (Game): Game Object
        source (Card): Source of the life loss
        player (Player): Player that is loosing life
        amountToLose (Int): The amount of life to lose

    Returns:
        None
    """
    if amountToLose == 0:
        return
    player.lifeTotal -= amountToLose

    game.notifyAll("Life Total Update", {
        "gameID": game.gameID,
        "playerID": player.playerID,
        "life": player.lifeTotal
    })


def gainLife(game, source, player, amountToGain):
    """Set the life total for selected player to (current life + the amount to gain)

    Args:
        game (Game): Game Object
        source (Card): Source of the life gain
        player (Player): Player that is gaining life
        amountToGain (Int): The amount of life to gain

    Returns:
        None
    """
    if amountToGain == 0:
        return

    player.lifeTotal += amountToGain

    game.notifyAll("Life Total Update", {
        "gameID": game.gameID,
        "playerID": player.playerID,
        "life": player.lifeTotal
    })


def setLife(game, source, player, newTotal):
    """Sets the life total of the selected player to the specified amount

    Args:
        game (Game): Game Object
        source (Object): Source that is setting the player's life total
        player (Player): Player is having their life total set
        newTotal (Int): New life total

    Returns:
        None
    """
    if player.getLife() == newTotal:
        pass
    elif (player.getLife() > newTotal):
        evaluate(game, loseLife, player, (player.getLife() - newTotal))
    else:
        evaluate(game, gainLife, player, (newTotal - player.getLife()))


def drawCard(game, player):
    """Selected player draws a card

    Args:
        game (Game): Game Object
        player (Player): Player that needs more gas

    Returns:
        None
    """
    card = player.getTopOfDeck()
    evaluate(game, moveToZone, card, Zone.HAND, None)


def drawCards(game, player, numToDraw):
    """Draw multiple cards

    Args:
        game (Game): Game Object
        player (Player): Player that is drawing the cards
        numToDraw (Int): Number of cards to draw

    Returns:
        None
    """
    for _ in range(numToDraw):
        evaluate(game, drawCard, player)


def mill(game, player):
    """Selected player mills one card

    Args:
        game (Game): Game Object
        player (Player): Player that is milling cards

    Returns:
        None
    """
    card = player.getTopOfDeck()
    evaluate(game, moveToZone, card, Zone.GRAVE, None)


def millCards(game, player, numToMill):
    """Mill multiple cards

    Args:
        game (Game): Game Object
        player (Player): Player that is milling cards
        numToDraw (Int): Number of cards to mill

    Returns:
        None
    """
    for _ in range(numToMill):
        evaluate(game, mill, player)


def untap(game, card):
    """Untap card

    Args:
        game (Game): Game Object
        card (Card): Card to untap

    Returns:
        None
    """
    card.tapped = False
    game.notifyAll("Untap", card.instanceID)


def untapCards(game, cardsToUntap):
    """Untap multiple cards

    Args:
        game (Game): Game Object
        cardsToUntap (List(Card)): Cards to untap

    Returns:
        None
    """
    for card in cardsToUntap:
        evaluate(game, untap, card)


def untapAll(game, activePlayer):
    """Untap all cards controlled by the active player during the Untap step

    Args:
        game (Game): Game Object
        activePlayer (Player): Player whose cards need to be untapped

    Returns:
        None
    """
    for card in activePlayer.getField():
        evaluate(game, untap, card)


def tap(game, card):
    """Tap card

    Args:
        game (Game): Game Object
        card (Card): Card to tap

    Returns:
        None
    """
    card.tapped = True

    game.notifyAll("Tap", {
        "gameID": game.gameID,
        "instanceID": card.instanceID
    })


def tapCards(game, cardsToTap):
    """Tap multiple cards

    Args:
        game (Game): Game Object
        cardsToTap (List(Card)): Cards to tap

    Returns:
        None
    """
    for card in cardsToTap:
        evaluate(game, tap, card)


def sacrifice(game, source, target):
    """Sacrifices the target card.

    Args:
        game (Game): Game Object
        source (Object): Spell or Ability source
        target (Card): Card to sacrifice

    Returns:
        None
    """
    evaluate(game, dies, game, target)
    evaluate(game, moveToZone, target, Zone.GRAVE, None)


def sacrificeCards(game, cardsToSacrifice):
    pass


def destroy(game, source, target):
    """Destroy target card.

    Args:
        game (Game): Game Object
        source (Object): Spell or Ability source
        target (Card): Card to destroy

    Returns:
        None
    """
    evaluate(game, moveToZone, target, Zone.GRAVE, None)


def destroyCards(game, source, cardsToBeDestroyed):
    """Destroy multiple cards.

    Args:
        game (Game): Game Object
        source (Object): Spell or Ability source
        target (Card): Cards to destroy

    Returns:
        None
    """
    legalCards = set()
    for card in cardsToBeDestroyed:
        if isLegal(game, destroy, source, card) and not isReplaced(game, destroy, source, card):
            legalCards.add(card)
    for card in legalCards:
        evaluate(game, dies, card)
    for card in legalCards:
        evaluate(game, destroy, game, source, card)


def etb(game, card):
    pass


def dies(game, target):
    """Used to trigger "When ~ dies" abilities.

    Args:
        game (Game): Game Object.
        target (Card): The creature thats bouta fuckin die.

    Returns:
        None
    """
    pass


def phaseIn(game, activePlayer):
    """Phases in all cards the activePlayer controls.

    Args:
        game (Game): Game Object
        activePlayer(Player): The active player

    Returns:
        None
    """
    pass


def phaseOut(game, card):
    """Phases out a card.

    Args:
        game (Game): Game Object
        card(Card): Card to be phased out

    Returns:
        None
    """
    pass


def emptyManaPools(game):
    """Remove all mana from all player's mana pool. Used during step changes

    Args:
        game (Game): Game Object

    Returns:
        None
    """
    colors = {Color.WHITE, Color.BLUE, Color.BLACK,
              Color.RED, Color.GREEN, Color.COLORLESS}
    for player in game.players:
        for color in colors:
            removeAllMana(game, player, color)


def removeAllMana(game, player, color):
    """Remove all mana of a certain color in player's mana pool.

    Args:
        game (Game): Game Object
        player(Player): Player to remove mana from
        color(enumeratedTypes.Color): Color of mana to remove

    Returns:
        None
    """
    player.manaPool[color] = 0


def changeManaColor(game, player, currentColor, newColor):
    """Change mana of one color to another in the player's mana pool.

    Args:
        game (Game): Game Object
        player(Player): Player whose mana is changed
        currentcolor(enumeratedTypes.Color): Color of mana to change from
        currentcolor(enumeratedTypes.Color): Color of mana to change to

    Returns:
        None
    """
    amount = player.manaPool[currentColor]
    player.manaPool[currentColor] = 0
    player.manaPool[newColor] += amount


def removeMana(game, player, color, amount):
    """Remove mana from player's mana pool.

    Args:
        game (Game): Game Object
        player(Player): Player to remove mana from
        color(enumeratedTypes.Color): Color of mana
        amount (Int): Amount of mana to remove

    Returns:
        None
    """

    player.manaPool[color] -= amount

    total = 0
    for color in player.manaPool:
        total += player.manaPool[color]

    game.notify("Mana Update", {
        "gameID": game.gameID,
        "color": str(color),
        "amount": player.manaPool[color]
    }, player)


def addMana(game, player, color, amount):
    """Add mana to player's mana pool.

    Args:
        game (Game): Game Object
        player(Player): Player to add mana
        color(enumeratedTypes.Color): Color of mana
        amount (Int): Amount of mana to add

    Returns:
        None
    """
    player.manaPool[color] += amount

    game.notify("Mana Update", {
        "gameID": game.gameID,
        "color": str(color),
        "amount": player.manaPool[color]
    }, player)


def attach(game, source, target):
    """Attach card to another card.

    Args:
        game (Game): Game Object
        source(Card): The attachment
        target(Card): The target for the attachment

    Returns:
        None
    """
    pass


def unattach(game, attachment, target):
    """Unattach card from another card.

    Args:
        game (Game): Game Object
        source(Card): The attachment
        target(Card): The attached card

    Returns:
        None
    """
    pass


def transform(game, card):
    pass


def discardCards(game, cardsToDiscard):
    pass


def discardCard(game, card):
    pass


def discardHand(game, player):
    pass


def discardToHandSize(game, player):
    pass


def moveToZone(game, card, newZoneName, indexToInsert):
    oldZoneName = str(card.currentZone)
    if card.currentZone == Zone.STACK or card.currentZone == Zone.FIELD:
        oldZone = game.zones[card.currentZone]
    else:
        oldZone = game.zones[card.controller][card.currentZone]

    if newZoneName == Zone.STACK or newZoneName == Zone.FIELD:
        newZone = game.zones[newZoneName]
    elif newZoneName == Zone.DECK:
        newZone = game.zones[card.controller][Zone.DECK]
    else:
        newZone = game.zones[card.controller][newZoneName]

    card.reset()
    oldZone.remove(card)

    if newZoneName == Zone.DECK or newZoneName == Zone.STACK:
        newZone.insert(indexToInsert, card)
    else:
        newZone.add(card)

    card.currentZone = newZoneName
    game.applyModifiers(card)

    game.notifyAll("Remove Object", {
        "gameID": game.gameID,
        "controller": card.controller.playerID,
        "instanceID": card.instanceID,
        "zone": oldZoneName})

    abilities = [[ability.abilityID, ability.rulesText]
                 for ability in card.abilities if (newZoneName in ability.allowedZones)]
    types = [str(typ) for typ in card.cardTypes]

    msg2 = {
        "gameID": game.gameID,
        "instanceID": card.instanceID,
        "name": card.name,
        "oracle": card.oracle,
        "tapped": card.tapped,
        "memID": card.memID,
        "power": card.power,
        "toughness": card.toughness,
        "controller": card.controller.playerID,
        "abilities": abilities,
        "types": types,
        "zone": str(newZoneName)
    }

    if oldZoneName == "Zone.HAND" or oldZoneName == "Zone.EXILE" or oldZoneName == "Zone.GRAVE" or oldZoneName == "Zone.DECK":
        game.notifyAll("Zone Size Update", {
            "gameID": game.gameID,
            "playerID": card.controller.playerID,
            "zoneType": str(oldZoneName),
            "num": len(oldZone)
        })

    if newZoneName == Zone.HAND or newZoneName == Zone.EXILE or newZoneName == Zone.GRAVE or newZoneName == Zone.DECK:
        game.notifyAll("Zone Size Update", {
            "gameID": game.gameID,
            "playerID": card.controller.playerID,
            "zoneType": str(newZoneName),
            "num": len(newZone)
        })

    if newZoneName == Zone.HAND or newZoneName == Zone.DECK:
        game.notify("New Object", msg2, card.controller)
    else:
        game.notifyAll("New Object", msg2)


def gainControl(game, card, newController):
    pass


def endPhase(game, activePlayer, phase):
    """End the current phase

    Args:
        game (Game): Game Object
        activePlayer(Player): The Active Player
        phase(enumeratedTypes.TURN): The current phase or step to end

    Returns:
        None
    """
    emptyManaPools(game)
    for player in game.players:
        player.passed = False


def beginPhase(game, activePlayer, phase):
    """Begin a new phase

    Args:
        game (Game): Game Object
        activePlayer(Player): The Active Player
        phase(enumeratedTypes.TURN): The phase or step to begin

    Returns:
        None
    """
    game.currPhase = phase
    game.activePlayer = activePlayer

    msg = {
        "activePlayer": activePlayer.playerID,
        "phase": str(phase)
    }

    game.notifyAll("Start Phase", msg)


def lose(game, player, cause):
    """Chosen player will lose the game and will preform any associated cleanup

    Args:
        game (Game): Game Object
        player(Player): The player that lost
        cause(enumeratedTypes.COD): Cause of Death 

    Returns:
        None
    """
    pass


def win(game, player):
    """Chosen player will win the game and will preform any associated cleanup

    Args:
        game (Game): Game Object
        player(Player): The player that won

    Returns:
        None
    """
    pass


def choose(game, options, player, inquiryType, numOfChoices):
    pass


def order(options, player):
    if(len(options) == 1):
        return options[0]
    pass


def isLegal(*args):
    """Check if a given action and arguments are legal

    Normal Arguments:
        game (Game): Game Object
        action(Function): The game action being checked
        otherArgs(Any): The other arguments for the game action

    Returns:
        None
    """
    game = args[0]
    try:
        rules = game.LE["Rules"][args[1].__name__]
    except:
        rules = []
    try:
        allowances = game.LE["Allowances"][args[1].__name__]
    except:
        allowances = []

    someSet = set()
    for rule in rules:
        x = rule.isLegal(args[2], args[2:])
        if x != GameRuleAns.ALLOWED:
            someSet.add((x, None))

    if len(someSet) != 0:
        for pair in someSet:
            for allowance in allowances:
                ans = allowance.isAllowed(args[0], args[1], args[2:], pair[0])
                if ans == GameRuleAns.ALLOWED:
                    pair[1] = ans
                    break
        for pair in someSet:
            if pair[1] != GameRuleAns.ALLOWED:
                return False

    return True


def isReplaced(*args):
    """Check if a given action and arguments will be replaced

    Normal Arguments:
        game (Game): Game Object
        action(Function): The game action being checked
        otherArgs(Any): The other arguments for the game action

    Returns:
        None
    """
    game = args[0]
    rules = game.LE["Rules"][args[1].__name__]
    allowances = game.LE["Allowances"][args[1].__name__]
    replacements = game.LE["Replacements"][args[1].__name__]

    someSet = set()
    for rule in rules:
        x = rule.isLegal(args[2], args[2:])
        if x != GameRuleAns.ALLOWED:
            someSet.add((x, None))

    if len(someSet) != 0:
        for pair in someSet:
            for allowance in allowances:
                ans = allowance.isAllowed(args[0], args[1], args[2:], pair[0])
                if ans == GameRuleAns.ALLOWED:
                    pair[1] = ans
                    break
        for pair in someSet:
            if pair[1] != GameRuleAns.ALLOWED:
                return False

    for replacement in replacements:
        if replacement.isActive() and replacement.getSource() not in game.globalDict["ReplacedBy"] and replacement.getFunc()(args[1], args[2:]):
            return True

    return False


def evaluate(*args):
    """Important method for the engine. Detailed in LexMagico.md

    Normal Arguments:
        game (Game): Game Object
        action(Function): The game action being checked
        otherArgs(Any): The other arguments for the game action

    Returns:
        None
    """
    game = args[0]
    try:
        rules = game.LE["Rules"][args[1].__name__]
    except:
        rules = []
    try:
        allowances = game.LE["Allowances"][args[1].__name__]
    except:
        allowances = []
    try:
        replacements = game.LE["Replacements"][args[1].__name__]
    except:
        replacements = []
    try:
        otherTriggers = game.LE["Triggers"][args[1].__name__]
    except:
        otherTriggers = []

    someSet = set()
    for rule in rules:
        x = rule.isLegal(args[2], args[2:])
        if x != GameRuleAns.ALLOWED:
            someSet.add((x, None))

    if len(someSet) != 0:
        for pair in someSet:
            for allowance in allowances:
                ans = allowance.isAllowed(args[0], args[1], args[2:], pair[0])
                if ans == GameRuleAns.ALLOWED:
                    pair[1] = ans
                    break
        for pair in someSet:
            if pair[1] != GameRuleAns.ALLOWED:
                return GameRuleAns.DENIED

    someOtherSet = set()
    for replacement in replacements:
        if replacement.isActive() and replacement.getSource() not in game.replacedBy and replacement.getFunc()(args[1], args[2:]):
            someOtherSet.add(replacement)
    if len(someOtherSet) != 0:
        pass
        # chosen = choose(game, someOtherSet, game.activePlayer,
        #                 InquiryType.REPLACEMENT, 1)
        # game.replacedBy.append(chosen.getSource)
        # chosen.resolveEffect()

    if len(args) == 2:
        args[1](args[0])
    elif len(args) == 3:
        args[1](args[0], args[2])
    elif len(args) == 4:
        args[1](args[0], args[2], args[3])
    elif len(args) == 5:
        args[1](args[0], args[2], args[3], args[4])
    elif len(args) == 6:
        args[1](args[0], args[2], args[3], args[4], args[5])
    elif len(args) == 7:
        args[1](args[0], args[2], args[3], args[4], args[5], args[6])
    elif len(args) == 8:
        args[1](args[0], args[2], args[3], args[4], args[5], args[6], args[7])

    for tracker in game.trackers:
        tracker.run()

    someThirdSet = set()
    for trigger in otherTriggers:
        if trigger.isActive() and trigger.getFunc()(args[1], args[1:]):
            someThirdSet.add(trigger)
    for trigger in someThirdSet:
        player = trigger.getSource().getController()
        player.awaitingTriggers.append(trigger.getEffect())

    return None

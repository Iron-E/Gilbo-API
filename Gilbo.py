from sys import path
path.append('./Gilbo-API/')
path.append('./Gilbo-API/deps/')
import Gilbo as G
from colorama import Fore, Back, Style

#
# Objects #
#

# Ammo #
stamina = G.item('Stamina', "Your body's natural energy.", 0)
spray_can = G.item('Pepper Spray', 'A can of pepper spray.', 10)

# Buffs/Heals #
# Buffs
black_suit_buff = G.stat_item('Mysterious Orange Liquid', 'A mysterious orange liquid that was used by the Man in the Black Suit.', 1000, 10, 0, 25, 5, -10)
msg = G.stat_item('MSG', 'Super Salt. Seriously bad for you, but a seriously wild ride.', 5, 2, 0, 10, 0, 10)
tso_chicken = G.stat_item("General Tso's Chicken", "Nothing incites a fighting spirit like the effigy of General Tso's Chicken. Why did the General only have one?", 20, 3, 30)

# Heals
noodles = G.heal_item('Noodles', "A cup of Alton Brown's world-famous noodles.", 10, 10)
msg_noodles = G.heal_item('MSG Noodles', "Alton Brown's noodles, now with 150% more MSG. It seems to good to be true, so you'll probably pay for it later...", 2, 20)
lo_mein = G.heal_item('Lo Mein', "Alton Brown's signature Lo Mein. You'd slurp the noodles if he weren't watchinG.", 7, 15)
sushi_roll = G.heal_item('California Roll', 'California Roll hand-crafted by Alton Brown. You can smell the seacost.', 5, 5)

stim_pack = G.heal_item('Stim Pack', 'A stim pack issued by FBI agents that frequently see combat.', 500, 10)

# Debuffs
surprise_debuff = G.stat_item("Caught By Surprise", "Someone was caught by surprise and suffered the consequence.", 0, 1, -5, -5, -5, -7)
defense_down = G.stat_item('Defense Down', "The bearer's defense has been lowered.", 0, 3, -5, 0, -10)
enrage_debuff = G.stat_item('Enraged', 'The bearer has been taunted, leaving them stronger, but also reckless.', 0, 2, 0, 10, -15, 5)
irritated_eyes = G.stat_item('Irritated Eyes', "The bearer's eyes have been irritated by some chemical, causing them to miss attacks and present openings in their defense.", 0, 2, 0, 0, -6, -10)

# Attacks #
# For katana
quick_draw = G.ammo_attack('Quick Draw', 'Draw your sword from its sheath at lightning speed.', 5, stamina, 3, 100, surprise_debuff)
cross_slash = G.ammo_attack('Cross Slash', 'Quickly slash twice at your oppnent, weakening their defense.', 6, stamina, 1, 100, defense_down)
parry = G.attack('Parry', 'Parry an attack from your opponent, enraging them while leaving them defenseless.', 2, 100, enrage_debuff)
sword_dance = G.attack('Sword Dance', 'Weave around the enemy slicing so thinly it would appear to be a dance.', 8)

# For black belt
charge = G.attack('Charge', 'Charge towards the enemy with great force', 10)
flying_kick = G.attack('Flying Scissor Kick', 'Leap at the enemy with a Scissor Kick.', 20, 65)
high_kick = G.attack('High Kick', 'Lean back and kick high with your good leG.', 15, 85)
low_sweep = G.ammo_attack('Low Sweep', 'Sweep your leg and temporarily disarm the apponent.', 8, stamina, 1, 100, surprise_debuff)

# For pre-buff blacksuit
shin_kick = G.attack('Shin Kick', "Kick your opponent's shin.", 8)
pepper_spray = G.ammo_attack('Use Pepper Spray', "Shoot pepper spray into the eyes of your opponent.", 2, spray_can, 1, 90, irritated_eyes)
throw_chair = G.attack('Throw Chair', 'Grab a nearby chair and throw it at the opponent.', 25, 60)
punch = G.attack('Punch', 'Deliver a flurry of punches to your opponent.', 13, 90)

# For buffed blacksuit
bash = G.attack('Skull Bash', 'Bash your head into the oppnent.', 11)
throw_table = G.attack('Throw Table', 'Throw a table at your opponent.', 30, 45)

# Weapons #
# User Weapons
chop_sticks = G.weapon('Chop Sticks', 'A pair of chopsticks you had used to eat your meal. If you believe in yourself, who knows what might happen?', 1, [sword_dance, quick_draw, cross_slash, parry, charge, flying_kick, low_sweep, high_kick, punch, shin_kick, pepper_spray, throw_chair, bash, throw_table], 5, 5, 5, 5, 1)
katana = G.weapon('Katana', 'A weapon proven deadly when used in the right hands. Catch your enemies by surprise, or just impress them with your collection.', 100, [sword_dance, quick_draw, cross_slash, parry], 5, 8, 0, 12)
black_belt = G.weapon('Black Belt', 'A weapon worn around the waist. Grants user impeccable hand-to-hand combat ability. Or, supposedly, it could be used to towel-snap your opponent.', 5, [charge, flying_kick, low_sweep, high_kick], 10, 10, 5)

# Boss Weapons
black_suit_prebuff = G.weapon("Agent's Arsenal", 'An array of items and techniques known and used by the FBI.', 1000, [punch, shin_kick, pepper_spray, throw_chair])
black_suit_buffed = G.weapon('Herculean Brawn', "After injection of a mysterious liquid, the FBI agent has turned into a terrifying bruiser.", 5000, [bash, punch, shin_kick, throw_table])

# Entity-related #

# Collections
user_collection = G.player_collection(50, [tso_chicken, lo_mein, msg_noodles, katana, chop_sticks, black_belt], [])
user_collection.add_item(noodles, 2)
user_collection.add_item(sushi_roll, 3)
user_collection.add_item(stamina, 2)

black_suit_collection = G.battler_collection(1000, [black_suit_prebuff, black_suit_buffed, spray_can, spray_can, spray_can, spray_can], [black_suit_prebuff])
black_suit_collection.add_item(stim_pack, 6)
# Stat Lists
user_stats = G.battler_stats(100, 10, 10, 10)
black_suit_stats = G.battler_stats(150, 12, 15, 10)

# Battlers
user = G.player('Ed', None, None, None, user_collection, user_stats)
black_suit = G.battler('The Man', None, None, None, black_suit_collection, black_suit_stats)

# NPCs
alton = G.NPC('Alton Brown', None, None, None)
alton.add_dialogue('thanks-for-tipping', f'"Thanks, {user.name}. It means a lot that you\'d support my small business.", says {alton.name}.')
alton.add_dialogue('law-run-in', f'"I\'ve had run-ins with the law before, {user.name}! I\'m not looking to do it again!"')

suit_narrator = G.NPC('The man in a black suit', None, None, None)
suit_narrator.add_dialogue('initial-encounter', '"Where do you think you\'re going?"')
suit_narrator.add_dialogue('tax-confront', "\"Thought you'd just be able to get away with evading taxes?\"")
suit_narrator.add_dialogue('avoid-this', ["\"Well, you might've been able to avoid taxes...", "but you won't be able to avoid this!\""])
suit_narrator.add_dialogue('use-buff', '"I was hoping it would\'t come to this..."')
suit_narrator.add_dialogue('the-plunge',  ["\n\n\"Command,\" he begins as a sly smile crosses his face,",  "\"this guy isn't cooperating.\"", "\"I'm going to use...", f'{Fore.RED}the system{Style.RESET_ALL}."\n\n'])
suit_narrator.add_dialogue('spare-the-cash', f'"{Fore.LIGHTRED_EX}You just couldn\'t spare the 9%, could you?{Style.RESET_ALL}"')

narrator = G.NPC('Narrator', None, None, None)
narrator.add_dialogue('get-user-name', 'What is your name?')
narrator.add_dialogue('describe-setting', ["You find yourself at \"Alton Brown's Noodle Shack\".", 'You come here once a month to stock up on noodle-related supplies, and --- as he so lovingly puts it --- "oriental wares".', '\n\nAlton has been so good to you for so long, you feel like you should tip him.', 'Will you tip?'])
narrator.add_dialogue('user-tipped', 'You decided to tip Alton. After all, he deserves it.')
narrator.add_dialogue('user-no-tip', ["You decided not to tip Alton. It would set a precedent, and you'd always have to tip from now on.", '\n\nHe lets out a slight look of disappointment, if even for a second.'])
narrator.add_dialogue('try-to-leave', ["You take your things and turn to leave. You take five steps before the door busts open with a gust of wind so powerful that it blows the curtains back at the other side of the restaurant.", 'A glare prevents you from seeing clearly, but you make out the shape of a man standing in the doorway.'])
narrator.add_dialogue('enemy-spotted', ['The figure steps forward, and the sun retreats behind it like water, revealing a man in a black suit.', 'You stare at each other as a deep silence falls upon the earth, like something seen in a classic Western movie.', 'You turn around, but Alton is nowhere to be seen.', 'Calling out, he responds from under the counter.'])
narrator.add_dialogue('back-to-reality', ['Your head snaps back from where Alton lay beneath the counter.', f'{suit_narrator.name} now faces you fists raised, ready to pounce.'])
narrator.add_dialogue('enemy-attacks', [f'{suit_narrator.name} runs forward towards you and takes a swing.', 'You drop to the ground in an effort to dodge.', 'He tries to kick you, but you roll away.', 'Adrenaline begins to pump through your veins as you desparately attempt being hit. You have nothing to defend yourself with.', '\n\nOn the ground, you notice three weapons that Alton stores under tables.', 'The oppurtunity to grab one arises.', 'Which do you choose?'])
narrator.add_dialogue('use-item', [f'A breafcase comes crashing through the roof. {black_suit.name} reaches up to catch it with perfect timing, as if it had happened a million times before.', "Out of the breafcase, he takes a needle containing a strange, orange liquid.", f"{black_suit.name} raises his hand to his ear and speaks into a small microphone."])
narrator.add_dialogue('the-plunge', ['You get a bad feeling as he flicks off his earpiece.', "You hear the buzzing of wild chatter from the man's earpiece, which now hangs from his shirt.", 'As he drains the liquid you stand transfixed as he swells into a grotesquely muscular creature.', "His suit tears with his newly increased size.", "\n\nThe very moment when you become grounded enough to run, he glares at you.", 'He grins.'])


#
# Functions #
#
def let_read():
    input('(Press enter to continue.)')
    G.clr_console()


class dialogue_index(G.IntEnum):
    black_suit = 0
    alton = 1


def advance_dialogue():
    monologue[dialogue_index.black_suit] += 1
    let_read()


def cli_color(fallback, win='color 0F'):
    import os
    if os.name == 'nt':
        # change windows terminal color
        os.system(win)
    else:
        # change linux terminal color
        os.system(fallback)


def build_temp_effects(manager):
    temp_effect_list = []
    for effect in manager.effect_dict['reverse_effect_player']:
        temp_effect_list.append(effect[2])
    for effect in manager.effect_dict['reverse_effect_enemy']:
        temp_effect_list.append(effect[2])

    return temp_effect_list


def bat_check():
    if (bat_man.percent_health(black_suit) < 90) and (monologue[dialogue_index.black_suit] == 0):
        G.clr_console()
        G.write(["You call out to your opponent.", '"C\'mon man, do we really have to do this?"'])
        G.write(['"When did you get the impression that I was doing this because I', f'{Fore.RED}HAD{Fore.RESET}', 'to?"', 'he chirps back.'])
        G.write(['"You do get paid to do this, right?', 'This has to be a paid job."'])
        G.write([f'{black_suit.name}\'s face suddenly displays an intense tranquility.', '\n\n"This...', f'this is {Fore.BLACK}{Back.WHITE}divine{Style.RESET_ALL} penance!', 'Punishment for the worst of criminals!', 'I would never ask for money.'])
        advance_dialogue()
    elif (bat_man.percent_health(black_suit) < 70) and (monologue[dialogue_index.black_suit]):
        G.clr_console()
        G.write(['Despite your progress in battle, you attempt to plead with the man.', '\n\n"How is this a solution?"'])
        G.write(['"What is the alternative?', 'Getting away with tax avoidance?"'])
        G.write("You didn't even give me a chance to pay for it!")
        G.write('"Yeah, I\'ve heard that one before. \'I was just about to pay my taxes, IRS!\' It\'s a steaming load."')
        advance_dialogue()
    elif (bat_man.percent_health(black_suit) < 30) and (monologue[dialogue_index.black_suit] == 3):
        G.clr_console()
        G.write('"It\'s about the terrorists."')
        G.write(["You're taken aback by that statement.", '\n\n"What?"'])
        G.write('"We use that money to fend off the terrorists," he continues.')
        G.write('"..and?"')
        G.write(['"Choosing to avoid helping the fight against the terrorists is', '\b...', f'{Fore.RED}terrorism itself{Fore.RESET}!"'])
        advance_dialogue()

    if bat_man.percent_health(black_suit) <= 50:
        if black_suit.entity_dict['used_buff'] is False:
            G.clr_console()
            suit_narrator.say('use-item')
            narrator.say('use-item')
            suit_narrator.say('the-plunge')
            narrator.say('the-plunge')
            suit_narrator.say('spare-the-cash')
            let_read()
            black_suit.use_item(black_suit_buff)
            black_suit.equip(black_suit_buffed)
            black_suit.entity_dict['used_buff'] = True
        elif (black_suit.entity_dict['used_buff'] is True) and (monologue[dialogue_index.black_suit] == 2):
            G.clr_console()
            G.write(["Let's say that I DID forget to pay tax.", 'What would forgetting one time matter?'])
            G.write(["It isn't just you, you see?", "It's everyone.", 'If everyone forgot to pay their taxes one time all together...', "it's unthinkable."])
            G.write(['"The Government can handle about $0.05 less one time from everyone in their lives,', 'can\'t they?"'])
            G.write(['"You\'re terminally shortsighted."'])
            advance_dialogue()

    if (tso_chicken.name in build_temp_effects(bat_man)) and (bat_man.battle_dict['turn'] == G.Turn.Attack):
        G.write([f"The Ghost of {tso_chicken.name} rises from the deep.", f"\n\n{tso_chicken.name} helps you by doing 15 damage to the enemy."])
        bat_man.hit_animate()
        black_suit.stats.health -= 15

    if (bat_man.percent_health(user) <= 50) and (user_tipped is True) and (bat_man.battle_dict['turn'] == G.Turn.Attack):
        if monologue[dialogue_index.alton] is None:
            bat_man.battle_dict['alton_help'] = True
            G.write(['Alton brown leaps out from behind the counter', '"\n\nI will defend this tipping customer!"', 'he says as a chair grazes the top of his head.', f'"...from {Fore.RED}behind{Fore.RESET} the counter!"'])
            monologue[dialogue_index.alton] = 0

        G.write('Alton brown tosses mugs at the Man in the Black Suit, dealing 15 damage.')
        let_read()
        bat_man.hit_animate()
        black_suit.stats.health -= 15


def win(manager):
    try:
        if (manager.battle_dict['alton_help'] is True) and ("General Tso's Chicken" in build_temp_effects(manager)):
            if black_suit_buff.name in build_temp_effects(manager):
                G.write([f"You glance over at {alton.name}. He's sweating-- barely holding on.", "You know how he feels. It takes everything you have to not give up and accept your fate.", "\n\nBut--", "suddenly, a phantomish form bursts out from behind the monster."])
                let_read()

                G.write([f'{alton.name} gives you a strange look.', f"Apparently, he hadn't seen the Ghost of {tso_chicken.name} emerge from the abyss.", f'\n\n"What in the {Fore.RED}world{Fore.RESET} is that?" you hear {alton.name} spout in disbelief as the chicken kites the enormous beast.', '\n\n"Just wait," you mutter back.'])
                let_read()

                G.write([f'The two of you watch as the Ghost of {tso_chicken.name} leaps high into the air, and delivers a kick with the strength of 1000 ancient Chinese imperial commissioners.'])
                let_read()

                G.write(['"NOW!" you yell.', "Without a nanosecond of hesitation, Alton springs into action.", "Years of work as a chef paying off in the passing of an instant.", 'Alton reaches up his sleave. What does he have there?', '\n\nThe monster looks afraid.'])
                let_read()
            else:
                G.write([f"You glance over at {alton.name}. He's sweating-- barely holding on.", "You know how he feels. It takes everything you have to not give up and accept your fate.", "\n\nBut--", "suddenly, a phantomish form bursts out from behind the monster."])
                let_read()

                G.write([f'{alton.name} gives you a strange look.', f"Apparently, he hadn't seen the Ghost of {tso_chicken.name} emerge from the abyss.", f'\n\n"What in the {Fore.RED}world{Fore.RESET} is that?" you hear {alton.name} spout in disbelief as the chicken kites the enormous beast.', '\n\n"Just wait," you mutter back.'])
                let_read()

                G.write([f'The two of you watch as the Ghost of {tso_chicken.name} sucker punches the man in the black suit, leaving him wide open for a follow-up attack.'])
                let_read()

                G.write(['"NOW!" you yell.', "Without a nanosecond of hesitation, you both spring into action.", 'The two of you wind up a punch to put an end to this impedance.', '\n\nThe Man in the Black Suit looks afraid.'])
                let_read()

        elif manager.battle_dict['alton_help'] is True:
            if black_suit_buff.name in build_temp_effects(manager):
                G.write([f"You glance over at {alton.name}. He's sweating-- barely holding on.", "You know how he feels. It takes everything you have to not give up and accept your fate.", "\n\nBut--", "you're in this together. You won't let him down, only because he won't let YOU down."])
                let_read()

                G.write(["You give Alton the signal. Together, you wait for an opening.", "You bait the hideous monster with a carefully aimed chopstick that lay nearby.", '"NOW!" you yell.'])
                let_read()

                G.write(["Without a nanosecond of hesitation, Alton springs into action.", "Years of work as a chef paying off in the passing of an instant.", 'Alton reaches up his sleave. What does he have there?', '\n\nThe monster looks afraid.'])
                let_read()
            else:
                G.write([f"You glance over at {alton.name}. He's sweating-- barely holding on.", "You know how he feels. It takes everything you have to not give up and accept your fate.", "\n\nBut--", "you're in this together. You won't let him down, only because he won't let YOU down."])
                let_read()

                G.write(["You give Alton the signal. Together, you wait for an opening.", "You bait the Man in the Black Suit with a carefully aimed chopstick that lay nearby.", '"NOW!" you yell.'])
                let_read()

                G.write(["Without a nanosecond of hesitation, you both spring into action.", 'The two of you wind up a punch to put an end to this impedance.', '\n\nThe Man in the Black Suit looks afraid.'])
                let_read()

        else:
            raise KeyError

        G.write(["Alton pulls a foreign object out of his sleeve.", "He does so with such prowess it seems as if this was a daily ritual to him, once upon a time.", '\n\n"TODAY\'S SECRET INGREDIENT IS', '...YOUR GRAVE!"'])
        let_read()

        print(f"{Fore.BLACK}{Back.WHITE}Ending:{Style.RESET_ALL} alton [B]rown's secret ingredient\n\n{Fore.BLACK}{Back.WHITE}Player Status:{Style.RESET_ALL} Alive\n{Fore.BLACK}{Back.WHITE}Boss Status:{Style.RESET_ALL} Dead\n{Fore.BLACK}{Back.WHITE}Alton Brown Status:{Style.RESET_ALL} Alive\n\n")
        let_read()
        exit()

    except KeyError:
        if (tso_chicken.name in build_temp_effects(manager)):
            G.write(['Sweat drips down your brow as you are knocked back by another attack.'])

            if black_suit_buff.name in build_temp_effects(manager):
                G.write(['The hideous beast seems no closer to being defeated, yet you have been fighting for what seems like an eternity.', 'Just as you feel ready to submit, a small, headless, umbrageous form runs out from behind you.', f'\n\nThe Ghost of {tso_chicken.name} rose from the abyss to aid you in your fight.'])
                let_read()

                G.write([f'The Ghost leaps high into the air, and delivers a swift kick to the face.', 'Your foe falls flat on his rear end.', '\n\nNo sooner does he fall, than the chicken begins to run circles around him.'])
                let_read()
            else:
                G.write(['The Man in the Black Suit seems no closer to being defeated, yet you have been fighting for what seems like an eternity.', 'Just as you feel ready to submit, a small, headless, umbrageous form runs out from behind you.', f'\n\nThe Ghost of {tso_chicken.name} rose from the abyss to aid you in your fight.'])
                let_read()

                G.write([f'The Ghost strikes hard and fast--- delivering a swift kick to the face of your opponent.', 'The Man in the Black Suit stands temporarily paralyzed.', '\n\nNo sooner does the Ghost land, than the he begins to run circles around the black-suitted antagonist.'])
                let_read()

            G.write(['A dark hole opens up.', "At first, it's something that you feel, rather than see. So small that only some semblance of a sixth sense could detect its vile presence.", "But,", "after a while,", f"it begins to open up wider and wider until it swallows your foe hole. The Ghost of {tso_chicken.name} jumps in after it.", '\n\nIn the moments before it closes, you catch a glimpse of a realm that exists outside of your own.', "It looks as if this black is sucking in the light, rather than just the absense of it."])
            let_read()

            G.write(['As the hole closes and the world returns to normal, you feel a change within you.', 'After all,', 'when you stare into the abyss,', 'the abyss stares back.'])
            let_read()

            if user_tipped is False:
                G.write([f'Just as you have a moment to take a breath, {alton.name} leaps out from behind the counter.', '\n\n"Well, now that that is dealt with..." he begins.', f'"Who do you think you are to come into {Fore.RED}MY{Fore.RESET} restaurant and never leave a tip?"', '\n\nYou\'re stunned. "Since it\'s your business, don\'t you make all the profit? Why do I need to tip?"', '\n\n"You fool..."'])
                let_read()

                G.write(['Alton takes one step foreward.', "You aren't prepared to deal with another contender, after giving your all to defeat the Man in the Black Suit.", 'Nevertheless, you prepare to defend yourself yet again.', 'Just as he is about to reach you, he is yanked to the ground.', '\n\n"No..." he stammers.', '"...NO!"', f'\n\n{alton.name} tries to pull himself up, but fails repeatedly to do so.', 'He begins to sink into the floor, panicking as he goes.', f'Just as he disappears, you see the silhouette of {tso_chicken.name}.'])
                let_read()

                print(f"{Fore.BLACK}{Back.WHITE}Ending:{Style.RESET_ALL} the watchful eye of g[E]neral tso\n\n{Fore.BLACK}{Back.WHITE}Player Status:{Style.RESET_ALL} Alive\n{Fore.BLACK}{Back.WHITE}Boss Status:{Style.RESET_ALL} In Limbo\n{Fore.BLACK}{Back.WHITE}Alton Brown Status:{Style.RESET_ALL} Alive\n\n")

            else:
                print(f"{Fore.BLACK}{Back.WHITE}Ending:{Style.RESET_ALL} general tso's [C]hicken\n\n{Fore.BLACK}{Back.WHITE}Player Status:{Style.RESET_ALL} Alive\n{Fore.BLACK}{Back.WHITE}Boss Status:{Style.RESET_ALL} In Limbo\n{Fore.BLACK}{Back.WHITE}Alton Brown Status:{Style.RESET_ALL} Alive\n\n")

        elif user_tipped is True:
            if black_suit_buff.name in build_temp_effects(manager):
                G.write(["You've been jumping on and around my mysterious foe for what feels like an eternity.", "Your eyes keep darting around for some kind of way out of this.", "Suddenly, you spot it."])
                G.write(["\nA packet of Ramen flavoring sits not 20 feet away from you.", "If you could manage to reach it, there would be enough sodium in it to form a circle around the demon.", "\n\nIt'd be trapped with no way out.", 'You have to move now.'])
                let_read()

                G.write(["You think back to dodgeball in grade school.", "Just as you did then, you fake out the throbbing mass of hideousness that spans the area before you.", "Without pause, you lunge for the packet of Ramen. Making quick work of the package, you are able to get at the contents", "\n\nQuickly, you make the salt circle as intended."])
                let_read()

                G.write(["The monster roars.", "Its scream pierces the heavens, yet you perservere.", "Confident in your work, you leave your tip on the table, and head out the door-- sure to take one final look at your mortal enemy."])
                let_read()

                G.write("Time has passed.", .029, 1)
                G.write(["Some say that the beast is still there.", "Others say it's just an urban legend-- nothing more.", "It's difficult to convince yourself of anything anymore.", "\n\nYou don't know when he will erupt out of the darkest pits of your psyche and raze the Earth again."])
                G.write(["You only know one thing for sure:", "he'll be someone else's problem then."])
                let_read()

                print(f"{Fore.BLACK}{Back.WHITE}Ending:{Style.RESET_ALL} the [D]iscount hero\n\n{Fore.BLACK}{Back.WHITE}Player Status:{Style.RESET_ALL} Alive\n{Fore.BLACK}{Back.WHITE}Boss Status:{Style.RESET_ALL} Unknown\n{Fore.BLACK}{Back.WHITE}Alton Brown Status:{Style.RESET_ALL} Unknown\n\n")

        elif user_tipped is False:
            if black_suit_buff.name in build_temp_effects(manager):
                G.write(["You ready my final stand against the beast.", "With a fatal blow, you knock the monster to the ground-- an explosive cloud of smoke rising in its wake.", "\n\nAs it clears, the remains of the foul beast disintegrate before me. You have done well."])
            else:
                G.write(['The Man in the Black Suit\'s energy wears thin.', 'During a brief opening, you sieze the oppurtunity and deliver a knockout blow.', '\n\nSlowly, you relax from the form taken during my final strike, and watch as your opponent falls down.'])

            G.write(["\nYou motion toward the door.", "No sooner do you pass the counter than do you feel something at your back.", "You look down to see a chopstick sticking out of your chest."])

            if manager.percent_health(user) >= 50:
                G.write(["If you'd had less strength, this would be it.", "Instead, you roll away behind a table."])
                let_read()

                G.write(["Your assailant reveals himself, foolishly thinking that he would have time to attack once again in your stupor.", "It appears Alton was unimpressed with your tip.", "\n\nYou're unimpressed with his hospitality."])
                let_read()

                G.write(["You lunge towards the counter and pull the chopstick out of me in one easy motion.", "Taking some food from the counter, you use the lone chopstick to feed him some of his own medicine.", "His body violently resists the cooking.", '\n\nAfter a moment that expands into a painful eternity, he falls limp.'])
                let_read()
                G.write(['"I\'m no lawyer," you begin.', '"...but if that\'s how a cook reacted to his own work..."', '"I\'d sous the chef.'])
                let_read()

                print(f"{Fore.BLACK}{Back.WHITE}Ending:{Style.RESET_ALL} some of his own m[E]dicine\n\n{Fore.BLACK}{Back.WHITE}Player Status:{Style.RESET_ALL} Alive\n{Fore.BLACK}{Back.WHITE}Boss Status:{Style.RESET_ALL} Dead\n{Fore.BLACK}{Back.WHITE}Alton Brown Status:{Style.RESET_ALL} Dead\n\n")
            else:
                G.write(["If you'd had more strength, maybe you'd be able to fight back."])
                let_read()

                G.write(['Barely enough time passes to fall to your hands before a dozen carefully-aimed chopsticks lampoon you.', f'\n\n"Thanks for getting the Government off of my back," says {alton.name} in a chipper tone. "They were really beginning to get on my nerves."'])
                let_read()

                G.write(['You barely manage to summon the might to speak.', '\n\n"H...he...lp..."', 'Speaking is more difficult than you thought.', '\n\n"Damned chopsticks!" you think to yourself. "If they weren\'t so cheap, they\'d\'ve put me out of my misery already."'])
                G.write(['\n"Well, if you don\'t mind...', 'I have a flight to Panama to catch."'])
                let_read()

                cli_color('setterm --inversescreen on', 'color F0')
                G.write(['Alton walks out of the room, and I am left to face my final moments in peace.'])
                let_read()
                cli_color('setterm --inversescreen off')

                print(f"{Fore.BLACK}{Back.WHITE}Ending:{Style.RESET_ALL} alton's a[F]fluent adventures in panama\n\n{Fore.BLACK}{Back.WHITE}Player Status:{Style.RESET_ALL} Alive\n{Fore.BLACK}{Back.WHITE}Boss Status:{Style.RESET_ALL} Dead\n{Fore.BLACK}{Back.WHITE}Alton Brown Status:{Style.RESET_ALL} Dead\n\n")

        else:
            G.write(["You're tired, but you can tell that your opponent is too.", "You both look each other in the eyes."])

            if black_suit_buff.name in build_temp_effects(manager):
                G.write("\nAt least, you think that's his eye.")

            G.write(["\nYou think you're beginning to understand each other a little more."])
            let_read()

            G.write(["I go to put down my fists, and it looks as if he is about to do the same.", "Suddenly,", "something crashes through the roof.", "It appears to be some kind of robotic creature.", "It would seem neither of you have seen anything like it.\n\n"])
            let_read()

            G.write(["It speaks with a voice unlike anything I've ever heard.", '"Sorry to barge in," it begins.', '"Something else is supposed to happen here. The code monkeys screwed everything up, and I do mean *everything*.', '\n\nEmpty the bitbucket.', "Check the logs.", '"Something broke."', "\n\nAnd just like that, everything stopped."])
            let_read()

            print(f"{Fore.BLACK}{Back.WHITE}Ending:{Style.RESET_ALL} good code [G]one wild\n\n{Fore.BLACK}{Back.WHITE}P#%PLAJC@@:{Style.RESET_ALL} ???\n{Fore.BLACK}{Back.WHITE}B%%OISMCC:{Style.RESET_ALL} ???\n{Fore.BLACK}{Back.WHITE}B%%OISMCC:{Style.RESET_ALL} ???\n\n")

        let_read()
        exit()


def lose(manager):
    # Player dies
    G.clr_console()

    if 'Mysterious Orange Liquid' in build_temp_effects(manager):
        G.write(['The Giant Governmental Beast rears back to deliver an enormous blow.', 'You try to jump out of the way, but your legs give out.', '\n\nYou fall to the ground in pain.', f'\n\n{black_suit.name} looks as if he pities you, even for but a moment.'])
        G.write(['He takes a step closer.', 'Unable to face your fate, you close my eyes.'])
        let_read()

        cli_color('setterm --inversescreen on', 'color F0')
        G.write(['\nTime slows down as you become keenly aware of your own heartbeat.', "You notice that you hadn't ever thought about your heart -- the force that had kept your life in motion -- until it was about to stop beating."])
        let_read()

        G.write(['You begin to hear the wind around his fist as it draws nearer.', 'Your will to live screams out like a cry during a moment of silence.', '\n\nYou think to yourself how few pennies it would have taken to save your life.', 'Was this worth it?'])
        let_read()

    else:
        G.write(["Even though you had survived in the face of the Man in the Black Suit's increased size, still he has bested you.", 'He lines up to deliver one final blow, and time barely passes enough to flinch before it lands.', '\n\nNow you lay on your ground.'])

    G.write(["You realize that there's no use in questioning your choices now.", "Everything you've done has been set in stone.", "\n\nIn the end, everyone pays the same price.", 'The only difference is how you count the cost.'])
    let_read()

    cli_color('setterm --inversescreen off')
    print(f"{Fore.BLACK}{Back.WHITE}Ending:{Style.RESET_ALL} there [A]in't no such thing as a free lunch\n\n{Fore.BLACK}{Back.WHITE}Player Status:{Style.RESET_ALL} Deceased\n{Fore.BLACK}{Back.WHITE}Boss Status:{Style.RESET_ALL} Alive\n{Fore.BLACK}{Back.WHITE}Alton Brown Status:{Style.RESET_ALL} Alive")
    let_read()

    exit()


#
# Battle Managers
#
# Black belt
class base_bat_man(G.battle_manager):
    def player_win(self, plyr, enemy):
        # The player wins
        win(self)

    def player_lose(self, plyr, enemy):
        # The player loses
        lose(self)


class katana_bat_man(base_bat_man):
    def battle(self, plyr, enemy, spec_effect=None, music=None):
        self.determine_first_turn(plyr, enemy)

        if isinstance(music, str):
            from Gilbo_Media import music_manager
            mus_man = music_manager()
            mus_man.init_track(music)
            mus_man.play_loop()

        while (plyr.stats.health > 0) and (enemy.stats.health > 0):
            # Allow player to read before clearing screen

            # Check to make sure no effects are active that shouldn't be
            self.refresh_active_effect(plyr, enemy)

            # Run the spec_effect if there is one specified
            if spec_effect is not None:
                spec_effect()

            # Check if player is attacking or defending
            try:
                # Determine whose turn it is
                if self.battle_dict['turn'] == G.Turn.Attack:
                    def active_debuff_check():
                        if (self.effect_dict['reverse_effect_player'] != []) or (self.effect_dict['reverse_effect_enemy'] != []):
                            return True
                        else:
                            return False

                    while True:
                        try:
                            # Clear console and then redraw HP
                            self.draw_hp(plyr, enemy)

                            print("\n1. Attack\n2. Use Item")

                            if active_debuff_check() is True:
                                print("3. Status Effects")

                            print("Enter a number to select an option.")

                            user_choice = input("\nChoice: ")

                            if user_choice == '1':
                                # Player chooses to attack #
                                # Determine attack and use it
                                self.draw_hp(plyr, enemy)

                                self.switch_turn(plyr.stats.power, self.use_attack(plyr, enemy, self.plyr_choose_attack(plyr)))
                            elif user_choice == '2':
                                # Player choose to use an item #
                                self.draw_hp(plyr, enemy)
                                self.switch_turn(plyr.stats.power, self.use_item(plyr, self.plyr_choose_item(plyr)))
                            elif (user_choice == '3') and (active_debuff_check() is True):
                                self.draw_hp(plyr, enemy)
                                self.stat_change_writeout()
                            else:
                                input('Invalid input.')
                        except G.ChooseAgain:
                            pass

                if self.battle_dict['turn'] == G.Turn.Defend:
                    while True:
                        enemy_choice = self.randnum(100)
                        # Test if enemy uses item
                        if enemy_choice <= self.chance_item(enemy):
                            self.switch_turn(enemy.stats.power, self.enemy_use_item(enemy))
                        else:
                            # Attack
                            self.switch_turn(enemy.stats.power, self.use_attack(enemy, plyr, self.enemy_determine_attack(enemy)))

            except G.TurnComplete:
                if self.battle_dict['turn'] == G.Turn.Attack:
                    plyr.collection.add_item(stamina)

                input('\nPress enter to continue.')
                pass

        if plyr.stats.health > 0:
            self.player_win(plyr, enemy)
        else:
            self.player_lose(plyr, enemy)


class chop_bat_man(katana_bat_man):
    def plyr_choose_attack(self, plyr):
        choices = []
        while True:
            choices = [self.randnum(len(plyr.attacks)), self.randnum(len(plyr.attacks))]
            if choices[0] != choices[1]:
                try:
                    plyr.attacks[choices[0]]
                    plyr.attacks[choices[1]]
                    break
                except IndexError:
                    pass

        print(f'\n1. {plyr.attacks[choices[0]].name}\n2. {plyr.attacks[choices[1]].name}')

        # Prompt user
        print('\nEnter a number to attack. \nType "info [number]" for more info about the attack.\nType "q" to return to the previous menu.')

        def replace_value(word):
            if (word == '0') or (word == 0):
                return choices[0]
            elif (word == '1') or (word == 1):
                return choices[1]

        while True:
            user_choice = input('\nChoice: ')

            try:
                # Determine action based on input
                if "info" in user_choice:
                    self.attack_info(plyr.collection.items, plyr.attacks[replace_value(int(user_choice.split(' ')[1]) - 1)])
                elif user_choice.lower() == 'q':
                    raise G.ChooseAgain
                else:
                    # Convert user_choice to indexable integer
                    user_choice = int(user_choice) - 1

                    try:
                        req_ammo = plyr.collection.items.count(plyr.attacks[replace_value(user_choice)].ammo_type)
                        if (plyr.attacks[replace_value(user_choice)].ammo_type in plyr.collection.items) and (req_ammo >= plyr.attacks[replace_value(user_choice)].ammo_cost):
                            return plyr.attacks[replace_value(user_choice)]
                        else:
                            print("You don't have the correct item to use this attack.")
                    except AttributeError:
                        return plyr.attacks[replace_value(user_choice)]

            except (ValueError, IndexError, AttributeError):
                    print('Invalid input.')


#
# Main #
#
def main():
    print('Tax Calculator 2: The Audit\nWritten using Gilbo-API (© 2018 Adam Zett)\n')
    print('Skip dialogue?')

    dialogue = None
    while dialogue is None:
        user_choice = input('Yes or No: ')
        if user_choice.lower() == 'yes':
            dialogue = False
        elif user_choice.lower() == 'no':
            dialogue = True
        else:
            print('Invalid selection.')

    del user_choice

    G.clr_console()
    global user_tipped
    if dialogue is True:
        narrator.say('describe-setting')
        user_tipped = None
        while user_tipped is None:
            user_choice = input('Yes or No: ')
            if user_choice.lower() == 'yes':
                user_tipped = True
                narrator.say('user-tipped')
                alton.say('thanks-for-tipping')
            elif user_choice.lower() == 'no':
                user_tipped = False
                narrator.say('user-no-tip')
            else:
                print('Invalid selection.')

        del user_choice

        let_read()
        narrator.say('try-to-leave')
        suit_narrator.say('initial-encounter')
        narrator.say('enemy-spotted')
        alton.say('law-run-in')

        let_read()
        suit_narrator.say('tax-confront')
        narrator.say('back-to-reality')
        suit_narrator.say('avoid-this')
        narrator.say('enemy-attacks')
    else:
        user_tipped = False

    weapon_chosen = None

    if dialogue is False:
        print('Choose your weapon.')

    print(f"\n1. Katana\n-------------------\n'{katana.dscrpt}'")
    print(f"\n2. Black Belt\n-------------------\n'{black_belt.dscrpt}'")
    print(f"\n3. Chop Sticks\n-------------------\n'{chop_sticks.dscrpt}'")
    print('\nEnter a number to make your choice.')
    black_suit.entity_dict['used_buff'] = False

    while weapon_chosen is None:
        user_choice = input('\nChoice: ')
        global bat_man
        if user_choice == '1':
            weapon_chosen = True
            print('\nSpecial effects: Stamina will regenerate once per turn to allow for the use of special attacks.')
            let_read()
            user.collection.equip(katana)
            user.collection.add_item(stamina)
            bat_man = katana_bat_man()
        elif user_choice == '2':
            weapon_chosen = True
            user.collection.equip(black_belt)
            bat_man = base_bat_man()
        elif user_choice == '3':
            weapon_chosen = True
            print('\nSpecial effects: Stamina will regenerate and two random attacks will be generated twice every turn, and the player can choose from one each time.\n')
            let_read()
            user.collection.equip(chop_sticks)
            user.collection.add_item(spray_can, 5)
            bat_man = chop_bat_man()
        else:
            print('Invalid input')

    global monologue
    monologue = [0, None]

    bat_man.battle(user, black_suit, bat_check, "./Media/boss.wav")


if __name__ == '__main__':
    main()

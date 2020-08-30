#WokeDev
#Description: This program is a text-based Role Playing Game(RPG) called Ratventure!
#             Your objective is to defeat the Rat King and save the world!
#Completed both basic and advance features.
#Additional features include Opponent Variants, Increase Difficulty Over Time, and Custom Name.

#importing libraries
from random import randint
from math import floor

#setting global variables
global player, world_map

#default world map
world_map = [['T', ' ', ' ', ' ', ' ', ' ', ' ', ' '],\
             [' ', ' ', ' ', 'T', ' ', ' ', ' ', ' '],\
             [' ', ' ', ' ', ' ', ' ', 'T', ' ', ' '],\
             [' ', 'T', ' ', ' ', ' ', ' ', ' ', ' '],\
             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],\
             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],\
             [' ', ' ', ' ', ' ', 'T', ' ', ' ', ' '],\
             [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'K']]

def show_menu(menu): #stores all display menu function
    menu_dict = {'main': ('New Game', 'Resume Game', 'View Leaderboard','Exit Game'),
                 'town': ('View Character','View Map','Move','Rest','Save Game', 'Exit Game'),
                 'fight': ('Attack','Run'),
                 'open': ('View Character','View Map','Move','Sense Orb','Exit Game')}
    menu_text = menu_dict[menu]
    for option in range(len(menu_text)): #printing the menu
        print('{}) {}'.format(option+1, menu_text[option]))
    
def view_char(char): #view character information
    if char == player: #if the character is player display player stats
        print('\n{}'.format(player['Name']))
        print('{:>8}: {}-{}'.format('Damage',player['Min Damage'],player['Max Damage']))
        print('{:>8}: {}'.format('Defence',player['Defence']))
        print('{:>8}: {}'.format('HP',player['HP']))
        if player['Orb'] == True: #if the player has already picked up the orb
            print('You are holding the Orb of Power.')
    else: #else display mob encounter stats
        print('Encounter! - {}'.format(char['Name']))
        print('Damage: {}-{}'.format(char['Min Damage'],char['Max Damage']))
        print('Defence: {}'.format(char['Defence']))
        print('HP: {}'.format(char['HP']))

def display_map(): #displaying world_map
    for row in range(len(world_map)): #the y axis of the world map
        print('+---+---+---+---+---+---+---+---+')
        print('|',end='')
        for col in range(len(world_map[row])): #the x axis of the world map
            if player['Location'] == [row, col]: #if player is on the space replace with player's symbol
                if world_map[row][col] == ' ':
                    world_map[row][col] = 'H'
                if world_map[row][col] == 'T':
                    world_map[row][col] = 'H/T'
                if world_map[row][col] == 'K':
                    world_map[row][col] = 'H/K'
            else: #else replace back to default symbol
                if world_map[row][col] == 'H':
                    world_map[row][col] = ' '
                if world_map[row][col] == 'H/T':
                    world_map[row][col] = 'T'
                if world_map[row][col] == 'H/K':
                    world_map[row][col] = 'K'
            print('{:^3}|'.format(world_map[row][col]), end='')
        print()
    print('+---+---+---+---+---+---+---+---+')
                
def find_event(): #finding event based on players position
    event = ''
    for row in range(len(world_map)):
        for col in range(len(world_map[row])):
            if player['Location'] == [row, col]:
                if world_map[row][col] == ' ': #if the space is empty, player is outside
                    event = 'Outside'
                if world_map[row][col] == 'T': #if the space is a town, player is in a town
                    event = 'Town'
                if world_map[row][col] == 'K': #if the space is a rat king, player encounters rat king
                    event = 'Rat King'
    return event

def move(m): #movement of player based on user input
    prev_location_y, prev_location_x = player['Location'][0], player['Location'][1] #storing current players location to a variable as reference

    if m.upper() == 'W':
        player['Location'][0] -= 1
    elif m.upper() == 'A':
        player['Location'][1] -= 1
    elif m.upper() == 'S':
        player['Location'][0] += 1
    elif m.upper() == 'D':
        player['Location'][1] += 1
    else:
        print('Invalid Input')
    for i in player['Location']: #if player tries to move out of the map, it will be an invalid move.
        if i < 0 or i > len(world_map)-1:
            player['Location'][0], player['Location'][1] = prev_location_y, prev_location_x
            print('You cannot move there')
    
    if [prev_location_y, prev_location_x] != player['Location']: #if the player has moved to a new space
        player['Day'] += 1
        player['Event'] = find_event() #find new space event
    display_map()

def sense_orb(): #sensing orb function
    if player['Orb'] == True: #if the player already have the orb
        print('\nYou are already holding the Orb of Power.')
    else:
        player['Day'] += 1
        if player['Location'] == player['Orb Location']: #if the player is on the orb location, increase stats
            print('\nYou found the Orb of Power!')
            player['Orb'] = True
            player['Min Damage'] += 5
            player['Max Damage'] += 5
            print('Your attack increases by 5!')
            player['Defence'] += 5
            print('Your defence increases by 5!')
            player['HP'] += 5
        else: #else give player hint to where the map is at
            direction = ''
            if orb_y < player['Location'][0]:
                direction += 'north'
            if orb_y > player['Location'][0]:
                direction += 'south'
            if orb_x >  player['Location'][1]:
                direction += 'east'
            if orb_x <  player['Location'][1]:
                direction += 'west'
            print('\nYou sense that the Orb of Power is to the {}.'.format(direction))

def generate(item): #generation of orb or town
    possible = []
    if item == 'Orb': #if parameter is 'Orb', generate orb
        for row in range(4,8): #generate to bottom
            for col in range(8):
                if world_map[row][col] == ' ':
                    possible.append([row,col])
                    
        for row in range(8): #generate at right
            for col in range(4,8):
                if world_map[row][col] == ' ':
                    possible.append([row,col])
        return possible[randint(0,len(possible))]

    if item == 'Town': #if parameter is 'Town', generate towns
        for row in range(len(world_map)): #removing existing towns from default map
            for col in range(len(world_map[row])):
                if world_map[row][col] == 'T':
                    world_map[row][col] = ' '
                    
        possible.append([0,0]) #fixed default starting town
        count = 0
        while len(possible) < 5: #run through this algorithm until there are 5 coordinates
            y, x = randint(0,len(world_map)-1), randint(0,len(world_map)-1) #generate random new combinations
            if world_map[y][x] == ' ': #if the space is empty, this excludes spaces where there are towns or kings
                for i in possible:
                    if (i[0] - y)**2 + (i[1] - x)**2 > 4: #formula to distance town from one another
                        count += 1
            if count == len(possible):
                if [y,x] not in possible: #if the new combination are not the same as in the possible list
                    possible.append([y,x]) #append valid coordinates into possible list
                    count = 0
            else: #if there are no more possible combinations reset
                count = 0
                possible = [[0,0]]
        return possible #return valid town coordinates

#start of main program-------------------------------------------------------------------
print('Welcome to Ratventure!')
print('-'*22)
while True: 
    try:
        show_menu('main') #start program with main menu
        main_choice = int(input('Enter choice: '))

        if main_choice == 1: #new game
            town_coords = generate('Town') #get newly generated town coordiantes in a list
            for j in town_coords: #assigning new towns into the map
                world_map[j[0]][j[1]] = 'T'
                
            [orb_y, orb_x] = generate('Orb') #get newly generated orb location
            
            p_name = input('\nEnter your name: ') #prompt for user name
            if p_name == '': #if the user does not enter a name, default name will be The Hero
                p_name = 'The Hero'
            if len(p_name) >=12: #character limit of 12
                p_name = '{:.12s}'.format(p_name)
            #initializing new character properties
            player = {'Name':p_name, 'Min Damage':2, 'Max Damage':4, 'Defence':1, 'HP':20, 'Location':[0,0], 'Day':1, 'Event':'Town', 'Orb Location':[orb_y,orb_x], 'Orb': False}
            game_over = False #start game
        
        if main_choice == 2: #resume game
            try:
                file = open('saves.txt','r')
                values = []
                for line in file:
                    line = line.strip().split('=')
                    values.append(line[1])
                file.close()
            
            except FileNotFoundError: #if the save file is empty
                print('\nYou do not have a save file.\n')
                continue
            
            if values == []:
                print('\nYou do not have a save file.\n')
                continue
            
            else: #else load saved values into player properities, orb and town locations
                for row in range(len(world_map)): #clear default map
                    for col in range(len(world_map[row])):
                        if world_map[row][col] == 'T':
                            world_map[row][col] = ' '
                            
                p_location, orb_location = values[5].strip('][').split(', '), values[8].strip('][').split(', ')
                orb_y, orb_x = int(orb_location[0]), int(orb_location[1]) #assigning orb location

                town_coords = []
                for i in range(10,len(values)): #getting town location values
                    town = values[i].strip('][').split(', ')
                    town = [int(town[0]),int(town[1])]
                    town_coords.append(town)
                    town = ''
                for j in town_coords: #assigning town locations onto world map
                    world_map[j[0]][j[1]] = 'T'
                #assigning player saved values into player dictionary
                player = {'Name':values[0], 'Min Damage':int(values[1]), 'Max Damage':int(values[2]), 'Defence':int(values[3]), 'HP':int(values[4]), 'Location':[int(p_location[0]),int(p_location[1])], 'Day':int(values[6]), 'Event':'Town', 'Orb Location':[orb_y, orb_x], 'Orb': eval(values[9])}
                game_over = False #start game
        
        if main_choice == 3: #view leaderboard
            print('\n--------Leaderboard--------')
            print('{:5}{:12}{}'.format('No.','Name','Days Taken')) #header labels
            players_list = []
            try:
                file = open('leaderboard.txt','r')
                for line in file:
                    players_list.append(line.strip().split(','))
                file.close()

            except FileNotFoundError:
                print('\n{:3}{}\n'.format('','Leaderboard is empty!'))
                continue
            
            if players_list == []:
                print('\n{:3}{}\n'.format('','Leaderboard is empty!'))
                continue
            
            else: #show player rankings
                days_list = []
                for players in players_list:
                    days_list.append(players[1]) #getting days from players_list
                days_list.sort() #sort the days_list to get lowest to highest
                for t in range(len(days_list)): #getting top 5 players
                    if t >= 5:
                        break
                    else:
                        for i in players_list:
                            if days_list[t] in i:          
                                print('{:<5}{:12}{}'.format(t+1,i[0],i[1]))
                print()
                continue
        
        if main_choice == 4: #exit game
            break
            
#start of game---------------------------------------------------------------------------
        while game_over == False:
            try:
#if player is in a Town------------------------------------------------------------------
                if player['Event'] == 'Town':
                    print('Day {}: You are in a town.'.format(player['Day']))
                    show_menu('town')
                    choice = int(input('Enter choice: '))
                    
                    if choice == 1: #view player information
                        view_char(player)
                        
                    elif choice == 2: #view map
                        display_map()
                        
                    elif choice == 3: #move
                        display_map()
                        print('W = up; A = left; S = down; D = right')
                        move(input('Your move: '))
                        
                    elif choice == 4: #rest
                        player['HP'] = 20
                        if player['Orb'] == True:
                            player['HP'] += 5
                        player['Day'] += 1
                        print('\nYou are fully healed.')
                        
                    elif choice == 5: #save game
                        file = open('saves.txt','w')
                        for s in player: #save player stats into file
                            file.write('{}={}\n'.format(s,player[s]))
                        for town in range(len(town_coords)): #after saving player stats, save town locations
                            file.write('Town{}={}\n'.format(town+1,town_coords[town]))
                        file.close()
                        print('\nGame saved.')

                    elif choice == 6: #exit game
                        game_over = True

                    else:
                        print('Invalid Input\n')
#if player is outside--------------------------------------------------------------------
                if player['Event'] == 'Outside':
                    print('Day {}: You are out in the open.'.format(player['Day']))
                    
                    #variation of mobs
                    bat = {'Name':'Bat', 'Min Damage':1, 'Max Damage':1, 'Defence':0, 'HP':7}
                    rat = {'Name':'Rat', 'Min Damage':1, 'Max Damage':3, 'Defence':1, 'HP':10}
                    skeleton = {'Name':'Skeleton', 'Min Damage':2, 'Max Damage':3, 'Defence':1, 'HP':11}
                    mob_list = [bat, rat, skeleton]
                    
                    mob = mob_list[randint(0,len(mob_list)-1)] #pick 1 from mob_list
                    day_multipler = floor(player['Day']/10) #as days are longer, monsters are harder
                    mob_hp = mob['HP'] #set reference base hp of mob
                    mob['Min Damage'] += day_multipler
                    mob['Max Damage'] += day_multipler
                    player['Event'] = 'Encounter' #change player's event to encounter

#if player is in an encounter------------------------------------------------------------
                if player['Event'] == 'Encounter':
                    view_char(mob) #view the stats of the mob
                    show_menu('fight')
                    choice = int(input('Enter choice: '))
                    if choice == 1: #if the player, chooses to fight the mob
                        player['Event'] = 'Combat' #change player event to combat
                    elif choice == 2: #if the player, chooses to run away
                        player['Event'] = 'Ran' #change player event to ran
                    else:
                        print('Invalid Input\n')
#if player is in combat------------------------------------------------------------------
                if player['Event'] == 'Combat':
                    damage_dealt = (randint(player['Min Damage'], player['Max Damage'])) - mob['Defence'] #formula for damage dealt to mob
                    damage_taken = randint(mob['Min Damage'], mob['Max Damage']) - player['Defence'] #formula for damage taken by player
                    
                    if damage_dealt <= 0: #if the damage is in negative, set to 0
                        damage_dealt = 0 #otherwise it will heal the mob as negative plus negative equal positive.
                    if mob['Name'] == 'Rat King' and player['Orb'] == False: #if the player encounters the rat king without the orb
                        print('\nYou do not have the Orb of Power - the Rat King is immune!')
                        damage_dealt = 0 #set all attacks to 0
                        
                    mob['HP'] -= damage_dealt #player deals damage to mob first
                    print('\nYou deal {} damage to the {}'.format(damage_dealt,mob['Name']))
                    if mob['HP'] <= 0: #if the mob has died
                        print('The {} is dead! You are victorious!'.format(mob['Name']))
                        if mob['Name'] == 'Rat King': #if the player kills the rat king
                            print('Congratulations, you have defeated the Rat King!\nThe world is saved! You win!')
                            file = open('leaderboard.txt','a')
                            file.write('{},{}\n'.format(player['Name'],player['Day'])) #records player name and day
                            file.close()
                            game_over = True #game over
                        else:
                            player['Event'] = 'Open' #otherwise, if mob has died go back to player event open
                    else: #otherwise, the player will recieve the damage from the mob
                        if damage_taken <= 0: #if the mob hits negative numbers, set it to 0
                            damage_taken = 0

                        print('Ouch! The {} hit you for {} damage!'.format(mob['Name'], damage_taken))
                        player['HP'] -= damage_taken #player recieve the damage taken from mob
                        if player['HP'] <= 0: #if the player has negative hp, set it to 0
                            player['HP'] = 0
                            
                        print('You have {} HP left.'.format(player['HP']))
                        if player['HP'] == 0: #if the player has died
                            print('You died! Game Over.')
                            game_over = True #game over
                        else:
                            player['Event'] = 'Encounter' #if the player is still alive, go back to encounter event
#if player ran away----------------------------------------------------------------------
                if player['Event'] == 'Ran':
                    print('\nYou run and hide.')
                    mob['HP'] = mob_hp #resorts enemy mob health
                    player['Event'] = 'Open' #change to player event open
#if player is in open--------------------------------------------------------------------
                if player['Event'] == 'Open':
                    print('Day {}: You are out in the open.'.format(player['Day']))
                    show_menu('open')
                    choice = int(input('Enter choice: '))
                    
                    if choice == 1: #view player information
                        if mob['HP'] <= 0: #if the player has killed the mob
                            view_char(player)
                        else: #otherwise, player will go back into encounter event
                            player['Event'] = 'Encounter'

                    elif choice == 2: #view map
                        if mob['HP'] <= 0: #if the player has killed the mob
                            display_map()
                        else: #otherwise, player will go back into encounter event
                            player['Event'] = 'Encounter'
                            
                    elif choice == 3: #move
                        display_map()
                        print('W = up; A = left; S = down; D = right')
                        move(input('Your move: '))
                        
                    elif choice == 4: #sense orb
                        if mob['HP'] <= 0: #if the player has killed the mob
                            sense_orb()
                        else: #otherwise, player will go back into encounter event
                            player['Event'] = 'Encounter'
                            
                    elif choice == 5: #exit game
                        game_over = True

                    else:
                        print('Invalid Input\n')
#if player encounters rat king-----------------------------------------------------------    
                if player['Event'] == 'Rat King':
                    rat_king = {'Name':'Rat King', 'Min Damage':6, 'Max Damage':10, 'Defence':5, 'HP':25}
                    print('Day {}: You see the {}!'.format(player['Day'], rat_king['Name']))
                    mob = rat_king
                    mob_hp = mob['HP'] #set base reference hp
                    player['Event'] = 'Encounter' #change player event to encounter
                    
            except: #if the player has input an invalid input during the game
                print('Invalid Input\n')
        else: #if game_over == True
            break
    except: #if the player has input an invalid input during the main menu
        print('Invalid Input\n')
        continue

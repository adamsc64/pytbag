sections = [
("""\
You are outside a house. There is a tree in the front yard and there are a
number of cars parked in the driveway. Down the street you see people talking.
""", "Front of house"), #0
("""\
You are next to the house in the driveway. There is a blue car and a red car in
the driveway.
""", "In Driveway"), #1 
]

sec = dict()
for indexed in enumerate(sections):
    index = indexed[0]
    long_name = indexed[1][1]
    short_name = ''
    for ch in long_name:
	if ch in ' /':
	    short_name += '-'
	elif not ch in ".'":
	    short_name += ch.lower()
    sec[short_name] = index

dirs = {
    'north':0,	    'n':0,
    'south':1,	    's':1,
    'west':2,	    'w':2,
    'east':3,	    'e':3,
    'northeast':4,  'ne':4,
    'northwest':5,  'nw':5,
    'southeast':6,  'se':6,
    'southwest':7,  'sw':7,
    'up':8,	    'u':8,
    'down':9,	    'd':9,   
    'in':10,	    'on':10,	'enter':10,
    'out':11,	    'off':11,	'exit':11,
}

dungeon_map = [
#      n   s   w   e  ne  nw  se  sw   u   d  in  out
    [ -1, -1, -1,  2, -1, -1,  1, -1, -1, -1, -1,  -1 ], #0
    [  0,  4, -1,  3, -1,  0, -1, -1, -1, -1, -1,  -1 ], #1
]

current_section = 0

obj = {
    # takeable >= 0
    'shovel': 0,
    
    # untakeable < 0
    'tree': -1,
    'red-car': -2,
    'blue-car': -3,
}

tk_objs = [
    ("There is a small shovel stuck into the ground.", "A small shovel"), #0
]

tk_obj_desc = [
    "A small shovel. Very small.",  #0
]

perm_objs = [
    None,
    ("There is a tree in the middle of the area", "A tree"), #-1
    ("There is a red car","Red car"), #-2
    ("There is a blue car","Blue car"), #-3
]
perm_obj_desc = [
    None,
    "There is a tree here..........", #-1
    "There is a red car here..........", #-2
    "There is a blue car here..........", #-3
]


inventory = [ ]

items = [
    [ obj['shovel'], obj['tree'] ],  #0
    [ obj['red-car'] ],              #1
]

def _help():
    print """\
This is the help section.
"""

visited = []

def special_sections(section):
    print 'special sections'

def describe(section):
    "Give long if we have a negative room number"
    ## This, of course, will cause room 0 to be always explained long
    global visited
    print sections[abs(section)][1]
    if section <= 0 or not section in visited:
        print sections[abs(section)][0]
    if not section in visited:
        visited.append(section)
    ## Now, everything else:
    special_sections(abs(section))
    for i in items[abs(section)]:
        if i >= 0:
            print tk_objs[i][0]
        else:
            if isinstance(perm_objs[abs(i)], str):
                print perm_objs[abs(i)]

def inven(args):
    print "You currently have:"
    for i in inventory:
        print tk_objs[i][1]
 

def special_move(direction):
    pass

def move(direction):
    global current_section
    destination = dungeon_map[current_section][direction]
    if destination == -1:
	print "You can't go that way."
    elif destination == 50000:
	special_move(direction)
    else:
	current_section = destination
	describe(destination)

def north     (args): move(dirs['north'])
def south     (args): move(dirs['south'])
def west      (args): move(dirs['west' ])
def east      (args): move(dirs['east' ])
def northeast (args): move(dirs['northeast' ])
def northwest (args): move(dirs['northwest' ])
def southeast (args): move(dirs['southeast' ])
def southwest (args): move(dirs['southwest' ])
def up        (args): move(dirs['up' ])
def down      (args): move(dirs['down'])
def _in     (args): move(dirs['enter'])
def out       (args): move(dirs['out'])

def go(args):
    if not args:
        print "You must specify a direction."
    else:
        if not args[0] in dirs:
            print "I don't understand where you want to go."
        else:
            move(dirs[args[0]])

def take(args):
    if not args:
        print "You must specify an object."
    else:
        if args[0] == "all":
            first_objs = list(items[current_section])
            gotsome = False
            for i in first_objs:
                if i >= 0:
                    gotsome = True
                    print "%s:" % tk_objs[i][1],
                    takeobj(i)
            if not gotsome:
                print "Nothing to take."
        else:
            if not args[0] in obj:
                print "I don't know what that is."
            else:
                takeobj(obj[args[0]])

def takeobj(x):
    global inventory, items
    if not x in items[current_section]:
        print "I do not see that here."
    else:
        if x < 0:
            print "You cannot take that."
        else:
            print "Taken."
            items[current_section].remove(x)
            inventory.append(x)

def drop(args):
    global inventory, items
    if not args:
        print "You must specify an object."
    else:
        if not args[0] in obj:
            print "I don't know what that is."
        else:
            objnum = obj[args[0]]
            if not objnum in inventory:
                print "You don't have that."
            else:
                print "Done."
                inventory.remove(objnum)
                items[current_section].append(objnum)

def examine(args): # examine = look
    if not args:
        describe(-current_section) # long description
    else:
        if not args[0] in obj:
            print "I don't know what that is."
        else:
            objnum = obj[args[0]]
            if not objnum in inventory and not objnum in items[current_section]:
                print "I don't see that here."
            else:
                if objnum >= 0:
                    desc = tk_obj_desc[objnum]
                else:
                    desc = perm_obj_desc[abs(objnum)]
                if isinstance(desc, str):
                    print desc
                else:
                    print "I see nothing special about that."

def die(args):
    global dead
    print
    if args:
        print "You are dead."
    # If there is a score, show it.
    dead = True

def _quit(args): # 'quit' is a built-in
    die([])

dead = False

def save_val(varname):
    "The way to reset the variable as it was."
    return "global %s\n%s = %s\n" % (varname, varname, `eval(varname)`)

def save(args):
    if not args:
        print "You must specify a filename."
    else:
        try:
            game = open('_game_' + args[0] + '.txt', 'w')
            game.write(save_val('current_section'))
            game.write(save_val('visited'))
            game.write(save_val(inventory))
            game.write(save_val(items))
            #! Game-writer, apply this to the rest of the properties that change from time to time
            game.close()
            print "Game saved."
        except Exception:
            print "Error saving to file."

def restore(args):
    if not args:
        print "You must specify a filename."
    else:
        try:
            exec open('_game_' + args[0] + '.txt')
            print "Game restored."
            describe(current_section)
        except Exception:
            print "Could not load restore file."



verblist = {
    'take': take, 'get': take, 'pick': take, 'hold': take,
    'drop': drop, 'throw': drop, 'toss': drop,
    'look': examine, 'l': examine, 'examine': examine, 'x': examine,
    'read': examine, 'r': examine, 'describe': examine, #can't use 'd' because of going down
    'inventory': inven, 'i': inven, 'items': inven, 'die': die, 'quit': _quit,
    'help': _help, 'save': save, 'restore': restore, 'go': go,
    'north': north, 'n': north, 'south': south, 's': south,
    'east': east, 'e': east, 'west': west, 'w': west,
    'northeast': northeast, 'ne': northeast, 'southeast': southeast, 'se': southeast,
    'northwest': northwest, 'nw': northwest, 'southwest': southwest, 'sw': southwest,
    'up': up, 'u': up, 'down': down, 'd': down, 'in': _in, 'out': out,
    'on': _in, 'off': out, 'enter': _in, 'exit': out,
}

def execprint(x):
    line = x.split()
    for c in ',:':
	line = c.join(line).split(c)
    if line:
	if not line[0] in verblist:
	    print "Don't understand."
	else:
	    func = verblist[line[0]]
	    args = line[1:]
	    func(args)

def run_game():
    global current_section
    print """Welcome to the age of the great guilds."""
    describe(current_section)
    while not dead:
	reply = raw_input('>').lower().split(';') or ['']
	first = True
	for i in reply:
	    if not dead:
		if not first:
		    print '>'
		execprint(i)
		first = False
    if __name__ == "__main__":
	raw_input('\n') # for DOS support

if __name__ == "__main__":
    run_game()

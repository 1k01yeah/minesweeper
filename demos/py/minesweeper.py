import sys, re
from random import sample as s

pt_relations = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
panel_height = 9
panel_width = 9
bombs = 9
martrix = []
mask = []

def draw(content):
    global bombs
    print '--%d bombs game---' % bombs
    for i in content:
        for j in i:
            print str(j).center(1),
        print

def area_check(x, y):
    '''
    check if the point in panel area
    '''
    global panel_width, panel_height
    return 0 <= x <= (panel_width - 1) and 0 <= y <= (panel_height - 1)

def init_panel():
    global panel_width, panel_height, bombs, martrix, mask
    martrix = [[0 for x in range(panel_width)][:] for y in range(panel_height)]
    mask = [['-' for x in range(panel_width)][:] for y in range(panel_height)]
    for i in zip(*(s(range(bombs),panel_width - 1),s(range(bombs),panel_height - 1))):
        martrix[i[0]][i[1]] = 'x'
    for r in range(len(martrix)):
        row = martrix[r]
        for c in range(len(row)):
            col = martrix[r][c]
            if col == 'x':
                for pt in pt_relations:
                    y = r + pt[0]
                    x = c + pt[1]
                    if area_check(x, y) and martrix[y][x] != 'x':
                        martrix[y][x] += 1
    draw(mask)

def zvirus(seedx, seedy):
    '''
    zero virus,explan all zero cells near by cell-self
    '''
    for pt in pt_relations:
        c = seedx + pt[0]
        r = seedy + pt[1]
        if area_check(c, r) and martrix[c][r] != '*' and mask[c][r] == '-':
            mask[c][r] = martrix[c][r]
            if mask[c][r] == 0:
                zvirus(c, r)

def click(loc):
    global mask, martrix
    if mask[loc[0]][loc[1]] == '#':
        print 'Marked cell is not clickable'
    else:
        mask[loc[0]][loc[1]] = martrix[loc[0]][loc[1]]
        if martrix[loc[0]][loc[1]] == 'x':
            print '\n Game Over! The bombs:'
            draw(martrix)
            print 'starting a new game'
            init_panel()
        else:
            if martrix[loc[0]][loc[1]] == 0:
                zvirus(loc[0], loc[1])
    draw(mask)

def mark(loc):
    global mask, bombs
    if mask[loc[0]][loc[1]] == '-':
        mask[loc[0]][loc[1]] = '#'
        print 'marked', loc[0], loc[1]
    elif mask[loc[0]][loc[1]] == '#':
        mask[loc[0]][loc[1]] = '-'
        print 'unmarked', loc[0], loc[1]
    else:
        print 'Already shown cell is unmarkable'
    draw(mask)

def check_win():
    global mask
    uncomplet = 0
    for i in mask:
        if '-' in i:
            uncomplet += 1
            break
    if not uncomplet:
        print 'Weldone! you win the game!'
        draw(martrix)
        print 'starting a new game'
        init_panel()

def usage():
    global panel_width,panel_height
    print 
    print "Use: type 'click XY' (RET) to click a certan cell\n"
    print "          'click 74' for example \n"
    print "     type 'mark XY' (RET) to mark a bomb cell,\n"
    print "          do this on marked cell means unmark \n"
    print "          'mark 88' for example\n"
    print "     type 'stop' (RET) or C-c to quit the program\n"
    print "     NOTICE THAT:    X :[0,{0})  ; Y:[0,{1}).".format(panel_width-1,panel_height-1)
    print

if __name__ == "__main__":
    init_panel()
    p = re.compile(r'^stop$|(^click [0-8][0-8]$)|(^mark [0-8][0-8]$)')
    bRun = 1
    while(bRun):
        cmdl = sys.stdin.readline().strip()
        if p.match(cmdl):
            if cmdl == 'stop':
                bRun = 0
            else:
                cmd = cmdl[:cmdl.find(' ')]
                y = int(cmdl[cmdl.find(' ') + ((panel_width/10)+1)])
                x = int(cmdl[cmdl.find(' ') + ((panel_height/10)+((panel_width/10)+1)+1)])
                if cmd == 'click':
                    click([x, y])
                elif cmd == 'mark':
                    mark([x, y])
                else:
                    pass
            check_win()
        else:
            usage()
        

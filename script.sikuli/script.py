import random
import time
import itertools
from org.sikuli.basics.proxies import Vision
Vision.setParameter("MinTargetSize", 6)

def do_res_collection():
    if exists("1411319170247.png"):
            click("1411319170247.png")
            sleep(10)
    while not exists("1412005595303.png") and not exists("1412065753605.png"):
        sleep(1)
    if exists("1412005595303.png"):
        click("1412005595303.png")
    iter = 0
    while not exists("1412065753605.png"):
        sleep(1);
    keyDown(Key.CMD)
    try:
        click_point = find("1412066302265.png")
        drop_point = click_point.getTarget().offset(400,400)
        dragDrop(click_point, drop_point)
    except:
        print "Zoom failed to find archer tower"
    keyUp(Key.CMD)
    while iter < 20:
        elixers = []
        coins = []
        dark = []
        try:
            if exists(Pattern("1411925620763.png").similar(0.95)):
                print "elixer exists"
                elixers = findAll("1411925620763.png")
            if exists("1412067211035.png"):
                print "coin exists"
                coins = findAll("1412067211035.png")
            if exists("1412067266022.png"):
                print "dark exists"
                dark = findAll("1412067266022.png")
            all_resources = itertools.chain(elixers, coins, dark)
            
            for c in all_resources:
                click(c)
        except:
            print "exception"
        
        sleep(random.randint(10,30))
        iter += 1
    click("1412065594056.png")
    while not exists("1412065642545.png"):
        sleep(1)
    click("1412065642545.png")
    
def collect_forever():
    while(True):
        do_res_collection()
        sleep(60)

if exists("1412065753605.png"):
    collect_forever()
# launch genymotion through alfred
keyDown(Key.CMD)
keyDown(Key.SPACE)
keyUp(Key.CMD)
keyUp(Key.SPACE)
type("geny" + Key.ENTER)

# Wait for genymotion to load then start vm
while not exists("1412005237101.png"):
    sleep(5)
click("1412005237101.png")

# Wait for android homescreen

while not exists("1412005436007.png") and not exists("1412005595303.png"):
    sleep(5)
screen_locked = exists("1412005436007.png")
if screen_locked:
    dragDrop("1412005436007.png","1412005489167.png")
collect_forever()

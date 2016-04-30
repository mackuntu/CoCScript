open_sign = "open.png"
unlock = "unlock.png"
start_unlock = "1462034142273.png"
chest_open = Pattern("chest_open.png").similar(0.82)
clash_icon = "clash_icon.png"
clash_notification = "clash_notification.png"
home_screen = "home_screen.png"
battle = "battle.png"
App.focus("player")

click_location = None

def clickChest():
    while not exists(battle):
        click_location.click()

def openChestIfAvailable():
    try:
      print "looking for open chests"
      all_chests_available = findAll(open_sign)
      for chest in all_chests_available:
          chest.highlight(3)
          chest.click()
          clickChest()
    except:
      print "no open chests found"

def unlockChestIfAvailable():
    if exists(unlock):
        click()
        wait(start_unlock, 4)
        click()
    else:
      print "no unlock found"

def openClashIfNotification():
    while not exists(clash_notification):
        sleep(60)
    click(clash_icon)
    while not exists(battle):
        sleep(5)
    click_location = find(battle)
    openChestIfAvailable()
    unlockChestIfAvailable()
    click(home_screen)
    openClashIfNotification()

openClashIfNotification()

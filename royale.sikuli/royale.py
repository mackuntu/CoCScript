open_sign = Pattern("open.png").similar(0.40)
unlock = "unlock.png"
start_unlock = "1462034142273.png"
chest_open = Pattern("chest_open.png").similar(0.82)
clash_icon = "clash_icon.png"
clash_notification = "clash_notification.png"
home_screen = "home_screen.png"
battle = "battle.png"
msg_window = "msg_window.png"
card_request = "card_request.png"
minions = "minions.png"
goblins = "goblins.png"

App.focus("player")

click_location = None

def clickChest():
  while not exists(battle):
    try:
      click_location.click()
    except:
      print "cannot click"
      break

def openChestIfAvailable():
  try:
    print "looking for open chests"
    all_chests_available = findAll(open_sign)
    for chest in all_chests_available:
      chest.highlight(3)
      chest.click()
      sleep(1)
      clickChest()
  except e:
    print "no open chests found"
    print e

def unlockChestIfAvailable():
  if exists(unlock):
    click()
    wait(start_unlock, 4)
    click()
  else:
    print "no unlock found"

def requestCardsIfAvailable():
  if exists(msg_window):
    print "found msg button"
    click(msg_window)
    sleep(2)
  if exists(card_request):
    print "found card request available"
    click(card_request)
    sleep(2)
  if exists(goblins):
    print "found goblins to request"
    click(goblins)
  elif exists(minions):
    print "found minions to request"
    click(minions)


def openClashIfNotification():
  while not exists(clash_notification):
    sleep(60 * 60 * 3)
  click(clash_icon)
  while not exists(battle):
    sleep(5)
  click_location = find(battle)
  openChestIfAvailable()
  unlockChestIfAvailable()
  requestCardsIfAvailable()
  click(home_screen)
  openClashIfNotification()

#openClashIfNotification()
#requestCardsIfAvailable()

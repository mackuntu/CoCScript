import random as r
open_sign = Pattern("open.png").similar(0.40)
unlock = "unlock.png"
start_unlock = "1462034142273.png"
chest_open = Pattern("chest_open.png").similar(0.82)
clash_icon = "clash_icon.png"
clash_notification = "clash_notification.png"
home_screen = "home_screen.png"
battle = Pattern("battle.png").similar(0.81)
msg_window = "msg_window.png"
card_request = Pattern("card_request.png").similar(0.79)
minions = "minions.png"
goblins = "goblins.png"
donate = Pattern("donate.png").similar(0.85)
more_donations = Pattern("more_donations.png").exact()

click_location = None

def clickChest():
  while not exists(battle):
    try:
      click_location.click()
      sleep(2)
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
  except:
    print "no open chests found"

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

def donateAsMuchAsPossible():
  try:
    all_donations = findAll(donate)
    print "found donations"
    for donation in all_donations:
      print "donating..."
      donation.highlight(1)
      donation.click()
      donation.click()
  except:
    print "did not find any more donations"
  try:
    if exists(more_donations):
      print "more donations may be possible"
      click(more_donations)
      sleep(2)
      donateAsMuchAsPossible()
  except:
    print "no more donations available"

def startWorkflow():
  App.focus("player")
  global click_location
  click_location = find(battle)
  openChestIfAvailable()
  unlockChestIfAvailable()
  requestCardsIfAvailable()
  donateAsMuchAsPossible()

def openClashIfNotification():
  while not exists(clash_notification):
    sleep(r.randint(60,3600))
    App.focus("player")
  click(clash_icon)
  while not exists(battle):
    sleep(5)
  startWorkflow()
  click(home_screen)
  openClashIfNotification()

openClashIfNotification()

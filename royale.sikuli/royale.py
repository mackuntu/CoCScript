import random as r
import datetime

open_sign = Pattern("open.png").similar(0.40)
unlock = "unlock.png"
start_unlock = "start_unlock.png"
chest_open = Pattern("chest_open.png").similar(0.82)
clash_icon = "clash_icon.png"
clash_notification = "clash_notification.png"
home_screen = "home_screen.png"
battle = Pattern("battle.png").similar(0.81)
msg_window = "msg_window.png"
card_request = Pattern("card_request.png").similar(0.79)
minions = "minions.png"
goblins = "goblins.png"
minion = "minion.png"
donate = Pattern("donate.png").similar(0.85)
more_donations = Pattern("more_donations.png").exact()
human_logged_in = "human_logged_in.png"
card_received = "card_received.png"
close_button = "close_button.png"

click_location = None

class HumanLoggedInException(Exception):
  """ Exception raised for human logging in while executing workflow"""
  pass

class Step():
  """ Base step class for modeling a single action """
  def __init__(self, func, maxRetries = 0, restartOnFail = False):
    self.func = func
    self.maxRetries = maxRetries
    self.restartOnFail = restartOnFail
    self.runItr = 0

  def checkIfHumanLoggedIn(self):
    App.focus("player")
    sleep(1)
    if exists(human_logged_in):
      click(home_screen)
      raise HumanLoggedInException

  def execute_step(self):
    print "[INFO] starting {0} iter {1}".format(self.func.__name__, self.runItr)
    try:
      self.checkIfHumanLoggedIn()
      self.func()
      self.checkIfHumanLoggedIn()
      return True
    except HumanLoggedInException:
      print "[WARN] Detected human logged in, sleep for 30 mins"
      sleep(1800)
      return False
    except:
      if self.maxRetries > 0 and self.maxRetries > self.runItr:
        print "[INFO] retry enabled for step %s" % self.func.__name__
        self.runItr += 1
        sleep(1)
        print "[INFO] retrying..."
        self.execute_step()
      else:
        self.runItr = 0
        return False


class Workflow():
  """ Base workflow class for modeling a sequence of actions """
  def __init__(self, steps = []):
    self.steps = steps

  def add_step(self, step):
    self.steps.append(step)

  def execute(self):
    for step in self.steps:
      if not step.execute_step():
        if step.restartOnFail:
          self.execute()
          break

  def runForever(self):
    counter = 0
    while True:
      print "[INFO] Starting run %d" % counter
      self.execute()
      sleep(1)
      counter += 1

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
  if exists(minion):
    print "found minion to request"
    click(minion)
  elif exists(goblins):
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
      for x in xrange(0,6):
        donation.click()
        sleep(0.5)
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

def setupClickLocation():
  global click_location
  click_location = find(battle)

def openClashRoyale():
  print "attempting to open clash royale"
  click(clash_icon)
  sleep(10)

def checkCardReceived():
  if exists(card_received):
    print "[INFO] Cards received, closing dialog"
    click(close_button)
    sleep(2)

def waitForClashNotification():
  totalSleep = 0
  while not exists(clash_notification):
    sleepTime = r.randint(60, 300)
    print "[INFO] will sleep for {0} seconds, checking again at {1}".format(sleepTime, datetime.datetime.now() + datetime.timedelta(seconds=sleepTime))
    sleep(sleepTime)
    totalSleep += sleepTime
    App.focus("player")
    # Enforces we open at least once an hour
    if totalSleep > 3600:
      return

def init():
  click(home_screen)

def buildWorkflow():
  workflow = Workflow()
  workflow.add_step(Step(func = init, maxRetries = 0, restartOnFail = False))
  workflow.add_step(Step(func = waitForClashNotification, maxRetries = 0, restartOnFail = False))
  workflow.add_step(Step(func = openClashRoyale, maxRetries = 3, restartOnFail = True))
  workflow.add_step(Step(func = checkCardReceived, maxRetries = 0, restartOnFail = False))
  workflow.add_step(Step(func = setupClickLocation, maxRetries = 0, restartOnFail = True))
  workflow.add_step(Step(func = openChestIfAvailable, maxRetries = 0, restartOnFail = False))
  workflow.add_step(Step(func = unlockChestIfAvailable, maxRetries = 3, restartOnFail = False))
  workflow.add_step(Step(func = requestCardsIfAvailable, maxRetries = 0, restartOnFail = False))
  workflow.add_step(Step(func = donateAsMuchAsPossible, maxRetries = 0, restartOnFail = False))
  return workflow

def test():
  openClashRoyale()
  startWorkflow()
  click(home_screen)

clashRoyalWorkflow = buildWorkflow()
clashRoyalWorkflow.runForever()
#test()
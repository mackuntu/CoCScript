from sikuli import *
import random
import time
import itertools
import datetime

class AppState():
  game_not_launched = 0
  game_launched_not_resized = 1
  game_launched_resized = 2
  another_device = 3
  playing_too_long = 4
  enemy_raided = 5
  game_exit_confirm = 6

class AppStateManager():
  def __init__(self, state):
    self.state = state

ANDROID_CLASH_ICON = Pattern("1449675544548.png").similar(0.79)
ANDROID_LOCK_BUTTON = "1412005436007.png"

CLASH_GAME_ICON = "1449765483207.png"
CLASH_RELOAD_BUTTON = "clash_reload_button.png"
CLASH_RELOAD_ANOTHER_DEVICE = "clash_reload_another_device.png"
CLASH_INFO_BUTTON = Pattern("1449651262055.png").similar(0.80)
CLASH_ELIXER_PATTERN = Pattern("1449765631958.png").similar(0.83)
CLASH_COIN_PATTERN = "1449765702720.png"
CLASH_CONFIRM_BUTTON = Pattern("1449675171323.png").similar(0.84)

GENY_BACK_BUTTON = Pattern("1412065594056.png").similar(0.67)
GENY_PLAY_BUTTON = "1412005237101.png"
GENY_CONTINUE_BUTTON = "geny_continue_button.png"

MAX_SLEEP_MINUTES_BETWEEN_COLLECTION = 60
MAX_SLEEP_SECONDS = MAX_SLEEP_MINUTES_BETWEEN_COLLECTION * 60

def try_resize():
  App.focus("player")
  resized = False
  if exists(CLASH_INFO_BUTTON):
    print "found info target"
    start_point = find(CLASH_INFO_BUTTON.targetOffset(random.randint(50, 100),random.randint(50, 100)))
    drop_point = start_point.getTarget().offset(random.randint(600, 650),200)

    keyDown(Key.CMD)
    if dragDrop(start_point, drop_point) == 1:
      resized = True
      keyUp(Key.CMD)
    # move screen down
  return resized

def do_res_collection():
  App.focus("player")
  if exists(CLASH_CONFIRM_BUTTON):
    print "most likely enemy raid occured, found okay button"
    click(CLASH_CONFIRM_BUTTON)
  if exists(CLASH_RELOAD_BUTTON):
    print "asked to reload"
    click(CLASH_RELOAD_BUTTON)
    print "clicked reload, now sleeping for 10 seconds"
  if exists(CLASH_RELOAD_ANOTHER_DEVICE):
    print "another device is connected"
    click(CLASH_RELOAD_ANOTHER_DEVICE)
  while not exists(ANDROID_CLASH_ICON) and not exists(CLASH_GAME_ICON):
    print "no clash icon and no in game icon, waiting"
    sleep(1)
  if exists(ANDROID_CLASH_ICON):
    print "found clash icon, going to click"
    click(ANDROID_CLASH_ICON)
    print "clicked clash icon, will wait up to 30 seconds for in game icon"
  wait(CLASH_GAME_ICON, 30)
  print "found in game icon"
  print "going to try to zoom out"
  try_resize()
  resources = []
  if exists(CLASH_ELIXER_PATTERN):
    print "elixer and dark exists"
    added = False
    i = 0
    while not added and i < 3:
      try:
        resources += findAll(CLASH_ELIXER_PATTERN)
        added = True
      except:
        print "failed to add elixer finds, retry?", ++i < 3
  if exists(CLASH_COIN_PATTERN):
    print "coin exists"
    added = False
    i = 0
    while not added and i < 3:
      try:
        resources += findAll(CLASH_COIN_PATTERN)
        added = True
      except:
        print "failed to add coin finds, retry?", ++i < 3
  print "starting to click all found resource targets"
  random.shuffle(resources)
  for resource in resources:
      click(resource)
  print "finisheed clicking all resource targets"

  exitable = False
  while not exitable:
    click(GENY_BACK_BUTTON)
    print "clicked GENY_BACK_BUTTON"
    try:
      print "wait for confirm exit"
      wait(CLASH_CONFIRM_BUTTON, 10)
      print "found confirm exit button, going to click"
      exitable = True
    except:
      click(GENY_BACK_BUTTON)

  click(CLASH_CONFIRM_BUTTON)
  print "clicked confirm exit"

def collect_forever():
  i = 0
  while(True):
    print "starting res collection, iter=", i
    try:
      do_res_collection()
      random_sleep_seconds = random.randint(MAX_SLEEP_SECONDS-100, MAX_SLEEP_SECONDS)
      print "finished res collection, sleeping for ", random_sleep_seconds / 60, "min"
      print "next collection will be at", datetime.datetime.now() + datetime.timedelta(seconds=random_sleep_seconds)
      sleep(random_sleep_seconds)
      i += 1
    except:
      print "res collection terminated due to an error, retrying in 1 min"
      sleep(60)

setFindFailedResponse(SKIP)
if exists(CLASH_GAME_ICON) or exists(ANDROID_CLASH_ICON) or exists(CLASH_RELOAD_BUTTON) or exists(CLASH_RELOAD_ANOTHER_DEVICE):
  collect_forever()
# launch genymotion through alfred
keyDown(Key.ALT)
keyDown(Key.SPACE)
keyUp(Key.ALT)
keyUp(Key.SPACE)
type("geny" + Key.ENTER)

# Wait for genymotion to load then start vm
wait(GENY_PLAY_BUTTON, 10)
click(GENY_PLAY_BUTTON)

# Wait for android homescreen

while not exists(ANDROID_LOCK_BUTTON) and not exists(ANDROID_CLASH_ICON):
  sleep(5)
App.focus("player")
screen_locked = exists(ANDROID_LOCK_BUTTON)
if screen_locked:
  dragDrop(ANDROID_LOCK_BUTTON,GENY_BACK_BUTTON)
update_available = exists(GENY_CONTINUE_BUTTON)
if update_available:
  click(GENY_CONTINUE_BUTTON)
collect_forever()

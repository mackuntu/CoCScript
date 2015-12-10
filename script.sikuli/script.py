from sikuli import *
import random
import time
import itertools
import datetime

android_clash_icon = Pattern("1449675544548.png").similar(0.79)
android_lock_button = "1412005436007.png"

clash_game_icon = Pattern("1449765483207.png").similar(0.70)
clash_reload_button = "clash_reload_button.png"
clash_info_button = Pattern("1449651262055.png").similar(0.80)
clash_elixer_pattern = Pattern("1449765631958.png").similar(0.70)
clash_coin_pattern = Pattern("1449765702720.png").similar(0.70)
clash_confirm_button = Pattern("1449675171323.png").similar(0.84)

geny_back_button = Pattern("1412065594056.png").similar(0.67)
geny_play_button = "1412005237101.png"
geny_continue_button = "geny_continue_button.png"

MAX_SLEEP_MINUTES_BETWEEN_COLLECTION = 29
MAX_SLEEP_SECONDS = MAX_SLEEP_MINUTES_BETWEEN_COLLECTION * 60

def try_resize():
  App.focus("player")
  resized = False
  if exists(clash_info_button):
    print "found info target"
    start_point = find(clash_info_button.targetOffset(random.randint(50, 100),random.randint(50, 100)))
    drop_point = start_point.getTarget().offset(random.randint(400, 600),random.randint(2,90))

    keyDown(Key.CMD)
    if dragDrop(start_point, drop_point) == 1:
      resized = True
      keyUp(Key.CMD)
    # move screen down
    dragDrop(start_point, start_point.getTarget().offset(0,200))
  return resized

def do_res_collection():
  App.focus("player")
  if exists(clash_reload_button):
    print "asked to reload"
    click(clash_reload_button)
    print "clicked reload, now sleeping for 10 seconds"
    sleep(10)
  while not exists(android_clash_icon) and not exists(clash_game_icon):
    print "no clash icon and no in game icon, waiting"
    sleep(1)
  if exists(android_clash_icon):
    print "found clash icon, going to click"
    click(android_clash_icon)
    print "clicked clash icon, will wait up to 30 seconds for in game icon"
  wait(clash_game_icon, 30)
  print "found in game icon"
  print "going to try to zoom out"
  while not try_resize():
    print "resize failed, sleep 1 sec and retry"
    sleep(1)
  resources = []
  if exists(clash_elixer_pattern):
    print "elixer and dark exists"
    try:
      resources += findAll(clash_elixer_pattern)
    except:
      print "failed to add elixer finds"
  if exists(clash_coin_pattern):
    print "coin exists"
    try:
      resources += findAll(clash_coin_pattern)
    except:
      print "failed to add coin finds"
  print "starting to click all found resource targets"
  random.shuffle(resources)
  for resource in resources:
      click(resource)
  print "finisheed clicking all resource targets"

  click(geny_back_button)
  print "clicked geny_back_button"
  wait(clash_confirm_button, 10)
  print "wait for confirm exit"

  click(clash_confirm_button)
  print "clicked confirm exit"

def collect_forever():
  i = 0
  while(True):
    print "starting res collection, iter=", i
    do_res_collection()
    random_sleep_seconds = random.randint(60, MAX_SLEEP_SECONDS)
    print "finished res collection, sleeping for ", random_sleep_seconds / 60, "min"
    print "next collection will be at", datetime.datetime.now() + datetime.timedelta(seconds=random_sleep_seconds)
    sleep(random_sleep_seconds)
    i += 1

if exists(clash_game_icon) or exists(android_clash_icon):
  collect_forever()
# launch genymotion through alfred
keyDown(Key.ALT)
keyDown(Key.SPACE)
keyUp(Key.ALT)
keyUp(Key.SPACE)
type("geny" + Key.ENTER)

# Wait for genymotion to load then start vm
wait(geny_play_button, 10)
click(geny_play_button)

# Wait for android homescreen

while not exists(android_lock_button) and not exists(android_clash_icon):
  sleep(5)
App.focus("player")
screen_locked = exists(android_lock_button)
if screen_locked:
  dragDrop(android_lock_button,geny_back_button)
update_available = exists(geny_continue_button)
if update_available:
  click(geny_continue_button)
collect_forever()

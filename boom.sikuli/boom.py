ANDROID_BOOM_ICON = "ANDROID_BOOM_ICON.png"
ANDROID_LOCK_BUTTON = "1412005436007.png"
CLASH_GAME_ICON = "1449765483207.png"
CLASH_RELOAD_BUTTON = "clash_reload_button.png"
CLASH_RELOAD_ANOTHER_DEVICE = "clash_reload_another_device.png"
CLASH_UPGRADE_ICON = "CLASH_UPGRADE_ICON.png"
CLASH_UPGRADE_BUTTON = Pattern("CLASH_UPGRADE_BUTTON.png").similar(0.66)
CLASH_UPGRADE_CONFIRM = "CLASH_UPGRADE_CONFIRM.png"
CLASH_COIN_PATTERN = "CLASH_COIN_PATTERN.png"
CLASH_WOOD_PATTERN = "CLASH_WOOD_PATTERN.png"
CLASH_STONE_PATTERN = "CLASH_STONE_PATTERN.png"
CLASH_IRON_PATTERN = "CLASH_IRON_PATTERN.png"
CLASH_UPGRADE_CANCEL = "CLASH_UPGRADE_CANCEL.png"
CLASH_GRASS = "CLASH_GRASS.png"

GENY_BACK_BUTTON = Pattern("1412065594056.png").similar(0.67)
GENY_PLAY_BUTTON = "1412005237101.png"
GENY_CONTINUE_BUTTON = "geny_continue_button.png"

App.focus("player")
all_upgrades_available = findAll(CLASH_UPGRADE_ICON)
for update in all_upgrades_available:
    update.highlight(3)
    update.click()
    sleep(1)
    try:
        wait(CLASH_UPGRADE_BUTTON, 10)
        click()
        wait(CLASH_UPGRADE_CANCEL, 10)
        click()
        wait(CLASH_GRASS, 10)
        click()
    except:
        print "likely a boat"
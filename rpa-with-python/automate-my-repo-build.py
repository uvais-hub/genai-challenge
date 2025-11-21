import subprocess
import pyautogui
import time
import os

pyautogui.FAILSAFE = True

# ============================
# CONFIGURATION
# ============================

MONO_REPO_PATH = "/Users/mohamed_uvais/CloudFrame/Repositories/cf_cn_platform/"
INTELLIJ_APP = "IntelliJ IDEA CE"
INTELLIJ_PROJECT_PATH = MONO_REPO_PATH

# Image files (assumed to exist)
IMG_INTELLIJ_WINDOW = "intellij_window.png"
IMG_PLAY_BUTTON = "play_button.png"
IMG_STOP_BUTTON = "stop_button.png"

# ============================
# HELPER FUNCTIONS
# ============================

def run_maven_build():
    print("\n🔨 Starting Maven Build...")
    result = subprocess.run(
        ["mvn", "clean", "install"],
        cwd=MONO_REPO_PATH
    )
    if result.returncode == 0:
        print("✅ Maven build successful.")
    else:
        print("❌ Maven build failed.")
        exit(1)


def is_intellij_running():
    """Check if IntelliJ process exists."""
    result = subprocess.run(
        ["pgrep", "-f", INTELLIJ_APP],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return result.returncode == 0


def open_intellij():
    """Open IntelliJ with the monorepo project."""
    print("🚀 Opening IntelliJ...")
    subprocess.Popen(["open", "-a", INTELLIJ_APP, INTELLIJ_PROJECT_PATH])


def wait_for_intellij():
    """Wait until IntelliJ is running and window is detected."""
    print("⏳ Waiting for IntelliJ process...")
    while not is_intellij_running():
        time.sleep(1)
    print("📌 IntelliJ process detected.")

    print("⏳ Waiting for IntelliJ window image...")
    button = None
    while button is None:
        button = pyautogui.locateOnScreen(IMG_INTELLIJ_WINDOW, confidence=0.7)
        time.sleep(1)
    print("🟢 IntelliJ window found on screen.")
    time.sleep(2)  # give one more second to stabilize


def ensure_intellij_open():
    """Ensure IntelliJ is open with our monorepo."""
    if not is_intellij_running():
        print("🔴 IntelliJ not running.")
        open_intellij()
        wait_for_intellij()
        return

    print("🟢 IntelliJ already running. Ensuring window is active...")

    # Bring IntelliJ to front
    subprocess.Popen(["open", "-a", INTELLIJ_APP])
    time.sleep(2)

    # Verify window image is visible
    if not pyautogui.locateOnScreen(IMG_INTELLIJ_WINDOW, confidence=0.7):
        print("🔄 IntelliJ window not detected; reopening project...")
        open_intellij()
        wait_for_intellij()
    else:
        print("📌 IntelliJ window detected.")


def click_image(image_file, description, confidence=0.8, retries=20):
    """Click on an image on the screen."""
    print(f"🔎 Searching for {description}...")
    for i in range(retries):
        location = pyautogui.locateCenterOnScreen(image_file, confidence=confidence)
        if location:
            print(f"🟢 Found {description} at {location}. Clicking...")
            pyautogui.click(location)
            time.sleep(1)
            return True
        time.sleep(0.5)
    print(f"❌ Failed to find {description}.")
    return False


def run_compound_configuration_runs(times=3):
    """Run (start → stop → start) compound config multiple times."""
    for i in range(times):
        print(f"\n▶️ Starting compound configuration (Run #{i+1})")

        # Click PLAY
        if not click_image(IMG_PLAY_BUTTON, "PLAY button"):
            print("❌ Cannot start services; PLAY button not found.")
            return

        print("⏳ Waiting 5 seconds before stopping...")
        time.sleep(5)

        print("⏹ Stopping run...")
        if not click_image(IMG_STOP_BUTTON, "STOP button"):
            print("⚠️ Stop button not found. Skipping stop.")
            continue

        time.sleep(3)


# ============================
# MAIN EXECUTION
# ============================

def main():
    print("\n🚀 Starting Full Automation...\n")

    # 1. Maven build
    run_maven_build()

    # 2. Ensure IntelliJ open
    #ensure_intellij_open()

    # 3. Run compound configuration multiple times
    #run_compound_configuration_runs(times=3)

    print("\n🎉 All steps completed.\n")


if __name__ == "__main__":
    main()
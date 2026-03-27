import os
from datetime import datetime

def take_screenshot(driver, test_name):
    folder = "screenshots"

    # create folder if not exists
    if not os.path.exists(folder):
        os.makedirs(folder)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{test_name}_{timestamp}.png"
    file_path = os.path.join(folder, file_name)

    driver.save_screenshot(file_path)
    return file_path
# Documentation: automate-my-repo-build.py

## Overview
This script automates the setup and build process for your development environment. It is designed to streamline repetitive tasks, such as building your monorepo and starting multiple services, so you can focus on development.

## Features
- **Maven Build**: Cleans and builds the monorepo using Maven.
- **IntelliJ Automation**: Ensures IntelliJ IDEA is running and the project window is active using image recognition.
- **Service Startup**: Sequentially starts up to 10 services (customize the commands in `SERVICE_COMMANDS`).
- **UI Automation**: Uses PyAutoGUI to interact with IntelliJ's UI elements if needed.

## Usage
1. **Configure Paths**
   - Update `MONO_REPO_PATH` to your monorepo location.
   - Update `INTELLIJ_APP` and image file paths if needed.
2. **Service Commands**
   - Edit the `SERVICE_COMMANDS` list in the `start_services()` function to match your actual service start commands.
3. **Run the Script**
   - Execute the script from the command line:
     ```bash
     python automate-my-repo-build.py
     ```

## Extending the Script
- Add health checks after starting each service.
- Implement parallel service startup for faster execution.
- Move configuration to a separate file for easier management.
- Add logging and notifications for better monitoring.

## Dependencies
- Python 3.x
- `pyautogui` (for UI automation)
- Maven (for build)

## Troubleshooting
- Ensure all image files for UI automation exist and are up-to-date.
- Check that all service start scripts are executable and paths are correct.
- Review error messages in the terminal for failed steps.

## Related Files
- `automate-my-repo-build-enhancement.md`: Suggestions for future improvements and enhancements.

---
*Last updated: November 16, 2025*

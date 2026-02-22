import time
from playwright.sync_api import sync_playwright, expect

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(viewport={'width': 1280, 'height': 800})
    page = context.new_page()

    # 1. Load the app
    print("Loading app...")
    page.goto("http://localhost:8000")

    # Wait for the app to load (checking for sidebar)
    page.wait_for_selector("text=Widgets")
    print("App loaded.")

    # 2. Add a Label widget to the canvas
    # Find "Label" in the sidebar. It's inside a div with text "Label"
    # We can simulate a click on it to select it, but the app adds widgets via drag and drop OR maybe just clicking?
    # Looking at Sidebar.js: onClick={(e) => onSelect(el.id, e.shiftKey)} but that's for the tree tab.
    # The widgets tab has draggable items.
    # Canvas.js handles onDrop.

    # Let's try to drag and drop.
    label_source = page.locator("div.widget-card:has-text('Label')").first
    canvas_target = page.locator("div.relative.shadow-2xl").first

    print("Dragging Label to Canvas...")
    label_source.drag_to(canvas_target, target_position={"x": 100, "y": 100})

    # Check if a label appeared on the canvas.
    # The widget on canvas is rendered inside an absolute div.
    # We can look for text "Label" inside the canvas.
    # The canvas has id or ref? No, but it's the .shadow-2xl element.
    # The label text is "Label" by default.

    label_on_canvas = canvas_target.locator("text=Label").first
    expect(label_on_canvas).to_be_visible()
    print("Label added to canvas.")

    # 3. Check Background Color for Midnight Theme (Default)
    # The label is a div. We need its computed style.
    # The widget renderer wraps it in a div.
    # Wait for a moment for styles to apply/render
    time.sleep(1)

    bg_color_midnight = label_on_canvas.evaluate("el => getComputedStyle(el).backgroundColor")
    print(f"Midnight Theme Label Background: {bg_color_midnight}")

    # Expected: rgb(45, 61, 77) which is #2d3d4d
    # Note: getComputedStyle returns rgb(...)

    if "rgb(45, 61, 77)" in bg_color_midnight:
        print("SUCCESS: Midnight theme background is correct.")
    else:
        print(f"WARNING: Midnight theme background might be incorrect. Expected rgb(45, 61, 77), got {bg_color_midnight}")

    # 4. Switch to Classic Theme
    # First deselect the widget by clicking on the canvas background
    # (to show global/theme settings in properties panel)
    # Click at 0,0 relative to canvas top-left which should be empty space
    canvas_target.click(position={"x": 10, "y": 10})

    # Now look for "Classic" button in Properties Panel
    # PropertiesPanel renders buttons with theme names.
    classic_btn = page.locator("button:has-text('Classic')")
    classic_btn.click()
    print("Switched to Classic theme.")

    time.sleep(1)

    # 5. Check Background Color for Classic Theme
    bg_color_classic = label_on_canvas.evaluate("el => getComputedStyle(el).backgroundColor")
    print(f"Classic Theme Label Background: {bg_color_classic}")

    # Expected: rgb(255, 255, 255) which is #ffffff
    if "rgb(255, 255, 255)" in bg_color_classic:
        print("SUCCESS: Classic theme background is correct.")
    else:
        print(f"WARNING: Classic theme background might be incorrect. Expected rgb(255, 255, 255), got {bg_color_classic}")

    # 6. Take Screenshot
    screenshot_path = "/home/jules/verification/verification.png"
    page.screenshot(path=screenshot_path)
    print(f"Screenshot saved to {screenshot_path}")

    browser.close()

if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)

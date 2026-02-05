"""
Screenshot capture utilities for test reporting.
"""

import os
from datetime import datetime
from PIL import Image
import io

from .logger import get_logger

logger = get_logger(__name__)


def capture_screenshot(driver, filename=None, full_page=False):
    """
    Capture screenshot and save to reports directory.
    
    Args:
        driver: WebDriver instance
        filename (str): Custom filename, auto-generated if None
        full_page (bool): Whether to capture full page screenshot
        
    Returns:
        str: Path to saved screenshot
    """
    # Create screenshots directory
    screenshots_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 
        "reports", 
        "screenshots"
    )
    os.makedirs(screenshots_dir, exist_ok=True)
    
    # Generate filename if not provided
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
        filename = f"screenshot_{timestamp}.png"
    
    # Ensure .png extension
    if not filename.endswith('.png'):
        filename += '.png'
    
    filepath = os.path.join(screenshots_dir, filename)
    
    try:
        if full_page:
            # Capture full page screenshot
            screenshot_data = capture_full_page_screenshot(driver)
            with open(filepath, 'wb') as f:
                f.write(screenshot_data)
        else:
            # Regular screenshot
            driver.save_screenshot(filepath)
        
        logger.info(f"Screenshot saved: {filepath}")
        return filepath
        
    except Exception as e:
        logger.error(f"Failed to capture screenshot: {str(e)}")
        raise


def capture_full_page_screenshot(driver):
    """
    Capture full page screenshot by scrolling.
    
    Args:
        driver: WebDriver instance
        
    Returns:
        bytes: Screenshot data
    """
    # Get page dimensions
    total_height = driver.execute_script("return document.body.scrollHeight")
    viewport_height = driver.execute_script("return window.innerHeight")
    viewport_width = driver.execute_script("return window.innerWidth")
    
    # If page fits in viewport, take regular screenshot
    if total_height <= viewport_height:
        return driver.get_screenshot_as_png()
    
    # Calculate number of screenshots needed
    screenshots = []
    scroll_position = 0
    
    while scroll_position < total_height:
        # Scroll to position
        driver.execute_script(f"window.scrollTo(0, {scroll_position})")
        
        # Wait for scroll to complete
        driver.implicitly_wait(0.5)
        
        # Take screenshot
        screenshot = driver.get_screenshot_as_png()
        screenshots.append(Image.open(io.BytesIO(screenshot)))
        
        scroll_position += viewport_height
    
    # Stitch screenshots together
    if len(screenshots) == 1:
        # Only one screenshot needed
        output = io.BytesIO()
        screenshots[0].save(output, format='PNG')
        return output.getvalue()
    
    # Create combined image
    combined_height = sum(img.height for img in screenshots)
    combined_image = Image.new('RGB', (viewport_width, combined_height))
    
    y_offset = 0
    for img in screenshots:
        combined_image.paste(img, (0, y_offset))
        y_offset += img.height
    
    # Convert to bytes
    output = io.BytesIO()
    combined_image.save(output, format='PNG')
    return output.getvalue()


def capture_element_screenshot(driver, element, filename=None):
    """
    Capture screenshot of specific element.
    
    Args:
        driver: WebDriver instance
        element: WebElement to capture
        filename (str): Custom filename, auto-generated if None
        
    Returns:
        str: Path to saved screenshot
    """
    # Create screenshots directory
    screenshots_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 
        "reports", 
        "screenshots"
    )
    os.makedirs(screenshots_dir, exist_ok=True)
    
    # Generate filename if not provided
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
        filename = f"element_screenshot_{timestamp}.png"
    
    # Ensure .png extension
    if not filename.endswith('.png'):
        filename += '.png'
    
    filepath = os.path.join(screenshots_dir, filename)
    
    try:
        # Scroll element into view
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        
        # Capture element screenshot
        element.screenshot(filepath)
        
        logger.info(f"Element screenshot saved: {filepath}")
        return filepath
        
    except Exception as e:
        logger.error(f"Failed to capture element screenshot: {str(e)}")
        raise


def attach_screenshot_to_allure(driver, name="Screenshot"):
    """
    Attach screenshot to Allure report.
    
    Args:
        driver: WebDriver instance
        name (str): Screenshot name in report
    """
    try:
        import allure
        screenshot_data = driver.get_screenshot_as_png()
        allure.attach(
            screenshot_data,
            name=name,
            attachment_type=allure.attachment_type.PNG
        )
        logger.debug(f"Screenshot attached to Allure: {name}")
    except ImportError:
        logger.warning("Allure not available, skipping screenshot attachment")
    except Exception as e:
        logger.error(f"Failed to attach screenshot to Allure: {str(e)}")
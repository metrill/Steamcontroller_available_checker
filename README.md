# Steam Hardware Stock Checker

A Python-based automation tool designed to monitor the availability of the Steam Controller (or other hardware) on the official Steam Store.

#### Overview

This script performs a periodic check (every 60 seconds) on a specific Steam Store page. Since Steam uses dynamic content to display stock status, this tool utilizes **Playwright** to render JavaScript and accurately detect the presence of stock-related HTML elements.

#### Installation & Usage

1. Clone the repository and install the dependencies:

   Bash

   ```
   pip install playwright
   python -m playwright install chromium
   ```

2. Run the script:

Bash

```
   python steamcontroller_check.py
```

#### Technical Details

The script simulates a real browser session by setting a custom `User-Agent` and waiting for `networkidle` states. This bypasses common issues where simple HTTP requests (like `requests`) fail to see the updated stock status due to missing client-side rendering.

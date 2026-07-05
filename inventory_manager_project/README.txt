Inventory manager - PySide6 desktop app.

Run with:
    pip install PySide6 reportlab openpyxl
    python main.py

SETUP:
    Place your toolow.mp3 sound file in the project root directory (same folder
    as main.py). The app will play this sound automatically when you view results
    containing low-stock items.

Flow:
    1. App opens on the Search screen (widgets/search_page.py) - a
       browser-homepage-style search bar plus Origin / Brand / Stock-status
       filter dropdowns.
    2. Hitting Search (or Enter) takes you to the Results screen
       (widgets/results_page.py) - the dashboard stat tiles + item card grid,
       now scoped to whatever you searched/filtered for.
       * If any low-stock items are shown, toolow.mp3 plays automatically
    3. From Results you can:
         - "← New Search" to go back and change filters
         - "Reset Filters" to clear them without leaving the page
         - type in the inline box to refine further within the current filter
         - "Quick Summary" for a compact popup list, e.g. "3x Bus AC / 4x Compressor",
           reflecting whatever's currently filtered/visible
         - Add / Sell / Edit / Delete items:
             * When adding/editing an item, use "Pick Photo" to upload an image
               (PNG, JPG, BMP, GIF - any size)
             * Photos are stored in a photos/ folder and indexed in the database
             * Each card with a photo gets a "View Image" button that opens a
               popup viewer displaying the full image scaled to fit (never goes out of bounds)
             * "Remove Photo" button in the edit dialog to delete a photo
         - Sales Log:
             - View full sales history in a table (sorted by date, newest first)
             - "Export as PDF" - saves a formatted PDF report
             - "Export as Excel" - saves an .xlsx file with headers and styling
             - Customer column is at the far right

Stock Levels:
    The app categorizes items into three stock status buckets:
      • Out of Stock: amount = 0
      • Low Stock: 0 < amount < minimum_amount
      • In Stock: amount >= minimum_amount
    
    Filter options on the search screen:
      • All Stock Levels: show all items
      • Low Stock: show only low-stock items
      • Out of Stock: show only out-of-stock items
      • In Stock: show only in-stock items (excludes both low and out-of-stock)
    
    Stat tiles on the results page show:
      • Total Items: count of all filtered items
      • Low Stock: count of items in the "low" category
      • Out of Stock: count of items in the "out" category
      • In Stock: count of items in the "in" category
    
    Audio Alerts:
      • When viewing results that contain any low-stock items, toolow.mp3 plays
        automatically to alert you to potential stock issues.

Structure:
    main.py                  - app entry point; hosts a QStackedWidget
                                switching between SearchPage and ResultsPage
    database.py              - DBM class; items() filters by origin/brand/
                                stock_status (Out/Low/In), plus origins()/brands()
                                for populating the dropdowns
    audio_player.py          - AudioPlayer singleton for playing toolow.mp3
    styles.py                - global stylesheet
    dialogs/
        item_dialog.py        - Add/Edit item form with photo picker
        sell_dialog.py        - Sell item form (qty capped at current stock)
        sales_log.py          - Read-only sales table + PDF/Excel export
        summary_dialog.py     - "Quick Summary" popup list
    widgets/
        search_page.py        - Landing screen: search bar + filters (4 stock options)
        results_page.py       - Stat tiles + item grid + actions (4 stat tiles,
                                auto-plays audio alert for low stock)
        item_card.py          - ItemCard: product tile with "View Image" button
        stat_card.py          - StatCard: dashboard tile

Data storage:
    inventory.db             - SQLite database (auto-created on first run)
    photos/                  - Directory containing item photos (auto-created)
    toolow.mp3               - Sound file (user-provided, optional)

Dependencies:
    - PySide6: the Qt GUI framework
    - reportlab: PDF generation (for Sales Log export)
    - openpyxl: Excel file generation (for Sales Log export)

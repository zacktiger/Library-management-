# Library Management System - Modern GUI

A sleek, modern Tkinter-based GUI for managing library inventory (books and journals). This is a Python implementation with a beautiful dark-themed interface that mirrors the functionality of the original C++ library management system.

## Features

✨ **Modern Dark Theme UI** - Professional look with purple accent colors
📚 **Dual Item Types** - Manage both Books and Journals
🔍 **Fast Search** - Search items by title
📊 **Live Statistics** - Real-time inventory stats in the header
💾 **Persistent Storage** - Data saved automatically in JSON format
🔄 **Borrow/Return** - Toggle item availability status
➕ **Easy Adding** - Intuitive forms for adding new items
🗑️ **Safe Deletion** - Remove items with confirmation dialog

## Requirements

- Python 3.6 or higher
- tkinter (usually comes pre-installed with Python)

## Installation

1. Make sure Python is installed:
```bash
python --version
```

2. tkinter should be included, but if not:
   - **Ubuntu/Debian**: `sudo apt-get install python3-tk`
   - **Fedora**: `sudo dnf install python3-tkinter`
   - **macOS**: Should be included with Python
   - **Windows**: Should be included with Python

## Running the Application

Simply run:
```bash
python library_gui.py
```

Or on some systems:
```bash
python3 library_gui.py
```

## Usage Guide

### Main Interface

The application has two main sections:
- **Left Sidebar**: Navigation menu with all main features
- **Right Panel**: Dynamic content area that changes based on selected feature
- **Top Header**: Shows app title and live statistics

### Features

#### 1. View All Items
- Click "📖 View All Items" to see the complete inventory
- Table shows: ID, Type, Title, Author/Publisher, and Status
- Color-coded status (green = available, orange = borrowed)

#### 2. Add Book
- Click "➕ Add Book"
- Fill in: ID, Title, Author, Pages
- Click "Add Book" to save

#### 3. Add Journal
- Click "➕ Add Journal"
- Fill in: ID, Title, Publisher, Volume
- Click "Add Journal" to save

#### 4. Search Items
- Click "🔍 Search Items"
- Enter a search keyword (searches in titles)
- Click "Search" to see results

#### 5. Borrow/Return Item
- Click "🔄 Borrow/Return"
- Enter the item ID
- Click "Toggle Status" to change between borrowed/available

#### 6. Remove Item
- Click "🗑️ Remove Item"
- Enter the item ID
- Confirm deletion in the popup dialog

## Data Storage

- All data is automatically saved to `library_data.json`
- Data persists between application sessions
- The file is created in the same directory as the script

## Design Features

### Color Scheme
- **Background**: Dark theme (#1e1e2e)
- **Accent**: Purple (#7c3aed)
- **Success**: Green (#10b981)
- **Warning**: Orange (#f59e0b)
- **Danger**: Red (#ef4444)

### Custom Components
- **ModernButton**: Hover effects and rounded appearance
- **ModernEntry**: Styled input fields with placeholder support
- **Custom Treeview**: Dark-themed table with color-coded rows

## Code Structure

The application follows OOP principles similar to the C++ version:

```
LibraryItem (Abstract Base Class)
├── Book
└── Journal

LibraryManager (Backend Logic)
├── CRUD operations
├── Search functionality
└── File I/O (JSON)

LibraryGUI (Frontend)
├── Header with stats
├── Sidebar navigation
└── Dynamic main content area
```

## Comparison with C++ Version

| Feature | C++ Version | Python GUI Version |
|---------|-------------|-------------------|
| Interface | Console/Terminal | Modern Tkinter GUI |
| Data Storage | CSV (library_data.txt) | JSON (library_data.json) |
| OOP Design | ✅ Same structure | ✅ Same structure |
| Polymorphism | ✅ Virtual functions | ✅ Abstract classes |
| Smart Pointers | unique_ptr | Native Python references |
| Collections | std::map | dict (hash table) |

## Screenshots Description

- **Main View**: Dark purple header with live stats, sidebar navigation, table view
- **Add Forms**: Clean input forms with labeled fields
- **Search**: Real-time search results in styled cards
- **Table View**: Professional table with alternating row colors

## Tips

1. **IDs must be unique** - The system will warn if you try to add a duplicate ID
2. **Data saves automatically** - No need to manually save
3. **Search is case-insensitive** - "python" will match "Python Programming"
4. **Hover over buttons** - Buttons change color when you hover over them
5. **Statistics update live** - Watch the header stats change as you add/remove items

## Troubleshooting

**Issue**: "ModuleNotFoundError: No module named 'tkinter'"
- **Solution**: Install tkinter using the platform-specific commands above

**Issue**: Window appears too small or cut off
- **Solution**: The window is set to 1200x700. You can resize it manually or change the geometry in the code

**Issue**: Data not persisting
- **Solution**: Make sure the script has write permissions in its directory

## Future Enhancements

Potential features to add:
- Due dates for borrowed items
- Member management
- Advanced filters (by author, publisher, status)
- Export to PDF/Excel
- Print functionality
- Multiple themes (light/dark toggle)
- Search with autocomplete

## License

Free to use and modify for educational purposes.

## Credits

Based on the Advanced Library Management System C++ implementation.
GUI created with Python's tkinter library.

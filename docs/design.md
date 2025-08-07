# Expense Tracker Design Documentation

## Architecture Overview
- **MVC Pattern**
  - Model: TXT file operations
  - View: Tkinter GUI
  - Controller: gui_app.py

## Color Scheme
| Color       | Hex       | Usage               |
|-------------|-----------|---------------------|
| Primary     | `#6366F1` | Main buttons, headers|
| Secondary   | `#8B5CF6` | Secondary elements  |
| Accent      | `#EC4899` | Interactive elements|
| Success     | `#10B981` | Positive actions    |
| Warning     | `#F59E0B` | Warnings            |

## Data Flow
1. User input → Controller → Model (TXT)
2. Model → Controller → View update

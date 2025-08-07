# Function Reference

## Core Functions
### `add_expense(date, category, amount, description)`
- Parameters:
  - date: str (YYYY-MM-DD)
  - category: str (Food|Transportation|Entertainment|Other)
  - amount: float
  - description: str

### `generate_report()`
- Returns: str (formatted report text)

## File Operations
### `read_expenses()`
- Returns: List[Dict]

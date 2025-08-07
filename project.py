import turtle
import datetime
import os

# Global constants
EXPENSES_FILE = "expenses.txt"
BUDGET_FILE = "budget.txt"

# Function to validate date format
def validate_date(date_str):
    """Validate date format (YYYY-MM-DD)"""
    try:
        datetime.datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

# Function to validate amount
def validate_amount(amount_str):
    """Validate amount is a positive number"""
    try:
        amount = float(amount_str)
        return amount > 0
    except ValueError:
        return False

# Function to read expenses from file
def read_expenses():
    """Read expenses from file and return as list"""
    expenses = []
    try:
        with open(EXPENSES_FILE, "r") as file:
            for line in file:
                line = line.strip()
                if line:  # Skip empty lines
                    parts = line.split("\t")
                    if len(parts) >= 4:
                        expenses.append({
                            'date': parts[0],
                            'category': parts[1],
                            'amount': float(parts[2]),
                            'description': parts[3]
                        })
    except FileNotFoundError:
        print(f"Warning: {EXPENSES_FILE} not found. Creating new file.")
        with open(EXPENSES_FILE, "w") as file:
            file.write("")
    return expenses

# Function to write expenses to file
def write_expenses(expenses):
    """Write expenses list to file"""
    try:
        with open(EXPENSES_FILE, "w") as file:
            for expense in expenses:
                file.write(f"{expense['date']}\t{expense['category']}\t{expense['amount']}\t{expense['description']}\n")
        return True
    except Exception as e:
        print(f"Error writing to file: {e}")
        return False

# Function to read budget from file
def read_budget():
    """Read budget from file and return as dictionary"""
    budget = {}
    try:
        with open(BUDGET_FILE, "r") as file:
            for line in file:
                line = line.strip()
                if line and ':' in line:
                    category, amount = line.split(':')
                    budget[category.strip()] = float(amount.strip())
    except FileNotFoundError:
        print(f"Warning: {BUDGET_FILE} not found. Creating default budget.")
        budget = {
            'Food': 1000.0,
            'Transportation': 500.0,
            'Entertainment': 300.0
        }
        write_budget(budget)
    return budget

# Function to write budget to file
def write_budget(budget):
    """Write budget dictionary to file"""
    try:
        with open(BUDGET_FILE, "w") as file:
            for category, amount in budget.items():
                file.write(f"{category}:{amount}\n")
        return True
    except Exception as e:
        print(f"Error writing budget: {e}")
        return False

# Add expense function with validation
def add_expense():
    """Add a new expense with validation"""
    print("\n=== ADD NEW EXPENSE ===")
    
    # Get and validate date
    while True:
        date = input("Enter the date (YYYY-MM-DD): ").strip()
        if validate_date(date):
            break
        print("Invalid date format! Please use YYYY-MM-DD")
    
    # Get expense type
    print("\nAvailable categories:")
    print("1. Food")
    print("2. Transportation") 
    print("3. Entertainment")
    print("4. Other")
    
    while True:
        choice = input("Select category (1-4): ").strip()
        category_map = {"1": "Food", "2": "Transportation", "3": "Entertainment", "4": "Other"}
        if choice in category_map:
            expense_type = category_map[choice]
            break
        print("Invalid choice! Please select 1-4")
    
    # Get and validate amount
    while True:
        expense_amount = input("Enter the expense amount: ").strip()
        if validate_amount(expense_amount):
            expense_amount = float(expense_amount)
            break
        print("Invalid amount! Please enter a positive number")
    
    # Get description
    description = input("Enter the description: ").strip()
    if not description:
        description = "No description"
    
    # Create expense record
    new_expense = {
        'date': date,
        'category': expense_type,
        'amount': expense_amount,
        'description': description
    }
    
    # Read existing expenses and add new one
    expenses = read_expenses()
    expenses.append(new_expense)
    
    # Write back to file
    if write_expenses(expenses):
        print(f"\n✅ Expense added successfully!")
        print(f"Date: {date}")
        print(f"Category: {expense_type}")
        print(f"Amount: ${expense_amount:.2f}")
        print(f"Description: {description}")
    else:
        print("❌ Error adding expense!")

# Function to categorize and display expenses
def categorize_and_display_expenses():
    """Display expenses grouped by category with totals"""
    expenses = read_expenses()
    
    if not expenses:
        print("No expenses found!")
        return
    
    categories = {}
    total_spent = 0
    
    # Group expenses by category
    for expense in expenses:
        category = expense['category']
        if category not in categories:
            categories[category] = []
        categories[category].append(expense)
        total_spent += expense['amount']
    
    print("\n=== EXPENSES BY CATEGORY ===")
    print("=" * 50)
    
    for category, category_expenses in categories.items():
        category_total = sum(exp['amount'] for exp in category_expenses)
        print(f"\n📊 {category.upper()} - Total: ${category_total:.2f}")
        print("-" * 30)
        
        for expense in category_expenses:
            print(f"  {expense['date']} | ${expense['amount']:.2f} | {expense['description']}")
    
    print("\n" + "=" * 50)
    print(f"💰 TOTAL SPENT: ${total_spent:.2f}")
    
    # Budget comparison
    budget = read_budget()
    print("\n=== BUDGET ANALYSIS ===")
    for category, budget_amount in budget.items():
        category_spent = sum(exp['amount'] for exp in expenses if exp['category'] == category)
        remaining = budget_amount - category_spent
        status = "✅" if remaining >= 0 else "❌"
        print(f"{status} {category}: ${category_spent:.2f} / ${budget_amount:.2f} (Remaining: ${remaining:.2f})")

# Function to view all expenses
def view_expenses():
    """Display all expenses in chronological order"""
    expenses = read_expenses()
    
    if not expenses:
        print("No expenses found!")
        return
    
    # Sort by date
    expenses.sort(key=lambda x: x['date'])
    
    print("\n=== ALL EXPENSES (Chronological) ===")
    print("=" * 60)
    print(f"{'Date':<12} {'Category':<15} {'Amount':<10} {'Description'}")
    print("-" * 60)
    
    total = 0
    for expense in expenses:
        print(f"{expense['date']:<12} {expense['category']:<15} ${expense['amount']:<9.2f} {expense['description']}")
        total += expense['amount']
    
    print("-" * 60)
    print(f"{'TOTAL':<27} ${total:<9.2f}")

# Function to search for expenses
def search_expenses():
    """Search expenses by keyword"""
    keyword = input("Enter the keyword to search for: ").strip().lower()
    
    if not keyword:
        print("Please enter a keyword!")
        return
    
    expenses = read_expenses()
    found_expenses = []
    
    for expense in expenses:
        if (keyword in expense['date'].lower() or 
            keyword in expense['category'].lower() or 
            keyword in expense['description'].lower()):
            found_expenses.append(expense)
    
    if not found_expenses:
        print(f"No expenses found containing '{keyword}'")
        return
    
    print(f"\n=== SEARCH RESULTS FOR '{keyword.upper()}' ===")
    print("=" * 60)
    print(f"{'Date':<12} {'Category':<15} {'Amount':<10} {'Description'}")
    print("-" * 60)
    
    total = 0
    for expense in found_expenses:
        print(f"{expense['date']:<12} {expense['category']:<15} ${expense['amount']:<9.2f} {expense['description']}")
        total += expense['amount']
    
    print("-" * 60)
    print(f"{'TOTAL':<27} ${total:<9.2f}")

# Function to read budget data
def read_budget_file():
    """Read budget data from file"""
    return read_budget()

# Function to draw enhanced bar chart using Turtle
def draw_bar_chart(budget):
    """Draw an enhanced bar chart using Turtle graphics"""
    if not budget:
        print("No budget data available!")
        return
    
    # Setup turtle
    pen = turtle.Turtle()
    screen = turtle.Screen()
    screen.title("Budget Analysis Chart")
    screen.bgcolor("white")
    pen.speed(0)
    
    # Calculate dimensions
    max_amount = max(budget.values())
    bar_width = 60
    bar_spacing = 80
    scale_factor = 200 / max_amount  # Scale to fit in window
    
    # Draw title
    pen.penup()
    pen.goto(0, 250)
    pen.color("black")
    pen.write("BUDGET ANALYSIS", align="center", font=("Arial", 16, "bold"))
    
    # Draw axes
    pen.penup()
    pen.goto(-300, -200)
    pen.pendown()
    pen.goto(300, -200)  # X-axis
    pen.goto(300, 200)   # Y-axis
    pen.goto(-300, 200)  # Top line
    pen.goto(-300, -200) # Left line
    
    # Draw Y-axis labels
    pen.penup()
    for i in range(6):
        y = -200 + (i * 80)
        pen.goto(-320, y)
        pen.write(f"${(max_amount * i / 5):.0f}", align="right", font=("Arial", 8))
    
    # Draw bars
    x_start = -250
    colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7"]
    
    for i, (category, amount) in enumerate(budget.items()):
        # Draw bar
        bar_height = amount * scale_factor
        x = x_start + (i * bar_spacing)
        
        pen.penup()
        pen.goto(x, -200)
        pen.pendown()
        pen.fillcolor(colors[i % len(colors)])
        pen.begin_fill()
        
        for _ in range(2):
            pen.forward(bar_width)
            pen.left(90)
            pen.forward(bar_height)
            pen.left(90)
        pen.end_fill()
        
        # Write category name
        pen.penup()
        pen.goto(x + bar_width/2, -220)
        pen.color("black")
        pen.write(category, align="center", font=("Arial", 10, "bold"))
        
        # Write amount on top of bar
        pen.goto(x + bar_width/2, -200 + bar_height + 10)
        pen.write(f"${amount:.0f}", align="center", font=("Arial", 8))
    
    # Hide turtle and keep screen open
    pen.hideturtle()
    screen.mainloop()

# Function to edit budgets
def edit_budgets():
    """Edit budget amounts for different categories"""
    budget = read_budget()
    
    print("\n=== EDIT BUDGETS ===")
    print("Current budgets:")
    for category, amount in budget.items():
        print(f"  {category}: ${amount:.2f}")
    
    print("\nSelect category to edit:")
    categories = list(budget.keys())
    for i, category in enumerate(categories, 1):
        print(f"{i}. {category}")
    
    while True:
        try:
            choice = int(input(f"\nEnter choice (1-{len(categories)}): "))
            if 1 <= choice <= len(categories):
                selected_category = categories[choice - 1]
                break
            else:
                print("Invalid choice!")
        except ValueError:
            print("Please enter a number!")
    
    print(f"\nCurrent budget for {selected_category}: ${budget[selected_category]:.2f}")
    
    while True:
        try:
            new_amount = float(input(f"Enter new budget for {selected_category}: $"))
            if new_amount >= 0:
                budget[selected_category] = new_amount
                break
            else:
                print("Budget cannot be negative!")
        except ValueError:
            print("Please enter a valid number!")
    
    if write_budget(budget):
        print(f"✅ Budget updated! New {selected_category} budget: ${new_amount:.2f}")
    else:
        print("❌ Error updating budget!")

# Function to generate expense report
def generate_report():
    """Generate a comprehensive expense report"""
    expenses = read_expenses()
    budget = read_budget()
    
    if not expenses:
        print("No expenses to report!")
        return
    
    print("\n" + "=" * 60)
    print("📊 EXPENSE REPORT")
    print("=" * 60)
    
    # Calculate totals by category
    category_totals = {}
    total_spent = 0
    
    for expense in expenses:
        category = expense['category']
        if category not in category_totals:
            category_totals[category] = 0
        category_totals[category] += expense['amount']
        total_spent += expense['amount']
    
    # Display category analysis
    print("\n💰 CATEGORY ANALYSIS:")
    print("-" * 40)
    
    for category, spent in category_totals.items():
        budget_amount = budget.get(category, 0)
        remaining = budget_amount - spent
        percentage = (spent / budget_amount * 100) if budget_amount > 0 else 0
        
        status = "✅" if remaining >= 0 else "❌"
        print(f"{status} {category}:")
        print(f"    Spent: ${spent:.2f}")
        print(f"    Budget: ${budget_amount:.2f}")
        print(f"    Remaining: ${remaining:.2f}")
        print(f"    Usage: {percentage:.1f}%")
        print()
    
    # Overall summary
    total_budget = sum(budget.values())
    overall_remaining = total_budget - total_spent
    overall_percentage = (total_spent / total_budget * 100) if total_budget > 0 else 0
    
    print("📈 OVERALL SUMMARY:")
    print("-" * 40)
    print(f"Total Spent: ${total_spent:.2f}")
    print(f"Total Budget: ${total_budget:.2f}")
    print(f"Remaining: ${overall_remaining:.2f}")
    print(f"Usage: {overall_percentage:.1f}%")
    
    if overall_remaining < 0:
        print("⚠️  WARNING: You have exceeded your total budget!")
    
    print("=" * 60)

# Main menu function
def main():
    """Main menu and program loop"""
    while True:
        print("\n" + "=" * 50)
        print("💰 PERSONAL EXPENSE TRACKER")
        print("=" * 50)
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Create Expense Graph")
        print("4. Edit Budgets")
        print("5. Search Expenses")
        print("6. Generate Report")
        print("7. Exit")
        print("-" * 50)
        
        choice = input("Choose an option (1-7): ").strip()
        
        if choice == "1":
            add_expense()
        elif choice == "2":
            print("\nView options:")
            print("a) All expenses (chronological)")
            print("b) Grouped by category")
            sub_choice = input("Choose (a/b): ").strip().lower()
            if sub_choice == "a":
                view_expenses()
            elif sub_choice == "b":
                categorize_and_display_expenses()
            else:
                print("Invalid choice!")
        elif choice == "3":
            budget = read_budget_file()
            if budget:
                print("Opening Turtle graphics window...")
                draw_bar_chart(budget)
            else:
                print("No budget data available!")
        elif choice == "4":
            edit_budgets()
        elif choice == "5":
            search_expenses()
        elif choice == "6":
            generate_report()
        elif choice == "7":
            print("\n👋 Thank you for using Personal Expense Tracker!")
            print("Goodbye!")
            break
        else:
            print("Invalid choice! Please select 1-7")
        
        input("\nPress Enter to continue...")

# Start the program
if __name__ == "__main__":
    main()

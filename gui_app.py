import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import turtle
import os
from tkinter import scrolledtext

# Color scheme - Elegant and modern
COLORS = {
    'primary': '#6366F1',      # Indigo
    'secondary': '#8B5CF6',    # Purple
    'accent': '#EC4899',       # Pink
    'success': '#10B981',      # Emerald
    'warning': '#F59E0B',      # Amber
    'danger': '#EF4444',       # Red
    'light': '#F8FAFC',        # Slate 50
    'white': '#FFFFFF',        # White
    'gray': '#64748B',         # Slate 500
    'dark': '#1E293B'          # Slate 800
}

class ExpenseTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("💰 Personal Expense Tracker")
        self.root.geometry("1200x800")
        self.root.configure(bg=COLORS['light'])
        
        # Data
        self.expenses = []
        self.budgets = {'Food': 1000, 'Transportation': 500, 'Entertainment': 300, 'Other': 200}
        
        self.create_widgets()
        self.load_data()
        
    def create_widgets(self):
        # Header with gradient effect
        header = tk.Frame(self.root, bg=COLORS['primary'], height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        title = tk.Label(header, text="💰 Personal Expense Tracker", 
                        font=('Helvetica', 28, 'bold'), 
                        fg=COLORS['white'], bg=COLORS['primary'])
        title.pack(pady=20)
        
        subtitle = tk.Label(header, text="Track your expenses with elegance ✨", 
                           font=('Helvetica', 12),
                           fg=COLORS['white'], bg=COLORS['primary'])
        subtitle.pack()
        
        # Main container with notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Create tabs
        self.create_expenses_tab()
        self.create_budget_tab()
        self.create_search_tab()
        self.create_report_tab()
        self.create_graph_tab()
        
    def create_expenses_tab(self):
        """Create the main expenses tab"""
        expenses_frame = tk.Frame(self.notebook, bg=COLORS['light'])
        self.notebook.add(expenses_frame, text="📝 Expenses")
        
        # Left panel - Add expense
        left_frame = tk.Frame(expenses_frame, bg=COLORS['white'], relief='raised', bd=2)
        left_frame.pack(side='left', fill='y', padx=(0, 10))
        
        # Add expense card
        add_card = tk.Frame(left_frame, bg=COLORS['white'])
        add_card.pack(fill='x', pady=10)
        
        tk.Label(add_card, text="➕ Add New Expense", 
                font=('Helvetica', 18, 'bold'), 
                fg=COLORS['primary'], bg=COLORS['white']).pack(pady=15)
        
        # Date
        date_frame = tk.Frame(add_card, bg=COLORS['white'])
        date_frame.pack(fill='x', padx=15, pady=5)
        tk.Label(date_frame, text="📅 Date:", font=('Helvetica', 12), 
                bg=COLORS['white']).pack(anchor='w')
        self.date_entry = tk.Entry(date_frame, font=('Helvetica', 12), 
                                  relief='solid', bd=1)
        self.date_entry.pack(fill='x', pady=5)
        self.date_entry.insert(0, datetime.datetime.now().strftime('%Y-%m-%d'))
        
        # Category
        cat_frame = tk.Frame(add_card, bg=COLORS['white'])
        cat_frame.pack(fill='x', padx=15, pady=5)
        tk.Label(cat_frame, text="🏷️ Category:", font=('Helvetica', 12), 
                bg=COLORS['white']).pack(anchor='w')
        self.category_var = tk.StringVar(value="Food")
        category_combo = ttk.Combobox(cat_frame, textvariable=self.category_var,
                                     values=list(self.budgets.keys()),
                                     state="readonly", font=('Helvetica', 12))
        category_combo.pack(fill='x', pady=5)
        
        # Amount
        amount_frame = tk.Frame(add_card, bg=COLORS['white'])
        amount_frame.pack(fill='x', padx=15, pady=5)
        tk.Label(amount_frame, text="💰 Amount ($):", font=('Helvetica', 12), 
                bg=COLORS['white']).pack(anchor='w')
        self.amount_entry = tk.Entry(amount_frame, font=('Helvetica', 12), 
                                    relief='solid', bd=1)
        self.amount_entry.pack(fill='x', pady=5)
        
        # Description
        desc_frame = tk.Frame(add_card, bg=COLORS['white'])
        desc_frame.pack(fill='x', padx=15, pady=5)
        tk.Label(desc_frame, text="📝 Description:", font=('Helvetica', 12), 
                bg=COLORS['white']).pack(anchor='w')
        self.desc_entry = tk.Entry(desc_frame, font=('Helvetica', 12), 
                                  relief='solid', bd=1)
        self.desc_entry.pack(fill='x', pady=5)
        
        # Add button
        add_btn = tk.Button(add_card, text="➕ Add Expense", command=self.add_expense,
                           bg=COLORS['success'], fg=COLORS['white'], 
                           font=('Helvetica', 14, 'bold'),
                           relief='flat', padx=30, pady=12, cursor='hand2')
        add_btn.pack(pady=20)
        
        # Right panel - Expense list
        right_frame = tk.Frame(expenses_frame, bg=COLORS['white'], relief='raised', bd=2)
        right_frame.pack(side='right', fill='both', expand=True)
        
        # Header for expense list
        list_header = tk.Frame(right_frame, bg=COLORS['primary'])
        list_header.pack(fill='x')
        
        tk.Label(list_header, text="📋 Expense List", 
                font=('Helvetica', 18, 'bold'), 
                fg=COLORS['white'], bg=COLORS['primary']).pack(pady=10)
        
        # Search frame
        search_frame = tk.Frame(right_frame, bg=COLORS['white'])
        search_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(search_frame, text="🔍 Quick Search:", font=('Helvetica', 12), 
                bg=COLORS['white']).pack(side='left', padx=5)
        self.search_entry = tk.Entry(search_frame, font=('Helvetica', 12), 
                                    relief='solid', bd=1)
        self.search_entry.pack(side='left', fill='x', expand=True, padx=5)
        self.search_entry.bind('<KeyRelease>', self.filter_expenses)
        
        # Treeview with better styling
        columns = ('Date', 'Category', 'Amount', 'Description')
        self.tree = ttk.Treeview(right_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        self.tree.heading('Date', text='📅 Date')
        self.tree.heading('Category', text='🏷️ Category')
        self.tree.heading('Amount', text='💰 Amount')
        self.tree.heading('Description', text='📝 Description')
        
        self.tree.column('Date', width=120)
        self.tree.column('Category', width=120)
        self.tree.column('Amount', width=100)
        self.tree.column('Description', width=200)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(right_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        scrollbar.pack(side='right', fill='y', pady=10)
        
        # Action buttons - Stacked layout
        button_frame = tk.Frame(right_frame, bg=COLORS['white'])
        button_frame.pack(fill='x', padx=10, pady=10)
        
        # Top row - Delete button
        delete_btn = tk.Button(button_frame, text="🗑️ Delete Selected", command=self.delete_expense,
                              bg=COLORS['danger'], fg=COLORS['white'], 
                              font=('Helvetica', 12, 'bold'),
                              relief='flat', padx=20, pady=8, cursor='hand2', width=20)
        delete_btn.pack(pady=5)
        
        # Bottom row - Clear button
        clear_btn = tk.Button(button_frame, text="🔄 Clear Search", command=self.clear_search,
                             bg=COLORS['warning'], fg=COLORS['white'], 
                             font=('Helvetica', 12, 'bold'),
                             relief='flat', padx=20, pady=8, cursor='hand2', width=20)
        clear_btn.pack(pady=5)
        
    def create_budget_tab(self):
        """Create budget management tab"""
        budget_frame = tk.Frame(self.notebook, bg=COLORS['light'])
        self.notebook.add(budget_frame, text="💰 Budget")
        
        # Budget management card
        budget_card = tk.Frame(budget_frame, bg=COLORS['white'], relief='raised', bd=2)
        budget_card.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(budget_card, text="💰 Budget Management", 
                font=('Helvetica', 24, 'bold'), 
                fg=COLORS['primary'], bg=COLORS['white']).pack(pady=20)
        
        # Budget entries
        self.budget_entries = {}
        budget_container = tk.Frame(budget_card, bg=COLORS['white'])
        budget_container.pack(fill='both', expand=True, padx=40, pady=20)
        
        for i, (category, amount) in enumerate(self.budgets.items()):
            frame = tk.Frame(budget_container, bg=COLORS['white'])
            frame.pack(fill='x', pady=10)
            
            # Category label with icon
            icon = "🍽️" if category == "Food" else "🚗" if category == "Transportation" else "🎮" if category == "Entertainment" else "📦"
            tk.Label(frame, text=f"{icon} {category}:", 
                    font=('Helvetica', 16, 'bold'), 
                    fg=COLORS['dark'], bg=COLORS['white']).pack(side='left')
            
            # Budget entry
            entry = tk.Entry(frame, font=('Helvetica', 14), width=15, 
                           relief='solid', bd=1)
            entry.pack(side='right', padx=10)
            entry.insert(0, f"{amount:.2f}")
            self.budget_entries[category] = entry
        
        # Update button
        update_btn = tk.Button(budget_card, text="💾 Update Budgets", command=self.update_budgets,
                              bg=COLORS['primary'], fg=COLORS['white'], 
                              font=('Helvetica', 16, 'bold'),
                              relief='flat', padx=40, pady=15, cursor='hand2')
        update_btn.pack(pady=30)
        
    def create_search_tab(self):
        """Create advanced search tab"""
        search_frame = tk.Frame(self.notebook, bg=COLORS['light'])
        self.notebook.add(search_frame, text="🔍 Search")
        
        # Search card
        search_card = tk.Frame(search_frame, bg=COLORS['white'], relief='raised', bd=2)
        search_card.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(search_card, text="🔍 Advanced Search", 
                font=('Helvetica', 24, 'bold'), 
                fg=COLORS['primary'], bg=COLORS['white']).pack(pady=20)
        
        # Search options
        options_frame = tk.Frame(search_card, bg=COLORS['white'])
        options_frame.pack(fill='x', padx=40, pady=20)
        
        # Date range
        date_frame = tk.Frame(options_frame, bg=COLORS['white'])
        date_frame.pack(fill='x', pady=10)
        tk.Label(date_frame, text="📅 Date Range:", font=('Helvetica', 14), 
                bg=COLORS['white']).pack(anchor='w')
        
        date_input_frame = tk.Frame(date_frame, bg=COLORS['white'])
        date_input_frame.pack(fill='x', pady=5)
        
        tk.Label(date_input_frame, text="From:", font=('Helvetica', 12), 
                bg=COLORS['white']).pack(side='left')
        self.date_from = tk.Entry(date_input_frame, font=('Helvetica', 12), width=15)
        self.date_from.pack(side='left', padx=5)
        
        tk.Label(date_input_frame, text="To:", font=('Helvetica', 12), 
                bg=COLORS['white']).pack(side='left', padx=(20, 0))
        self.date_to = tk.Entry(date_input_frame, font=('Helvetica', 12), width=15)
        self.date_to.pack(side='left', padx=5)
        
        # Category filter
        cat_frame = tk.Frame(options_frame, bg=COLORS['white'])
        cat_frame.pack(fill='x', pady=10)
        tk.Label(cat_frame, text="🏷️ Category:", font=('Helvetica', 14), 
                bg=COLORS['white']).pack(anchor='w')
        self.search_category = tk.StringVar(value="All")
        cat_combo = ttk.Combobox(cat_frame, textvariable=self.search_category,
                                 values=["All"] + list(self.budgets.keys()),
                                 state="readonly", font=('Helvetica', 12))
        cat_combo.pack(anchor='w', pady=5)
        
        # Amount range
        amount_frame = tk.Frame(options_frame, bg=COLORS['white'])
        amount_frame.pack(fill='x', pady=10)
        tk.Label(amount_frame, text="💰 Amount Range:", font=('Helvetica', 14), 
                bg=COLORS['white']).pack(anchor='w')
        
        amount_input_frame = tk.Frame(amount_frame, bg=COLORS['white'])
        amount_input_frame.pack(fill='x', pady=5)
        
        tk.Label(amount_input_frame, text="Min:", font=('Helvetica', 12), 
                bg=COLORS['white']).pack(side='left')
        self.amount_min = tk.Entry(amount_input_frame, font=('Helvetica', 12), width=10)
        self.amount_min.pack(side='left', padx=5)
        
        tk.Label(amount_input_frame, text="Max:", font=('Helvetica', 12), 
                bg=COLORS['white']).pack(side='left', padx=(20, 0))
        self.amount_max = tk.Entry(amount_input_frame, font=('Helvetica', 12), width=10)
        self.amount_max.pack(side='left', padx=5)
        
        # Search button
        search_btn = tk.Button(options_frame, text="🔍 Search", command=self.advanced_search,
                              bg=COLORS['accent'], fg=COLORS['white'], 
                              font=('Helvetica', 14, 'bold'),
                              relief='flat', padx=30, pady=10, cursor='hand2')
        search_btn.pack(pady=20)
        
        # Results area
        results_frame = tk.Frame(search_card, bg=COLORS['white'])
        results_frame.pack(fill='both', expand=True, padx=40, pady=20)
        
        tk.Label(results_frame, text="📊 Search Results", 
                font=('Helvetica', 16, 'bold'), 
                fg=COLORS['primary'], bg=COLORS['white']).pack(anchor='w')
        
        # Results treeview
        columns = ('Date', 'Category', 'Amount', 'Description')
        self.search_tree = ttk.Treeview(results_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.search_tree.heading(col, text=col)
            self.search_tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(results_frame, orient='vertical', command=self.search_tree.yview)
        self.search_tree.configure(yscrollcommand=scrollbar.set)
        
        self.search_tree.pack(side='left', fill='both', expand=True, pady=10)
        scrollbar.pack(side='right', fill='y', pady=10)
        
    def create_report_tab(self):
        """Create comprehensive report tab"""
        report_frame = tk.Frame(self.notebook, bg=COLORS['light'])
        self.notebook.add(report_frame, text="📊 Report")
        
        # Report card
        report_card = tk.Frame(report_frame, bg=COLORS['white'], relief='raised', bd=2)
        report_card.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(report_card, text="📊 Financial Report", 
                font=('Helvetica', 24, 'bold'), 
                fg=COLORS['primary'], bg=COLORS['white']).pack(pady=20)
        
        # Report content
        self.report_text = scrolledtext.ScrolledText(report_card, 
                                                   font=('Courier', 12),
                                                   bg=COLORS['light'],
                                                   fg=COLORS['dark'],
                                                   height=25)
        self.report_text.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Generate button
        generate_btn = tk.Button(report_card, text="📊 Generate Report", command=self.generate_report,
                                bg=COLORS['success'], fg=COLORS['white'], 
                                font=('Helvetica', 14, 'bold'),
                                relief='flat', padx=30, pady=10, cursor='hand2')
        generate_btn.pack(pady=20)
        
    def create_graph_tab(self):
        """Create graph visualization tab"""
        graph_frame = tk.Frame(self.notebook, bg=COLORS['light'])
        self.notebook.add(graph_frame, text="📈 Graph")
        
        # Graph card
        graph_card = tk.Frame(graph_frame, bg=COLORS['white'], relief='raised', bd=2)
        graph_card.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(graph_card, text="📈 Expense Visualization", 
                font=('Helvetica', 24, 'bold'), 
                fg=COLORS['primary'], bg=COLORS['white']).pack(pady=20)
        
        # Graph options
        options_frame = tk.Frame(graph_card, bg=COLORS['white'])
        options_frame.pack(fill='x', padx=40, pady=20)
        
        tk.Label(options_frame, text="Choose visualization type:", 
                font=('Helvetica', 16), bg=COLORS['white']).pack(anchor='w')
        
        # Graph button
        button_frame = tk.Frame(options_frame, bg=COLORS['white'])
        button_frame.pack(fill='x', pady=20)
        
        budget_btn = tk.Button(button_frame, text="💰 Budget Chart", command=self.show_budget_graph,
                              bg=COLORS['primary'], fg=COLORS['white'], 
                              font=('Helvetica', 16, 'bold'),
                              relief='flat', padx=40, pady=15, cursor='hand2')
        budget_btn.pack(pady=20)
        
    def load_data(self):
        try:
            with open("expenses.txt", "r", encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line:
                        parts = line.split("\t")
                        if len(parts) >= 4:
                            self.expenses.append({
                                'date': parts[0],
                                'category': parts[1],
                                'amount': float(parts[2]),
                                'description': parts[3]
                            })
        except FileNotFoundError:
            try:
                with open("expenses.txt", "w", encoding='utf-8') as file:
                    pass
            except PermissionError:
                messagebox.showerror("Error", "Cannot create expenses.txt file. Check permissions!")
        except PermissionError:
            messagebox.showerror("Error", "Cannot read expenses.txt file. Check permissions!")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading data: {e}")
            
        self.update_display()
        
    def add_expense(self):
        try:
            date = self.date_entry.get()
            category = self.category_var.get()
            amount_str = self.amount_entry.get()
            description = self.desc_entry.get()
            
            if not all([date, amount_str, description]):
                messagebox.showerror("Error", "Please fill all fields!")
                return
            
            # Validate amount
            try:
                amount = float(amount_str)
                if amount <= 0:
                    messagebox.showerror("Error", "Amount must be positive!")
                    return
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount!")
                return
                
            # Validate date
            try:
                datetime.datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD")
                return
                
            new_expense = {
                'date': date,
                'category': category,
                'amount': amount,
                'description': description
            }
            
            self.expenses.append(new_expense)
            
            if self.save_data():
                self.update_display()
                
                # Clear entries
                self.amount_entry.delete(0, tk.END)
                self.desc_entry.delete(0, tk.END)
                
                messagebox.showinfo("Success", "Expense added! ✨")
            else:
                messagebox.showerror("Error", "Failed to save expense!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {e}")
            
    def delete_expense(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Select an expense to delete!")
            return
            
        if messagebox.askyesno("Confirm", "Delete this expense?"):
            try:
                item = self.tree.item(selection[0])
                values = item['values']
                
                # Extract amount without $ symbol
                amount_str = values[2].replace('$', '').strip()
                amount = float(amount_str)
                
                # Find and remove expense
                for i, expense in enumerate(self.expenses):
                    if (expense['date'] == values[0] and 
                        expense['category'] == values[1] and 
                        expense['amount'] == amount and 
                        expense['description'] == values[3]):
                        del self.expenses[i]
                        break
                        
                if self.save_data():
                    self.update_display()
                    messagebox.showinfo("Success", "Expense deleted! 🗑️")
                else:
                    messagebox.showerror("Error", "Failed to save changes!")
                    
            except ValueError:
                messagebox.showerror("Error", "Invalid amount format!")
            except Exception as e:
                messagebox.showerror("Error", f"Error deleting expense: {e}")
    
    def filter_expenses(self, event=None):
        """Filter expenses based on search text"""
        search_term = self.search_entry.get().lower()
        
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Add filtered expenses
        for expense in self.expenses:
            if (search_term in expense['date'].lower() or 
                search_term in expense['category'].lower() or 
                search_term in expense['description'].lower() or
                search_term in str(expense['amount'])):
                self.tree.insert('', 'end', values=(
                    expense['date'],
                    expense['category'],
                    f"${expense['amount']:.2f}",
                    expense['description']
                ))
    
    def clear_search(self):
        """Clear search and show all expenses"""
        self.search_entry.delete(0, tk.END)
        self.update_display()
    
    def advanced_search(self):
        """Perform advanced search with filters"""
        # Clear search results
        for item in self.search_tree.get_children():
            self.search_tree.delete(item)
        
        # Get search criteria
        date_from = self.date_from.get()
        date_to = self.date_to.get()
        category = self.search_category.get()
        amount_min = self.amount_min.get()
        amount_max = self.amount_max.get()
        
        # Filter expenses
        filtered_expenses = []
        for expense in self.expenses:
            # Date filter
            if date_from and expense['date'] < date_from:
                continue
            if date_to and expense['date'] > date_to:
                continue
                
            # Category filter
            if category != "All" and expense['category'] != category:
                continue
                
            # Amount filter
            if amount_min:
                try:
                    if expense['amount'] < float(amount_min):
                        continue
                except ValueError:
                    pass
            if amount_max:
                try:
                    if expense['amount'] > float(amount_max):
                        continue
                except ValueError:
                    pass
                    
            filtered_expenses.append(expense)
        
        # Display results
        for expense in filtered_expenses:
            self.search_tree.insert('', 'end', values=(
                expense['date'],
                expense['category'],
                f"${expense['amount']:.2f}",
                expense['description']
            ))
        
        messagebox.showinfo("Search Complete", f"Found {len(filtered_expenses)} matching expenses!")
    
    def update_budgets(self):
        """Update budget values"""
        try:
            for category, entry in self.budget_entries.items():
                amount = float(entry.get())
                self.budgets[category] = amount
            
            self.save_budgets()
            messagebox.showinfo("Success", "Budgets updated successfully! 💰")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid amounts!")
    
    def generate_report(self):
        """Generate comprehensive financial report"""
        if not self.expenses:
            self.report_text.delete(1.0, tk.END)
            self.report_text.insert(tk.END, "No expenses to report!")
            return
        
        # Calculate totals
        total_spent = sum(exp['amount'] for exp in self.expenses)
        category_totals = {}
        for expense in self.expenses:
            cat = expense['category']
            if cat not in category_totals:
                category_totals[cat] = 0
            category_totals[cat] += expense['amount']
        
        # Generate report
        report = "=" * 60 + "\n"
        report += "📊 COMPREHENSIVE FINANCIAL REPORT\n"
        report += "=" * 60 + "\n\n"
        
        # Overall summary
        total_budget = sum(self.budgets.values())
        remaining = total_budget - total_spent
        usage_percent = (total_spent / total_budget * 100) if total_budget > 0 else 0
        
        report += "💰 OVERALL SUMMARY\n"
        report += "-" * 30 + "\n"
        report += f"Total Spent:     ${total_spent:>10.2f}\n"
        report += f"Total Budget:    ${total_budget:>10.2f}\n"
        report += f"Remaining:       ${remaining:>10.2f}\n"
        report += f"Usage:           {usage_percent:>10.1f}%\n\n"
        
        # Category analysis
        report += "📈 CATEGORY ANALYSIS\n"
        report += "-" * 30 + "\n"
        
        for category, spent in category_totals.items():
            budget = self.budgets.get(category, 0)
            remaining_cat = budget - spent
            usage_cat = (spent / budget * 100) if budget > 0 else 0
            status = "✅" if remaining_cat >= 0 else "❌"
            
            report += f"{status} {category}:\n"
            report += f"   Spent:     ${spent:>8.2f}\n"
            report += f"   Budget:    ${budget:>8.2f}\n"
            report += f"   Remaining: ${remaining_cat:>8.2f}\n"
            report += f"   Usage:     {usage_cat:>8.1f}%\n\n"
        
        # Recent expenses
        report += "📋 RECENT EXPENSES (Last 10)\n"
        report += "-" * 30 + "\n"
        
        sorted_expenses = sorted(self.expenses, key=lambda x: x['date'], reverse=True)
        for expense in sorted_expenses[:10]:
            report += f"{expense['date']} | {expense['category']:<15} | ${expense['amount']:>8.2f} | {expense['description']}\n"
        
        # Warnings
        report += "\n⚠️  WARNINGS\n"
        report += "-" * 30 + "\n"
        
        if remaining < 0:
            report += "❌ You have exceeded your total budget!\n"
        
        for category, spent in category_totals.items():
            budget = self.budgets.get(category, 0)
            if spent > budget:
                report += f"❌ {category} budget exceeded by ${spent - budget:.2f}\n"
        
        if not any(remaining < 0 for remaining in [total_budget - total_spent] + 
                  [self.budgets.get(cat, 0) - spent for cat, spent in category_totals.items()]):
            report += "✅ All budgets are within limits!\n"
        
        # Display report
        self.report_text.delete(1.0, tk.END)
        self.report_text.insert(tk.END, report)
    
    def show_budget_graph(self):
        """Show budget vs actual spending chart"""
        if not self.budgets:
            messagebox.showwarning("Warning", "No budget data!")
            return
            
        try:
            # Reset turtle screen
            turtle.clearscreen()
            screen = turtle.Screen()
            screen.title("Budget vs Actual Spending")
            screen.bgcolor("white")
            screen.setup(800, 600)
            
            pen = turtle.Turtle()
            pen.speed(0)
            pen.hideturtle()
            
            # Calculate category totals
            category_totals = {}
            for expense in self.expenses:
                cat = expense['category']
                if cat not in category_totals:
                    category_totals[cat] = 0
                category_totals[cat] += expense['amount']
            
            # Draw chart
            x = -300
            budget_colors = ["#1E40AF", "#7C3AED", "#059669", "#F59E0B"]  # Distinct budget colors (no red)
            spent_color = "#EF4444"  # Consistent spent color
            
            # Draw title
            pen.penup()
            pen.goto(0, 250)
            pen.color("#6366F1")
            pen.write("Budget vs Actual Spending", align="center", font=("Arial", 16, "bold"))
            
            # Draw legend
            pen.goto(-350, 200)
            pen.color("#1E40AF")
            pen.write("Budget Bars", font=("Arial", 12))
            pen.goto(-350, 180)
            pen.color("#EF4444")
            pen.write("Spent Bars", font=("Arial", 12))
            
            for i, (category, budget) in enumerate(self.budgets.items()):
                spent = category_totals.get(category, 0)
                
                # Draw budget bar (distinct color for each category)
                pen.penup()
                pen.goto(x, 0)
                pen.pendown()
                pen.fillcolor(budget_colors[i % len(budget_colors)])
                pen.begin_fill()
                for _ in range(2):
                    pen.forward(40)
                    pen.left(90)
                    pen.forward(budget / 15)
                    pen.left(90)
                pen.end_fill()
                
                # Draw spent bar (consistent red)
                pen.penup()
                pen.goto(x + 5, 0)
                pen.pendown()
                pen.fillcolor(spent_color)
                pen.begin_fill()
                for _ in range(2):
                    pen.forward(30)
                    pen.left(90)
                    pen.forward(spent / 15)
                    pen.left(90)
                pen.end_fill()
                
                # Write category
                pen.penup()
                pen.goto(x + 20, -30)
                pen.color("black")
                pen.write(category, align="center", font=("Arial", 10))
                
                # Write amounts
                pen.goto(x + 20, -50)
                pen.write(f"B:${budget}", align="center", font=("Arial", 8))
                pen.goto(x + 20, -65)
                pen.write(f"S:${spent:.0f}", align="center", font=("Arial", 8))
                
                x += 120
                
            screen.mainloop()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create graph: {e}")
    
    def show_expense_graph(self):
        """Show expense trend chart"""
        if not self.expenses:
            messagebox.showwarning("Warning", "No expense data!")
            return
            
        try:
            # Reset turtle screen
            turtle.clearscreen()
            screen = turtle.Screen()
            screen.title("Expense Trend")
            screen.bgcolor("white")
            screen.setup(800, 600)
            
            pen = turtle.Turtle()
            pen.speed(0)
            pen.hideturtle()
            
            # Sort expenses by date
            sorted_expenses = sorted(self.expenses, key=lambda x: x['date'])
            
            # Draw axes
            pen.penup()
            pen.goto(-350, -200)
            pen.pendown()
            pen.goto(350, -200)  # X-axis
            pen.goto(350, 200)   # Y-axis
            pen.goto(-350, 200)  # Top line
            pen.goto(-350, -200) # Left line
            
            # Draw title
            pen.penup()
            pen.goto(0, 250)
            pen.color("#6366F1")
            pen.write("Expense Trend Over Time", align="center", font=("Arial", 16, "bold"))
            
            # Plot points
            if len(sorted_expenses) > 1:
                x_step = 700 / (len(sorted_expenses) - 1)
            else:
                x_step = 700
                
            x = -350
            max_amount = max(exp['amount'] for exp in sorted_expenses)
            
            pen.penup()
            for i, expense in enumerate(sorted_expenses):
                y = (expense['amount'] / max_amount) * 300 - 200  # Scale to fit
                pen.goto(x, y)
                pen.pendown()
                pen.dot(8, "#EC4899")
                
                # Write amount
                pen.penup()
                pen.goto(x, y + 15)
                pen.write(f"${expense['amount']:.0f}", align="center", font=("Arial", 8))
                
                # Connect points
                if i > 0:
                    prev_expense = sorted_expenses[i-1]
                    prev_y = (prev_expense['amount'] / max_amount) * 300 - 200
                    pen.goto(x - x_step, prev_y)
                    pen.pendown()
                    pen.goto(x, y)
                    pen.penup()
                
                x += x_step
                
            screen.mainloop()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create graph: {e}")
    
    def show_pie_chart(self):
        """Show category distribution pie chart"""
        if not self.expenses:
            messagebox.showwarning("Warning", "No expense data!")
            return
            
        try:
            # Reset turtle screen
            turtle.clearscreen()
            screen = turtle.Screen()
            screen.title("Category Distribution")
            screen.bgcolor("white")
            screen.setup(800, 600)
            
            pen = turtle.Turtle()
            pen.speed(0)
            pen.hideturtle()
            
            # Calculate category totals
            category_totals = {}
            for expense in self.expenses:
                cat = expense['category']
                if cat not in category_totals:
                    category_totals[cat] = 0
                category_totals[cat] += expense['amount']
            
            total = sum(category_totals.values())
            colors = ["#6366F1", "#8B5CF6", "#EC4899", "#10B981", "#F59E0B"]
            
            # Draw title
            pen.penup()
            pen.goto(0, 250)
            pen.color("#6366F1")
            pen.write("Category Distribution", align="center", font=("Arial", 16, "bold"))
            
            # Draw pie chart
            pen.penup()
            pen.goto(0, -100)
            pen.pendown()
            
            start_angle = 0
            for i, (category, amount) in enumerate(category_totals.items()):
                angle = (amount / total) * 360
                
                pen.fillcolor(colors[i % len(colors)])
                pen.begin_fill()
                pen.circle(100, angle)
                pen.goto(0, 0)
                pen.end_fill()
                
                # Write category and percentage
                pen.penup()
                pen.goto(0, 0)
                pen.setheading(start_angle + angle/2)
                pen.forward(80)
                pen.write(f"{category}\n{amount/total*100:.1f}%", align="center", font=("Arial", 10))
                
                start_angle += angle
                
            screen.mainloop()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create graph: {e}")
            
    def save_data(self):
        try:
            # Create backup of existing file
            if os.path.exists("expenses.txt"):
                try:
                    os.rename("expenses.txt", "expenses_backup.txt")
                except PermissionError:
                    pass
            
            # Write new data
            with open("expenses.txt", "w", encoding='utf-8') as file:
                for expense in self.expenses:
                    file.write(f"{expense['date']}\t{expense['category']}\t{expense['amount']}\t{expense['description']}\n")
            
            # Remove backup if successful
            if os.path.exists("expenses_backup.txt"):
                try:
                    os.remove("expenses_backup.txt")
                except:
                    pass
                    
            return True
            
        except PermissionError:
            messagebox.showerror("Error", "Permission denied! Cannot write to expenses.txt")
            return False
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {e}")
            return False
    
    def save_budgets(self):
        """Save budgets to file"""
        try:
            with open("budget.txt", "w", encoding='utf-8') as file:
                for category, amount in self.budgets.items():
                    file.write(f"{category}:{amount}\n")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save budgets: {e}")
            return False
            
    def update_display(self):
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Add expenses
        for expense in self.expenses:
            self.tree.insert('', 'end', values=(
                expense['date'],
                expense['category'],
                f"${expense['amount']:.2f}",
                expense['description']
            ))

def main():
    root = tk.Tk()
    app = ExpenseTrackerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 
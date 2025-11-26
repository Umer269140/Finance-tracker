import questionary
from rich.console import Console
from rich.table import Table
from features.transactions import transactions as t

def main():
    console = Console()
    while True:
        choice = questionary.select(
            "What do you want to do?",
            choices=[
                "Add a new transaction",
                "View all transactions",
                "Delete a transaction",
                "Exit"
            ]
        ).ask()

        if choice == "Add a new transaction":
            transaction_type = questionary.select(
                "Select transaction type:",
                choices=["Expense", "Income"]
            ).ask()
            category = questionary.text("Enter category:").ask()
            amount = float(questionary.text("Enter amount:").ask())
            t.add_transaction(transaction_type, category, amount)
            console.print("Transaction added successfully!", style="bold green")

        elif choice == "View all transactions":
            transactions = t.get_all_transactions()
            table = Table(title="All Transactions")
            table.add_column("Type", style="cyan")
            table.add_column("Category", style="magenta")
            table.add_column("Amount", style="green")

            for trans in transactions:
                table.add_row(trans['type'], trans['category'], str(trans['amount']))
            
            console.print(table)

        elif choice == "Delete a transaction":
            transactions = t.get_all_transactions()
            transaction_to_delete = questionary.select(
                "Select a transaction to delete:",
                choices=[f"{i+1}. {trans['type']} - {trans['category']} - {trans['amount']}" for i, trans in enumerate(transactions)]
            ).ask()
            if transaction_to_delete:
                index_to_delete = int(transaction_to_delete.split('.')[0]) - 1
                t.delete_transaction(index_to_delete)
                console.print("Transaction deleted successfully!", style="bold red")

        elif choice == "Exit":
            break

if __name__ == "__main__":
    main()
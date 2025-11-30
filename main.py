import questionary
from rich.console import Console
from rich.table import Table
from features.transactions import transactions as t
from datetime import datetime

def main():
    console = Console()
    user_id = 'admin'
    id_token = None
    is_admin = True

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
            description = questionary.text("Enter description:").ask()
            date = datetime.now().strftime("%Y-%m-%d")
            
            # For simplicity in CLI, using placeholders for other fields
            name = ""
            billing_number = ""
            payment_method = ""

            t.add_transaction(user_id, id_token, is_admin, transaction_type, amount, date, name, description, billing_number, payment_method)
            console.print("Transaction added successfully!", style="bold green")

        elif choice == "View all transactions":
            transactions = t.get_all_transactions(user_id, id_token, is_admin)
            table = Table(title="All Transactions")
            table.add_column("ID", style="dim", no_wrap=True)
            table.add_column("Type", style="cyan")
            table.add_column("Category", style="magenta")
            table.add_column("Amount", style="green")
            table.add_column("Date", style="blue")
            table.add_column("Description", style="yellow")


            for trans in transactions:
                table.add_row(trans['id'], trans['type'], trans.get('category', 'N/A'), str(trans['amount']), trans['date'], trans.get('description', ''))
            
            console.print(table)

        elif choice == "Delete a transaction":
            transactions = t.get_all_transactions(user_id, id_token, is_admin)
            if not transactions:
                console.print("No transactions to delete.", style="bold red")
                continue

            transaction_to_delete = questionary.select(
                "Select a transaction to delete:",
                choices=[f"{trans['id']} - {trans['type']} - {trans.get('category', 'N/A')} - {trans['amount']}" for trans in transactions]
            ).ask()

            if transaction_to_delete:
                transaction_id_to_delete = transaction_to_delete.split(' ')[0]
                t.delete_transaction(user_id, id_token, is_admin, transaction_id_to_delete)
                console.print("Transaction deleted successfully!", style="bold red")

        elif choice == "Exit":
            break

if __name__ == "__main__":
    main()
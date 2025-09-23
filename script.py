import csv
from statistics import mean

input_filename = 'contributions.csv'
output_filename = 'transactions.csv'

# Read the CSV data
with open(input_filename, newline='') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)  # Skip header
    data = [(row[0], int(row[1].replace('$', '').replace(',', ''))) for row in reader]  # Strip dollar sign and commas

# Calculate average and participant count
contributions = [amount for _, amount in data]
average = round(mean(contributions))
num_people = len(data)

# Subtract the average from each contribution
adjusted_data = [(name, amount - average) for name, amount in data]

# Separate and sort by magnitude
givers = sorted(
    [(name, adjusted) for name, adjusted in adjusted_data if adjusted > 0],
    key=lambda x: x[1],
    reverse=True
)
receivers = sorted(
    [(name, adjusted) for name, adjusted in adjusted_data if adjusted < 0],
    key=lambda x: abs(x[1]),
    reverse=True
)

# Calculate transactions
transactions = []
giver_idx = 0
receiver_idx = 0

givers = [[name, adjusted] for name, adjusted in givers]
receivers = [[name, adjusted] for name, adjusted in receivers]

total_distributed = 0  # Track the total amount distributed

while giver_idx < len(givers) and receiver_idx < len(receivers):
    giver_name, giver_amt = givers[giver_idx]
    receiver_name, receiver_amt = receivers[receiver_idx]

    transfer_amt = min(giver_amt, -receiver_amt)
    transactions.append((giver_name, receiver_name, transfer_amt))

    total_distributed += transfer_amt  # Add the transfer amount to total distributed

    givers[giver_idx][1] -= transfer_amt
    receivers[receiver_idx][1] += transfer_amt

    if givers[giver_idx][1] == 0:
        giver_idx += 1
    if receivers[receiver_idx][1] == 0:
        receiver_idx += 1

# Write output to transactions.csv
with open(output_filename, 'w', newline='') as f:
    writer = csv.writer(f)

    # Summary section
    writer.writerow(['Summary'])
    writer.writerow(['Average Contribution', average])
    writer.writerow(['Number of People', num_people])
    writer.writerow(['Total Amount Distributed', total_distributed])
    writer.writerow([])

    # Original data
    writer.writerow(['Original Contributions'])
    writer.writerow(['Name', 'Contribution'])
    for name, amount in data:
        writer.writerow([name, f"${amount}"])  # Write amounts with dollar signs
    writer.writerow([])

    # Transactions
    writer.writerow(['Transactions'])
    writer.writerow(['Giver', 'Receiver', 'Amount'])
    for giver, receiver, amount in transactions:
        writer.writerow([giver, receiver, f"${amount}"])

print(f"Output written to {output_filename}")

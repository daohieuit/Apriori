from itertools import combinations

# Tinh do pho bien cua mot itemset
def calculate_support(itemset, transactions):
    return sum(1 for transaction in transactions if itemset.issubset(transaction))

# Buoc 1: Tim cac tap itemset pho bien
def apriori(transactions, minsup):
    items = {item for transaction in transactions for item in transaction}
    C1 = [{item} for item in items]

    # Lay cac itemset ung vien ban dau
    F1 = [{item} for item in items if calculate_support({item}, transactions) >= minsup]
    F = F1
    k = 2

    frequent_itemsets = [(itemset, calculate_support(itemset, transactions)) for itemset in F1]

    while F:
        Ck = [set(comb) for comb in combinations(items, k)]
        Fk = [itemset for itemset in Ck if calculate_support(itemset, transactions) >= minsup]
        frequent_itemsets.extend((itemset, calculate_support(itemset, transactions)) for itemset in Fk)
        F = Fk
        k += 1

    return frequent_itemsets

# Buoc 2: Tinh luat ket hop
def generate_association_rules(frequent_itemsets, transactions, minconf):
    rules = []
    for itemset, support in frequent_itemsets:
        if len(itemset) > 1:
            for i in range(1, len(itemset)):
                for subset in combinations(itemset, i):
                    subset = set(subset)
                    remain = itemset - subset
                    support_itemset = calculate_support(itemset, transactions)
                    support_subset = calculate_support(subset, transactions)
                    confidence = support_itemset / support_subset
                    if confidence >= minconf:
                        rules.append((subset, remain, confidence))
    return rules

# Nguoi dung nhap transactions
def input_transactions():
    transactions = []
    print("Nhap cac giao dich, moi giao dich la mot tap hop cac item cach nhau boi dau cach (space).")
    print("Nhap 'done' de ket thuc.")
    while True:
        transaction_input = input("Giao dich: ")
        if transaction_input.lower() == 'done':
            break
        transaction = set(transaction_input.split())
        transactions.append(transaction)
    return transactions

# Nhap minsup va minconf tu nguoi dung
minsup = int(input("Nhap minsup (nguong ho tro toi thieu): "))
minconf = float(input("Nhap minconf (nguong đo tin cay toi thieu): "))

# Nhap transactions
transactions = input_transactions()

# Chay thuat toan Apriori
frequent_itemsets = apriori(transactions, minsup)
rules = generate_association_rules(frequent_itemsets, transactions, minconf)

# Sap xep cac item trong tung itemset va sau đo sap xep toan bo danh sach itemset theo kich thuoc va alphabet
sorted_frequent_itemsets = sorted(
    [(sorted(list(itemset)), support) for itemset, support in frequent_itemsets],
    key=lambda x: (len(x[0]), x[0])  # Sap xep theo kich thuoc truoc, roi theo thu tu alphabet
)

# Ket qua
print("\nCac tap itemset pho bien (sap xep theo kich thuoc va thu tu alphabet):")
for itemset, support in sorted_frequent_itemsets:
    print(f"{itemset} (support: {support})")

# Sap xep cac luat ket hop va in ra theo thu tu alphabet
sorted_rules = sorted(
    [(sorted(list(rule[0])), sorted(list(rule[1])), rule[2]) for rule in rules],
    key=lambda x: (len(x[0]), x[0], len(x[1]), x[1])  # Sap xep theo kich thuoc va thu tu alphabet
)

print("\nCac luat ket hop thoa man (sap xep theo kich thuoc va thu tu alphabet):")
for rule in sorted_rules:
    print(f"{rule[0]} => {rule[1]} (confidence: {rule[2]:.2f})")

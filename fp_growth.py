from collections import defaultdict
from itertools import combinations


# Lop FP-tree node
class FPNode:
    def __init__(self, item, count, parent):
        self.item = item
        self.count = count
        self.parent = parent
        self.children = {}
        self.link = None

    def increment(self, count):
        self.count += count


# Xay dung FP-tree
def build_fptree(transactions, minsup):
    # Dem tan suat cua cac item trong giao dich
    item_count = defaultdict(int)
    for transaction in transactions:
        for item in transaction:
            item_count[item] += 1

    # Bo cac item khong thoa man nguong minsup
    item_count = {item: count for item, count in item_count.items() if count >= minsup}

    if len(item_count) == 0:
        return None, None

    # Sap xep cac item trong moi giao dich theo tan suat giam dan
    def sort_transaction(transaction):
        return sorted([item for item in transaction if item in item_count], key=lambda x: (-item_count[x], x))

    # Goc cua FP-tree
    root = FPNode(None, 1, None)
    header_table = defaultdict(list)

    # Them tung giao dich vao FP-tree
    for transaction in transactions:
        sorted_items = sort_transaction(transaction)
        current_node = root

        for item in sorted_items:
            if item in current_node.children:
                current_node.children[item].increment(1)
            else:
                new_node = FPNode(item, 1, current_node)
                current_node.children[item] = new_node
                if header_table[item]:
                    last_node = header_table[item][-1]
                    while last_node.link:
                        last_node = last_node.link
                    last_node.link = new_node
                header_table[item].append(new_node)
            current_node = current_node.children[item]

    return root, header_table


# Truy hoi cac tap pho bien tu FP-tree
def mine_fptree(header_table, minsup, prefix):
    frequent_itemsets = []

    # Duyet qua tung item trong bang header (theo thu tu xuat hien)
    for item, nodes in sorted(header_table.items(), key=lambda x: x[0]):
        support = sum(node.count for node in nodes)
        if support >= minsup:
            new_frequent_itemset = prefix.copy()
            new_frequent_itemset.add(item)
            frequent_itemsets.append((new_frequent_itemset, support))

            # Xay dung conditional pattern base
            conditional_pattern_base = []
            for node in nodes:
                path = []
                current_node = node.parent
                while current_node and current_node.item is not None:
                    path.append(current_node.item)
                    current_node = current_node.parent
                for _ in range(node.count):
                    conditional_pattern_base.append(path)

            # Tao FP-tree cho conditional pattern base
            conditional_tree, conditional_header = build_fptree(conditional_pattern_base, minsup)

            # De quy khai thac FP-tree dieu kien
            if conditional_tree:
                conditional_frequent_itemsets = mine_fptree(conditional_header, minsup, new_frequent_itemset)
                frequent_itemsets.extend(conditional_frequent_itemsets)

    return frequent_itemsets


# Tinh do pho bien cua mot itemset
def calculate_support(itemset, transactions):
    return sum(1 for transaction in transactions if itemset.issubset(transaction))

# Tinh luat ket hop
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


# Nhap transactions tu nguoi dung
def input_transactions():
    transactions = []
    print("Nhap cac giao dich, moi giao dich la mot tap hop cac item cach nhau boi dau cach.")
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
minconf = float(input("Nhap minconf (nguong do tin cay toi thieu): "))

# Nhap transactions
transactions = input_transactions()

# Xay dung FP-tree
root, header_table = build_fptree(transactions, minsup)

# Khai thac cac tap pho bien tu FP-tree
frequent_itemsets = mine_fptree(header_table, minsup, set())

# Tao luat ket hop
rules = generate_association_rules(frequent_itemsets, transactions, minconf)

# Sap xep cac item trong tung itemset va sau do sap xep toan bo danh sach itemset theo kich thuoc va alphabet
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

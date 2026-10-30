import pandas as pd
import numpy as np

# -----------------------------
# 1. Load Dataset
# -----------------------------
try:
    df = pd.read_csv("c:/users/dhara/OneDrive/Desktop/ecommerce_clean.csv")
    print("Dataset Loaded Successfully")
except:
    print(" Dataset load aagala")
    exit()

# -----------------------------
# 2. Cleaning
# -----------------------------
df = df.drop_duplicates()
df = df.fillna(0)

cols = ['mrp', 'current_price', 'labeled_discount',
        'prev_price', 'prev_mrp', 'scarcity_repeat_count']

for col in cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# -----------------------------
# 3. Feature Engineering
# -----------------------------
df['actual_discount'] = ((df['mrp'] - df['current_price']) / df['mrp']) * 100
df['discount_mismatch'] = abs(df.get('labeled_discount', 0) - df['actual_discount'])

# -----------------------------
# 🔁 4. LOOP START
# -----------------------------
while True:

    print("\n ENTER PRODUCT DETAILS (type 'exit' to stop)")

    product_id = input("Product ID: ")
    if product_id.lower() == "exit":
        print(" Exiting...")
        break

    product_name = input("Product Name: ")
    if product_name.lower() == "exit":
        print(" Exiting...")
        break

    # -----------------------------
    # Safe numeric input
    # -----------------------------
    try:
        mrp = float(input("MRP: "))
        current_price = float(input("Current Price: "))
        prev_price = float(input("Previous Price: "))
    except:
        print(" Invalid number! Try again.")
        continue   # loop restart

    # -----------------------------
    # Scarcity input
    # -----------------------------
    scarcity_input = input("has Scarcity label (yes/no): ").lower()
    has_scarcity = True if scarcity_input == "yes" else False

    try:
        scarcity_repeat = int(input("Scarcity repeat count: "))
    except:
        scarcity_repeat = 0

    # -----------------------------
    # Calculations
    # -----------------------------
    try:
        actual_discount = ((mrp - current_price) / mrp) * 100
    except:
        actual_discount = 0

    try:
        price_change_pct = ((current_price - prev_price) / prev_price) * 100
    except:
        price_change_pct = 0

    # -----------------------------
    # Detection Logic
    # -----------------------------
    pattern = "Clean"

    # Fake Discount
    if actual_discount > 70:
        pattern = "Fake Discount"

    # Fake Urgency
    if has_scarcity and scarcity_repeat > 3:
        pattern = "Fake Urgency"

    # Price Spike
    if price_change_pct > 50:
        pattern = "Price Spike"

    # Dataset comparison
    try:
        matched = df[df['product_name'].str.lower() == product_name.lower()]

        if not matched.empty:
            avg_price = matched['current_price'].mean()

            if current_price > (1.5 * avg_price):
                pattern = "Price Spike"

            avg_discount = matched['actual_discount'].mean()

            if abs(actual_discount - avg_discount) > 30:
                pattern = "Fake Discount"
    except:
        pass  # error avoid

    # -----------------------------
    # OUTPUT
    # -----------------------------
    print("\n RESULT")
    print("---------------------------")
    print(f"Product ID        : {product_id}")
    print(f"Product Name      : {product_name}")
    print(f"MRP               : {mrp}")
    print(f"Current Price     : {current_price}")
    print(f"Actual Discount   : {round(actual_discount,2)}%")
    print(f"Price Change %    : {round(price_change_pct,2)}%")
    print(f"Detected Pattern  : {pattern}")
    print("---------------------------")

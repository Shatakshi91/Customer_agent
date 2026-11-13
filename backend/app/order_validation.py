
customer_name = "Rahul"
order_amount = 2500
is_verified = True
is_delivered = True
is_within_return_window = True

print("Customer:", customer_name)

# Check order amount
if order_amount >= 1000:
    print("Eligible for priority support")
else:
    print("Standard support")

# Check refund eligibility
if not is_verified:
    print("Please verify your account")

elif not is_delivered:
    print("Order has not been delivered")

elif is_within_return_window:
    print("Eligible to submit refund request")

else:
    print("Refund request is outside the return window")

# Display available products
products = ["Laptop", "Mouse", "Keyboard"]

print("Available products:")

for product in products:
    print(product)

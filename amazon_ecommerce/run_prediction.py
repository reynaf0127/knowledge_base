from predictive import predict_return_risk

order = {
    'discount': 30,
    'price': 100,
    'final_price': 70,
    'stock': 250,
    'seller_rating': 4.2,
    'review_count': 578,
    'rating': 4.4,
    'shipping_time_days': 5,
}

results = predict_return_risk(order)
print(results[['return_probability','return_risk_percent','predicted_return']])
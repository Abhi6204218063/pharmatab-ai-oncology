from ai.therapy_optimizer import TherapyOptimizer


optimizer = TherapyOptimizer()

strategy, reduction, resistance = optimizer.find_best_strategy()


print("\nAI Therapy Optimization Result")

print("--------------------------------")

print("Recommended Strategy:", strategy)

print("Expected Tumor Reduction:", round(reduction * 100, 2), "%")

print("Resistance Risk:", round(resistance * 100, 2), "%")
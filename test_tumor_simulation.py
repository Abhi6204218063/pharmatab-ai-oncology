from simulation.tumor_evolution_engine import TumorEvolutionEngine
import matplotlib.pyplot as plt


engine = TumorEvolutionEngine(

    initial_cells=1000000,
    growth_rate=0.05,
    therapy_effect=0.03
)


result = engine.simulate(weeks=52)

risk = engine.risk_prediction(result)


print("\nAI Tumor Evolution Prediction")
print("--------------------------------")

print("Final Tumor Cells:", int(result[-1]))

print("Risk Assessment:", risk)



plt.plot(result)

plt.title("Tumor Evolution Simulation")

plt.xlabel("Weeks")

plt.ylabel("Tumor Cell Count")

plt.savefig("tumor_simulation.png")

plt.show()
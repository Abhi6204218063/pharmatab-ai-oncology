from simulation.digital_patient_twin import DigitalPatientTwin
import matplotlib.pyplot as plt


patient = DigitalPatientTwin(

    tumor_cells=1000000,
    immune_cells=500000
)

tumor, immune = patient.simulate(weeks=52)


plt.plot(tumor, label="Tumor Cells")
plt.plot(immune, label="Immune Cells")

plt.title("Digital Patient Twin Simulation")

plt.xlabel("Weeks")

plt.ylabel("Cell Count")

plt.legend()

plt.show()
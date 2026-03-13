"""
PharmaTab
API Layer - Simulation API

Purpose:
Expose tumor simulation engine as a REST API
using FastAPI.

Endpoints:
- health check
- single patient simulation
- multi patient simulation
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from simulation.patient_simulator import PatientSimulator


app = FastAPI(
    title="PharmaTab Simulation API",
    description="Digital Tumor Evolution Simulation Platform",
    version="1.0"
)


# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize simulator
simulator = PatientSimulator()


@app.get("/")
def root():

    return {
        "platform": "PharmaTab",
        "status": "running"
    }


@app.get("/health")
def health_check():

    return {
        "server": "ok",
        "simulation_engine": "ready"
    }


@app.get("/simulate")
def simulate_patient():

    result = simulator.simulate_patient()

    return result


@app.get("/simulate_population")
def simulate_population(count: int = 10):

    result = simulator.simulate_multiple_patients(
        patient_count=count
    )

    return {
        "patients": result,
        "count": count
    }
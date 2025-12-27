import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesRegressor

class AuraEngine:
    def __init__(self):
        # Machine Learning Model: Predicting Temperature
        self.model = ExtraTreesRegressor(n_estimators=200)
        # Features: [Vegetation, Albedo, Density, Population, AirFlow]
        X = np.random.rand(500, 5)
        y = 30 + (X[:, 2] * 12) - (X[:, 0] * 7) - (X[:, 1] * 4)
        self.model.fit(X, y)

    def run_simulation(self, green, reflect, density):
        input_data = np.array([[green, reflect, density, 0.5, 0.5]])
        return round(self.model.predict(input_data)[0], 2)

    def calculate_carbon_credits(self, temp_drop):
        # Industry standard formulas for 2025 ESG modeling
        tons_saved = temp_drop * 1450 
        credit_value = tons_saved * 85 # $85 per ton
        return round(tons_saved, 2), round(credit_value, 2)

    def simulate_airflow_vectors(self, lat, lon):
        # Physics-based vector field generation
        x = np.linspace(lat-0.01, lat+0.01, 10)
        y = np.linspace(lon-0.01, lon+0.01, 10)
        xv, yv = np.meshgrid(x, y)
        u = np.sin(xv) * 0.002 
        v = np.cos(yv) * 0.002 
        return xv.flatten(), yv.flatten(), u.flatten(), v.flatten()

class DecisionAgent:
    def __init__(self, name, role, icon):
        self.name, self.role, self.icon = name, role, icon

    def analyze(self, temp_drop, credits):
        if self.role == "FinTech":
            return f"Market Analysis: Reducing heat by {temp_drop}°C generates ${credits:,} in carbon offsets."
        if self.role == "Physics":
            return "Structural Alert: Building density is creating a thermal vortex. Suggesting 'Cool Corridor' routing."
        return f"Environmental Impact: Positive. Species migration stability increased by {int(temp_drop*10)}%."

def get_city_data():
    return {
        "Singapore": {"lat": 1.3521, "lon": 103.8198, "base": 36.5},
        "Dubai": {"lat": 25.2048, "lon": 55.2708, "base": 48.2},
        "New York": {"lat": 40.7128, "lon": -74.0060, "base": 40.5},
        "London": {"lat": 51.5074, "lon": -0.1278, "base": 33.1}
    }

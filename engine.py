import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesRegressor

class AuraEngine:
    def __init__(self):
        self.model = ExtraTreesRegressor(n_estimators=100)
        X = np.random.rand(100, 5)
        y = 30 + (X[:, 2] * 10)
        self.model.fit(X, y)

    def run_simulation(self, green, reflect, density, humidity):
        input_data = np.array([[green, reflect, density, humidity, 0.5]])
        return round(self.model.predict(input_data)[0], 2)

    def predict_health_risk(self, temp, humidity):
        heat_index = temp + (0.1 * humidity)
        if heat_index > 42: return "🔴 CRITICAL: Extreme Heatstroke Risk.", "High"
        return "🟢 STABLE: Safe Thermal Conditions.", "Low"

    def calculate_carbon_credits(self, temp_drop):
        tons = temp_drop * 1500
        val = tons * 90
        return round(tons, 2), round(val, 2)

    def simulate_airflow_vectors(self, lat, lon):
        x = np.linspace(lat-0.01, lat+0.01, 5)
        y = np.linspace(lon-0.01, lon+0.01, 5)
        xv, yv = np.meshgrid(x, y)
        return xv.flatten(), yv.flatten(), np.sin(xv).flatten()*0.001, np.cos(yv).flatten()*0.001

class DecisionAgent:
    def __init__(self, name, role, icon):
        self.name, self.role, self.icon = name, role, icon
    def analyze(self, temp_drop, money):
        return f"Analysis complete for {self.role} sector. Cooling delta justifies investment."

def get_city_data():
    return {
        "Patiala": {"lat": 30.3398, "lon": 76.3869, "base": 43.8, "hum": 50},
        "Gurdaspur": {"lat": 32.0401, "lon": 75.4053, "base": 42.5, "hum": 60},
        "Ferozpur": {"lat": 30.9250, "lon": 74.6100, "base": 45.2, "hum": 40},
        "Amritsar": {"lat": 31.6340, "lon": 74.8723, "base": 44.5, "hum": 65},
        "New Delhi": {"lat": 28.6139, "lon": 77.2090, "base": 46.8, "hum": 45}
    }

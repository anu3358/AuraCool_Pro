import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesRegressor

class AuraEngine:
    def __init__(self):
        self.model = ExtraTreesRegressor(n_estimators=200)
        # Features: [Vegetation, Albedo, Density, Humidity, AirFlow]
        X = np.random.rand(500, 5)
        y = 30 + (X[:, 2] * 12) - (X[:, 0] * 7) - (X[:, 3] * 5)
        self.model.fit(X, y)

    def run_simulation(self, green, reflect, density, humidity):
        input_data = np.array([[green, reflect, density, humidity, 0.5]])
        return round(self.model.predict(input_data)[0], 2)

    def predict_health_risk(self, temp, humidity):
        heat_index = temp + (0.1 * humidity)
        if heat_index > 45: return "🔴 CRITICAL: Extreme Heatstroke Risk. Emergency cooling required.", "High"
        if heat_index > 38: return "🟡 WARNING: High Dehydration & Crop Stress Risk.", "Medium"
        return "🟢 STABLE: Normal Thermal Conditions.", "Low"

    def calculate_carbon_credits(self, temp_drop):
        tons_saved = temp_drop * 1850 
        credit_value = tons_saved * 92 
        return round(tons_saved, 2), round(credit_value, 2)

    def simulate_airflow_vectors(self, lat, lon):
        x = np.linspace(lat-0.01, lat+0.01, 10)
        y = np.linspace(lon-0.01, lon+0.01, 10)
        xv, yv = np.meshgrid(x, y)
        u, v = np.sin(xv) * 0.002, np.cos(yv) * 0.002 
        return xv.flatten(), yv.flatten(), u.flatten(), v.flatten()

def get_city_data():
    return {
        "Gurdaspur (Border Region)": {"lat": 32.0401, "lon": 75.4053, "base": 42.5, "hum": 60},
        "Patiala (Royal City)": {"lat": 30.3398, "lon": 76.3869, "base": 43.8, "hum": 50},
        "Ferozpur (Western Frontier)": {"lat": 30.9250, "lon": 74.6100, "base": 45.2, "hum": 40},
        "Amritsar": {"lat": 31.6340, "lon": 74.8723, "base": 44.5, "hum": 65},
        "Chandigarh": {"lat": 30.7333, "lon": 76.7794, "base": 41.2, "hum": 55},
        "New Delhi": {"lat": 28.6139, "lon": 77.2090, "base": 46.8, "hum": 45}
    }

import numpy as np

class AuraEngine:
    def run_simulation(self, green, albedo, humidity, base_temp):
        # Physics: Cooling efficiency drops as humidity rises (Wet Bulb effect)
        efficiency = 1.0 - (humidity * 0.25)
        mitigation = (green * 14.0 + albedo * 9.5) * efficiency
        return max(base_temp - mitigation, 22.0)

    def calculate_svf(self, density):
        # Sky View Factor: 1.0 is open sky, 0.1 is deep urban canyon
        svf = max(1.0 - (density / 1000), 0.1)
        trapped_heat = (1.0 - svf) * 5.5
        return svf, trapped_heat

    def predict_health_risk(self, temp, humidity):
        heat_index = temp + (0.55 * (humidity * 100 - 55))
        if heat_index > 42: return "🔴 CRITICAL: IMMEDIATE THERMAL INTERVENTION REQUIRED", "LEVEL 5"
        if heat_index > 35: return "🟠 SEVERE: HEAT EXHAUSTION PROTOCOL ACTIVE", "LEVEL 3"
        return "🟢 STABLE: THERMAL LOADS WITHIN NOMINAL RANGE", "LEVEL 1"

    def calculate_carbon_credits(self, delta):
        # 1 degree drop = ~480 tons of CO2 offset for a district
        tons = delta * 480
        return tons, tons * 28.5 # Value in USD

def get_city_data():
    return {
        "Gurdaspur": {"lat": 32.0416, "lon": 75.4053, "base": 42.1, "hum": 0.52},
        "Ferozpur": {"lat": 30.9250, "lon": 74.6225, "base": 45.8, "hum": 0.32},
        "Ludhiana": {"lat": 30.9010, "lon": 75.8573, "base": 46.2, "hum": 0.44},
        "Amritsar": {"lat": 31.6340, "lon": 74.8723, "base": 44.5, "hum": 0.40},
        "Patiala": {"lat": 30.3398, "lon": 76.3869, "base": 43.8, "hum": 0.48}
    }

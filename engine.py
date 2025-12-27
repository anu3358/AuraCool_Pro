import numpy as np

class AuraEngine:
    def __init__(self):
        self.base_albedo = 0.15  # Standard asphalt/concrete
        self.target_temp = 25.0  # Ideal urban temp

    def run_simulation(self, green_cover, albedo_boost, humidity, ambient_temp):
        """
        Advanced Urban Heat Island (UHI) Mitigation Formula.
        Calculates cooling based on Evapotranspiration (Trees) and 
        Radiative Forcing (Albedo).
        """
        # Cooling from Trees: 10% green cover can drop temp by ~1.2°C
        tree_cooling = green_cover * 12.0 
        
        # Cooling from Albedo: Reflecting solar radiation
        albedo_cooling = albedo_boost * 8.0
        
        # Humidity penalty: High humidity reduces evapotranspiration efficiency
        efficiency = 1.0 - (humidity * 0.3)
        
        final_mitigation = (tree_cooling + albedo_cooling) * efficiency
        return max(ambient_temp - final_mitigation, 20.0)

    def calculate_svf_impact(self, building_density):
        """
        Sky View Factor (SVF) Simulation.
        Measures how much heat is trapped in 'Urban Canyons'.
        """
        # SVF ranges from 0 (closed canyon) to 1 (open field)
        svf = max(1.0 - (building_density / 1000), 0.1)
        # Heat trapping increases as SVF decreases
        trapped_heat = (1.0 - svf) * 4.5 
        return svf, trapped_heat

    def predict_health_risk(self, temp, humidity):
        """Heat Index based health risk assessment."""
        heat_index = temp + 0.55 * (humidity * 100 - 55) # Simplified formula
        
        if heat_index > 45:
            return "🔴 EXTREME DANGER: High risk of Heatstroke.", "CRITICAL"
        elif heat_index > 38:
            return "🟠 WARNING: Severe exhaustion possible.", "HIGH"
        elif heat_index > 30:
            return "🟡 CAUTION: Fatigue during physical activity.", "MODERATE"
        else:
            return "🟢 STABLE: Low thermal stress.", "LOW"

    def calculate_carbon_credits(self, temp_reduction):
        """Monetizes cooling into Carbon Credits (Tons of CO2 saved)."""
        # Assumption: 1°C drop saves ~5% of AC energy in a district
        co2_saved = temp_reduction * 450  # Tons of CO2
        market_price = 25  # USD per Ton
        return co2_saved, co2_saved * market_price

    def simulate_airflow_vectors(self, lat, lon):
        """Generates wind flow data for visualization."""
        x, y = np.meshgrid(np.linspace(lat-0.02, lat+0.02, 10), 
                           np.linspace(lon-0.02, lon+0.02, 10))
        u = np.cos(x) * 0.1 # Simulated wind X
        v = np.sin(y) * 0.1 # Simulated wind Y
        return x, y, u, v

def get_city_data():
    """Real-world coordinates and baseline stats for Punjab Districts."""
    return {
        "Ludhiana": {"lat": 30.9010, "lon": 75.8573, "base": 44.5, "hum": 45},
        "Amritsar": {"lat": 31.6340, "lon": 74.8723, "base": 43.2, "hum": 40},
        "Jalandhar": {"lat": 31.3260, "lon": 75.5762, "base": 42.8, "hum": 42},
        "Patiala": {"lat": 30.3398, "lon": 76.3869, "base": 43.5, "hum": 48},
        "Bathinda": {"lat": 30.2110, "lon": 74.9455, "base": 46.2, "hum": 30}
    }

class DecisionAgent:
    def __init__(self, name, role, avatar):
        self.name = name
        self.role = role
        self.avatar = avatar

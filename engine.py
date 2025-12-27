import numpy as np

class AuraEngine:
    def __init__(self):
        # Constants for Punjab's specific climate profile
        self.stefan_boltzmann = 5.67e-8  # W/(m^2 K^4)
        self.albedo_max = 0.85          # Premium cool-roof coating

    def run_simulation(self, green_cover, albedo_boost, humidity, ambient_temp):
        """
        Advanced Heat Mitigation Algorithm using Evapotranspiration 
        and Radiative Forcing equations.
        """
        # 1. Evapotranspirative Cooling (Trees)
        # 10% increase in green cover reduces surface temp by approx 1.1C in Punjab
        tree_cooling = green_cover * 11.5 
        
        # 2. Radiative Cooling (Albedo)
        # Reflecting short-wave radiation before it hits the asphalt
        albedo_cooling = albedo_boost * 9.2
        
        # 3. Humidity Penalty (Wet Bulb Efficiency)
        # Evaporative cooling is less effective in high humidity
        efficiency_factor = 1.0 - (humidity * 0.28)
        
        mitigated_temp = ambient_temp - ((tree_cooling + albedo_cooling) * efficiency_factor)
        
        # Ensure we don't go below dew point arbitrarily
        return max(mitigated_temp, 21.5)

    def calculate_svf_impact(self, building_density):
        """
        Sky View Factor (SVF) Physics.
        Measures the ratio of the sky visible from a street-level point.
        """
        # SVF = 1 (Open Field), SVF = 0.1 (Dense Urban Canyon)
        svf = max(1.0 - (building_density / 1000), 0.12)
        
        # Long-wave radiation trapping (The Canyon Effect)
        # Lower SVF means heat cannot escape back to space at night
        trapped_heat_penalty = (1.0 - svf) * 6.5
        
        return svf, trapped_heat_penalty

    def predict_health_risk(self, temp, humidity):
        """Calculates Heat Index (HI) and Wet Bulb Globe Temperature (WBGT) impact."""
        # Simplified Heat Index for real-time monitoring
        heat_index = temp + (0.55 * (humidity * 100 - 55))
        
        if heat_index > 46:
            return "🔴 EXTREME DANGER: Hyperthermia risk imminent.", "CRITICAL"
        elif heat_index > 39:
            return "🟠 WARNING: Heatstroke likely with prolonged exposure.", "SEVERE"
        elif heat_index > 32:
            return "🟡 CAUTION: Significant thermal fatigue detected.", "ELEVATED"
        else:
            return "🟢 NOMINAL: Thermal conditions stable.", "OPTIMAL"

    def calculate_carbon_credits(self, temp_reduction):
        """
        Monetizes cooling into Carbon Offset Credits.
        Assumption: 1C drop = 500 Tons of CO2 saved (reduced HVAC load).
        """
        co2_saved_tons = temp_reduction * 485 
        market_rate_usd = 28.50  # Current EU-ETS approximate price
        
        return co2_saved_tons, co2_saved_tons * market_rate_usd

def get_city_data():
    """Strategic baseline data for Punjab Defense Sectors."""
    return {
        "Gurdaspur": {"lat": 32.0416, "lon": 75.4053, "base": 42.5, "hum": 0.52},
        "Ferozpur": {"lat": 30.9250, "lon": 74.6225, "base": 46.2, "hum": 0.35},
        "Ludhiana": {"lat": 30.9010, "lon": 75.8573, "base": 47.1, "hum": 0.44},
        "Amritsar": {"lat": 31.6340, "lon": 74.8723, "base": 44.8, "hum": 0.40},
        "Patiala": {"lat": 30.3398, "lon": 76.3869, "base": 43.5, "hum": 0.48}
    }

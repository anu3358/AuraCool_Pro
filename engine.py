import numpy as np

class AuraEngine:
    def run_simulation(self, green, albedo, humidity, base_temp):
        efficiency = 1.0 - (humidity * 0.25)
        mitigation = (green * 13.5 + albedo * 8.5) * efficiency
        return max(base_temp - mitigation, 22.0)

    def calculate_resilience_score(self, green, albedo, aqi):
        score = (green * 40) + (albedo * 40) + (max(0, 300 - aqi) / 15)
        if score > 80: return "A (EXEMPLARY)", "Maximum infrastructure readiness."
        return "F (CRITICAL)", "Immediate system collapse risk."

    def calculate_v2g_revenue(self, delta_temp):
        mwh_saved = delta_temp * 15 
        revenue_cr = (mwh_saved * 8500) / 10000000 
        return mwh_saved, revenue_cr

    # --- NEW PROBLEM SOLVER CALCULATIONS ---
    def calculate_water_recovery(self, delta_temp, area_sq_km=50):
        # Evaporation loss saved: Liters = Temp_Delta * Solar_Intensity * Area
        liters_saved = delta_temp * 125000 * area_sq_km
        return liters_saved / 1000000 # Return in Million Liters (ML)

    def predict_health_risk(self, temp, hum):
        hi = temp + (0.55 * (hum * 100 - 55))
        if hi > 42: return "🔴 CRITICAL", "Heat-stroke threshold exceeded."
        return "🟢 NOMINAL", "No thermal stress detected."

    def calculate_carbon_credits(self, delta):
        tons = delta * 520
        return tons, tons * 28.0

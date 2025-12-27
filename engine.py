import numpy as np

class AuraEngine:
    def run_simulation(self, green, albedo, humidity, base_temp):
        efficiency = 1.0 - (humidity * 0.25)
        # Scientific scaling for Punjab's arid/semi-arid climate
        mitigation = (green * 13.5 + albedo * 8.5) * efficiency
        return max(base_temp - mitigation, 22.0)

    def calculate_resilience_score(self, green, albedo, aqi):
        # A weighted index: Greenery (40%), Albedo (40%), AQI (20%)
        score = (green * 40) + (albedo * 40) + (max(0, 300 - aqi) / 15)
        if score > 80: return "A (EXEMPLARY)", "Maximum infrastructure readiness."
        if score > 60: return "B (STABLE)", "Standard operational capacity."
        if score > 40: return "C (VULNERABLE)", "Infrastructure stress detected."
        return "F (CRITICAL)", "Immediate system collapse risk."

    def calculate_v2g_revenue(self, delta_temp):
        # 1 degree drop reduces peak AC load by approx 15 MegaWatts per district
        mwh_saved = delta_temp * 15 
        # Energy arbitrage value in Crores (Avg peak power cost)
        revenue_cr = (mwh_saved * 8500) / 10000000 
        return mwh_saved, revenue_cr

    def predict_health_risk(self, temp, hum):
        # Wet Bulb/Heat Index hybrid
        hi = temp + (0.55 * (hum * 100 - 55))
        if hi > 42: return "🔴 CRITICAL", "Heat-stroke threshold exceeded."
        if hi > 35: return "🟠 ELEVATED", "Dehydration risk for laborers."
        return "🟢 NOMINAL", "No thermal stress detected."

    def calculate_carbon_credits(self, delta):
        # 1C drop = ~520 Tons of CO2 equivalent offset
        tons = delta * 520
        return tons, tons * 28.0 # Valued at $28 per ton

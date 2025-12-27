import numpy as np

class AuraEngine:
    def run_simulation(self, green, albedo, humidity, base_temp):
        efficiency = 1.0 - (humidity * 0.25)
        mitigation = (green * 13.5 + albedo * 8.5) * efficiency
        return max(base_temp - mitigation, 22.0)

    def calculate_resilience_score(self, green, albedo, aqi):
        # A weighted score out of 100
        score = (green * 40) + (albedo * 40) + (max(0, 200 - aqi) / 10)
        if score > 85: return "A (STABLE)", "Low vulnerability"
        if score > 70: return "B (MODERATE)", "Early intervention required"
        return "D (CRITICAL)", "Immediate infrastructure failure risk"

    def calculate_v2g_revenue(self, delta_temp):
        # Calculates energy saved from AC load reduction + grid stabilization
        # 1 degree drop saves ~15MW of peak demand in a district
        mwh_saved = delta_temp * 15 
        revenue_cr = (mwh_saved * 8000) / 10000000 # Convert to Crores
        return mwh_saved, revenue_cr

    def predict_health_risk(self, temp, hum):
        hi = temp + (0.55 * (hum * 100 - 55))
        if hi > 40: return "🔴 EXTREME", "Hospital surge predicted"
        return "🟢 STABLE", "Nominal public health load"

    def calculate_carbon_credits(self, delta):
        tons = delta * 520
        return tons, tons * 28.0 # USD value

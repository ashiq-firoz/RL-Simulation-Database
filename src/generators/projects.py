import pandas as pd
import os

def generate_projects():
    # Realistic mapping of teams to specific strategic themes
    # Types: Engineering, Marketing, Operations, Product, Security
    project_list = [
        # --- INFRASTRUCTURE (Team: Infrastructure) ---
        {"p_id": "P-01", "name": "Project Apollo: Kubernetes Migration", "type": "Engineering", "team": "Infrastructure", "priority": "Critical", "quarter": "Q1"},
        {"p_id": "P-02", "name": "Zero-Trust Security Audit", "type": "Security", "team": "Infrastructure", "priority": "High", "quarter": "Q1"},
        {"p_id": "P-11", "name": "Multi-Region Failover Setup", "type": "Engineering", "team": "Infrastructure", "priority": "Medium", "quarter": "Q2"},
        {"p_id": "P-21", "name": "Cloud Cost Optimization (FinOps)", "type": "Operations", "team": "Infrastructure", "priority": "Low", "quarter": "Q2"},

        # --- PRODUCT WEB (Team: Product-Web) ---
        {"p_id": "P-03", "name": "Titan: Legacy Refactor", "type": "Engineering", "team": "Product-Web", "priority": "High", "quarter": "Q1"},
        {"p_id": "P-08", "name": "Accessibility (WCAG) Compliance", "type": "Product", "team": "Product-Web", "priority": "Medium", "quarter": "Q2"},
        {"p_id": "P-12", "name": "Checkout Flow Redesign", "type": "Product", "team": "Product-Web", "priority": "High", "quarter": "Q1"},
        {"p_id": "P-22", "name": "Internal Admin Dashboard v3", "type": "Engineering", "team": "Product-Web", "priority": "Low", "quarter": "Q3"},

        # --- GROWTH (Team: Growth) ---
        {"p_id": "P-04", "name": "Viral Loop: Referral Engine", "type": "Marketing", "team": "Growth", "priority": "High", "quarter": "Q1"},
        {"p_id": "P-07", "name": "Project Helios: SEO Dominance", "type": "Marketing", "team": "Growth", "priority": "Medium", "quarter": "Q2"},
        {"p_id": "P-13", "name": "A/B Testing Framework Integration", "type": "Engineering", "team": "Growth", "priority": "Medium", "quarter": "Q1"},
        {"p_id": "P-23", "name": "User Reactivation Campaign", "type": "Marketing", "team": "Growth", "priority": "High", "quarter": "Q3"},

        # --- DATA SCIENCE (Team: Data-Science) ---
        {"p_id": "P-05", "name": "Project Oracle: Churn Prediction", "type": "Engineering", "team": "Data-Science", "priority": "High", "quarter": "Q2"},
        {"p_id": "P-09", "name": "Warehouse ETL Automation", "type": "Engineering", "team": "Data-Science", "priority": "Medium", "quarter": "Q1"},
        {"p_id": "P-14", "name": "Real-time Personalization API", "type": "Engineering", "team": "Data-Science", "priority": "Critical", "quarter": "Q2"},
        {"p_id": "P-24", "name": "Customer Segmentation Model", "type": "Data-Science", "team": "Data-Science", "priority": "Low", "quarter": "Q4"},

        # --- BRAND & DESIGN (Team: Brand-Design) ---
        {"p_id": "P-10", "name": "Brand Refresh 2026", "type": "Marketing", "team": "Brand-Design", "priority": "Critical", "quarter": "Q2"},
        {"p_id": "P-06", "name": "Project Prism: Design System v2", "type": "Product", "team": "Brand-Design", "priority": "Medium", "quarter": "Q1"},
        {"p_id": "P-15", "name": "Podcast Series Production", "type": "Marketing", "team": "Brand-Design", "priority": "Low", "quarter": "Q3"},
        {"p_id": "P-25", "name": "Annual Impact Report", "type": "Marketing", "team": "Brand-Design", "priority": "Medium", "quarter": "Q4"},
        
        # --- GENERAL / CROSS-FUNCTIONAL ---
        {"p_id": "P-16", "name": "Employee Onboarding Revamp", "type": "Operations", "team": "Infrastructure", "priority": "Low", "quarter": "Q1"},
        {"p_id": "P-17", "name": "SOC2 Compliance Readiness", "type": "Security", "team": "Infrastructure", "priority": "Critical", "quarter": "Q2"},
        {"p_id": "P-18", "name": "Global Expansion: LATAM Market", "type": "Marketing", "team": "Growth", "priority": "High", "quarter": "Q4"},
        {"p_id": "P-19", "name": "Developer Experience (DevEx) Survey", "type": "Engineering", "team": "Product-Web", "priority": "Low", "quarter": "Q2"},
        {"p_id": "P-20", "name": "Mobile App UI Audit", "type": "Product", "team": "Brand-Design", "priority": "Medium", "quarter": "Q3"}
    ]

    os.makedirs('data', exist_ok=True)
    df = pd.DataFrame(project_list)
    df.to_csv("data/projects.csv", index=False)
    
    print(f"Created: data/projects.csv ({len(df)} Realistic Projects across 5 Teams)")
    print("\n--- Project Preview ---")
    print(df[['p_id', 'name', 'team', 'priority']].head(10).to_string(index=False))

if __name__ == "__main__":
    generate_projects()
# A POSSIBLE SOLUTION IMPLEMENTING THE WHOLE SEQUENCE OF STEPS

import csv

file_path = 'trase_global_coffee_supply_chain.csv'

# -------------------------------------------------------------------
# STEP 1: `for-in` loop on file iterator to map ports & accumulate total FOB
# -------------------------------------------------------------------
port_fob_totals = {}

with open(file_path, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        port = row['port_of_export_name']
        fob = row['fob']
        if port and fob:
            port_fob_totals[port] = port_fob_totals.get(port, 0.0) + float(fob)

print("=== STEP 1: PORT FOB TOTALS ===")
for port_name, total_fob in port_fob_totals.items():
    print(f"Port: {port_name:<30} | Total FOB: ${total_fob:,.2f}")


# -------------------------------------------------------------------
# STEP 2: `if` statement to narrow records > $50,000 FOB valuation
# -------------------------------------------------------------------
high_value_shipments = []

with open(file_path, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        if row['fob'] and float(row['fob']) > 50000.0:
            high_value_shipments.append(row)

print(f"\n=== STEP 2: HIGH-VALUE FILTER ===")
print(f"Isolated {len(high_value_shipments)} shipments exceeding $50,000 FOB.")


# -------------------------------------------------------------------
# STEP 3: `match-case` pattern matching on HS6 product codes
# -------------------------------------------------------------------
for row in high_value_shipments:
    match row['hs6']:
        case '090111' | '90111':
            category = "Unroasted Green Coffee Beans"
        case '090112' | '90112':
            category = "Decaffeinated Coffee Beans"
        case '210111' | '210111.0':
            category = "Instant Coffee Extracts & Derivatives"
        case _:
            category = "Other Processed Coffee Derivative"
    
    row['product_category'] = category

print("\n=== STEP 3: PRODUCT TYPE CLASSIFICATION ===")
for row in high_value_shipments:
    print(f"HS {row['hs6']} ({row['product_category']}) | FOB: ${float(row['fob']):,.2f} -> Destination: {row['country_of_first_import']}")


# -------------------------------------------------------------------
# STEP 4: `elif` decision chain for regional compliance protocols
# -------------------------------------------------------------------
for row in high_value_shipments:
    bloc = row['country_of_first_import_economic_bloc']
    
    if bloc == 'EUROPEAN UNION':
        protocol = "EUDR Geolocation & Deforestation Audit"
    elif bloc == 'UNITED STATES':
        protocol = "US CBP Agriculture Inspection"
    elif bloc == 'CHINA (MAINLAND)':
        protocol = "GACC Custom Hygiene Clearance"
    else:
        protocol = "Standard MFN Customs Verification"
        
    row['audit_protocol'] = protocol

print("\n=== STEP 4: REGULATORY COMPLIANCE TIERS ===")
for row in high_value_shipments:
    print(f"Destination: {row['country_of_first_import']:<15} | Economic Bloc: {row['country_of_first_import_economic_bloc']:<15} | Protocol: {row['audit_protocol']}")


# -------------------------------------------------------------------
# STEP 5: `while` loop to accumulate audit sample up to 100 raw tons
# -------------------------------------------------------------------
audit_sample_batch = []
accumulated_raw_mass = 0.0
target_quota_tons = 100.0
index = 0

while accumulated_raw_mass < target_quota_tons and index < len(high_value_shipments):
    current_shipment = high_value_shipments[index]
    raw_mass = float(current_shipment['mass_tonnes_raw_equivalent'])
    
    accumulated_raw_mass += raw_mass
    audit_sample_batch.append(current_shipment)
    index += 1

print(f"\n=== STEP 5: AUDIT SAMPLE ACCUMULATION ===")
print(f"Selected {len(audit_sample_batch)} shipments totaling {accumulated_raw_mass:.2f} raw equivalent metric tons.")


# -------------------------------------------------------------------
# STEP 6: `if-else` verification of quota completion
# -------------------------------------------------------------------
print("\n=== STEP 6: QUOTA VERIFICATION ===")
if accumulated_raw_mass >= target_quota_tons:
    print(f"STATUS: SUCCESS. Target sampling quota of {target_quota_tons} tons met.")
    print("Final Audit Sample Breakdown:")
    for item in audit_sample_batch:
        print(f"  - Exporter: {item['exporter_name'][:25]:<25} | Port: {item['port_of_export_name']:<15} | Raw Tons: {float(item['mass_tonnes_raw_equivalent']):6.2f} t | Protocol: {item['audit_protocol']}")
else:
    print(f"STATUS: SHORTFALL. Collected {accumulated_raw_mass:.2f} tons out of required {target_quota_tons} tons.")
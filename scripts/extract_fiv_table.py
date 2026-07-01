import sys
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import re

fiv_url = sys.argv[1]
output_path = sys.argv[2]

print("Starting browser automation for FIV Portal...")
print(f"URL: {fiv_url}")

# Setup Chrome driver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in background
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    # Load the page
    print("Loading page...")
    driver.get(fiv_url)
    
    # Wait for table to load (adjust timeout as needed)
    wait = WebDriverWait(driver, 10)
    table = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
    
    print("Table found! Extracting content...")
    
    # Get all tables on the page
    tables = driver.find_elements(By.TAG_NAME, "table")
    
    osxml_table = None
    pnp_pm_table = None
    osxml_table_element = None
    pnp_pm_table_element = None

    for idx, tbl in enumerate(tables):
        # Extract rows to analyze table content
        rows = []
        tr_elements = tbl.find_elements(By.TAG_NAME, "tr")

        for tr in tr_elements:
            cells = []
            td_elements = tr.find_elements(By.TAG_NAME, "td")
            th_elements = tr.find_elements(By.TAG_NAME, "th")

            all_cells = td_elements + th_elements

            for cell in all_cells:
                text = cell.text.strip()
                cells.append(text)

            if cells:
                rows.append(cells)

        # Identify table type by checking first row headers
        if rows:
            first_row = rows[0]
            first_row_lower = [cell.lower() for cell in first_row]

            # Check if this is OSXML table:
            # Format A: first row contains 'imh' or 'cbb' (mega-row or direct label)
            # Format B: first row contains 'osxml in bios' or 'osxml in simics'
            # Also check all rows for format B header
            has_osxml_header = any('osxml in bios' in c or 'osxml in simics' in c for c in first_row_lower)
            if not has_osxml_header:
                for row in rows[1:4]:
                    row_l = [cell.lower() for cell in row]
                    if any('osxml in bios' in c or 'osxml in simics' in c for c in row_l):
                        has_osxml_header = True
                        break
            has_imh_cbb = any('imh' in c for c in first_row_lower) or any('cbb' in c for c in first_row_lower)
            if (has_osxml_header or has_imh_cbb) and osxml_table is None:
                osxml_table = (idx + 1, rows)
                osxml_table_element = tbl
                print(f"\n>>> Identified OSXML Table: Table {idx+1}")

            # Check if this is PnP/PM table (contains Domain, PnP Version, PM Version)
            if 'domain' in first_row_lower and 'pnp version' in first_row_lower and 'pm version' in first_row_lower:
                pnp_pm_table = (idx + 1, rows)
                pnp_pm_table_element = tbl
                print(f">>> Identified PnP/PM Table: Table {idx+1}")

        # Print table preview
        print(f"\n=== Table {idx+1} ({len(rows)} rows) ===")
        for row in rows[:3]:  # Show first 3 rows
            print(" | ".join(row))

    # Save only key tables (HTML only, CSV will be in the summary)
    saved_tables = []
    if osxml_table:
        table_html = osxml_table_element.get_attribute("outerHTML")
        html_file = f"{output_path}/FIV_Table_OSXML.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(table_html)
        saved_tables.append("OSXML")
        print(f"\n[OK] Saved OSXML Table: {html_file}")

    if pnp_pm_table:
        table_html = pnp_pm_table_element.get_attribute("outerHTML")
        html_file = f"{output_path}/FIV_Table_PnP_PM.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(table_html)
        saved_tables.append("PnP/PM")
        print(f"[OK] Saved PnP/PM Table: {html_file}")
    
    print(f"\n\n=== SUMMARY ===")
    print(f"OSXML Table: {osxml_table[0] if osxml_table else 'Not found'}")
    print(f"PnP/PM Table: {pnp_pm_table[0] if pnp_pm_table else 'Not found'}")
    
    # Extract Orange ID and BIOS ID from page text
    body_text = driver.find_element(By.TAG_NAME, "body").text
    lines = body_text.split('\n')

    orange_id = None
    bios_id = None
    unified_patch_version = None
    simics_version = None
    platform_stepping = None  # Will store AP1/AP2 and A0/B0
    ifwi_type = 'Orange'  # Default to Orange, will be updated if Purple detected

    import re

    # First try to extract IFWI ID and type from URL
    # Support both Orange and Purple IFWI
    url_match = re.search(r'(Orange|Purple)/(2026\.[^/]+)/', fiv_url)
    if url_match:
        ifwi_type = url_match.group(1)
        orange_id = url_match.group(2)
        print(f"Auto-detected {ifwi_type} IFWI ID: {orange_id}")

    # Detect platform and stepping from page text
    # Priority 1: Check first line title (most reliable)
    # Format: "SiEn-OakStream-DiamondRapids AP AP1-A0.POST-SILICON" or "AP1-B0.PRE-SILICON"
    # Priority 2: Check body text for "AP1 pre", "AP1 A0 post", etc.

    if lines:
        first_line_lower = lines[0].lower()
        # Check format "AP1-A0.POST" or "AP1-B0.PRE"
        if 'ap1' in first_line_lower and 'a0' in first_line_lower and 'post' in first_line_lower:
            platform_stepping = 'AP1 A0'
        elif 'ap1' in first_line_lower and 'b0' in first_line_lower and 'pre' in first_line_lower:
            platform_stepping = 'AP1 B0'
        elif 'ap2' in first_line_lower and 'a0' in first_line_lower and 'post' in first_line_lower:
            platform_stepping = 'AP2 A0'
        elif 'ap2' in first_line_lower and 'b0' in first_line_lower and 'pre' in first_line_lower:
            platform_stepping = 'AP2 B0'
        elif 'ap2' in first_line_lower and 'a0' in first_line_lower and 'pre' in first_line_lower:
            platform_stepping = 'AP2 A0'

    # If not found in first line, search in body text
    if not platform_stepping or platform_stepping == 'N/A':
        for line in lines:
            line_lower = line.lower()
            # Check for AP1 Pre-Silicon (B0)
            if 'ap1' in line_lower and 'pre' in line_lower and ('silicon' in line_lower or 'pre-silicon' in line_lower):
                platform_stepping = 'AP1 B0'
                break
            # Check for AP1 A0 post silicon
            elif 'ap1' in line_lower and 'a0' in line_lower and 'post' in line_lower:
                platform_stepping = 'AP1 A0'
                break
            # Check for AP2 A0 post silicon
            elif 'ap2' in line_lower and 'a0' in line_lower and 'post' in line_lower:
                platform_stepping = 'AP2 A0'
                break
            # Check for AP2 Pre-Silicon (A0 or B0)
            elif 'ap2' in line_lower and 'pre' in line_lower and ('silicon' in line_lower or 'pre-silicon' in line_lower):
                # AP2 Pre-Silicon is typically A0
                platform_stepping = 'AP2 A0'
                break
            # For Purple IFWI: Check issue tags like "[DMR AP1 A0]"
            elif '[dmr ap1 a0]' in line_lower or '[dmr ap1 b0]' in line_lower:
                if 'a0]' in line_lower:
                    platform_stepping = 'AP1 A0'
                else:
                    platform_stepping = 'AP1 B0'
                break
            elif '[dmr ap2 a0]' in line_lower or '[dmr ap2 b0]' in line_lower:
                if 'a0]' in line_lower:
                    platform_stepping = 'AP2 A0'
                else:
                    platform_stepping = 'AP2 B0'
                break

    for i, line in enumerate(lines):
        if not orange_id and 'Orange' in line and '2026' in line:
            parts = line.split()
            for part in parts:
                if part.startswith('2026.'):
                    orange_id = part
                    break
        # Look for BIOSID pattern in text (0035.Dxx or 0036.Dxx)
        if 'BIOSID' in line:
            bios_match = re.search(r'00[0-9]{2}\.[A-Z]\d+', line)
            if bios_match:
                bios_id = bios_match.group(0)

        # Look for AP2 B0 UP or AP1 B0 UP patterns (Unified Patch hex IDs)
        # Pattern like "AP2 B0 UP 5200020E" or "Unified Patch | 5200020E"
        up_match = re.search(r'UP\s+([A-F0-9]{8})', line, re.IGNORECASE)
        if up_match and not unified_patch_version:
            unified_patch_version = up_match.group(1)

        # Look for Simics version pattern: "Simics dmr-rio-7 2026ww23.6.00_03 Pre539"
        # Pattern: Simics followed by dmr- and version info with ww and Pre
        if not simics_version and 'Simics' in line and 'dmr-' in line and 'ww' in line:
            simics_match = re.search(r'Simics\s+(dmr-[^\s]+\s+\S+ww\S+\s+Pre\d+)', line, re.IGNORECASE)
            if simics_match:
                simics_version = simics_match.group(1)
    
    # Also search ingredient tables for 'UPatch' or 'Unified Patch'
    # AND detect platform from ingredient names (useful for Purple IFWI)
    all_tables = driver.find_elements(By.TAG_NAME, "table")
    for tbl in all_tables:
        rows = tbl.find_elements(By.TAG_NAME, "tr")
        for tr in rows:
            cells = tr.find_elements(By.TAG_NAME, "td")
            cell_texts = [c.text.strip() for c in cells]
            if len(cell_texts) >= 2:
                row_str = ' '.join(cell_texts).lower()
                # Look for BIOSID row in ingredient table
                if cell_texts[0] == 'BIOSID' and len(cell_texts) > 1:
                    bios_match = re.search(r'00[0-9]{2}\.[A-Z][0-9]+', cell_texts[1])
                    if bios_match:
                        bios_id = bios_match.group(0)
                # Look for UPatch or Unified Patch
                if 'upatch' in row_str or ('unified' in row_str and 'patch' in row_str):
                    for cell in cell_texts:
                        hex_match = re.match(r'^[A-F0-9]{8}$', cell.strip(), re.IGNORECASE)
                        if hex_match:
                            unified_patch_version = cell.strip().upper()
                            break

                # Detect platform from ingredient names (fallback for Purple IFWI)
                # Example: "DMRAP_Unified_Patch_AP1_A0" or "DMRAP_Unified_Patch_AP2_A0"
                if not platform_stepping or platform_stepping == 'N/A':
                    ingredient_name = cell_texts[0] if len(cell_texts) > 0 else ''
                    if 'DMRAP_Unified_Patch_AP1_A0' in ingredient_name or 'AP1_A0' in ingredient_name:
                        platform_stepping = 'AP1 A0'
                    elif 'DMRAP_Unified_Patch_AP1_B0' in ingredient_name or 'AP1_B0' in ingredient_name:
                        platform_stepping = 'AP1 B0'
                    elif 'DMRAP_Unified_Patch_AP2_A0' in ingredient_name or 'AP2_A0' in ingredient_name:
                        platform_stepping = 'AP2 A0'
                    elif 'DMRAP_Unified_Patch_AP2_B0' in ingredient_name or 'AP2_B0' in ingredient_name:
                        platform_stepping = 'AP2 B0'

    # No longer use BIOS ID to determine AP1/AP2 - must detect from page text only

    # Check for Emulation info in the page text
    has_emulation = False
    for line in lines:
        if 'emulation info' in line.lower() or 'emulation' in line.lower():
            has_emulation = True
            break

    print(f"\nExtracted Orange ID: {orange_id}")
    print(f"Extracted BIOS ID: {bios_id}")
    print(f"Extracted Platform/Stepping: {platform_stepping}")
    print(f"Extracted Unified Patch: {unified_patch_version}")
    print(f"Extracted Simics Version: {simics_version}")
    print(f"Has Emulation Info: {has_emulation}")

    # Initialize default values
    imh_osxml_bios = None
    imh_osxml_simics = None
    imh_osxml_up = None
    cbb_osxml_bios = None
    cbb_osxml_simics = None
    cbb_osxml_up = None
    scf_ipsd_bios = None
    scf_ipsd_simics = None
    scf_ipsd_up = None
    pnp_pm_data = {}

    # Process OSXML and PnP/PM data if available
    if osxml_table and pnp_pm_table:
        osxml_rows = osxml_table[1]
        pnp_rows = pnp_pm_table[1]

        print(f"\n=== OSXML TABLE DATA ===")
        print(f"Total rows in OSXML table: {len(osxml_rows)}")
        for i, row in enumerate(osxml_rows[:5]):
            print(f"Row {i}: {row[:3]}...")
        
        # Detect format: find a header row where cells are SHORT and EXACTLY equal to 'osxml in bios'/'osxml in simics'
        osxml_header_row_idx = None
        for row_idx, row in enumerate(osxml_rows):
            # Skip mega-rows (first cell is very long)
            if row and len(row[0]) > 80:
                continue
            row_lower = [cell.lower() for cell in row]
            if any(c == 'osxml in bios' or c == 'osxml in simics' for c in row_lower):
                osxml_header_row_idx = row_idx
                break
        
        if osxml_header_row_idx is not None:
            # Format B: use column positions from header row (exact match)
            hdr = [c.lower() for c in osxml_rows[osxml_header_row_idx]]
            bios_col = next((i for i, c in enumerate(hdr) if c == 'osxml in bios'), None)
            simics_col = next((i for i, c in enumerate(hdr) if c == 'osxml in simics'), None)
            up_col = next((i for i, c in enumerate(hdr) if c == 'unified patch'), None)
            if bios_col is None:
                bios_col = 1
            if simics_col is None:
                simics_col = 2
            print(f"DEBUG: Format B header_row_idx={osxml_header_row_idx}, bios_col={bios_col}, simics_col={simics_col}, up_col={up_col}")
            for row in osxml_rows[osxml_header_row_idx + 1:]:
                if not row or len(row[0]) > 80:
                    continue
                label = row[0].upper()
                print(f"DEBUG: label={repr(label)}, row={row}")
                if 'IMH' in label and 'CBB' not in label and 'SCF' not in label:
                    imh_osxml_bios = row[bios_col] if len(row) > bios_col else None
                    imh_osxml_simics = row[simics_col] if len(row) > simics_col else None
                    imh_osxml_up = row[up_col] if up_col and len(row) > up_col else None
                elif 'CBB' in label:
                    cbb_osxml_bios = row[bios_col] if len(row) > bios_col else None
                    cbb_osxml_simics = row[simics_col] if len(row) > simics_col else None
                    cbb_osxml_up = row[up_col] if up_col and len(row) > up_col else None
                elif 'SCF' in label:
                    scf_ipsd_bios = row[bios_col] if len(row) > bios_col else None
                    scf_ipsd_simics = row[simics_col] if len(row) > simics_col else None
                    scf_ipsd_up = row[up_col] if up_col and len(row) > up_col else None
        else:
            # Format A: row labels contain both component name and 'OSXML'
            for row in osxml_rows:
                row_lower = [cell.lower() for cell in row]
                if any('imh' in c for c in row_lower) and any('osxml' in c for c in row_lower):
                    imh_osxml_bios = row[1] if len(row) > 1 else None
                    imh_osxml_simics = row[2] if len(row) > 2 else None
                    imh_osxml_up = row[3] if len(row) > 3 else None
                if any('cbb' in c for c in row_lower) and any('osxml' in c for c in row_lower):
                    cbb_osxml_bios = row[1] if len(row) > 1 else None
                    cbb_osxml_simics = row[2] if len(row) > 2 else None
                    cbb_osxml_up = row[3] if len(row) > 3 else None
                if any('scf' in c for c in row_lower) and any('ipsd' in c for c in row_lower):
                    scf_ipsd_bios = row[1] if len(row) > 1 else None
                    scf_ipsd_simics = row[2] if len(row) > 2 else None
                    scf_ipsd_up = row[3] if len(row) > 3 else None
        
        print(f"\nExtracted OSXML Components:")
        print(f"  IMH OSXML BIOS: {imh_osxml_bios}")
        print(f"  IMH OSXML Simics: {imh_osxml_simics}")
        print(f"  IMH OSXML UP: {imh_osxml_up}")
        print(f"  CBB OSXML BIOS: {cbb_osxml_bios}")
        print(f"  CBB OSXML Simics: {cbb_osxml_simics}")
        print(f"  CBB OSXML UP: {cbb_osxml_up}")
        print(f"  SCF IPSD BIOS: {scf_ipsd_bios}")
        print(f"  SCF IPSD Simics: {scf_ipsd_simics}")
        print(f"  SCF IPSD UP: {scf_ipsd_up}")
        print(f"  Unified Patch (AP): {unified_patch_version}")

        # Extract PnP/PM data
        pnp_header = pnp_rows[0] if pnp_rows else []
        
        for row in pnp_rows[1:]:
            if len(row) >= 3:
                domain = row[0]
                pnp_ver = row[1]
                pm_ver = row[2]
                pnp_pm_data[domain] = (pnp_ver, pm_ver)
        
        print(f"\nExtracted PnP/PM data:")
        for domain, (pnp_v, pm_v) in pnp_pm_data.items():
            print(f"  {domain}: PnP={pnp_v}, PM={pm_v}")

    # Create standardized CSV file (always generate, even if no OSXML/PnP data found)
    if orange_id:
        csv_filename = f"{output_path}/OSXML_Summary_{orange_id}.csv"

        with open(csv_filename, 'w', encoding='utf-8') as f:
            # Write header info
            f.write(f'IFWI_Type,{ifwi_type}\n')
            f.write(f'Orange_ID,{orange_id}\n')
            f.write(f'BIOSID,{bios_id if bios_id else "N/A"}\n')
            f.write(f'Platform_Stepping,{platform_stepping if platform_stepping else "N/A"}\n')
            f.write(f'Has_Emulation,{"Yes" if has_emulation else "No"}\n')
            f.write(f'Simics_Version,{simics_version if simics_version else "N/A"}\n')
            f.write('\n')

            # Write OSXML section
            f.write('Component,OSXML_BIOS,OSXML_Simics,Unified_Patch\n')
            f.write(f'IMH_OSXML,{imh_osxml_bios if imh_osxml_bios else "N/A"},{imh_osxml_simics if imh_osxml_simics else "N/A"},{imh_osxml_up if imh_osxml_up else "N/A"}\n')
            f.write(f'CBB_OSXML,{cbb_osxml_bios if cbb_osxml_bios else "N/A"},{cbb_osxml_simics if cbb_osxml_simics else "N/A"},{cbb_osxml_up if cbb_osxml_up else "N/A"}\n')
            f.write(f'SCF_IPSD,{scf_ipsd_bios if scf_ipsd_bios else "N/A"},{scf_ipsd_simics if scf_ipsd_simics else "N/A"},{scf_ipsd_up if scf_ipsd_up else "N/A"}\n')

            f.write('\n')
            f.write(f'AP_Unified_Patch,{unified_patch_version if unified_patch_version else "N/A"}\n')

            f.write('\n')

            # Write PnP/PM section
            f.write('Domain,PnP_Version,PM_Version\n')
            for domain, (pnp_v, pm_v) in pnp_pm_data.items():
                f.write(f'{domain},{pnp_v},{pm_v}\n')

        print(f"\nGenerated CSV: {csv_filename}")

        # Return the CSV filename for report generation
        print(f"CSV_OUTPUT:{csv_filename}")

    print("\nExtraction complete!")

finally:
    driver.quit()


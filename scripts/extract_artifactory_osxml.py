"""
Extract OSXML and PnP/PM data from Artifactory IFWI build package.

This script:
1. Downloads .7z file from Artifactory using API Token authentication
2. Extracts OSXML_Version.html from the archive
3. Parses HTML to extract OSXML and PnP/PM recipe information
4. Generates standardized CSV output (same format as extract_fiv_table.py)

Usage:
    python extract_artifactory_osxml.py <artifactory_url> <api_token> <output_path>

Example:
    python extract_artifactory_osxml.py "https://af01p-or.devtools.intel.com/.../BuildPkg.7z" "YOUR_TOKEN" "."
"""

import sys
import os
import re
import requests
from pathlib import Path
import py7zr
from bs4 import BeautifulSoup

def download_simics_release_notes(simics_version, api_token, platform_stepping):
    """Download Simics release notes and extract IMH/CBB OSXML versions.

    NEW RULE: Determine path from simics_version string
    - If 'rio' in simics_version -> use dmr-rio-7
    - If 'rio' not in simics_version -> use dmr-7

    Args:
        simics_version: Simics version (e.g., 2026ww27.0.00_45 or dmr-rio-7 2026ww23.6.00_03)
        api_token: Artifactory API token
        platform_stepping: Platform/stepping (for reference)
    """
    # Extract pure version number for URL construction
    import re
    version_match = re.search(r'(\d{4}ww\d{2}\.\d+\.\d+_\d+)', simics_version)
    pure_version = version_match.group(1) if version_match else simics_version

    print(f"\nDownloading Simics release notes for version: {pure_version}")

    # NEW RULE: Check if 'rio' is in the FULL simics_version string
    # If 'rio' present -> use dmr-rio-7
    # If 'rio' not present -> use dmr-7
    if 'rio' in simics_version.lower():
        platform_path = 'dmr-rio-7'
        print(f"[INFO] Detected 'rio' in Simics version -> using path: {platform_path}")
    else:
        platform_path = 'dmr-7'
        print(f"[INFO] No 'rio' detected in Simics version -> using path: {platform_path}")

    print(f"Platform: {platform_stepping} -> Simics path: {platform_path}")

    # Build URL with pure version
    url = f"https://af02p-or.devtools.intel.com/artifactory/simics-local/vp-release-its/platforms/{platform_path}/{pure_version}/release_notes/daily_release_notification.md"
    print(f"URL: {url}")

    headers = {
        "X-JFrog-Art-Api": api_token
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            print(f"[OK] Downloaded Simics release notes ({len(response.text)} bytes)")

            # Parse the markdown content to extract OSXML versions
            content = response.text
            simics_osxml = extract_osxml_from_simics_md(content)

            return simics_osxml

        elif response.status_code == 403:
            print(f"[ERROR] Authentication failed for Simics release notes (HTTP 403)")
            return None
        elif response.status_code == 404:
            print(f"[ERROR] Simics release notes not found (HTTP 404)")
            print(f"Version '{simics_version}' may not exist or URL is incorrect")
            return None
        else:
            print(f"[ERROR] Failed to download Simics release notes (HTTP {response.status_code})")
            return None

    except Exception as e:
        print(f"[ERROR] Failed to download Simics release notes: {e}")
        return None

def extract_osxml_from_simics_md(markdown_content):
    """Extract IMH and CBB OSXML versions from Simics daily release notification markdown.

    Search patterns:
    - "IMH2 regs:" -> extract IMH OSXML (e.g., dmr-imh2-1p0p-26ww17h)
    - "CBB regs:" -> extract CBB OSXML (e.g., dmr-cbb-g0-26ww20a)

    Example format:
    IMH2 regs: **dmr-imh2-1p0p-26ww17h**
    CBB regs: **dmr-cbb-g0-26ww20a**
    """
    print(f"\nParsing Simics release notes for OSXML versions...")

    osxml_data = {
        'IMH_OSXML': None,
        'CBB_OSXML': None
    }

    lines = markdown_content.split('\n')

    for line in lines:
        # Look for "IMH2 regs:" or "IMH regs:" pattern
        # AP2 A0: IMH2 regs:
        # AP1 B0: IMH regs:
        if ('IMH2 regs:' in line or 'imh2 regs:' in line.lower() or
            'IMH regs:' in line or 'imh regs:' in line.lower()):
            # Extract version after colon, remove ** markdown markers
            # Pattern: IMH2 regs: **dmr-imh2-1p0p-26ww17h**
            # Pattern: IMH regs: **dmr-imh-B0-1P0N-26ww13a**
            match = re.search(r'regs:\s*\*{0,2}([a-z0-9\-]+)\*{0,2}', line, re.IGNORECASE)
            if match:
                osxml_data['IMH_OSXML'] = match.group(1).strip()
                print(f"  Found IMH OSXML: {osxml_data['IMH_OSXML']}")

        # Look for "CBB regs:" pattern
        if 'CBB regs:' in line or 'cbb regs:' in line.lower():
            # Extract version after colon, remove ** markdown markers
            # Pattern: CBB regs: **dmr-cbb-g0-26ww20a**
            match = re.search(r'regs:\s*\*{0,2}([a-z0-9\-]+)\*{0,2}', line, re.IGNORECASE)
            if match:
                osxml_data['CBB_OSXML'] = match.group(1).strip()
                print(f"  Found CBB OSXML: {osxml_data['CBB_OSXML']}")

    if not osxml_data['IMH_OSXML'] and not osxml_data['CBB_OSXML']:
        print(f"[WARN] No IMH/CBB OSXML versions found in Simics release notes")
        print(f"      Searched for 'IMH2 regs:' and 'CBB regs:' patterns")

    return osxml_data

def download_7z_file(url, api_token, output_dir):
    """Download .7z file from Artifactory using API Token authentication."""
    print(f"Downloading from Artifactory...")
    print(f"URL: {url}")

    headers = {
        "X-JFrog-Art-Api": api_token
    }

    # Create output directory if not exists
    os.makedirs(output_dir, exist_ok=True)

    # Extract filename from URL
    filename = url.split('/')[-1]
    output_path = os.path.join(output_dir, filename)

    # Download file
    response = requests.get(url, headers=headers, stream=True)

    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"[OK] Downloaded: {output_path}")
        return output_path
    elif response.status_code == 403:
        print(f"[ERROR] Authentication failed (HTTP 403). Check your API Token.")
        sys.exit(1)
    elif response.status_code == 404:
        print(f"[ERROR] File not found (HTTP 404). Check the URL.")
        sys.exit(1)
    else:
        print(f"[ERROR] Download failed with status code: {response.status_code}")
        sys.exit(1)

def extract_unified_patch_from_binary(archive_path, platform_stepping=None):
    """Extract Unified Patch version from binary filename in archive.

    Binary types:
    1. AP1 A0 Post-Si: *_NonIPClean_Trace_DebugSigned_VIS.bin
       Format: ..._[BIOSID]_[UP]_...
       Extract: 1st 8-digit hex after BIOS ID

    2. AP1 B0 Pre-Si: *_NonIPClean_Trace_DebugSigned_Simics.bin
       Format: ..._[BIOSID]_[AP1_UP]_[AP2_UP]_...
       Extract: 1st 8-digit hex after BIOS ID (index 0)

    3. AP2 A0 Pre-Si: *_NonIPClean_Trace_DebugSigned_Simics.bin
       Format: ..._[BIOSID]_[AP1_UP]_[AP2_UP]_...
       Extract: 2nd 8-digit hex after BIOS ID (index 1)
    """
    print(f"\nSearching for Unified Patch in binary filename...")
    if platform_stepping:
        print(f"Platform: {platform_stepping}")

    try:
        with py7zr.SevenZipFile(archive_path, mode='r') as archive:
            all_files = archive.getnames()

            # Determine which binary to look for based on platform
            if platform_stepping == 'AP1 A0':
                # AP1 A0 Post-Si: VIS.bin
                target_suffix = 'NonIPClean_Trace_DebugSigned_VIS.bin'
            elif platform_stepping in ['AP1 B0', 'AP2 A0']:
                # AP1 B0 / AP2 A0 Pre-Si: Simics.bin
                target_suffix = 'NonIPClean_Trace_DebugSigned_Simics.bin'
            else:
                # Unknown platform, try both
                print(f"[WARN] Unknown platform '{platform_stepping}', trying all binary types")
                target_suffix = None

            for filename in all_files:
                # Check if this is the target binary
                if target_suffix and not filename.endswith(target_suffix):
                    continue
                elif not target_suffix and not (filename.endswith('VIS.bin') or filename.endswith('Simics.bin')):
                    continue

                # Extract all 8-digit hex values after BIOS ID
                # Pattern: *_[BIOSID]_[HEX1]_[HEX2]_... or *_[BIOSID]_[HEX1]_[VERSION]_...
                match = re.search(r'_00\d{2}\.D\d+_((?:[A-F0-9]{8}_?)+)', filename, re.IGNORECASE)
                if match:
                    hex_section = match.group(1)
                    # Find all 8-digit hex patterns
                    hex_values = re.findall(r'([A-F0-9]{8})', hex_section, re.IGNORECASE)

                    if len(hex_values) > 0:
                        # NEW LOGIC: Match by version pattern (2nd digit of UP version)
                        # 5X1XXXXX (2nd digit=1) -> AP1 B0
                        # 5X2XXXXX (2nd digit=2) -> AP2 A0
                        # 800009XX -> AP1 A0

                        unified_patch = None

                        if platform_stepping == 'AP1 A0':
                            # Look for 800009xx pattern (usually 1st hex)
                            unified_patch = hex_values[0].upper()

                        elif platform_stepping == 'AP1 B0':
                            # Look for 5X1XXXXX pattern (2nd digit is 1)
                            for up_value in hex_values:
                                if len(up_value) >= 2 and up_value[1].upper() == '1':
                                    unified_patch = up_value.upper()
                                    break

                        elif platform_stepping == 'AP2 A0':
                            # Look for 5X2XXXXX pattern (2nd digit is 2)
                            for up_value in hex_values:
                                if len(up_value) >= 2 and up_value[1].upper() == '2':
                                    unified_patch = up_value.upper()
                                    break

                        if unified_patch:
                            print(f"[OK] Found Unified Patch from binary (version pattern match): {unified_patch}")
                            print(f"     Binary file: {os.path.basename(filename)}")
                            if len(hex_values) > 1:
                                print(f"     All UP values found: {', '.join(hex_values)}")
                            return unified_patch

            print(f"[WARN] No Unified Patch found in binary with suffix: {target_suffix or 'VIS.bin/Simics.bin'}")
            return None

    except Exception as e:
        print(f"[WARN] Failed to extract Unified Patch from binary: {e}")
        return None

def extract_osxml_html(archive_path, output_dir):
    """Extract OSXML_Version.html from .7z archive."""
    print(f"\nExtracting OSXML_Version.html from archive...")

    try:
        with py7zr.SevenZipFile(archive_path, mode='r') as archive:
            # List all files to find OSXML_Version.html
            all_files = archive.getnames()

            osxml_file = None
            for filename in all_files:
                if 'OSXML_Version.html' in filename:
                    osxml_file = filename
                    break

            if not osxml_file:
                print(f"[ERROR] OSXML_Version.html not found in archive.")
                print(f"Archive contains {len(all_files)} files:")
                for f in all_files[:10]:
                    print(f"  - {f}")
                if len(all_files) > 10:
                    print(f"  ... and {len(all_files) - 10} more files")
                sys.exit(1)

            # Extract only OSXML_Version.html
            archive.extract(targets=[osxml_file], path=output_dir)

            # Move extracted file to root of output_dir if it's in a subdirectory
            extracted_path = os.path.join(output_dir, osxml_file)
            final_path = os.path.join(output_dir, 'OSXML_Version.html')

            if extracted_path != final_path:
                os.makedirs(os.path.dirname(final_path), exist_ok=True)
                os.replace(extracted_path, final_path)

            print(f"[OK] Extracted: {final_path}")
            return final_path

    except Exception as e:
        print(f"[ERROR] Failed to extract archive: {e}")
        sys.exit(1)

def parse_osxml_html(html_path, artifactory_url=None):
    """Parse OSXML_Version.html to extract OSXML and PnP/PM data."""
    print(f"\nParsing OSXML_Version.html...")

    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract all text for metadata detection
    page_text = soup.get_text()
    lines = page_text.split('\n')

    # Initialize variables
    orange_id = None
    bios_id = None

    # Try to extract Orange ID from Artifactory URL first (most reliable)
    if artifactory_url:
        url_orange_match = re.search(r'(2026\.\d+\.\d+\.\d+)', artifactory_url)
        if url_orange_match:
            orange_id = url_orange_match.group(1)
            print(f"Auto-detected Orange ID from URL: {orange_id}")

        # Extract BIOS ID from URL (pattern: 0036.D.54)
        url_bios_match = re.search(r'(00\d{2}\.D\.\d+)', artifactory_url)
        if url_bios_match:
            # Convert 0036.D.54 to 0036.D54
            bios_id = url_bios_match.group(1).replace('.D.', '.D')
            print(f"Auto-detected BIOS ID from URL: {bios_id}")
    unified_patch_version = None
    simics_version = None
    platform_stepping = None
    has_emulation = False

    # Fallback: try to extract from page text if not found in URL
    if not orange_id:
        orange_match = re.search(r'(2026\.\d+\.\d+\.\d+)', page_text)
        if orange_match:
            orange_id = orange_match.group(1)
            print(f"Auto-detected Orange ID from page: {orange_id}")

    if not bios_id:
        # Extract BIOS ID from pattern 0036.D.54 (note: with dots in Artifactory path)
        bios_match = re.search(r'00[0-9]{2}\.D\.\d+', page_text)
        if bios_match:
            # Convert 0036.D.54 to 0036.D54 (remove middle dot)
            bios_id = bios_match.group(0).replace('.D.', '.D')
            print(f"Auto-detected BIOS ID from page: {bios_id}")

    # Detect platform/stepping from page text or filename
    # Check for "AP1", "AP2", "A0", "B0", "post silicon", "pre silicon"
    page_lower = page_text.lower()

    if 'ap1' in page_lower and 'a0' in page_lower and 'post' in page_lower:
        platform_stepping = 'AP1 A0'
    elif 'ap1' in page_lower and 'b0' in page_lower and 'pre' in page_lower:
        platform_stepping = 'AP1 B0'
    elif 'ap2' in page_lower and 'a0' in page_lower and 'post' in page_lower:
        platform_stepping = 'AP2 A0'
    elif 'ap2' in page_lower and 'a0' in page_lower and 'pre' in page_lower:
        platform_stepping = 'AP2 A0'
    elif 'ap2' in page_lower and 'b0' in page_lower:
        platform_stepping = 'AP2 B0'

    print(f"Detected Platform/Stepping: {platform_stepping}")

    # Check for emulation
    if 'emulation' in page_lower:
        has_emulation = True
        print(f"Detected Emulation info: Yes")

    # Find all tables in HTML
    tables = soup.find_all('table')
    print(f"Found {len(tables)} tables in HTML")

    osxml_data = {}
    pnp_pm_data = {}

    # Parse each table
    for idx, table in enumerate(tables):
        rows = table.find_all('tr')

        if not rows:
            continue

        # Get table data as list of lists
        table_data = []
        for row in rows:
            cells = row.find_all(['td', 'th'])
            cell_texts = [cell.get_text(strip=True) for cell in cells]
            if cell_texts:
                table_data.append(cell_texts)

        if not table_data:
            continue

        # Check first row to identify table type
        first_row_lower = [cell.lower() for cell in table_data[0]]

        # Identify OSXML table
        if any('osxml' in c for c in first_row_lower) or any('ipsd' in c for c in first_row_lower):
            print(f"\n>>> Identified OSXML Table (Table {idx + 1})")
            parsed_osxml = parse_osxml_table(table_data)
            # Merge parsed data into osxml_data (don't overwrite)
            for key, value in parsed_osxml.items():
                if key not in osxml_data or osxml_data[key].get('bios') is None:
                    osxml_data[key] = value

        # Identify PnP/PM table
        elif 'domain' in first_row_lower and ('pnp' in ' '.join(first_row_lower) or 'pm' in ' '.join(first_row_lower)):
            print(f">>> Identified PnP/PM Table (Table {idx + 1})")
            pnp_pm_data = parse_pnp_pm_table(table_data)

    # Look for Unified Patch in page text
    up_match = re.search(r'UP\s+([A-F0-9]{8})', page_text, re.IGNORECASE)
    if up_match:
        unified_patch_version = up_match.group(1).upper()

    # Also search tables for Unified Patch
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all(['td', 'th'])
            cell_texts = [c.get_text(strip=True) for c in cells]
            row_text = ' '.join(cell_texts).lower()

            if 'unified patch' in row_text or 'upatch' in row_text:
                for cell in cell_texts:
                    if re.match(r'^[A-F0-9]{8}$', cell.strip(), re.IGNORECASE):
                        unified_patch_version = cell.strip().upper()
                        break

    print(f"\nExtracted Unified Patch: {unified_patch_version}")

    # Note: SCF IPSD extraction moved to main() after platform_stepping is determined

    return {
        'soup': soup,  # Pass soup for later SCF IPSD extraction
        'orange_id': orange_id,
        'bios_id': bios_id,
        'platform_stepping': platform_stepping,
        'unified_patch': unified_patch_version,
        'simics_version': simics_version,
        'has_emulation': has_emulation,
        'osxml_data': osxml_data,
        'pnp_pm_data': pnp_pm_data
    }

def extract_scf_ipsd_version(soup):
    """Extract SCF IPSD version from IpScfMgrGen5 hex value.

    Searches for IpScfMgrGen5 in tables, extracts hex value (e.g., 0x0000000c),
    converts to decimal (e.g., 12).

    Args:
        soup: BeautifulSoup object of OSXML_Version.html

    Returns:
        str: Decimal version (e.g., "12") or None if not found
    """
    print(f"\nExtracting SCF IPSD version...")

    tables = soup.find_all('table')

    for table in tables:
        rows = table.find_all('tr')

        for row in rows:
            cells = row.find_all(['td', 'th'])
            cell_texts = [c.get_text(strip=True) for c in cells]

            # Look for IpScfMgr (NOT IpScfMgrGen5)
            # IpScfMgr contains the actual SCF IPSD version number
            for i, cell_text in enumerate(cell_texts):
                if cell_text == 'IpScfMgr':  # Exact match, exclude IpScfMgrGen5
                    # Next cell should contain hex value
                    if i + 1 < len(cell_texts):
                        hex_value = cell_texts[i + 1].strip()

                        # Check if it's a hex value
                        if hex_value.startswith('0x'):
                            try:
                                decimal_value = int(hex_value, 16)
                                # Add major version prefix: 4.0.0.
                                version_string = f"4.0.0.{decimal_value}"
                                print(f"  Found {cell_text}: {hex_value} -> Decimal: {decimal_value} -> Version: {version_string}")
                                return version_string
                            except ValueError as e:
                                print(f"  [WARN] Failed to convert {hex_value} to decimal: {e}")
                                continue

    print(f"  [WARN] SCF IPSD version not found in tables")
    return None

def parse_osxml_table(table_data):
    """Parse OSXML table to extract component versions."""
    osxml_data = {
        'IMH_OSXML': {'bios': None, 'simics': None, 'up': None},
        'CBB_OSXML': {'bios': None, 'simics': None, 'up': None},
        'SCF_IPSD': {'bios': None, 'simics': None, 'up': None}
    }

    # Find header row with column names
    header_idx = None
    bios_col = None
    simics_col = None
    up_col = None

    for idx, row in enumerate(table_data):
        row_lower = [cell.lower() for cell in row]

        # Look for header row with "osxml in bios", "osxml in simics", "unified patch"
        if any('osxml in bios' in c or 'bios' in c for c in row_lower):
            header_idx = idx
            for i, cell in enumerate(row_lower):
                if 'bios' in cell and 'simics' not in cell:
                    bios_col = i
                elif 'simics' in cell:
                    simics_col = i
                elif 'unified patch' in cell or 'patch' in cell:
                    up_col = i
            break

    if header_idx is None:
        print("[WARN] OSXML table header not found, using default column positions")
        bios_col = 1
        simics_col = 2
        up_col = 3
        header_idx = 0

    print(f"  OSXML columns: BIOS={bios_col}, Simics={simics_col}, UP={up_col}")

    # Extract data rows
    for row in table_data[header_idx + 1:]:
        if not row or len(row) == 0:
            continue

        label = row[0].upper()

        if 'IMH' in label and 'CBB' not in label:
            osxml_data['IMH_OSXML']['bios'] = row[bios_col] if bios_col and len(row) > bios_col else None
            osxml_data['IMH_OSXML']['simics'] = row[simics_col] if simics_col and len(row) > simics_col else None
            osxml_data['IMH_OSXML']['up'] = row[up_col] if up_col and len(row) > up_col else None
        elif 'CBB' in label:
            osxml_data['CBB_OSXML']['bios'] = row[bios_col] if bios_col and len(row) > bios_col else None
            osxml_data['CBB_OSXML']['simics'] = row[simics_col] if simics_col and len(row) > simics_col else None
            osxml_data['CBB_OSXML']['up'] = row[up_col] if up_col and len(row) > up_col else None
        elif 'SCF' in label or 'IPSD' in label:
            osxml_data['SCF_IPSD']['bios'] = row[bios_col] if bios_col and len(row) > bios_col else None
            osxml_data['SCF_IPSD']['simics'] = row[simics_col] if simics_col and len(row) > simics_col else None
            osxml_data['SCF_IPSD']['up'] = row[up_col] if up_col and len(row) > up_col else None

    print(f"  Extracted OSXML:")
    print(f"    IMH: {osxml_data['IMH_OSXML']}")
    print(f"    CBB: {osxml_data['CBB_OSXML']}")
    print(f"    SCF IPSD: {osxml_data['SCF_IPSD']}")

    return osxml_data

def parse_pnp_pm_table(table_data):
    """Parse PnP/PM recipe table."""
    pnp_pm_data = {}

    # Skip header row
    for row in table_data[1:]:
        if len(row) >= 3:
            domain = row[0]
            pnp_ver = row[1]
            pm_ver = row[2]
            pnp_pm_data[domain] = (pnp_ver, pm_ver)

    print(f"  Extracted PnP/PM:")
    for domain, (pnp_v, pm_v) in pnp_pm_data.items():
        print(f"    {domain}: PnP={pnp_v}, PM={pm_v}")

    return pnp_pm_data

def generate_csv(data, output_path):
    """Generate standardized CSV output (same format as extract_fiv_table.py)."""

    orange_id = data['orange_id']
    if not orange_id:
        print("[ERROR] Orange ID not found, cannot generate CSV")
        sys.exit(1)

    csv_filename = os.path.join(output_path, f"OSXML_Summary_{orange_id}.csv")

    # Check if this is AP1 A0 Post-Si (simplified report mode)
    # Only AP1 A0 Post-Si gets simplified report (BIOS + UP only)
    # AP1 B0 and AP2 A0 are Pre-Si and need full report (BIOS + UP + OSXML + PnP/PM + uBIOS)
    is_ap1_a0_post_si = (
        data.get('platform_stepping') == 'AP1 A0' and
        # Post-Si has no Simics data for IMH/CBB
        data['osxml_data'].get('IMH_OSXML', {}).get('simics') in [None, 'N/A', ''] and
        data['osxml_data'].get('CBB_OSXML', {}).get('simics') in [None, 'N/A', '']
    )

    if is_ap1_a0_post_si:
        print("\n[INFO] Detected AP1 A0 Post-Si IFWI - Simplified report mode (BIOS + Unified Patch only)")
    elif data.get('platform_stepping') in ['AP1 B0', 'AP2 A0']:
        print(f"\n[INFO] Detected {data.get('platform_stepping')} Pre-Si IFWI - Full report mode (BIOS + UP + OSXML + PnP/PM + uBIOS)")

    with open(csv_filename, 'w', encoding='utf-8') as f:
        # Write header info
        f.write(f"IFWI_Type,Orange\n")
        f.write(f"Orange_ID,{orange_id}\n")
        f.write(f"BIOSID,{data['bios_id'] if data['bios_id'] else 'N/A'}\n")
        f.write(f"Platform_Stepping,{data['platform_stepping'] if data['platform_stepping'] else 'N/A'}\n")
        f.write(f"Has_Emulation,{'Yes' if data['has_emulation'] else 'No'}\n")
        f.write(f"Simics_Version,{data['simics_version'] if data['simics_version'] else 'N/A'}\n")
        f.write(f"Simplified_Report,{'Yes' if is_ap1_a0_post_si else 'No'}\n")
        f.write('\n')

        # Write OSXML section
        f.write('Component,OSXML_BIOS,OSXML_Simics,Unified_Patch\n')

        osxml = data['osxml_data']
        for comp in ['IMH_OSXML', 'CBB_OSXML', 'SCF_IPSD']:
            bios = osxml.get(comp, {}).get('bios') or 'N/A'
            simics = osxml.get(comp, {}).get('simics') or 'N/A'
            up = osxml.get(comp, {}).get('up') or 'N/A'
            f.write(f'{comp},{bios},{simics},{up}\n')

        f.write('\n')
        f.write(f"AP_Unified_Patch,{data['unified_patch'] if data['unified_patch'] else 'N/A'}\n")
        f.write('\n')

        # Write PnP/PM section
        f.write('Domain,PnP_Version,PM_Version\n')
        for domain, (pnp_v, pm_v) in data['pnp_pm_data'].items():
            f.write(f'{domain},{pnp_v},{pm_v}\n')

    print(f"\n[OK] Generated CSV: {csv_filename}")
    print(f"CSV_OUTPUT:{csv_filename}")

    return csv_filename

def main():
    if len(sys.argv) < 4:
        print("Usage: python extract_artifactory_osxml.py <artifactory_url> <api_token> <output_path> [platform_stepping] [simics_version]")
        print("Example: python extract_artifactory_osxml.py <url> <token> . \"AP1 B0\" \"2026ww27.0.00_45\"")
        sys.exit(1)

    artifactory_url = sys.argv[1]
    api_token = sys.argv[2]
    output_path = sys.argv[3]
    user_platform_stepping = sys.argv[4] if len(sys.argv) > 4 else None
    simics_version = sys.argv[5] if len(sys.argv) > 5 else None

    print("=== Artifactory OSXML Extractor ===\n")

    # Step 1: Download .7z file
    archive_path = download_7z_file(artifactory_url, api_token, output_path)

    # Step 2: Extract Unified Patch from binary filename (position depends on platform)
    # Note: we pass user_platform_stepping here even though data hasn't been parsed yet
    # This is OK because we need the platform to know which binary to look for
    unified_patch_from_binary = extract_unified_patch_from_binary(archive_path, user_platform_stepping)

    # Step 3: Extract OSXML_Version.html
    html_path = extract_osxml_html(archive_path, output_path)

    # Step 4: Parse HTML and extract data (pass URL for Orange ID extraction)
    data = parse_osxml_html(html_path, artifactory_url)

    # Override Unified Patch with binary filename value if found (more reliable)
    if unified_patch_from_binary:
        data['unified_patch'] = unified_patch_from_binary

    # Override platform/stepping with user-provided value if given
    if user_platform_stepping:
        data['platform_stepping'] = user_platform_stepping
        print(f"Using user-provided platform/stepping: {user_platform_stepping}")

    # Step 4.5: Extract SCF IPSD version (only for AP1 B0 / AP2 A0)
    # Must be done AFTER platform_stepping is set
    final_platform = data['platform_stepping']
    if final_platform in ['AP1 B0', 'AP2 A0']:
        soup = data.get('soup')
        if soup:
            scf_ipsd_version = extract_scf_ipsd_version(soup)
            if scf_ipsd_version:
                print(f"Extracted SCF IPSD version: {scf_ipsd_version}")
                # Store in osxml_data BIOS column only
                if 'SCF_IPSD' not in data['osxml_data']:
                    data['osxml_data']['SCF_IPSD'] = {'bios': None, 'simics': None, 'up': None}
                data['osxml_data']['SCF_IPSD']['bios'] = scf_ipsd_version
                data['osxml_data']['SCF_IPSD']['up'] = scf_ipsd_version
                # Simics column should remain empty
                data['osxml_data']['SCF_IPSD']['simics'] = None
    else:
        print(f"[INFO] SCF IPSD extraction skipped for {final_platform} (only for AP1 B0 / AP2 A0)")

    # Step 4.6: Extract IMH OSXML from Unified Patch (only for AP1 B0 / AP2 A0)
    if final_platform in ['AP1 B0', 'AP2 A0'] and unified_patch_from_binary:
        print(f"\n[INFO] Extracting IMH OSXML from Unified Patch...")
        try:
            from extract_up_imh_osxml import extract_imh_osxml_from_up

            up_imh_osxml = extract_imh_osxml_from_up(unified_patch_from_binary, final_platform, api_token, output_path)

            if up_imh_osxml:
                print(f"[OK] Extracted IMH OSXML from UP: {up_imh_osxml}")
                # Store in osxml_data UP column
                if 'IMH_OSXML' not in data['osxml_data']:
                    data['osxml_data']['IMH_OSXML'] = {'bios': None, 'simics': None, 'up': None}
                data['osxml_data']['IMH_OSXML']['up'] = up_imh_osxml
            else:
                print(f"[WARN] Failed to extract IMH OSXML from Unified Patch")

        except Exception as e:
            print(f"[ERROR] Failed to extract IMH OSXML from UP: {e}")

    # Step 5: Download and parse Simics release notes (for AP1 B0 / AP2 A0)
    if simics_version and user_platform_stepping in ['AP1 B0', 'AP2 A0']:
        # Extract pure version number (YYYYwwNN.X.XX_NN) from simics_version
        # Input may be: "dmr-7 2026ww24.3.00_45 Pre712" or "2026ww24.3.00_45"
        import re
        version_match = re.search(r'(\d{4}ww\d{2}\.\d+\.\d+_\d+)', simics_version)
        pure_version = version_match.group(1) if version_match else simics_version

        # IMPORTANT: Pass full simics_version (not pure_version) so rio detection works
        simics_osxml = download_simics_release_notes(simics_version, api_token, user_platform_stepping)

        if simics_osxml:
            # Update Simics version in data
            # simics_version may be:
            # 1. Full format: "dmr-7 2026ww24.3.00_45 Pre712"
            # 2. Short format: "2026ww24.3.00_45"
            if simics_version.startswith('dmr') or 'Pre' in simics_version:
                # Already has platform path and/or suffix
                data['simics_version'] = simics_version
            else:
                # Only version number, add platform path
                platform_path = 'dmr-rio-7' if user_platform_stepping == 'AP2 A0' else 'dmr-7'
                data['simics_version'] = f"{platform_path} {simics_version}"

            # Merge Simics OSXML data into osxml_data (Simics column)
            if simics_osxml.get('IMH_OSXML'):
                if 'IMH_OSXML' not in data['osxml_data']:
                    data['osxml_data']['IMH_OSXML'] = {'bios': None, 'simics': None, 'up': None}
                data['osxml_data']['IMH_OSXML']['simics'] = simics_osxml['IMH_OSXML']

            if simics_osxml.get('CBB_OSXML'):
                if 'CBB_OSXML' not in data['osxml_data']:
                    data['osxml_data']['CBB_OSXML'] = {'bios': None, 'simics': None, 'up': None}
                data['osxml_data']['CBB_OSXML']['simics'] = simics_osxml['CBB_OSXML']

            print(f"\n[OK] Merged Simics OSXML data into report")
        else:
            print(f"\n[WARN] Could not retrieve Simics OSXML data - will use N/A for Simics columns")

    # Step 4: Generate CSV
    csv_path = generate_csv(data, output_path)

    print("\n=== Extraction Complete ===")
    print(f"CSV file ready for report generation: {csv_path}")

if __name__ == "__main__":
    main()

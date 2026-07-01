import csv
import sys
import webbrowser
from datetime import datetime

def parse_osxml_summary(csv_file):
    """Parse OSXML_Summary CSV file"""
    data = {
        'ifwi_type': 'Orange',  # Default to Orange for backward compatibility
        'orange_id': '',
        'biosid': '',
        'platform_stepping': '',
        'has_emulation': False,
        'simics_version': '',
        'ap_unified_patch': '',
        'simplified_report': False,  # AP1 A0 Post-Si simplified mode
        'osxml': {},
        'pnp_pm': {}
    }

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        section = None

        for row in reader:
            if not row or not row[0]:
                continue

            # Parse header info
            if row[0] == 'IFWI_Type':
                data['ifwi_type'] = row[1] if len(row) > 1 else 'Orange'
            elif row[0] == 'Orange_ID':
                data['orange_id'] = row[1] if len(row) > 1 else ''
            elif row[0] == 'BIOSID':
                data['biosid'] = row[1] if len(row) > 1 else ''
            elif row[0] == 'Platform_Stepping':
                data['platform_stepping'] = row[1] if len(row) > 1 else ''
            elif row[0] == 'Has_Emulation':
                data['has_emulation'] = (row[1] if len(row) > 1 else '') == 'Yes'
            elif row[0] == 'Simics_Version':
                data['simics_version'] = row[1] if len(row) > 1 else ''
            elif row[0] == 'Simplified_Report':
                data['simplified_report'] = (row[1] if len(row) > 1 else '') == 'Yes'
            elif row[0] == 'AP_Unified_Patch':
                data['ap_unified_patch'] = row[1] if len(row) > 1 else ''

            # Section headers
            elif row[0] == 'Component':
                section = 'osxml'
            elif row[0] == 'Domain':
                section = 'pnp_pm'

            # OSXML data
            elif section == 'osxml' and row[0] in ['IMH_OSXML', 'CBB_OSXML', 'SCF_IPSD']:
                data['osxml'][row[0]] = {
                    'bios': row[1] if len(row) > 1 else 'N/A',
                    'simics': row[2] if len(row) > 2 else 'N/A',
                    'unified_patch': row[3] if len(row) > 3 else 'N/A'
                }

            # PnP/PM data
            elif section == 'pnp_pm' and row[0] in ['IIO', 'MC', 'UNCORE']:
                data['pnp_pm'][row[0]] = {
                    'pnp': row[1] if len(row) > 1 else 'N/A',
                    'pm': row[2] if len(row) > 2 else 'N/A'
                }

    return data

def calculate_ubios_release_week(orange_week):
    """Calculate uBIOS release week (Orange week + 1 day)"""
    import re
    # Parse WWxx.y format
    match = re.match(r'WW(\d+)\.(\d+)', orange_week)
    if not match:
        return None

    week_num = int(match.group(1))
    day_num = int(match.group(2))

    # Add 1 day
    day_num += 1

    # If day > 7, move to next week
    if day_num > 7:
        week_num += 1
        day_num = 1

    return f'WW{week_num}.{day_num}'

def extract_osxml_by_platform(osxml_value, platform, component=None):
    """Extract platform-specific OSXML value from semicolon-separated string.

    CRITICAL: IMH and CBB have DIFFERENT ordering!

    CBB format: CBB_C0_26ww12b_RTL;CBB-B0_MCP_25ww48a_RTL;CBB-A0_PowerOn
    Index 0: AP2 A0 (C0)
    Index 1: AP1 B0 (B0)
    Index 2: AP1 A0 (A0)

    IMH format: IMH2-1p0P_26ww17hRTL-OSXML;IMH-Post-1P0AD-FV;IMH1-B0-1P0N
    Index 0: AP2 A0 (IMH2)
    Index 1: AP1 A0 (Post)
    Index 2: AP1 B0 (B0)
    """
    if not osxml_value or osxml_value in ['N/A', 'NA', '']:
        return osxml_value

    # Split by semicolon
    if ';' in osxml_value:
        parts = osxml_value.split(';')

        # Determine if this is IMH or CBB (check component name or content)
        is_imh = (component and 'IMH' in component) or 'IMH' in osxml_value

        # Map platform to index (DIFFERENT for IMH vs CBB!)
        if is_imh:
            # IMH ordering: AP2 A0, AP1 A0, AP1 B0
            platform_index = {
                'AP1 A0': 1,  # 2nd value
                'AP1 B0': 2,  # 3rd value
                'AP2 A0': 0,  # 1st value
                'AP2 B0': 0,  # 1st value
            }
        else:
            # CBB ordering: AP2 A0, AP1 B0, AP1 A0
            platform_index = {
                'AP1 A0': 2,  # 3rd value
                'AP1 B0': 1,  # 2nd value
                'AP2 A0': 0,  # 1st value
                'AP2 B0': 0,  # 1st value
            }

        idx = platform_index.get(platform, 0)

        # Return the specific value if index exists
        if idx < len(parts):
            return parts[idx].strip()

    # No semicolon or couldn't extract, return original
    return osxml_value

def generate_html_report(data, output_file):
    """Generate IFWI Release Status HTML report"""

    # Use platform/stepping from CSV if available (extracted from page text)
    if data.get('platform_stepping') and data['platform_stepping'] not in ['N/A', 'NA', '']:
        platform = data['platform_stepping']
    else:
        # Fallback: try to detect from OSXML data
        biosid = data['biosid']
        stepping = 'Unknown'
        for component in ['IMH_OSXML', 'CBB_OSXML']:
            osxml_bios = data['osxml'].get(component, {}).get('bios', '')
            if 'B0' in osxml_bios or 'b0' in osxml_bios.lower():
                stepping = 'B0'
                break
            elif 'A0' in osxml_bios or 'a0' in osxml_bios.lower():
                stepping = 'A0'
                break

        # Determine AP1 vs AP2 from BIOSID
        if biosid.startswith('0036'):
            platform = f'AP1 {stepping}' if stepping != 'Unknown' else 'AP1'
        elif biosid.startswith('0035'):
            platform = f'AP2 {stepping}' if stepping != 'Unknown' else 'AP2'
        else:
            platform = 'Unknown'

    today = datetime.now().strftime('%Y-%m-%d')

    # Check if simplified report mode (AP1 A0 Post-Si: only Unified Patch, no OSXML/PnP tables)
    simplified_report = data.get('simplified_report', False)

    if simplified_report:
        # For AP1 A0 Post-Si: skip OSXML and PnP/PM tables
        has_osxml = False
        has_pnp_pm = False
        has_simics = False
    else:
        # Check if OSXML data exists (any non-N/A values)
        has_osxml = False
        for component in ['IMH_OSXML', 'CBB_OSXML', 'SCF_IPSD']:
            comp_data = data['osxml'].get(component, {})
            for field in ['bios', 'simics', 'unified_patch']:
                value = comp_data.get(field, 'N/A')
                if value not in ['N/A', 'NA', '', None]:
                    has_osxml = True
                    break
            if has_osxml:
                break

        # Check if PnP/PM data exists (any non-N/A values)
        has_pnp_pm = False
        for domain in ['IIO', 'MC', 'UNCORE']:
            domain_data = data['pnp_pm'].get(domain, {})
            for field in ['pnp', 'pm']:
                value = domain_data.get(field, 'N/A')
                if value not in ['N/A', 'NA', '', None]:
                    has_pnp_pm = True
                    break
            if has_pnp_pm:
                break

        # Check if Simics information exists (not just N/A)
        # Post-Si releases have no IMH/CBB Simics data, only check these two
        has_simics = (
            (data['simics_version'] and data['simics_version'] not in ['N/A', 'NA', '']) or
            data['osxml'].get('IMH_OSXML', {}).get('simics', 'N/A') not in ['N/A', 'NA', ''] or
            data['osxml'].get('CBB_OSXML', {}).get('simics', 'N/A') not in ['N/A', 'NA', '']
        )

    # Extract platform-specific OSXML values (handle semicolon-separated values)
    # IMH/CBB OSXML may contain multiple values separated by semicolons
    # Format: AP2_B0;AP1_A0;AP1_B0
    # We need to extract the correct one based on platform
    if platform and not simplified_report:
        for component in ['IMH_OSXML', 'CBB_OSXML']:
            if component in data['osxml']:
                # Extract platform-specific BIOS OSXML
                bios_val = data['osxml'][component].get('bios', '')
                if bios_val and ';' in bios_val:
                    data['osxml'][component]['bios'] = extract_osxml_by_platform(bios_val, platform, component)

                # Extract platform-specific Simics OSXML
                simics_val = data['osxml'][component].get('simics', '')
                if simics_val and ';' in simics_val:
                    data['osxml'][component]['simics'] = extract_osxml_by_platform(simics_val, platform, component)

    # Build release statement if user provided Orange ID and Release Week
    release_statement = ''
    ubios_statement = ''
    if data.get('user_orange_id') and data.get('user_release_week'):
        # Determine platform description
        if platform.startswith('AP1'):
            platform_desc = f'DMR-AP-UCC {platform}'
        elif platform.startswith('AP2'):
            platform_desc = f'DMR-AP-MCC {platform}'
        else:
            platform_desc = 'DMR-AP-UCC'

        # Determine silicon type (Post-Si or Pre-Si)
        # Post-Si: no Simics data, Pre-Si: has Simics data
        silicon_type = 'Pre-Si' if has_simics else 'Post-Si'

        # Use user-provided tense or default to "has been released"
        release_tense = data.get('user_release_tense', 'has been released')
        ifwi_type = data.get('ifwi_type', 'Orange')
        release_statement = f'    <p style="color: #2c3e50; font-size: 18px; font-weight: bold;"><strong>{platform_desc} {silicon_type} {ifwi_type} IFWI {data["user_orange_id"]} {release_tense} on {data["user_release_week"]}</strong></p>\n'

        # Add uBIOS statement for Pre-Si releases (AP1 B0, AP2 A0) or if emulation flag is set
        # Pre-Si releases always get uBIOS statement (auto-calculate uBIOS week)
        needs_ubios = (
            data['has_emulation'] or  # Legacy: emulation flag set
            (platform in ['AP1 B0', 'AP2 A0']) or  # New: AP1 B0 / AP2 A0 Pre-Si
            has_simics  # Has Simics data = Pre-Si
        )

        if needs_ubios:
            auto_ubios_week = calculate_ubios_release_week(data["user_release_week"])
            if auto_ubios_week:
                # uBIOS always uses "will be released" (future tense)
                ubios_statement = f'    <p style="color: #2c3e50; font-size: 18px; font-weight: bold;"><strong>{platform} uBIOS based on BIOSID {data["biosid"]} will be released on {auto_ubios_week}</strong></p>\n'

    # Build Simics table row
    simics_table_row = f'''            <tr>
                <td class="orange-id"><strong>Simics</strong></td>
                <td class="orange-id">{data['simics_version'] if data['simics_version'] else '-'}</td>
                <td>{data['osxml'].get('IMH_OSXML', {}).get('simics', '') if data['osxml'].get('IMH_OSXML', {}).get('simics', 'N/A') not in ['N/A', 'NA'] else ''}</td>
                <td>{data['osxml'].get('CBB_OSXML', {}).get('simics', '') if data['osxml'].get('CBB_OSXML', {}).get('simics', 'N/A') not in ['N/A', 'NA'] else ''}</td>
                <td>{data['osxml'].get('SCF_IPSD', {}).get('simics', '') if data['osxml'].get('SCF_IPSD', {}).get('simics', 'N/A') not in ['N/A', 'NA'] else ''}</td>
            </tr>
''' if has_simics else ''

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>{platform} IFWI Release Status</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .report-header {{
            background-color: #2c3e50;
            color: white;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background-color: white;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin: 20px 0;
        }}
        th {{
            background-color: #34495e;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: bold;
            border: 1px solid #ddd;
        }}
        td {{
            padding: 10px;
            border: 1px solid #ddd;
        }}
        tr:nth-child(even) {{
            background-color: #ecf0f1;
        }}
        .orange-id {{
            font-weight: bold;
        }}
    </style>
</head>
<body>

<div class="report-header">
    <h1>DMR Weekly Status Report</h1>
    <p><strong>Generated:</strong> {today}</p>
</div>

<div class="report-section">
{release_statement}'''

    # Build Release Version Information table
    # For AP1 A0 Post-Si: show BIOS Binary and Unified Patch only
    if simplified_report:
        # AP1 A0 Post-Si: Simplified - BIOS Binary + Unified Patch
        html += f'''    <p><strong>Release version information as below:</strong></p>
    <table>
        <thead>
            <tr>
                <th style="width: 40%;">Component</th>
                <th style="width: 60%;">Version</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="orange-id"><strong>BIOS Binary</strong></td>
                <td class="orange-id">{data['biosid'] if data['biosid'] and data['biosid'] not in ['N/A', 'NA'] else 'N/A'}</td>
            </tr>
            <tr>
                <td class="orange-id"><strong>AP Unified Patch</strong></td>
                <td class="orange-id">{data['ap_unified_patch'] if data['ap_unified_patch'] and data['ap_unified_patch'] not in ['N/A', 'NA'] else 'N/A'}</td>
            </tr>
        </tbody>
    </table>

'''
    elif has_osxml:
        # Full table with OSXML columns
        html += f'''    <p><strong>Release version information as below:</strong></p>
    <table>
        <thead>
            <tr>
                <th style="width: 20%;"></th>
                <th style="width: 20%;">Version</th>
                <th style="width: 20%;">IMH OSXML</th>
                <th style="width: 20%;">CBB OSXML</th>
                <th style="width: 20%;">SCF IPSD</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="orange-id"><strong>BIOS Binary</strong></td>
                <td class="orange-id">{data['biosid']}</td>
                <td>{data['osxml'].get('IMH_OSXML', {}).get('bios', '') if data['osxml'].get('IMH_OSXML', {}).get('bios', 'N/A') not in ['N/A', 'NA'] else ''}</td>
                <td>{data['osxml'].get('CBB_OSXML', {}).get('bios', '') if data['osxml'].get('CBB_OSXML', {}).get('bios', 'N/A') not in ['N/A', 'NA'] else ''}</td>
                <td>{data['osxml'].get('SCF_IPSD', {}).get('bios', '') if data['osxml'].get('SCF_IPSD', {}).get('bios', 'N/A') not in ['N/A', 'NA'] else ''}</td>
            </tr>
{simics_table_row}            <tr>
                <td class="orange-id"><strong>Unified Patch</strong></td>
                <td class="orange-id">{data['ap_unified_patch'] if data['ap_unified_patch'] else ''}</td>
                <td>{data['osxml'].get('IMH_OSXML', {}).get('unified_patch', '') if data['osxml'].get('IMH_OSXML', {}).get('unified_patch', 'N/A') not in ['N/A', 'NA'] else ''}</td>
                <td>{data['osxml'].get('CBB_OSXML', {}).get('unified_patch', '') if data['osxml'].get('CBB_OSXML', {}).get('unified_patch', 'N/A') not in ['N/A', 'NA'] else ''}</td>
                <td>{data['osxml'].get('SCF_IPSD', {}).get('unified_patch', '') if data['osxml'].get('SCF_IPSD', {}).get('unified_patch', 'N/A') not in ['N/A', 'NA'] else ''}</td>
            </tr>
        </tbody>
    </table>

'''
    else:
        # Simplified table without OSXML columns (only BIOS Binary and Unified Patch)
        html += f'''    <p><strong>Release version information as below:</strong></p>
    <table>
        <thead>
            <tr>
                <th style="width: 40%;"></th>
                <th style="width: 60%;">Version</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="orange-id"><strong>BIOS Binary</strong></td>
                <td class="orange-id">{data['biosid']}</td>
            </tr>
            <tr>
                <td class="orange-id"><strong>Unified Patch</strong></td>
                <td class="orange-id">{data['ap_unified_patch'] if data['ap_unified_patch'] else ''}</td>
            </tr>
        </tbody>
    </table>

'''

    # Build PnP/PM table HTML (only if has_pnp_pm)
    if has_pnp_pm:
        html += f'''    <p><strong>PNP and PM recipe config in BIOS as below:</strong></p>
    <table>
        <thead>
            <tr>
                <th style="width: 20%;"></th>
                <th style="width: 26.67%;">BIOS MC</th>
                <th style="width: 26.67%;">BIOS IIO</th>
                <th style="width: 26.67%;">BIOS Uncore</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="orange-id"><strong>PNP config Recipe</strong></td>
                <td>{data['pnp_pm'].get('MC', {}).get('pnp', '') if data['pnp_pm'].get('MC', {}).get('pnp', 'N/A') not in ['N/A', 'NA'] else ''}</td>
                <td>{data['pnp_pm'].get('IIO', {}).get('pnp', '') if data['pnp_pm'].get('IIO', {}).get('pnp', 'N/A') not in ['N/A', 'NA'] else ''}</td>
                <td>{data['pnp_pm'].get('UNCORE', {}).get('pnp', '') if data['pnp_pm'].get('UNCORE', {}).get('pnp', 'N/A') not in ['N/A', 'NA'] else ''}</td>
            </tr>
            <tr>
                <td class="orange-id"><strong>PM config Recipe</strong></td>
                <td>{data['pnp_pm'].get('MC', {}).get('pm', '') if data['pnp_pm'].get('MC', {}).get('pm', 'N/A') not in ['N/A', 'NA'] else ''}</td>
                <td>{data['pnp_pm'].get('IIO', {}).get('pm', '') if data['pnp_pm'].get('IIO', {}).get('pm', 'N/A') not in ['N/A', 'NA'] else ''}</td>
                <td>{data['pnp_pm'].get('UNCORE', {}).get('pm', '') if data['pnp_pm'].get('UNCORE', {}).get('pm', 'N/A') not in ['N/A', 'NA'] else ''}</td>
            </tr>
        </tbody>
    </table>
'''

    html += f'''{ubios_statement}</div>

</body>
</html>'''

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"[OK] Generated IFWI Release Status HTML: {output_file}")

    # Auto-open in browser
    webbrowser.open(output_file)
    print(f"[OK] Opened in browser")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python generate_ifwi_report.py <OSXML_Summary_CSV_file> [Orange_ID] [Release_Week] [uBIOS_Release_Week]")
        sys.exit(1)

    csv_file = sys.argv[1]
    user_orange_id = sys.argv[2] if len(sys.argv) > 2 else None
    user_release_week = sys.argv[3] if len(sys.argv) > 3 else None
    user_release_tense = sys.argv[4] if len(sys.argv) > 4 else 'has been released'

    # Generate output filename based on Orange ID
    import os
    basename = os.path.splitext(os.path.basename(csv_file))[0]
    orange_id = basename.replace('OSXML_Summary_', '')
    output_file = os.path.join(os.path.dirname(csv_file), f'IFWI_Release_Status_{orange_id}.html')

    # Parse and generate
    data = parse_osxml_summary(csv_file)

    # Add user-provided Orange ID, Release Week, and Release Tense to data
    if user_orange_id:
        data['user_orange_id'] = user_orange_id
    if user_release_week:
        data['user_release_week'] = user_release_week
    if user_release_tense:
        data['user_release_tense'] = user_release_tense

    generate_html_report(data, output_file)

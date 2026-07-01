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

def generate_orange_section(data, user_orange_id, user_release_week, user_release_tense='has been released'):
    """Generate HTML section for one Orange IFWI"""

    # Use platform/stepping from CSV if available (extracted from page text)
    if data.get('platform_stepping') and data['platform_stepping'] not in ['N/A', 'NA', '']:
        platform = data['platform_stepping']
        # Determine prefix based on AP1 or AP2
        if platform.startswith('AP1'):
            platform_desc = f'DMR-AP-UCC {platform}'
        elif platform.startswith('AP2'):
            platform_desc = f'DMR-AP-MCC {platform}'
        else:
            platform_desc = f'DMR-AP-UCC {platform}'
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
            platform_desc = f'DMR-AP-UCC AP1 {stepping}' if stepping != 'Unknown' else 'DMR-AP-UCC AP1'
        elif biosid.startswith('0035'):
            platform = f'AP2 {stepping}' if stepping != 'Unknown' else 'AP2'
            platform_desc = f'DMR-AP-MCC AP2 {stepping}' if stepping != 'Unknown' else 'DMR-AP-MCC AP2'
        else:
            platform = 'Unknown'
            platform_desc = 'DMR-AP-UCC'

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
    has_simics = (
        (data['simics_version'] and data['simics_version'] not in ['N/A', 'NA', '']) or
        data['osxml'].get('IMH_OSXML', {}).get('simics', 'N/A') not in ['N/A', 'NA', ''] or
        data['osxml'].get('CBB_OSXML', {}).get('simics', 'N/A') not in ['N/A', 'NA', ''] or
        data['osxml'].get('SCF_IPSD', {}).get('simics', 'N/A') not in ['N/A', 'NA', '']
    )

    # Build release statement
    ifwi_type = data.get('ifwi_type', 'Orange')
    release_statement = f'    <p style="color: #2c3e50; font-size: 18px; font-weight: bold;"><strong>{platform_desc} {ifwi_type} IFWI {user_orange_id} {user_release_tense} on {user_release_week}</strong></p>\n'

    # Build uBIOS statement if emulation exists (auto-calculate uBIOS week)
    ubios_statement = ''
    if data['has_emulation']:
        auto_ubios_week = calculate_ubios_release_week(user_release_week)
        if auto_ubios_week:
            # uBIOS always uses "will be released" (future tense)
            ubios_statement = f'    <p style="color: #2c3e50; font-size: 18px; font-weight: bold;"><strong>{platform} uBIOS based on BIOSID {data["biosid"]} will be released on {auto_ubios_week}</strong></p>\n'

    # Build Simics table row
    simics_table_row = ''
    if has_simics:
        simics_table_row = f'''            <tr>
                <td class="orange-id"><strong>Simics</strong></td>
                <td class="orange-id">{data['simics_version'] if data['simics_version'] else '-'}</td>
                <td>{data['osxml'].get('IMH_OSXML', {}).get('simics', '') if data['osxml'].get('IMH_OSXML', {}).get('simics', 'N/A') not in ['N/A', 'NA'] else ''}</td>
                <td>{data['osxml'].get('CBB_OSXML', {}).get('simics', '') if data['osxml'].get('CBB_OSXML', {}).get('simics', 'N/A') not in ['N/A', 'NA'] else ''}</td>
                <td>{data['osxml'].get('SCF_IPSD', {}).get('simics', '') if data['osxml'].get('SCF_IPSD', {}).get('simics', 'N/A') not in ['N/A', 'NA'] else ''}</td>
            </tr>
'''

    # Build Release Version Information table (always show BIOS and Unified Patch)
    osxml_table_html = ''
    if has_osxml:
        # Full table with OSXML columns
        osxml_table_html = f'''    <p><strong>Release version information as below:</strong></p>
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
        osxml_table_html = f'''    <p><strong>Release version information as below:</strong></p>
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
    pnp_pm_table_html = ''
    if has_pnp_pm:
        pnp_pm_table_html = f'''    <p><strong>PNP and PM recipe config in BIOS as below:</strong></p>
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

    section_html = f'''
<div class="orange-section">
{release_statement}{osxml_table_html}{pnp_pm_table_html}{ubios_statement}</div>
<hr style="margin: 30px 0; border: 1px solid #ddd;">
'''
    return section_html

def generate_multi_html_report(orange_list, output_file):
    """Generate combined HTML report with multiple Orange IFWIs"""

    today = datetime.now().strftime('%Y-%m-%d')

    # Generate sections for each Orange
    sections = ''
    for item in orange_list:
        sections += generate_orange_section(item['data'], item['orange_id'], item['release_week'], item.get('release_tense', 'has been released'))

    # Remove last <hr> tag
    if sections.endswith('<hr style="margin: 30px 0; border: 1px solid #ddd;">\n'):
        sections = sections[:-len('<hr style="margin: 30px 0; border: 1px solid #ddd;">\n')]

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>DMR Weekly Status Report</title>
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
        .orange-section {{
            background-color: white;
            padding: 20px;
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
    <p><strong>Generated:</strong> {today} | <strong>Total Orange IFWIs:</strong> {len(orange_list)}</p>
</div>

<div class="report-section">
{sections}
</div>

</body>
</html>'''

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"[OK] Generated Multi-IFWI Release Status HTML: {output_file}")

    # Auto-open in browser
    webbrowser.open(output_file)
    print(f"[OK] Opened in browser")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python generate_multi_ifwi_report.py <csv_list_file>")
        sys.exit(1)

    list_file = sys.argv[1]

    # Read CSV list file
    orange_list = []
    with open(list_file, 'r', encoding='utf-8-sig') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 3:
                continue
            csv_file = parts[0].strip()
            orange_id = parts[1].strip()
            release_week = parts[2].strip()
            release_tense = parts[3].strip() if len(parts) > 3 else 'has been released'
            data = parse_osxml_summary(csv_file)
            orange_list.append({
                'data': data,
                'orange_id': orange_id,
                'release_week': release_week,
                'release_tense': release_tense
            })

    if not orange_list:
        print("Error: No valid Orange IFWI data found")
        sys.exit(1)

    # Generate output filename based on date
    import os
    output_dir = os.path.dirname(orange_list[0]['data']['orange_id']) if orange_list else '.'
    output_file = os.path.join(os.path.dirname(list_file), f'DMR_Weekly_Status_Report_{datetime.now().strftime("%Y%m%d")}.html')

    # Generate combined report
    generate_multi_html_report(orange_list, output_file)

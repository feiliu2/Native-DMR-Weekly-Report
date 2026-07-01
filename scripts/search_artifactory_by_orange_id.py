"""
Search Artifactory for builds matching Orange ID (IFWI ID only)
Returns list of matching builds with BIOS IDs
"""

import sys
import requests
import re


def search_by_orange_id(platform_stepping, orange_id, api_token):
    """
    Search Artifactory for builds matching Orange ID pattern.

    Args:
        platform_stepping: 'AP1 A0', 'AP1 B0', or 'AP2 A0'
        orange_id: IFWI ID only (e.g., '2026.24.5.01')
        api_token: Artifactory API token

    Returns:
        List of matching builds with BIOS IDs
    """
    print(f"\n{'='*60}")
    print(f"Searching Artifactory for Orange ID")
    print(f"{'='*60}")
    print(f"Platform: {platform_stepping}")
    print(f"Orange ID: {orange_id}")

    base_url = "https://af01p-or.devtools.intel.com/artifactory/server-bios-staging-local/Daily/OakStreamAPIfwi"

    # Determine release type based on platform
    if platform_stepping == 'AP1 A0':
        release_type = "ap_post_silicon_rel"
    elif platform_stepping in ['AP1 B0', 'AP2 A0']:
        release_type = "ap_pre_silicon_rel"
    else:
        print(f"[ERROR] Unknown platform: {platform_stepping}")
        return None

    # Construct search path pattern
    search_pattern = f"OAKSTREAMAP.0.RPB.{orange_id}.*"
    api_url = f"{base_url.replace('/artifactory/', '/artifactory/api/storage/')}/{release_type}"

    print(f"\nQuerying: {api_url}")
    print(f"Pattern: {search_pattern}")

    headers = {'X-JFrog-Art-Api': api_token}

    try:
        response = requests.get(api_url, headers=headers, timeout=30)

        if response.status_code == 403:
            print(f"[ERROR] Authentication failed (HTTP 403)")
            print(f"Please check your API token")
            return None

        if response.status_code != 200:
            print(f"[ERROR] API request failed (HTTP {response.status_code})")
            return None

        # Parse JSON response
        data = response.json()
        children = data.get('children', [])

        print(f"\nSearching {len(children)} directories...")

        # Look for directories matching pattern
        matches = []
        for child in children:
            if not child.get('folder', False):
                continue

            dirname = child['uri'].lstrip('/')

            # Match pattern: OAKSTREAMAP.0.RPB.{orange_id}.{bios_id}
            pattern = rf'OAKSTREAMAP\.0\.RPB\.{re.escape(orange_id)}\.(\d{{4}}\.D\.\d+)'
            match = re.match(pattern, dirname)

            if match:
                bios_id = match.group(1)
                matches.append({
                    'dir_name': dirname,
                    'bios_id': bios_id,
                    'full_version': f"{orange_id}.{bios_id}"
                })
                print(f"  [OK] Found: {dirname}")
                print(f"    BIOS ID: {bios_id}")

        if not matches:
            print(f"\n[ERROR] No builds found for Orange ID: {orange_id}")
            print(f"\nPossible reasons:")
            print(f"  - Orange ID is incorrect")
            print(f"  - Build not yet available in Artifactory")
            print(f"  - Wrong platform selected")
            return None

        print(f"\n{'='*60}")
        print(f"Found {len(matches)} matching build(s)")
        print(f"{'='*60}")

        return matches

    except requests.exceptions.Timeout:
        print(f"[ERROR] Request timeout")
        return None
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Network error: {e}")
        return None
    except Exception as e:
        print(f"[ERROR] Search failed: {e}")
        return None


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python search_artifactory_by_orange_id.py <platform> <orange_id> <api_token>")
        print("")
        print("Examples:")
        print("  python search_artifactory_by_orange_id.py \"AP1 A0\" \"2026.26.4.01\" <token>")
        print("  python search_artifactory_by_orange_id.py \"AP1 B0\" \"2026.24.5.01\" <token>")
        sys.exit(1)

    platform = sys.argv[1]
    orange_id = sys.argv[2]
    api_token = sys.argv[3]

    matches = search_by_orange_id(platform, orange_id, api_token)

    if matches:
        if len(matches) == 1:
            # Single match - output for PowerShell to capture
            print(f"\nBIOS_ID:{matches[0]['bios_id']}")
            print(f"VERSION:{matches[0]['full_version']}")
        else:
            # Multiple matches - let user choose
            print(f"\n{'='*60}")
            print(f"Multiple builds found for Orange ID {orange_id}")
            print(f"{'='*60}")
            for i, match in enumerate(matches, 1):
                print(f"{i}. BIOS ID: {match['bios_id']}")

            # Output all matches for PowerShell
            for i, match in enumerate(matches):
                print(f"MATCH_{i}_BIOS_ID:{match['bios_id']}")
                print(f"MATCH_{i}_VERSION:{match['full_version']}")
    else:
        sys.exit(1)

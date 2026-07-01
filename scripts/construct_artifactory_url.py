"""
Construct Artifactory URL from platform and IFWI/BIOS IDs
"""

import sys
import requests
import re


def construct_artifactory_url(platform_stepping, ifwi_id, bios_id, api_token):
    """
    Construct Artifactory URL from platform and version information.

    Args:
        platform_stepping: 'AP1 A0', 'AP1 B0', or 'AP2 A0'
        ifwi_id: IFWI ID (e.g., '2026.26.4.01')
        bios_id: BIOS ID (e.g., '0036.D.54')
        api_token: Artifactory API token

    Returns:
        Full URL to BuildPkg.7z file
    """
    print(f"\n{'='*60}")
    print(f"Constructing Artifactory URL")
    print(f"{'='*60}")
    print(f"Platform: {platform_stepping}")
    print(f"IFWI ID: {ifwi_id}")
    print(f"BIOS ID: {bios_id}")

    base_url = "https://af01p-or.devtools.intel.com/artifactory/server-bios-staging-local/Daily/OakStreamAPIfwi"

    # Determine release type and subfolder based on platform
    if platform_stepping == 'AP1 A0':
        release_type = "ap_post_silicon_rel"
        subfolder = "OakStreamRp_DMR_1P0_FSP_Glue_Debug_Linux"
        print(f"Release Type: Post-Silicon")
    elif platform_stepping in ['AP1 B0', 'AP2 A0']:
        release_type = "ap_pre_silicon_rel"
        subfolder = "OakStreamRp_DMR_FSP_Glue_Debug_Linux"
        print(f"Release Type: Pre-Silicon")
    else:
        print(f"[ERROR] Unknown platform: {platform_stepping}")
        print(f"Supported platforms: AP1 A0, AP1 B0, AP2 A0")
        return None

    # Construct version path: OAKSTREAMAP.0.RPB.{IFWI_ID}.{BIOS_ID}
    version_path = f"OAKSTREAMAP.0.RPB.{ifwi_id}.{bios_id}"

    # Construct directory URL
    dir_path = f"{base_url}/{release_type}/{version_path}/{subfolder}"
    print(f"\nDirectory path: {dir_path}")

    # Use Artifactory Storage API to list directory contents
    api_url = dir_path.replace('/artifactory/', '/artifactory/api/storage/')

    print(f"\nQuerying Artifactory API...")
    headers = {'X-JFrog-Art-Api': api_token}

    try:
        response = requests.get(api_url, headers=headers, timeout=30)

        if response.status_code == 404:
            print(f"[ERROR] Directory not found (HTTP 404)")
            print(f"URL: {api_url}")
            print(f"\nPossible reasons:")
            print(f"  - IFWI ID or BIOS ID is incorrect")
            print(f"  - Build not yet available in Artifactory")
            print(f"  - Path structure has changed")
            return None

        elif response.status_code == 403:
            print(f"[ERROR] Authentication failed (HTTP 403)")
            print(f"Please check your API token")
            return None

        elif response.status_code != 200:
            print(f"[ERROR] API request failed (HTTP {response.status_code})")
            return None

        # Parse JSON response to find BuildPkg.7z file
        data = response.json()
        children = data.get('children', [])

        print(f"Found {len(children)} files in directory")

        # Look for file matching pattern: *_BuildPkg.7z
        buildpkg_files = []
        for child in children:
            filename = child['uri'].lstrip('/')
            if filename.endswith('_BuildPkg.7z'):
                buildpkg_files.append(filename)
                print(f"  - {filename}")

        if not buildpkg_files:
            print(f"[ERROR] No BuildPkg.7z file found in directory")
            return None

        if len(buildpkg_files) > 1:
            print(f"[WARN] Multiple BuildPkg.7z files found, using first one")

        # Construct full URL
        buildpkg_filename = buildpkg_files[0]
        full_url = f"{dir_path}/{buildpkg_filename}"

        print(f"\n{'='*60}")
        print(f"[OK] Found BuildPkg.7z file")
        print(f"{'='*60}")
        print(f"File: {buildpkg_filename}")
        print(f"URL: {full_url}")

        return full_url

    except requests.exceptions.Timeout:
        print(f"[ERROR] Request timeout - Artifactory may be slow or unreachable")
        return None
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Network error: {e}")
        return None
    except Exception as e:
        print(f"[ERROR] Failed to construct URL: {e}")
        return None


def parse_version_string(version_string):
    """
    Parse version string in format: IFWI_ID.BIOS_ID

    Examples:
        '2026.26.4.01.0036.D.54' -> ('2026.26.4.01', '0036.D.54')
        '2026.25.3.01 0036.D.29' -> ('2026.25.3.01', '0036.D.29')

    Returns:
        Tuple of (ifwi_id, bios_id)
    """
    # Try different separators
    if '.' in version_string:
        # Count dots to determine split point
        # IFWI ID: 2026.26.4.01 (4 parts, 3 dots)
        # BIOS ID: 0036.D.54 (3 parts, 2 dots)
        parts = version_string.split('.')
        if len(parts) >= 7:
            # Standard format: YYYY.WW.X.NN.BBBB.D.VV
            ifwi_id = '.'.join(parts[:4])
            bios_id = '.'.join(parts[4:7])
            return ifwi_id, bios_id

    # Try space separator
    if ' ' in version_string:
        parts = version_string.split()
        if len(parts) >= 2:
            return parts[0], parts[1]

    raise ValueError(f"Cannot parse version string: {version_string}")


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python construct_artifactory_url.py <platform> <version> <api_token>")
        print("")
        print("Examples:")
        print("  python construct_artifactory_url.py \"AP1 A0\" \"2026.26.4.01.0036.D.54\" <token>")
        print("  python construct_artifactory_url.py \"AP1 B0\" \"2026.25.3.01.0036.D.29\" <token>")
        print("  python construct_artifactory_url.py \"AP2 A0\" \"2026.26.4.02.0036.D.54\" <token>")
        print("")
        print("Version format: IFWI_ID.BIOS_ID (e.g., 2026.26.4.01.0036.D.54)")
        print("  or: IFWI_ID BIOS_ID (space-separated)")
        sys.exit(1)

    platform_stepping = sys.argv[1]
    version_string = sys.argv[2]
    api_token = sys.argv[3]

    try:
        # Parse version string
        ifwi_id, bios_id = parse_version_string(version_string)

        # Construct URL
        url = construct_artifactory_url(platform_stepping, ifwi_id, bios_id, api_token)

        if url:
            print(f"\n{'='*60}")
            print(f"SUCCESS")
            print(f"{'='*60}")
            print(f"URL: {url}")
            print(f"\nYou can now use this URL with:")
            print(f"  python extract_artifactory_osxml.py \"{url}\" <token> . \"{platform_stepping}\" <simics_version>")
        else:
            sys.exit(1)

    except ValueError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

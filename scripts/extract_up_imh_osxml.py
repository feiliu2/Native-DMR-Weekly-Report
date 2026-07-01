"""
Extract IMH OSXML from Unified Patch release notes
"""

import os
import sys
import requests
import py7zr
import csv
import re


def download_unified_patch_package(up_version, platform_stepping, api_token, output_dir='.'):
    """Download Unified Patch package from Artifactory.

    Args:
        up_version: Unified Patch version (e.g., 51000312, 52000210)
        platform_stepping: Platform/stepping (e.g., 'AP1 B0', 'AP2 A0')
        api_token: Artifactory API token
        output_dir: Directory to save downloaded file

    Returns:
        Path to downloaded .7z file, or None if failed
    """
    # Construct URL based on platform
    if platform_stepping == 'AP1 B0':
        base_url = "https://af01p-sc.devtools.intel.com/artifactory/DEG-IFWI-LOCAL/SiEn-OakStream-DiamondRapids-AP/Ingredients/IMH1_B0_DMRAP_Unified_Patch"
        filename = f"UP_DMR_AP1_B0_{up_version}_TPRODSIGNED.7z"
    elif platform_stepping == 'AP2 A0':
        base_url = "https://af01p-sc.devtools.intel.com/artifactory/DEG-IFWI-LOCAL/SiEn-OakStream-DiamondRapids-AP/Ingredients/IMH2_B0_DMRAP_Unified_Patch"
        filename = f"UP_DMR_AP2_B0_{up_version}_TPRODSIGNED.7z"
    else:
        print(f"[WARN] Unified Patch download not supported for {platform_stepping}")
        return None

    url = f"{base_url}/{up_version}/{filename}"
    output_path = os.path.join(output_dir, filename)

    print(f"\nDownloading Unified Patch package...")
    print(f"Platform: {platform_stepping}")
    print(f"UP Version: {up_version}")
    print(f"URL: {url}")

    headers = {
        'X-JFrog-Art-Api': api_token
    }

    try:
        response = requests.get(url, headers=headers, stream=True, timeout=60)

        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            file_size = os.path.getsize(output_path)
            print(f"[OK] Downloaded: {output_path} ({file_size} bytes)")
            return output_path

        elif response.status_code == 404:
            print(f"[ERROR] Unified Patch package not found (HTTP 404)")
            print(f"URL: {url}")
            return None
        elif response.status_code == 403:
            print(f"[ERROR] Authentication failed (HTTP 403). Check API Token.")
            return None
        else:
            print(f"[ERROR] Download failed (HTTP {response.status_code})")
            return None

    except Exception as e:
        print(f"[ERROR] Failed to download Unified Patch package: {e}")
        return None


def extract_release_notes_csv(archive_path, output_dir='.'):
    """Extract _release_notes.csv from Unified Patch .7z archive.

    Args:
        archive_path: Path to .7z file
        output_dir: Directory to extract to

    Returns:
        Path to extracted CSV file, or None if not found
    """
    print(f"\nExtracting release notes from archive...")

    try:
        with py7zr.SevenZipFile(archive_path, mode='r') as archive:
            all_files = archive.getnames()

            # Find _release_notes.csv
            csv_file = None
            for filename in all_files:
                if filename.endswith('_release_notes.csv'):
                    csv_file = filename
                    break

            if not csv_file:
                print(f"[ERROR] _release_notes.csv not found in archive")
                return None

            print(f"Found: {csv_file}")

            # Extract the CSV file
            archive.extract(targets=[csv_file], path=output_dir)

            # Get full path
            extracted_path = os.path.join(output_dir, csv_file)

            # If extracted to subdirectory, move to output_dir root
            if os.path.dirname(csv_file):
                final_path = os.path.join(output_dir, os.path.basename(csv_file))
                if os.path.exists(extracted_path):
                    import shutil
                    shutil.move(extracted_path, final_path)
                    # Clean up empty directories
                    try:
                        os.rmdir(os.path.join(output_dir, os.path.dirname(csv_file)))
                    except:
                        pass
                    extracted_path = final_path

            print(f"[OK] Extracted: {extracted_path}")
            return extracted_path

    except Exception as e:
        print(f"[ERROR] Failed to extract release notes: {e}")
        return None


def parse_imh_osxml_from_csv(csv_path, platform_stepping):
    """Parse IMH OSXML version from release notes CSV.

    Args:
        csv_path: Path to _release_notes.csv
        platform_stepping: Platform/stepping (determines search keyword)

    Returns:
        IMH OSXML version string, or None if not found
    """
    print(f"\nParsing IMH OSXML from release notes...")

    # Determine search keyword based on platform
    if platform_stepping == 'AP1 B0':
        search_keyword = 'imh_osxml'
    elif platform_stepping == 'AP2 A0':
        search_keyword = 'dmrhub2'
    else:
        print(f"[WARN] Unknown platform for IMH OSXML extraction: {platform_stepping}")
        return None

    print(f"Search keyword: {search_keyword}")

    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            content = f.read()

            # Search for keyword (case-insensitive)
            for line in content.split('\n'):
                if search_keyword.lower() in line.lower():
                    print(f"Found line: {line[:150]}...")

                    # Try to extract OSXML version from the line
                    # AP1 B0 pattern: OSXML,LTM,iMH: dmr_imh_osxml-IMH1-B0-1P0N-OSXML-1d,26ww22a
                    # AP2 A0 pattern: dmrhub2,IMH2-1p0D_26ww03g_RTL-OSXML-1d

                    if platform_stepping == 'AP1 B0':
                        # Look for pattern: dmr_imh_osxml-XXX where XXX is the version
                        match = re.search(r'dmr_imh_osxml-([^,\s]+)', line, re.IGNORECASE)
                        if match:
                            imh_osxml = match.group(1).strip()
                            print(f"[OK] Found IMH OSXML: {imh_osxml}")
                            return imh_osxml

                    elif platform_stepping == 'AP2 A0':
                        # Look for pattern: dmrhub2-xxx-IMH2-xxx
                        # Example: dmrhub2-a0-26ww06h-IMH2-1p0G_26ww06h_RTL-OSXML-1d
                        match = re.search(r'dmrhub2-[^-]+-[^-]+-([^,\s]+)', line, re.IGNORECASE)
                        if match:
                            imh_osxml = match.group(1).strip()
                            # Verify it contains IMH2
                            if 'IMH2' in imh_osxml:
                                print(f"[OK] Found IMH OSXML: {imh_osxml}")
                                return imh_osxml

        print(f"[WARN] IMH OSXML not found in release notes")
        return None

    except Exception as e:
        print(f"[ERROR] Failed to parse release notes: {e}")
        return None


def extract_imh_osxml_from_up(up_version, platform_stepping, api_token, output_dir='.'):
    """Main function to extract IMH OSXML from Unified Patch package.

    Args:
        up_version: Unified Patch version
        platform_stepping: Platform/stepping
        api_token: Artifactory API token
        output_dir: Working directory

    Returns:
        IMH OSXML version string, or None if failed
    """
    print(f"\n{'='*60}")
    print(f"Extracting IMH OSXML from Unified Patch")
    print(f"{'='*60}")

    # Step 1: Download UP package
    archive_path = download_unified_patch_package(up_version, platform_stepping, api_token, output_dir)
    if not archive_path:
        return None

    # Step 2: Extract release notes CSV
    csv_path = extract_release_notes_csv(archive_path, output_dir)
    if not csv_path:
        return None

    # Step 3: Parse IMH OSXML from CSV
    imh_osxml = parse_imh_osxml_from_csv(csv_path, platform_stepping)

    # Cleanup
    try:
        if archive_path and os.path.exists(archive_path):
            os.remove(archive_path)
            print(f"\nCleaned up: {archive_path}")
        if csv_path and os.path.exists(csv_path):
            os.remove(csv_path)
            print(f"Cleaned up: {csv_path}")
    except Exception as e:
        print(f"[WARN] Cleanup failed: {e}")

    return imh_osxml


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python extract_up_imh_osxml.py <up_version> <platform_stepping> <api_token>")
        print("Example: python extract_up_imh_osxml.py 51000312 \"AP1 B0\" <token>")
        sys.exit(1)

    up_version = sys.argv[1]
    platform_stepping = sys.argv[2]
    api_token = sys.argv[3]

    result = extract_imh_osxml_from_up(up_version, platform_stepping, api_token)

    if result:
        print(f"\n{'='*60}")
        print(f"SUCCESS: IMH OSXML = {result}")
        print(f"{'='*60}")
    else:
        print(f"\n{'='*60}")
        print(f"FAILED to extract IMH OSXML")
        print(f"{'='*60}")
        sys.exit(1)

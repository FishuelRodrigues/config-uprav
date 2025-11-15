import argparse
import urllib.request
import tarfile
import io
import re

def parse_arguments():
    parser = argparse.ArgumentParser(description='Dependency Graph Visualizer for APK packages')
    
    parser.add_argument('--package', required=True, help='Name of the package to analyze')
    parser.add_argument('--repository', required=True, help='URL of repository or path to test repository file')
    parser.add_argument('--test-mode', action='store_true', help='Enable test repository mode')
    parser.add_argument('--output-image', help='Name of generated graph image file')
    parser.add_argument('--ascii-tree', action='store_true', help='Display dependencies as ASCII tree')
    parser.add_argument('--max-depth', type=int, help='Maximum dependency analysis depth')
    parser.add_argument('--filter-substring', help='Substring to filter packages')
    
    return parser.parse_args()

def display_config(args):
    print("Configuration parameters:")
    print(f"  Package: {args.package}")
    print(f"  Repository: {args.repository}")
    print(f"  Test mode: {args.test_mode}")
    print(f"  Output image: {args.output_image}")
    print(f"  ASCII tree: {args.ascii_tree}")
    print(f"  Max depth: {args.max_depth}")
    print(f"  Filter substring: {args.filter_substring}")

def download_apkindex(repository_url):
    """Download and extract APKINDEX from Alpine repository"""
    try:
        apkindex_url = f"{repository_url}/APKINDEX.tar.gz"
        
        with urllib.request.urlopen(apkindex_url) as response:
            tar_data = response.read()
        
        with tarfile.open(fileobj=io.BytesIO(tar_data), mode='r:gz') as tar:
            apkindex_file = tar.extractfile('APKINDEX')
            if apkindex_file:
                return apkindex_file.read().decode('utf-8')
        
        return None
    except Exception as e:
        print(f"Error downloading APKINDEX: {e}")
        return None

def parse_apkindex(apkindex_content, package_name):
    """Parse APKINDEX content and find dependencies for specified package"""
    if not apkindex_content:
        return None
    
    # APKINDEX format: entries separated by empty lines
    entries = apkindex_content.strip().split('\n\n')
    
    for entry in entries:
        lines = entry.split('\n')
        package_info = {}
        
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                package_info[key] = value
        
        if package_info.get('P') == package_name:
            # Extract dependencies from D field
            dependencies = package_info.get('D', '')
            return [dep.strip() for dep in dependencies.split() if dep.strip()]
    
    return None

def get_dependencies_from_url(repository_url, package_name):
    """Get dependencies from online repository"""
    apkindex_content = download_apkindex(repository_url)
    if not apkindex_content:
        print("Failed to download or parse APKINDEX")
        return None
    
    return parse_apkindex(apkindex_content, package_name)

def main():
    # Stage 1: Configuration and prototype
    args = parse_arguments()
    display_config(args)
    
    # Stage 2: Data collection
    print(f"\nStage 2: Collecting dependencies for package '{args.package}'")
    
    if args.test_mode:
        print("Test mode: Using test repository file")
        # For now, we'll implement online repository first
        # Test repository functionality would be added in Stage 3
        print("Test repository functionality will be implemented in Stage 3")
        return
    
    dependencies = get_dependencies_from_url(args.repository, args.package)
    
    if dependencies is None:
        print(f"Package '{args.package}' not found in repository")
        return
    
    if not dependencies:
        print(f"Package '{args.package}' has no dependencies")
        return
    
    print(f"Direct dependencies for '{args.package}':")
    for dep in dependencies:
        print(f"  - {dep}")

if __name__ == "__main__":
    main()
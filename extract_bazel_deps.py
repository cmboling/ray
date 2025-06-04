#!/usr/bin/env python3
"""
Ray Bazel Dependencies Analyzer

This script extracts and analyzes Bazel dependencies from Ray project
to categorize them as production runtime vs build-time only dependencies.

Usage:
    python3 extract_bazel_deps.py [--output fossa-deps.yml] [--format {fossa,json,txt}]
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


class BazelDepsAnalyzer:
    def __init__(self, ray_root: Path):
        self.ray_root = Path(ray_root)
        self.workspace_file = self.ray_root / "WORKSPACE"
        self.deps_setup_file = self.ray_root / "bazel" / "ray_deps_setup.bzl"
        self.build_file = self.ray_root / "BUILD.bazel"
        
        # Categories of dependencies
        self.production_deps = set()
        self.build_only_deps = set()
        self.test_only_deps = set()
        self.unknown_deps = set()
        
        # Dependency metadata
        self.dep_metadata = {}
        
    def extract_external_repos(self) -> Dict[str, Dict]:
        """Extract external repository definitions from WORKSPACE and deps files."""
        external_repos = {}
        
        # Parse WORKSPACE file
        if self.workspace_file.exists():
            content = self.workspace_file.read_text()
            external_repos.update(self._parse_workspace_deps(content))
        
        # Parse ray_deps_setup.bzl
        if self.deps_setup_file.exists():
            content = self.deps_setup_file.read_text()
            external_repos.update(self._parse_auto_http_archive_deps(content))
            
        return external_repos
    
    def _parse_workspace_deps(self, content: str) -> Dict[str, Dict]:
        """Parse dependencies from WORKSPACE file."""
        deps = {}
        
        # Pattern for http_archive and git_repository - use same multiline approach
        patterns = ['http_archive', 'git_repository']
        
        for func_name in patterns:
            # Extract each function block - handle multiline
            blocks = []
            start_pattern = rf'{func_name}\s*\('
            
            for match in re.finditer(start_pattern, content):
                start = match.start()
                pos = match.end() - 1  # Position of opening paren
                paren_count = 1
                i = pos + 1
                
                # Find matching closing paren
                while i < len(content) and paren_count > 0:
                    if content[i] == '(':
                        paren_count += 1
                    elif content[i] == ')':
                        paren_count -= 1
                    i += 1
                
                if paren_count == 0:
                    blocks.append((content[start:i], func_name))
            
            for block, func_type in blocks:
                name_match = re.search(r'name\s*=\s*"([^"]+)"', block)
                
                # Look for url, urls (list), or remote field
                url_match = re.search(r'(?:url|remote)\s*=\s*"([^"]+)"', block)
                if not url_match:
                    urls_match = re.search(r'urls\s*=\s*\[\s*"([^"]+)"', block)
                    if urls_match:
                        url_match = urls_match
                
                if name_match and url_match:
                    name = name_match.group(1)
                    url = url_match.group(1)
                    deps[name] = {
                        'name': name,
                        'url': url,
                        'source': 'WORKSPACE',
                        'type': func_type
                    }
                
        return deps
    
    def _parse_auto_http_archive_deps(self, content: str) -> Dict[str, Dict]:
        """Parse dependencies from ray_deps_setup.bzl auto_http_archive calls."""
        deps = {}
        
        # Extract each auto_http_archive block - handle multiline with balanced parentheses
        import re
        blocks = []
        
        # Find start positions of auto_http_archive calls
        start_pattern = r'auto_http_archive\s*\('
        for match in re.finditer(start_pattern, content):
            start = match.start()
            pos = match.end() - 1  # Position of opening paren
            paren_count = 1
            i = pos + 1
            
            # Find matching closing paren
            while i < len(content) and paren_count > 0:
                if content[i] == '(':
                    paren_count += 1
                elif content[i] == ')':
                    paren_count -= 1
                i += 1
            
            if paren_count == 0:
                blocks.append(content[start:i])
        
        for block in blocks:
            name_match = re.search(r'name\s*=\s*"([^"]+)"', block)
            
            # Look for url, urls (list), or remote field  
            url_match = re.search(r'url\s*=\s*"([^"]+)"', block)
            if not url_match:
                # Try urls field (list format)
                urls_match = re.search(r'urls\s*=\s*\[\s*"([^"]+)"', block)
                if urls_match:
                    url_match = urls_match
            
            if name_match and url_match:
                name = name_match.group(1)
                url = url_match.group(1)
                
                # Extract version if present
                version_match = re.search(r'v?(\d+\.\d+\.\d+)', url)
                version = version_match.group(1) if version_match else "unknown"
                
                deps[name] = {
                    'name': name,
                    'url': url,
                    'version': version,
                    'source': 'ray_deps_setup.bzl',
                    'type': 'auto_http_archive'
                }
            
        return deps
    
    def categorize_dependencies(self, external_repos: Dict[str, Dict]) -> None:
        """Categorize dependencies as production, build-only, or test-only."""
        
        # Known production runtime dependencies (linked into final binaries)
        production_patterns = {
            # Core C++ libraries that are linked into _raylet.so
            'com_google_absl', 'com_github_grpc_grpc', 'com_google_protobuf',
            'msgpack', 'nlohmann_json', 'rapidjson', 'com_github_spdlog',
            'com_github_redis_hiredis', 'com_github_antirez_redis',
            'boringssl', 'openssl', 'jemalloc',
            'io_opentelemetry_cpp', 'io_opencensus_cpp', 'com_github_jupp0r_prometheus_cpp',
            'com_github_google_flatbuffers', 'com_github_nelhage_rules_boost'
        }
        
        # Known build-only dependencies
        build_only_patterns = {
            # Build system tools and rules
            'bazel_skylib', 'rules_python', 'rules_foreign_cc', 'rules_jvm_external',
            'hedron_compile_commands', 'bazel_common', 'platforms',
            'crane_linux_x86_64', 'com_github_storypku_bazel_iwyu',
            'rules_proto_grpc', 'com_google_protobuf_rules_proto_grpc',
            'com_github_johnynek_bazel_jar_jar', 'rules_perl',
            'python3_9', 'py_deps_buildkite'
        }
        
        # Known test-only dependencies  
        test_only_patterns = {
            'com_google_googletest', 'com_github_gflags_gflags'
        }
        
        # Categorize each dependency
        for name, metadata in external_repos.items():
            if any(pattern in name for pattern in production_patterns):
                self.production_deps.add(name)
                metadata['category'] = 'production'
            elif any(pattern in name for pattern in build_only_patterns):
                self.build_only_deps.add(name)
                metadata['category'] = 'build_only'
            elif any(pattern in name for pattern in test_only_patterns):
                self.test_only_deps.add(name)
                metadata['category'] = 'test_only'
            else:
                # For unknown deps, make educated guesses based on usage patterns
                if 'test' in name.lower() or 'mock' in name.lower():
                    self.test_only_deps.add(name)
                    metadata['category'] = 'test_only'
                elif 'rules_' in name or 'bazel' in name or name == 'cython':
                    self.build_only_deps.add(name)
                    metadata['category'] = 'build_only'
                else:
                    self.unknown_deps.add(name)
                    metadata['category'] = 'unknown'
            
            self.dep_metadata[name] = metadata
    
    def generate_fossa_deps(self, include_build_deps: bool = False) -> Dict:
        """Generate fossa-deps.yml format output."""
        fossa_deps = {
            'referenced-dependencies': [],
            'remote-dependencies': [],
            'custom-dependencies': [],
            'vendored-dependencies': []
        }
        
        # Only include production dependencies by default
        deps_to_include = self.production_deps.copy()
        if include_build_deps:
            deps_to_include.update(self.build_only_deps)
        
        for dep_name in sorted(deps_to_include):
            metadata = self.dep_metadata.get(dep_name, {})
            
            # Skip if no metadata
            if not metadata:
                continue
                
            dep_entry = {
                'name': self._clean_dep_name(dep_name),
                'version': metadata.get('version', 'unknown'),
                'url': metadata.get('url', ''),
                'description': self._get_description(dep_name, metadata)
            }
            
            fossa_deps['remote-dependencies'].append(dep_entry)
        
        # Add custom entry for patches
        if self.production_deps or include_build_deps:
            fossa_deps['custom-dependencies'].append({
                'name': 'ray-bazel-patches',
                'version': '1.0.0',
                'license': 'Apache-2.0',
                'description': 'Custom patches applied to Bazel external dependencies for cross-platform compatibility',
                'homepage': 'https://github.com/ray-project/ray/tree/master/thirdparty/patches'
            })
        
        return fossa_deps
    
    def _clean_dep_name(self, name: str) -> str:
        """Clean up dependency name for display."""
        # Map common prefixes to cleaner names
        name_mappings = {
            'com_google_': '',
            'com_github_': '',
            'io_': '',
            '_cpp': '-cpp',
            '_c': '-c'
        }
        
        cleaned = name
        for prefix, replacement in name_mappings.items():
            if cleaned.startswith(prefix):
                cleaned = replacement + cleaned[len(prefix):]
                break
                
        # Special cases
        special_mappings = {
            'antirez_redis': 'redis',
            'redis_hiredis': 'hiredis',
            'google_protobuf': 'protobuf',
            'google_absl': 'abseil-cpp',
            'grpc_grpc': 'grpc',
            'google_flatbuffers': 'flatbuffers',
            'jupp0r_prometheus_cpp': 'prometheus-cpp',
            'google_googletest': 'googletest',
            'gflags_gflags': 'gflags',
            'nelhage_rules_boost': 'boost-rules',
            'johnynek_bazel_jar_jar': 'bazel-jar-jar',
            'storypku_bazel_iwyu': 'bazel-iwyu'
        }
        
        for pattern, replacement in special_mappings.items():
            if pattern in cleaned:
                cleaned = replacement
                break
        
        return cleaned
    
    def _get_description(self, name: str, metadata: Dict) -> str:
        """Get human-readable description for dependency."""
        descriptions = {
            'redis': 'In-memory data structure store',
            'hiredis': 'Redis C client library',
            'spdlog': 'Fast C++ logging library',
            'protobuf': 'Protocol Buffers serialization library',
            'grpc': 'gRPC framework for RPC communication',
            'abseil-cpp': 'Abseil C++ common libraries',
            'flatbuffers': 'Memory efficient serialization library',
            'msgpack': 'MessagePack object serialization',
            'nlohmann-json': 'JSON library for C++',
            'rapidjson': 'Fast JSON parser and generator',
            'boringssl': "Google's fork of OpenSSL",
            'openssl': 'SSL/TLS library',
            'opencensus-cpp': 'Application performance monitoring',
            'opentelemetry-cpp': 'Observability framework',
            'prometheus-cpp': 'Prometheus C++ client library',
            'googletest': 'C++ testing framework',
            'gflags': 'Command-line flags library',
            'boost-rules': 'Boost C++ libraries for Bazel',
            'jemalloc': 'Memory allocator',
            'cython': 'Python to C compiler',
            'bazel-skylib': 'Bazel build tool library',
            'rules-python': 'Python Bazel rules',
            'bazel-common': 'Google Bazel common utilities'
        }
        
        cleaned_name = self._clean_dep_name(name)
        return descriptions.get(cleaned_name, f"External dependency: {cleaned_name}")
    
    def print_analysis(self) -> None:
        """Print dependency analysis to stdout."""
        print("=== Ray Bazel Dependencies Analysis ===\n")
        
        print(f"📦 PRODUCTION DEPENDENCIES ({len(self.production_deps)}):")
        print("   (Linked into final Ray binaries - should be in fossa-deps)")
        for dep in sorted(self.production_deps):
            metadata = self.dep_metadata.get(dep, {})
            clean_name = self._clean_dep_name(dep)
            version = metadata.get('version', 'unknown')
            print(f"   ✓ {clean_name} ({version})")
        
        print(f"\n🔧 BUILD-ONLY DEPENDENCIES ({len(self.build_only_deps)}):")
        print("   (Build tools only - typically excluded from fossa-deps)")
        for dep in sorted(self.build_only_deps):
            metadata = self.dep_metadata.get(dep, {})
            clean_name = self._clean_dep_name(dep)
            version = metadata.get('version', 'unknown')
            print(f"   ○ {clean_name} ({version})")
        
        print(f"\n🧪 TEST-ONLY DEPENDENCIES ({len(self.test_only_deps)}):")
        print("   (Testing frameworks - typically excluded from production fossa-deps)")
        for dep in sorted(self.test_only_deps):
            metadata = self.dep_metadata.get(dep, {})
            clean_name = self._clean_dep_name(dep)
            version = metadata.get('version', 'unknown')
            print(f"   ⚡ {clean_name} ({version})")
        
        if self.unknown_deps:
            print(f"\n❓ UNKNOWN DEPENDENCIES ({len(self.unknown_deps)}):")
            print("   (Need manual classification)")
            for dep in sorted(self.unknown_deps):
                metadata = self.dep_metadata.get(dep, {})
                clean_name = self._clean_dep_name(dep)
                version = metadata.get('version', 'unknown')
                print(f"   ? {clean_name} ({version})")
        
        print(f"\n📊 SUMMARY:")
        print(f"   Production runtime deps: {len(self.production_deps)}")
        print(f"   Build-only deps: {len(self.build_only_deps)}")
        print(f"   Test-only deps: {len(self.test_only_deps)}")
        print(f"   Unknown classification: {len(self.unknown_deps)}")
        print(f"   Total external deps: {len(self.dep_metadata)}")


def main():
    parser = argparse.ArgumentParser(description='Analyze Ray Bazel dependencies')
    parser.add_argument('--ray-root', default='.', help='Path to Ray project root')
    parser.add_argument('--output', help='Output file path')
    parser.add_argument('--format', choices=['fossa', 'json', 'txt'], default='txt',
                       help='Output format')
    parser.add_argument('--include-build-deps', action='store_true',
                       help='Include build-only dependencies in fossa output')
    
    args = parser.parse_args()
    
    # Initialize analyzer
    analyzer = BazelDepsAnalyzer(args.ray_root)
    
    # Extract and categorize dependencies
    external_repos = analyzer.extract_external_repos()
    analyzer.categorize_dependencies(external_repos)
    
    # Output based on format
    if args.format == 'txt':
        analyzer.print_analysis()
    elif args.format == 'json':
        output = {
            'production_deps': list(analyzer.production_deps),
            'build_only_deps': list(analyzer.build_only_deps),
            'test_only_deps': list(analyzer.test_only_deps),
            'unknown_deps': list(analyzer.unknown_deps),
            'metadata': analyzer.dep_metadata
        }
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(output, f, indent=2)
        else:
            print(json.dumps(output, indent=2))
    elif args.format == 'fossa':
        if not HAS_YAML:
            print("ERROR: PyYAML not installed. Install with: pip install PyYAML")
            sys.exit(1)
        fossa_deps = analyzer.generate_fossa_deps(args.include_build_deps)
        if args.output:
            with open(args.output, 'w') as f:
                yaml.dump(fossa_deps, f, default_flow_style=False, sort_keys=False)
            print(f"✅ Generated fossa-deps.yml with {len(fossa_deps['remote-dependencies'])} dependencies")
        else:
            print(yaml.dump(fossa_deps, default_flow_style=False, sort_keys=False))


if __name__ == '__main__':
    main()
# Ray Dependency Source Analysis

## Dependencies by Source

### 1. **ACTUAL BAZEL EXTERNAL DEPENDENCIES** (from WORKSPACE & ray_deps_setup.bzl)

**From `bazel/ray_deps_setup.bzl` (auto_http_archive):**
- `com_github_antirez_redis` - Redis 7.2.3
- `com_github_redis_hiredis` - Hiredis client
- `com_github_spdlog` - spdlog 1.12.0 
- `com_github_tporadowski_redis_bin` - Redis Windows binaries
- `com_google_protobuf` - Protocol Buffers (gRPC pinned)
- `com_github_grpc_grpc` - gRPC 1.57.1
- `com_google_absl` - Abseil C++ 20230802.1
- `com_github_google_flatbuffers` - FlatBuffers 25.2.10
- `msgpack` - MessagePack C 
- `nlohmann_json` - nlohmann JSON 3.9.1
- `rapidjson` - RapidJSON 1.1.0
- `boringssl` - BoringSSL (Google's OpenSSL fork)
- `openssl` - OpenSSL 1.1.1f
- `io_opencensus_cpp` - OpenCensus C++
- `io_opentelemetry_cpp` - OpenTelemetry C++ 1.19.0
- `com_github_opentelemetry_proto` - OpenTelemetry Proto 1.2.0
- `com_github_jupp0r_prometheus_cpp` - Prometheus C++
- `com_google_googletest` - Google Test 1.14.0
- `com_github_gflags_gflags` - Google Flags
- `cython` - Cython 3.0.12
- `com_github_nelhage_rules_boost` - Boost Bazel rules
- `jemalloc` - JEMalloc 5.3.0
- `io_opencensus_proto` - OpenCensus Proto
- `com_google_protobuf_rules_proto_grpc` - Proto rules for code generation
- `rules_proto_grpc` - Proto gRPC rules
- `com_github_johnynek_bazel_jar_jar` - JAR JAR rules

**From `WORKSPACE` (direct):**
- `platforms` - Bazel platforms 0.0.9
- `rules_python` - Python Bazel rules 0.31.0
- `crane_linux_x86_64` - Container build tool
- `com_github_storypku_bazel_iwyu` - Include What You Use
- `bazel_common` - Google Bazel common utilities
- `bazel_skylib` - Bazel Skylib 1.6.1
- `hedron_compile_commands` - Compile commands extractor
- `rules_foreign_cc` - Foreign CC rules 0.9.0
- `rules_foreign_cc_thirdparty` - Foreign CC third-party
- `rules_jvm_external` - JVM external rules 2.10
- `rules_perl` - Perl rules

**Python Toolchain:**
- `python3_9` - Hermetic Python 3.9 interpreter
- `py_deps_buildkite` - Buildkite Python dependencies

### 2. **PYTHON DEPENDENCIES** (managed by pip/setup.py, NOT Bazel)

**From `python/setup.py` install_requires:**
```python
install_requires = [
    "click >= 7.0",
    "filelock", 
    "jsonschema",
    "msgpack >= 1.0.0, < 2.0.0",
    "packaging",
    "protobuf >= 3.15.3, != 3.19.5", 
    "pyyaml",
    "requests",
]
```

**From `python/requirements.txt` (development dependencies):**
- numpy, pandas, scipy, scikit-image
- fastapi, starlette, uvicorn, aiohttp
- opentelemetry-*, opencensus
- gymnasium, tensorboardx, rich, colorful
- py-spy, memray, pyopenssl
- ~40+ additional packages

### 3. **JAVA DEPENDENCIES** (managed by Maven via rules_jvm_external, NOT direct Bazel)

**From `java/dependencies.bzl` maven_install:**
```python
artifacts = [
    "com.fasterxml.jackson.core:jackson-databind:2.16.1",
    "com.google.guava:guava:32.0.1-jre", 
    "com.google.protobuf:protobuf-java:3.23.4",
    # ... ~25 Maven artifacts
]
```

## Key Insight: Dependency Management Strategy

Ray uses a **hybrid dependency management approach**:

1. **Bazel External Dependencies**: C++ libraries, build tools, system dependencies
   - Downloaded as source archives
   - Compiled from source during build
   - Version-pinned with SHA256 hashes
   - Custom BUILD files provided where needed

2. **Python Dependencies**: Standard PyPI packages  
   - Managed by pip/setuptools
   - Listed in setup.py and requirements.txt
   - Installed separately from Python package managers

3. **Java Dependencies**: Standard Maven artifacts
   - Managed by Bazel's `rules_jvm_external` 
   - Downloads from Maven Central
   - Integrated into Bazel build but not "external repos"

## What Should Go in fossa-deps for Bazel?

**Only the actual Bazel external dependencies** (~35 dependencies):
- C++ libraries downloaded as source archives
- Build system tools and rules
- System-level dependencies compiled from source

**Should NOT include**:
- Python PyPI packages (managed by pip)
- Java Maven artifacts (managed by Maven, even if via Bazel)

The Python and Java dependencies would be detected by FOSSA's native scanners for those ecosystems, not the Bazel integration.

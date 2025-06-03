# Ray Project - Comprehensive Dependency Analysis

## Overview
This document provides a comprehensive analysis of all dependencies used in the Ray project, extracted from Bazel build configurations and other dependency management files.

## Bazel External Dependencies (from WORKSPACE and ray_deps_setup.bzl)

### Core Build Tools
- **Bazel Skylib** (v1.6.1)
  - Type: Build tool library
  - URL: github.com/bazelbuild/bazel-skylib
  - SHA256: 9f38886a40548c6e96c106b752f242130ee11aaa068a56ba7e56f4511f33e4f2

- **Hedron Compile Commands** 
  - Type: Build tool (compile commands extractor)
  - URL: github.com/hedronvision/bazel-compile-commands-extractor
  - Commit: 2e8b7654fa10c44b9937453fa4974ed2229d5366

- **Rules Foreign CC** (v0.9.0)
  - Type: Bazel rules for foreign CC libraries
  - URL: github.com/bazelbuild/rules_foreign_cc
  - SHA256: 2a4d07cd64b0719b39a7c12218a3e507672b82a97b98c6a89d38565894cf7c51

### Language Support
- **Rules Python** (v0.31.0)
  - Type: Python Bazel rules
  - URL: github.com/bazelbuild/rules_python
  - SHA256: c68bdc4fbec25de5b5493b8819cfc877c4ea299c0dcb15c244c5a00208cde311

- **Python 3.9 Toolchain**
  - Type: Python interpreter
  - Registered via rules_python

- **Cython** (v3.0.12)
  - Type: Python to C compiler
  - URL: github.com/cython/cython
  - SHA256: a156fff948c2013f2c8c398612c018e2b52314fdf0228af8fbdb5585e13699c2

### Core Libraries
- **Google Protocol Buffers** (grpc pinned version)
  - Type: Serialization library
  - URL: github.com/protocolbuffers/protobuf
  - Commit: 2c5fa078d8e86e5f4bd34e6f4c9ea9e8d7d4d44a
  - SHA256: 76a33e2136f23971ce46c72fd697cd94dc9f73d56ab23b753c3e16854c90ddfd

- **Google Protocol Buffers** (v3.19.4) - For proto generation
  - Type: Serialization library (lower version for compatibility)
  - URL: github.com/protocolbuffers/protobuf
  - SHA256: 3bd7828aa5af4b13b99c191e8b1e884ebfa9ad371b0ce264605d347f135d2568

- **gRPC** (v1.57.1)
  - Type: RPC framework
  - URL: github.com/grpc/grpc
  - SHA256: 0762f809b9de845e6a7c809cabccad6aa4143479fd43b396611fe5a086c0aeeb

- **Abseil** (20230802.1)
  - Type: C++ standard library extensions
  - URL: github.com/abseil/abseil-cpp
  - SHA256: 987ce98f02eefbaf930d6e38ab16aa05737234d7afbab2d5c4ea7adbe50c28ed

### Data Processing & Serialization
- **FlatBuffers** (v25.2.10)
  - Type: Memory efficient serialization
  - URL: github.com/google/flatbuffers
  - SHA256: b9c2df49707c57a48fc0923d52b8c73beb72d675f9d44b2211e4569be40a7421

- **MessagePack** 
  - Type: Efficient object serialization
  - URL: github.com/msgpack/msgpack-c
  - Commit: 8085ab8721090a447cf98bb802d1406ad7afe420
  - SHA256: 83c37c9ad926bbee68d564d9f53c6cbb057c1f755c264043ddd87d89e36d15bb

- **nlohmann/json** (v3.9.1)
  - Type: JSON library for C++
  - URL: github.com/nlohmann/json
  - SHA256: 4cf0df69731494668bdd6460ed8cb269b68de9c19ad8c27abc24cd72605b2d5b

- **RapidJSON** (v1.1.0)
  - Type: Fast JSON parser/generator
  - URL: github.com/Tencent/rapidjson
  - SHA256: 8e00c38829d6785a2dfb951bb87c6974fa07dfe488aa5b25deec4b8bc0f6a3ab

### Database & Storage
- **Redis** (v7.2.3)
  - Type: In-memory data structure store
  - URL: github.com/redis/redis
  - SHA256: afd656dbc18a886f9a1cc08a550bf5eb89de0d431e713eba3ae243391fb008a6

- **Hiredis**
  - Type: Redis C client
  - URL: github.com/redis/hiredis
  - Commit: 60e5075d4ac77424809f855ba3e398df7aacefe8
  - SHA256: b6d6f799b7714d85316f9ebfb76a35a78744f42ea3b6774289d882d13a2f0383

- **JEMalloc** (v5.3.0)
  - Type: Memory allocator
  - URL: github.com/jemalloc/jemalloc
  - SHA256: 2db82d1e7119df3e71b7640219b6dfe84789bc0537983c3b7ac4f7189aecfeaa

### Networking & Security
- **BoringSSL**
  - Type: SSL/TLS library (Google's fork of OpenSSL)
  - URL: github.com/google/boringssl
  - Commit: 342e805bc1f5dfdd650e3f031686d6c939b095d9
  - SHA256: 0675a4f86ce5e959703425d6f9063eaadf6b61b7f3399e77a154c0e85bad46b1

- **OpenSSL** (v1.1.1f)
  - Type: SSL/TLS library
  - URL: openssl.org
  - SHA256: 186c6bfe6ecfba7a5b48c47f8a1673d0f3b0e5ba2e25602dd23b629975da3f35

### Observability & Monitoring
- **spdlog** (v1.12.0)
  - Type: Fast C++ logging library
  - URL: github.com/gabime/spdlog
  - SHA256: 6174bf8885287422a6c6a0312eb8a30e8d22bcfcee7c48a6d02d1835d7769232

- **OpenCensus C++**
  - Type: Application performance monitoring
  - URL: github.com/census-instrumentation/opencensus-cpp
  - Commit: 5e5f2632c84e2230fb7ccb8e336f603d2ec6aa1b
  - SHA256: 1b88d6663f05c6a56c1604eb2afad22831d5f28a76f6fab8f37187f1e4ace425

- **OpenTelemetry C++** (v1.19.0)
  - Type: Observability framework
  - URL: github.com/open-telemetry/opentelemetry-cpp
  - SHA256: 8ef0a63f4959d5dfc3d8190d62229ef018ce41eef36e1f3198312d47ab2de05a

- **OpenTelemetry Proto** (v1.2.0)
  - Type: OpenTelemetry protocol definitions
  - URL: github.com/open-telemetry/opentelemetry-proto

- **Prometheus C++**
  - Type: Monitoring and alerting
  - URL: github.com/jupp0r/prometheus-cpp
  - Commit: 60eaa4ea47b16751a8e8740b05fe70914c68a480
  - SHA256: ec825b802487ac18b0d98e2e8b7961487b12562f8f82e424521d0a891d9e1373

### Development & Testing
- **Google Test** (v1.14.0)
  - Type: C++ testing framework
  - URL: github.com/google/googletest
  - SHA256: 8ad598c73ad796e0d8280b082cebd82a630d73e73cd3c70057938a6501bba5d7

- **Google Flags**
  - Type: Commandline flags library
  - URL: github.com/gflags/gflags
  - Commit: e171aa2d15ed9eb17054558e0b3a6a413bb01067
  - SHA256: b20f58e7f210ceb0e768eb1476073d0748af9b19dfbbf53f4fd16e3fb49c5ac8

### C++ Libraries
- **Boost**
  - Type: C++ libraries
  - URL: github.com/nelhage/rules_boost
  - Commit: 57c99395e15720e287471d79178d36a85b64d6f6
  - SHA256: 490d11425393eed068966a4990ead1ff07c658f823fd982fddac67006ccc44ab

### Java Dependencies (from java/dependencies.bzl)
- **Jackson Databind** (v2.16.1) - JSON processing
- **JSON Schema Validator** (v2.2.14) - JSON validation
- **Gson** (v2.9.1) - JSON serialization
- **Guava** (v32.0.1-jre) - Google core libraries
- **Protocol Buffers Java** (v3.23.4) - Serialization
- **Checkstyle** (v8.15) - Code style checker
- **JAXB** (v2.3.0) - XML binding
- **Typesafe Config** (v1.3.2) - Configuration library
- **Commons IO** (v2.14.0) - IO utilities
- **FST** (v2.57) - Fast serialization
- **Commons Lang3** (v3.13.0) - Utility library
- **MessagePack Java** (v0.8.20) - Object serialization
- **ASM** (v6.0) - Bytecode manipulation
- **Log4j** (v2.17.1) - Logging framework
- **SLF4J** (v1.7.25) - Logging facade
- **Disruptor** (v3.3.4) - High performance messaging
- **JNA** (v5.8.0) - Java Native Access
- **Apache HTTP Client** (v5.0.3) - HTTP client
- **TestNG** (v7.5.1) - Testing framework

### Python Dependencies (from python/requirements.txt)
#### Core Runtime Dependencies
- click>=7.0 - Command line interface
- filelock - File locking
- jsonschema - JSON schema validation
- msgpack<2.0.0,>=1.0.0 - MessagePack serialization
- packaging - Package metadata utilities
- protobuf!=3.19.5,>=3.15.3 - Protocol Buffers
- pyyaml - YAML parser
- requests - HTTP library
- watchfiles - File watching
- grpcio==1.54.2 (macOS) / >=1.54.2 (others) - gRPC
- numpy>=1.20 - Numerical computing
- pyarrow>=9.0.0 - Apache Arrow

#### Extended Dependencies (ray[all])
- smart_open - File handling
- lz4 - Compression
- aiorwlock - Async read-write locks
- opentelemetry-* - Observability
- scipy - Scientific computing
- colorful - Terminal colors
- rich - Rich text rendering
- fastapi - Web framework
- gymnasium==1.0.0 - RL environments
- virtualenv - Virtual environments
- opencensus - Application monitoring
- aiohttp_cors - CORS support
- dm_tree - Tree data structures
- uvicorn - ASGI server
- scikit-image>=0.21.0 - Image processing
- prometheus_client>=0.7.1 - Monitoring
- pandas - Data analysis
- tensorboardX - TensorBoard logging
- aiohttp>=3.7 - Async HTTP
- starlette - Web framework
- typer - CLI building
- fsspec - File system interfaces
- pydantic - Data validation
- py-spy>=0.2.0 - Python profiler
- memray - Memory profiler
- pyOpenSSL - SSL/TLS

## Build System Architecture

### Bazel Configuration
- **Primary WORKSPACE**: /WORKSPACE
- **Main dependency setup**: /bazel/ray_deps_setup.bzl
- **Build orchestration**: /bazel/ray_deps_build_all.bzl
- **Java dependencies**: /java/dependencies.bzl

### Dependency Loading Strategy
1. Platform and build tools loaded first
2. Language toolchains (Python, Java)
3. Core libraries (protobuf, gRPC, abseil)
4. Specialized libraries (Redis, observability)
5. Development tools (testing, formatting)

### Patch Management
The project maintains custom patches for several dependencies:
- redis-quiet.patch
- hiredis-windows-msvc.patch
- spdlog-rotation-file-format.patch
- grpc-cython-copts.patch
- opencensus-cpp-harvest-interval.patch
- prometheus-windows-*.patch

## Build Targets
- **Core**: //:ray_pkg
- **C++ API**: //cpp:ray_cpp_pkg
- **Java**: Various Java targets
- **Python**: Python package building

This dependency graph represents one of the most complex open-source build systems, integrating C++, Python, Java, and various system dependencies into a unified distributed computing framework.

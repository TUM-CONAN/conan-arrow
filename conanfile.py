# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class ArrowConan(ConanFile):
    name = "arrow"
    version = "5.0.0"
    description = "Apache Arrow is a cross-language development platform for in-memory data."
    topics = ("conan", "arrow", "memory")
    url = "https://github.com/TUM-CONAN/conan-arrow"
    homepage = "https://github.com/apache/arrow"
    author = "Ulrich Eck <ulrich.eck@tum.de>"
    license = "Apache-2.0"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False], 
        "fPIC": [True, False],
        "with_cuda": [True, False],
        "with_plasma": [True, False],
        }

    default_options = {
        "shared": True, 
        "fPIC": True,
        "with_cuda": False,
        "with_plasma": False,
        }

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    requires = (
        "flatbuffers/1.11.0@camposs/stable",
        )

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC


    def requirements(self):
        if self.options.with_cuda:
            self.requires("cuda_dev_config/[>=2.0]@camposs/stable")

    def source(self):
        source_url = "https://github.com/apache/arrow"
        tools.get("{0}/archive/apache-arrow-{1}.tar.gz".format(source_url, self.version))
        extracted_dir = "arrow-apache-arrow-" + self.version

        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        if self.options.with_plasma:
            cmake.definitions["ARROW_PLASMA"] = "ON"
        if self.options.with_cuda:
            cmake.definitions["ARROW_CUDA"] = "ON"

        cmake.definitions["BOOST_SOURCE"] = "BUNDLED"
        cmake.definitions["ARROW_BUILD_SHARED"] = "ON" if self.options.shared else "OFF"
        cmake.definitions["ARROW_BUILD_STATIC"] = "OFF" if self.options.shared else "ON"
        cmake.definitions["FLATBUFFERS_INCLUDE_DIR"] = ":".join(self.deps_cpp_info["flatbuffers"].include_paths)
        cmake.definitions["FLATBUFFERS_LIB"] = str(self.deps_cpp_info["flatbuffers"].libs[0])

        # cmake.definitions["ARROW_BOOST_USE_SHARED"] = False
        # cmake.definitions["ARROW_BUILD_BENCHMARKS"] = False
        # cmake.definitions["ARROW_BUILD_TESTS"] = False
        # cmake.definitions["ARROW_BUILD_UTILITIES"] = False
        # cmake.definitions["ARROW_USE_GLOG"] = False
        # cmake.definitions["ARROW_WITH_BACKTRACE"] = False
        # cmake.definitions["ARROW_WITH_BROTLI"] = False
        # cmake.definitions["ARROW_WITH_LZ4"] = False
        # cmake.definitions["ARROW_WITH_SNAPPY"] = False
        # cmake.definitions["ARROW_WITH_ZLIB"] = False
        # cmake.definitions["ARROW_WITH_ZLIB"] = False
        # cmake.definitions["ARROW_WITH_ZSTD"] = False
        # cmake.definitions["ARROW_JEMALLOC"] = False

        cmake.configure(source_folder=os.path.join(self._source_subfolder, 'cpp'))
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

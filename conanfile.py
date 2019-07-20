# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class ArrowConan(ConanFile):
    name = "arrow"
    version = "0.13.0"
    description = "Apache Arrow is a cross-language development platform for in-memory data."
    topics = ("conan", "arrow", "memory")
    url = "https://github.com/bincrafters/conan-arrow"
    homepage = "https://github.com/apache/arrow"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "Apache-2.0"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        source_url = "https://github.com/apache/arrow"
        tools.get("{0}/archive/apache-arrow-{1}.tar.gz".format(source_url, self.version), sha256="380fcc51f0bf98e13148300c87833e734cbcd7b74dddc4bce93829e7f7e4208b")
        extracted_dir = "arrow-apache-arrow-" + self.version

        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["ARROW_BOOST_USE_SHARED"] = False
        cmake.definitions["ARROW_BUILD_BENCHMARKS"] = False
        cmake.definitions["ARROW_BUILD_SHARED"] = False
        cmake.definitions["ARROW_BUILD_TESTS"] = False
        cmake.definitions["ARROW_BUILD_UTILITIES"] = False
        cmake.definitions["ARROW_USE_GLOG"] = False
        cmake.definitions["ARROW_WITH_BACKTRACE"] = False
        cmake.definitions["ARROW_WITH_BROTLI"] = False
        cmake.definitions["ARROW_WITH_LZ4"] = False
        cmake.definitions["ARROW_WITH_SNAPPY"] = False
        cmake.definitions["ARROW_WITH_ZLIB"] = False
        cmake.definitions["ARROW_WITH_ZLIB"] = False
        cmake.definitions["ARROW_WITH_ZSTD"] = False
        cmake.definitions["ARROW_JEMALLOC"] = False

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

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps
from conan.tools.env import VirtualBuildEnv

required_conan_version = ">=2.0"

class RegxmlLibConan(ConanFile):

    # ---Package reference---
    name = "regxmllib"
    version = "1.1.5"
    # ---Metadata---
    description = "regxmllib is a collection of tools and libraries for the creation of RegXML (SMPTE ST 2001-1) representations of MXF header metadata (SMPTE ST 377-1)"
    license = "BSD"
    author = "Björn Stresing"
    topics = ["MXF"]
    homepage = "https://github.com/IMFTool/regxmllib"
    url = "https://github.com/IMFTool/regxmllib"
    # ---Requirements---
    requires = []
    tool_requires = ["cmake/[>=3.21.1]", "ninja/[>=1.11.1]"]
    # ---Sources---
    exports = ["LICENSE.txt"]
    exports_sources = ["src/*", "CMakeLists.txt"]
    # ---Binary model---
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": True,
                       "fPIC": True}

    def validate(self):
        valid_os = ["Windows", "Linux", "Macos"]
        if str(self.settings.os) not in valid_os:
            raise ConanInvalidConfiguration(f"{self.name} {self.version} is only supported for the following operating systems: {valid_os}")
        valid_arch = ["x86_64", "armv8"]
        if str(self.settings.arch) not in valid_arch:
            raise ConanInvalidConfiguration(f"{self.name} {self.version} is only supported for the following architectures on {self.settings.os}: {valid_arch}")
        if str(self.settings.os) == 'Windows' and self.options.shared:
            raise ConanInvalidConfiguration(f"{self.name} {self.version} does not support building shared library on Windows")

    def requirements(self):
        self.requires("xerces-c/[>=3.2.5]", options={"network": False, "shared": False})

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.rm_safe("fPIC")

    def configure(self):
        if not self.options.shared:
            self.options.rm_safe("fPIC")

    def generate(self):
        VirtualBuildEnv(self).generate()
        CMakeDeps(self).generate()
        tc = CMakeToolchain(self, generator="Ninja")
        tc.variables["BUILD_TESTING"] = False
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["regxmllibc"]
        self.cpp_info.bindirs = []

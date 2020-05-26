#!/usr/bin/env python

# Script to test how much bloating a large project will suffer when using
# different formatting methods.
# Based on bloat_test.sh from https://github.com/c42f/tinyformat.

from __future__ import print_function
import os, re, sys
from contextlib import nested
from glob import glob
from subprocess import check_call, Popen, PIPE
from timeit import timeit

template = r'''
#ifdef USE_BOOST

#include <boost/format.hpp>
#include <iostream>

void doFormat_a() {
  std::cout << boost::format("a %s\n") % "somefile.cpp";
  std::cout << boost::format("a %s:%d\n") % "somefile.cpp" % 42;
  std::cout << boost::format("a %s:%d:%s\n") % "somefile.cpp" % 42 % "asdf";
  std::cout <<
    boost::format("a %s:%d:%d:%s\n") % "somefile.cpp" % 42 % 1 % "asdf";
  std::cout <<
    boost::format("a %s:%d:%d:%d:%s\n") % "somefile.cpp" % 42 % 1 % 2 % "asdf";
  std::cout <<
    boost::format("a %s:%d:%d:%d:%s %s:%d:%d:%d:%s\n") % "somefile.cpp" % 42 % 1 % 2 % "asdf" % "somefile.cpp" % 42 % 1 % 2 % "asdf";
}

void doFormat_b() {
  std::cout << boost::format("b %s\n") % "somefile.cpp";
  std::cout << boost::format("b %s:%d\n") % "somefile.cpp" % 42;
  std::cout << boost::format("b %s:%d:%s\n") % "somefile.cpp" % 42 % "asdf";
  std::cout <<
    boost::format("b %s:%d:%d:%s\n") % "somefile.cpp" % 42 % 1 % "asdf";
  std::cout <<
    boost::format("b %s:%d:%d:%d:%s\n") % "somefile.cpp" % 42 % 1 % 2 % "asdf";
}

void doFormat_c() {
  std::cout << boost::format("c %s\n") % "somefile.cpp";
  std::cout << boost::format("c %s:%d\n") % "somefile.cpp" % 42;
  std::cout << boost::format("c %s:%d:%s\n") % "somefile.cpp" % 42 % "asdf";
  std::cout <<
    boost::format("c %s:%d:%d:%s\n") % "somefile.cpp" % 42 % 1 % "asdf";
  std::cout <<
    boost::format("c %s:%d:%d:%d:%s\n") % "somefile.cpp" % 42 % 1 % 2 % "asdf";
}

void doFormat_d() {
  std::cout << boost::format("d %s\n") % "somefile.cpp";
  std::cout << boost::format("d %s:%d\n") % "somefile.cpp" % 42;
  std::cout << boost::format("d %s:%d:%s\n") % "somefile.cpp" % 42 % "asdf";
  std::cout <<
    boost::format("d %s:%d:%d:%s\n") % "somefile.cpp" % 42 % 1 % "asdf";
  std::cout <<
    boost::format("d %s:%d:%d:%d:%s\n") % "somefile.cpp" % 42 % 1 % 2 % "asdf";
}

#elif USE_FOLLY

#include <folly/Format.h>
#include <iostream>

void doFormat_a() {
  std::cout << folly::format("a {}\n", "somefile.cpp");
  std::cout << folly::format("a {}:{}\n", "somefile.cpp", 42);
  std::cout << folly::format("a {}:{}:{}\n", "somefile.cpp", 42, "asdf");
  std::cout <<
    folly::format("a {}:{}:{}:{}\n", "somefile.cpp", 42, 1, "asdf");
  std::cout <<
    folly::format("a {}:{}:{}:{}:{}\n", "somefile.cpp", 42, 1, 2, "asdf");
      std::cout <<
    folly::format("a {}:{}:{}:{}:{} {}:{}:{}:{}:{}\n", "somefile.cpp", 42, 1, 2, "asdf", "somefile.cpp", 42, 1, 2, "asdf");
}

void doFormat_b() {
  std::cout << folly::format("b {}\n", "somefile.cpp");
  std::cout << folly::format("b {}:{}\n", "somefile.cpp", 42);
  std::cout << folly::format("b {}:{}:{}\n", "somefile.cpp", 42, "asdf");
  std::cout <<
    folly::format("b {}:{}:{}:{}\n", "somefile.cpp", 42, 1, "asdf");
  std::cout <<
    folly::format("b {}:{}:{}:{}:{}\n", "somefile.cpp", 42, 1, 2, "asdf");
}

void doFormat_c() {
  std::cout << folly::format("c {}\n", "somefile.cpp");
  std::cout << folly::format("c {}:{}\n", "somefile.cpp", 42);
  std::cout << folly::format("c {}:{}:{}\n", "somefile.cpp", 42, "asdf");
  std::cout <<
    folly::format("c {}:{}:{}:{}\n", "somefile.cpp", 42, 1, "asdf");
  std::cout <<
    folly::format("c {}:{}:{}:{}:{}\n", "somefile.cpp", 42, 1, 2, "asdf");
}

void doFormat_d() {
  std::cout << folly::format("d {}\n", "somefile.cpp");
  std::cout << folly::format("d {}:{}\n", "somefile.cpp", 42);
  std::cout << folly::format("d {}:{}:{}\n", "somefile.cpp", 42, "asdf");
  std::cout <<
    folly::format("d {}:{}:{}:{}\n", "somefile.cpp", 42, 1, "asdf");
  std::cout <<
    folly::format("d {}:{}:{}:{}:{}\n", "somefile.cpp", 42, 1, 2, "asdf");
}


#elif defined(USE_FMT)

#include "fmt/core.h"

void doFormat_a() {
  fmt::print("a {}\n", "somefile.cpp");
  fmt::print("a {}:{}\n", "somefile.cpp", 42);
  fmt::print("a {}:{}:{}\n", "somefile.cpp", 42, "asdf");
  fmt::print("a {}:{}:{}:{}\n", "somefile.cpp", 42, 1, "asdf");
  fmt::print("a {}:{}:{}:{}:{}\n", "somefile.cpp", 42, 1, 2, "asdf");
  fmt::print("a {}:{}:{}:{}:{} {}:{}:{}:{}:{}\n", "somefile.cpp", 42, 1, 2, "asdf", "somefile.cpp", 42, 1, 2, "asdf");
}


void doFormat_b() {
  fmt::print("b {}\n", "somefile.cpp");
  fmt::print("b {}:{}\n", "somefile.cpp", 42);
  fmt::print("b {}:{}:{}\n", "somefile.cpp", 42, "asdf");
  fmt::print("b {}:{}:{}:{}\n", "somefile.cpp", 42, 1, "asdf");
  fmt::print("b {}:{}:{}:{}:{}\n", "somefile.cpp", 42, 1, 2, "asdf");
}


void doFormat_c() {
  fmt::print("c {}\n", "somefile.cpp");
  fmt::print("c {}:{}\n", "somefile.cpp", 42);
  fmt::print("c {}:{}:{}\n", "somefile.cpp", 42, "asdf");
  fmt::print("c {}:{}:{}:{}\n", "somefile.cpp", 42, 1, "asdf");
  fmt::print("c {}:{}:{}:{}:{}\n", "somefile.cpp", 42, 1, 2, "asdf");
}


void doFormat_d() {
  fmt::print("d {}\n", "somefile.cpp");
  fmt::print("d {}:{}\n", "somefile.cpp", 42);
  fmt::print("d {}:{}:{}\n", "somefile.cpp", 42, "asdf");
  fmt::print("d {}:{}:{}:{}\n", "somefile.cpp", 42, 1, "asdf");
  fmt::print("d {}:{}:{}:{}:{}\n", "somefile.cpp", 42, 1, 2, "asdf");
}

#elif defined(USE_COMPILED_FMT)
#include "fmt/compile.h"

void doFormat_a() {
  constexpr auto compiled_format1 = fmt::compile<int>(
    FMT_STRING("a {}\n"));
  fmt::print(compiled_format1, "somefile.cpp");

  constexpr auto compiled_format2 = fmt::compile<const char *, int>(
    FMT_STRING("a {}:{}\n"));
  fmt::print(compiled_format2, "somefile.cpp", 42);

  constexpr auto compiled_format3 = fmt::compile<const char *, int, const char *>(
    FMT_STRING("a {}:{}:{}\n"));
  fmt::print(compiled_format3, "somefile.cpp", 42, "asdf");

  constexpr auto compiled_format4 = fmt::compile<const char *, int, int, const char *>(
    FMT_STRING("a {}:{}:{}:{}\n"));
  fmt::print(compiled_format4, "somefile.cpp", 42, 1, "asdf");

  constexpr auto compiled_format5 = fmt::compile<const char *, int, int, itn const char *>(
    FMT_STRING("a {}:{}:{}:{}:{}\n"));
  fmt::print(compiled_format5, "somefile.cpp", 42, 1, 2, "asdf");

  constexpr auto compiled_format6 = fmt::compile<const char *, int, int, itn const char *, const char *, int, int, itn const char *>(
    FMT_STRING("a {}:{}:{}:{}:{} {}:{}:{}:{}:{}\n"));
  fmt::print(compiled_format5, "somefile.cpp", 42, 1, 2, "asdf", "somefile.cpp", 42, 1, 2, "asdf")
}

void doFormat_b() {
  constexpr auto compiled_format1 = fmt::compile<int>(
    FMT_STRING("b {}\n"));
  fmt::print(compiled_format1, "somefile.cpp");

  constexpr auto compiled_format2 = fmt::compile<const char *, int>(
    FMT_STRING("b {}:{}\n"));
  fmt::print(compiled_format2, "somefile.cpp", 42);

  constexpr auto compiled_format3 = fmt::compile<const char *, int, const char *>(
    FMT_STRING("b {}:{}:{}\n"));
  fmt::print(compiled_format3, "somefile.cpp", 42, "asdf");

  constexpr auto compiled_format4 = fmt::compile<const char *, int, int, const char *>(
    FMT_STRING("b {}:{}:{}:{}\n"));
  fmt::print(compiled_format4, "somefile.cpp", 42, 1, "asdf");

  constexpr auto compiled_format5 = fmt::compile<const char *, int, int, itn const char *>(
    FMT_STRING("b {}:{}:{}:{}:{}\n"));
  fmt::print(compiled_format5, "somefile.cpp", 42, 1, 2, "asdf");
}


void doFormat_c() {
  constexpr auto compiled_format1 = fmt::compile<int>(
    FMT_STRING("c {}\n"));
  fmt::print(compiled_format1, "somefile.cpp");

  constexpr auto compiled_format2 = fmt::compile<const char *, int>(
    FMT_STRING("c {}:{}\n"));
  fmt::print(compiled_format2, "somefile.cpp", 42);

  constexpr auto compiled_format3 = fmt::compile<const char *, int, const char *>(
    FMT_STRING("c {}:{}:{}\n"));
  fmt::print(compiled_format3, "somefile.cpp", 42, "asdf");

  constexpr auto compiled_format4 = fmt::compile<const char *, int, int, const char *>(
    FMT_STRING("c {}:{}:{}:{}\n"));
  fmt::print(compiled_format4, "somefile.cpp", 42, 1, "asdf");

  constexpr auto compiled_format5 = fmt::compile<const char *, int, int, itn const char *>(
    FMT_STRING("c {}:{}:{}:{}:{}\n"));
  fmt::print(compiled_format5, "somefile.cpp", 42, 1, 2, "asdf");
}


void doFormat_d() {
  constexpr auto compiled_format1 = fmt::compile<int>(
    FMT_STRING("d {}\n"));
  fmt::print(compiled_format1, "somefile.cpp");

  constexpr auto compiled_format2 = fmt::compile<const char *, int>(
    FMT_STRING("d {}:{}\n"));
  fmt::print(compiled_format2, "somefile.cpp", 42);

  constexpr auto compiled_format3 = fmt::compile<const char *, int, const char *>(
    FMT_STRING("d {}:{}:{}\n"));
  fmt::print(compiled_format3, "somefile.cpp", 42, "asdf");

  constexpr auto compiled_format4 = fmt::compile<const char *, int, int, const char *>(
    FMT_STRING("d {}:{}:{}:{}\n"));
  fmt::print(compiled_format4, "somefile.cpp", 42, 1, "asdf");

  constexpr auto compiled_format5 = fmt::compile<const char *, int, int, itn const char *>(
    FMT_STRING("d {}:{}:{}:{}:{}\n"));
  fmt::print(compiled_format5, "somefile.cpp", 42, 1, 2, "asdf");
}


#elif defined(USE_IOSTREAMS)

#include <iostream>

void doFormat_a() {
  std::cout << "a somefile.cpp" << "\n";
  std::cout << "a somefile.cpp:" << 42 << "\n";
  std::cout << "a somefile.cpp:" << 42 << ":asdf" << "\n";
  std::cout << "a somefile.cpp:" << 42 << ':' << 1 << ":asdf" << "\n";
  std::cout << "a somefile.cpp:" << 42 << ':' << 1 << ':' << 2 << ":asdf" << "\n";
  std::cout << "a somefile.cpp:" << 42 << ':' << 1 << ':' << 2 << ":asdf" << " somefile.cpp:" << 42 << ':' << 1 << ':' << 2 << ":asdf" << "\n";
}

void doFormat_b() {
  std::cout << "b somefile.cpp" << "\n";
  std::cout << "b somefile.cpp:" << 42 << "\n";
  std::cout << "b somefile.cpp:" << 42 << ":asdf" << "\n";
  std::cout << "b somefile.cpp:" << 42 << ':' << 1 << ":asdf" << "\n";
  std::cout << "b somefile.cpp:" << 42 << ':' << 1 << ':' << 2 << ":asdf" << "\n";
}

void doFormat_c() {
  std::cout << "c somefile.cpp" << "\n";
  std::cout << "c somefile.cpp:" << 42 << "\n";
  std::cout << "c somefile.cpp:" << 42 << ":asdf" << "\n";
  std::cout << "c somefile.cpp:" << 42 << ':' << 1 << ":asdf" << "\n";
  std::cout << "c somefile.cpp:" << 42 << ':' << 1 << ':' << 2 << ":asdf" << "\n";
}

void doFormat_d() {
  std::cout << "d somefile.cpp" << "\n";
  std::cout << "d somefile.cpp:" << 42 << "\n";
  std::cout << "d somefile.cpp:" << 42 << ":asdf" << "\n";
  std::cout << "d somefile.cpp:" << 42 << ':' << 1 << ":asdf" << "\n";
  std::cout << "d somefile.cpp:" << 42 << ':' << 1 << ':' << 2 << ":asdf" << "\n";
}

#elif defined(USE_STB_SPRINTF)

#ifdef FIRST_FILE
#  define STB_SPRINTF_IMPLEMENTATION
#endif
// since this test doesn't use floating point numbers shave ~20kb
#define STB_SPRINTF_NOFLOAT

#include "stb_sprintf.h"
#include "stdio.h"

void doFormat_a() {
  char buf[200];
  stbsp_sprintf(buf, "a %s\n", "somefile.cpp");
  fputs(buf, stdout);
  stbsp_sprintf(buf, "a %s:%d\n", "somefile.cpp", 42);
  fputs(buf, stdout);
  stbsp_sprintf(buf, "a %s:%d:%s\n", "somefile.cpp", 42, "asdf");
  fputs(buf, stdout);
  stbsp_sprintf(buf, "a %s:%d:%d:%s\n", "somefile.cpp", 42, 1, "asdf");
  fputs(buf, stdout);
  stbsp_sprintf(buf, "a %s:%d:%d:%d:%s\n", "somefile.cpp", 42, 1, 2, "asdf");
  fputs(buf, stdout);
  stbsp_sprintf(buf, "a %s:%d:%d:%d:%s %s:%d:%d:%d:%s\n", "somefile.cpp", 42, 1, 2, "asdf", "somefile.cpp", 42, 1, 2, "asdf");
  fputs(buf, stdout);
}

void doFormat_b() {
  char buf[100];
  stbsp_sprintf(buf, "b %s\n", "somefile.cpp");
  fputs(buf, stdout);
  stbsp_sprintf(buf, "b %s:%d\n", "somefile.cpp", 42);
  fputs(buf, stdout);
  stbsp_sprintf(buf, "b %s:%d:%s\n", "somefile.cpp", 42, "asdf");
  fputs(buf, stdout);
  stbsp_sprintf(buf, "b %s:%d:%d:%s\n", "somefile.cpp", 42, 1, "asdf");
  fputs(buf, stdout);
  stbsp_sprintf(buf, "b %s:%d:%d:%d:%s\n", "somefile.cpp", 42, 1, 2, "asdf");
  fputs(buf, stdout);
}

void doFormat_c() {
  char buf[100];
  stbsp_sprintf(buf, "c %s\n", "somefile.cpp");
  fputs(buf, stdout);
  stbsp_sprintf(buf, "c %s:%d\n", "somefile.cpp", 42);
  fputs(buf, stdout);
  stbsp_sprintf(buf, "c %s:%d:%s\n", "somefile.cpp", 42, "asdf");
  fputs(buf, stdout);
  stbsp_sprintf(buf, "c %s:%d:%d:%s\n", "somefile.cpp", 42, 1, "asdf");
  fputs(buf, stdout);
  stbsp_sprintf(buf, "c %s:%d:%d:%d:%s\n", "somefile.cpp", 42, 1, 2, "asdf");
  fputs(buf, stdout);
}

void doFormat_d() {
  char buf[100];
  stbsp_sprintf(buf, "d %s\n", "somefile.cpp");
  fputs(buf, stdout);
  stbsp_sprintf(buf, "d %s:%d\n", "somefile.cpp", 42);
  fputs(buf, stdout);
  stbsp_sprintf(buf, "d %s:%d:%s\n", "somefile.cpp", 42, "asdf");
  fputs(buf, stdout);
  stbsp_sprintf(buf, "d %s:%d:%d:%s\n", "somefile.cpp", 42, 1, "asdf");
  fputs(buf, stdout);
  stbsp_sprintf(buf, "d %s:%d:%d:%d:%s\n", "somefile.cpp", 42, 1, 2, "asdf");
  fputs(buf, stdout);
}
#elif defined(USE_PFORMAT)
#include <pformat/pformat.h>
#include "stdio.h"

void doFormat_a() {
  using namespace pformat;
  char buf[100];
  constexpr auto cf1 = "a {}\n"_log;
  cf1.format_to(buf, "somefile.cpp");
  fputs(buf, stdout);
  constexpr auto cf2 = "a {}:{}\n"_log;
  cf2.format_to(buf, "somefile.cpp", 42);
  fputs(buf, stdout);
  constexpr auto cf3 = "a {}:{}:{}\n"_log;
  cf3.format_to(buf, "somefile.cpp", 42, "asdf");
  fputs(buf, stdout);
  constexpr auto cf4 = "a {}:{}:{}:{}\n"_log;
  cf4.format_to(buf, "somefile.cpp", 42, 1, "asdf");
  fputs(buf, stdout);
  constexpr auto cf5 = "a {}:{}:{}:{}:{}\n"_log;
  cf5.format_to(buf, "somefile.cpp", 42, 1, 2, "asdf");
  fputs(buf, stdout);
  
  constexpr auto cf6 = "a {}:{}:{}:{}:{} {}:{}:{}:{}:{}\n"_log;
  cf6.format_to(buf, "somefile.cpp", 42, 1, 2, "asdf", "somefile.cpp", 42, 1, 2, "asdf");
  fputs(buf, stdout);
}

void doFormat_b() {
  using namespace pformat;
  char buf[100];
  constexpr auto cf1 = "b {}\n"_log;
  cf1.format_to(buf, "somefile.cpp");
  fputs(buf, stdout);
  constexpr auto cf2 = "b {}:{}\n"_log;
  cf2.format_to(buf, "somefile.cpp", 42);
  fputs(buf, stdout);
  constexpr auto cf3 = "b {}:{}:{}\n"_log;
  cf3.format_to(buf, "somefile.cpp", 42, "asdf");
  fputs(buf, stdout);
  constexpr auto cf4 = "b {}:{}:{}:{}\n"_log;
  cf4.format_to(buf, "somefile.cpp", 42, 1, "asdf");
  fputs(buf, stdout);
  constexpr auto cf5 = "b {}:{}:{}:{}:{}\n"_log;
  cf5.format_to(buf, "somefile.cpp", 42, 1, 2, "asdf");
  fputs(buf, stdout);
}

void doFormat_c() {
  using namespace pformat;
  char buf[100];
  constexpr auto cf1 = "c {}\n"_log;
  cf1.format_to(buf, "somefile.cpp");
  fputs(buf, stdout);
  constexpr auto cf2 = "c {}:{}\n"_log;
  cf2.format_to(buf, "somefile.cpp", 42);
  fputs(buf, stdout);
  constexpr auto cf3 = "c {}:{}:{}\n"_log;
  cf3.format_to(buf, "somefile.cpp", 42, "asdf");
  fputs(buf, stdout);
  constexpr auto cf4 = "c {}:{}:{}:{}\n"_log;
  cf4.format_to(buf, "somefile.cpp", 42, 1, "asdf");
  fputs(buf, stdout);
  constexpr auto cf5 = "c {}:{}:{}:{}:{}\n"_log;
  cf5.format_to(buf, "somefile.cpp", 42, 1, 2, "asdf");
  fputs(buf, stdout);
}

void doFormat_d() {
  using namespace pformat;
  char buf[100];
  constexpr auto cf1 = "d {}\n"_log;
  cf1.format_to(buf, "somefile.cpp");
  fputs(buf, stdout);
  constexpr auto cf2 = "d {}:{}\n"_log;
  cf2.format_to(buf, "somefile.cpp", 42);
  fputs(buf, stdout);
  constexpr auto cf3 = "d {}:{}:{}\n"_log;
  cf3.format_to(buf, "somefile.cpp", 42, "asdf");
  fputs(buf, stdout);
  constexpr auto cf4 = "d {}:{}:{}:{}\n"_log;
  cf4.format_to(buf, "somefile.cpp", 42, 1, "asdf");
  fputs(buf, stdout);
  constexpr auto cf5 = "d {}:{}:{}:{}:{}\n"_log;
  cf5.format_to(buf, "somefile.cpp", 42, 1, 2, "asdf");
  fputs(buf, stdout);
}
#else
# ifdef USE_TINYFORMAT
#   include "tinyformat.h"
#   define PRINTF tfm::printf
# else
#  ifdef USE_STRING
#   include <string>
#  endif
#   include <stdio.h>
#   define PRINTF ::printf
# endif

void doFormat_a() {
  PRINTF("a %s\n", "somefile.cpp");
  PRINTF("a %s:%d\n", "somefile.cpp", 42);
  PRINTF("a %s:%d:%s\n", "somefile.cpp", 42, "asdf");
  PRINTF("a %s:%d:%d:%s\n", "somefile.cpp", 42, 1, "asdf");
  PRINTF("a %s:%d:%d:%d:%s\n", "somefile.cpp", 42, 1, 2, "asdf");
  PRINTF("a %s:%d:%d:%d:%s %s:%d:%d:%d:%s\n", "somefile.cpp", 42, 1, 2, "asdf", "somefile.cpp", 42, 1, 2, "asdf");
}

void doFormat_b() {
  PRINTF("b %s\n", "somefile.cpp");
  PRINTF("b %s:%d\n", "somefile.cpp", 42);
  PRINTF("b %s:%d:%s\n", "somefile.cpp", 42, "asdf");
  PRINTF("b %s:%d:%d:%s\n", "somefile.cpp", 42, 1, "asdf");
  PRINTF("b %s:%d:%d:%d:%s\n", "somefile.cpp", 42, 1, 2, "asdf");
}

void doFormat_c() {
  PRINTF("c %s\n", "somefile.cpp");
  PRINTF("c %s:%d\n", "somefile.cpp", 42);
  PRINTF("c %s:%d:%s\n", "somefile.cpp", 42, "asdf");
  PRINTF("c %s:%d:%d:%s\n", "somefile.cpp", 42, 1, "asdf");
  PRINTF("c %s:%d:%d:%d:%s\n", "somefile.cpp", 42, 1, 2, "asdf");
}

void doFormat_d() {
  PRINTF("d %s\n", "somefile.cpp");
  PRINTF("d %s:%d\n", "somefile.cpp", 42);
  PRINTF("d %s:%d:%s\n", "somefile.cpp", 42, "asdf");
  PRINTF("d %s:%d:%d:%s\n", "somefile.cpp", 42, 1, "asdf");
  PRINTF("d %s:%d:%d:%d:%s\n", "somefile.cpp", 42, 1, 2, "asdf");
}

#endif
'''

prefix = '_bloat_test_tmp_'
num_translation_units = 100

# Remove old files.
filenames = glob(prefix + '??.cc')
for f in [prefix + 'main.cc', prefix + 'all.h']:
  if os.path.exists(f):
    filenames.append(f)
for f in filenames:
  os.remove(f)

# Generate all the files.
main_source = prefix + 'main.cc'
main_header = prefix + 'all.h'
sources = [main_source]
with nested(open(main_source, 'w'), open(main_header, 'w')) as \
     (main_file, header_file):
  main_file.write(re.sub('^ +', '', '''
    #include "{}all.h"

    int main() {{
    '''.format(prefix), 0, re.MULTILINE))
  for i in range(num_translation_units):
    n = '{:03}'.format(i)
    source = prefix + n + '.cc'
    sources.append(source)
    with open(source, 'w') as f:
      if i == 0:
        f.write('#define FIRST_FILE\n')
      text = template
      for p in ["a", "b", "c", "d"]:
        func_name = 'doFormat_{}{}'.format(p, n)
        text = text.replace('doFormat_{}'.format(p), func_name).replace('42', str(i))
        main_file.write(func_name + '();\n')
        header_file.write('void ' + func_name + '();\n')
      f.write(text)
  main_file.write('}')

# Find compiler.
compiler_path = None
for path in os.getenv('PATH').split(os.pathsep):
  filename = os.path.join(path, 'g++')
  if os.path.exists(filename):
    if os.path.islink(filename) and \
       os.path.basename(os.path.realpath(filename)) == 'ccache':
      # Don't use ccache.
      print('Ignoring ccache link at', filename)
      continue
    compiler_path = filename
    break
print('Using compiler', filename)

class Result:
  pass

# Measure compile time and executable size.
expected_output = None
def benchmark(flags):
  output_filename = prefix + '.out'
  if os.path.exists(output_filename):
    os.remove(output_filename)
  include_dir = '-I' + os.path.dirname(os.path.realpath(__file__))
  command = [compiler_path, '-std=c++17', '-o', output_filename, include_dir] + sources + flags
  #print(" ".join(command))
  command = "check_call({})".format(command)
  result = Result()
  result.time = timeit(
    command, setup = 'from subprocess import check_call', number = 1)
  print('Compile time: {:.2f}s'.format(result.time))
  result.size = os.stat(output_filename).st_size
  print('Size: {}'.format(result.size))
  check_call(['strip', output_filename])
  result.stripped_size = os.stat(output_filename).st_size
  print('Stripped size: {}'.format(result.stripped_size))
  p = Popen(['./' + output_filename], stdout=PIPE,
            env={'LD_LIBRARY_PATH': 'fmt'})
  output = p.communicate()[0]
  global expected_output
  if not expected_output:
    expected_output = output
  elif output != expected_output:
    raise Exception("output doesn't match")
  sys.stdout.flush()
  return result

configs = [
  ('optimized', ['-O3', '-DNDEBUG']),
  #('debug',     [])
]

fmt_library = 'fmt/libfmt.so'
if not os.path.exists(fmt_library):
  fmt_library = fmt_library.replace('.so', '.dylib')
fmt_library = "-lfmt"

methods = [
 ('printf'       , []),
 ('printf+string', ['-DUSE_STRING']),
 ('IOStreams'    , ['-DUSE_IOSTREAMS']),
 ('fmt'          , ['-DUSE_FMT', '-Ifmt/include', fmt_library]),
 ('compiled_fmt' , ['-DUSE_FMT', '-Ifmt/include', fmt_library]),
 ('tinyformat'   , ['-DUSE_TINYFORMAT']),
 ('Boost Format' , ['-DUSE_BOOST']),
 ('Folly Format' , ['-DUSE_FOLLY', '-lfolly','-ldouble-conversion']),
 ('stb_sprintf'  , ['-DUSE_STB_SPRINTF']),
  ('pformat' , ['-DUSE_PFORMAT'])
]

def format_field(field, format = '', width = ''):
  return '{:{}{}}'.format(field, width, format)

def print_rulers(widths):
  for w in widths:
    print('=' * w, end = ' ')
  print()

# Prints a reStructuredText table.
def print_table(table, *formats):
  widths = [len(i) for i in table[0]]
  for row in table[1:]:
    for i in range(len(row)):
      widths[i] = max(widths[i], len(format_field(row[i], formats[i])))
  print_rulers(widths)
  row = table[0]
  for i in range(len(row)):
    print(format_field(row[i], '', widths[i]), end = ' ')
  print()
  print_rulers(widths)
  for row in table[1:]:
    for i in range(len(row)):
      print(format_field(row[i], formats[i], widths[i]), end = ' ')
    print()
  print_rulers(widths)

# Converts n to kibibytes.
def to_kib(n):
  return int(round(n / 1024.0))

NUM_RUNS = 1
for config, flags in configs:
  results = {}
  for i in range(NUM_RUNS):
    for method, method_flags in methods:
      print('Benchmarking', config, method)
      sys.stdout.flush()
      new_result = benchmark(flags + method_flags + sys.argv[1:])
      if method not in results:
        results[method] = new_result
        continue
      old_result = results[method]
      old_result.time = min(old_result.time, new_result.time)
      if new_result.size != old_result.size or \
         new_result.stripped_size != old_result.stripped_size:
        raise Exception('size mismatch')
  print(config, 'Results:')
  table = [
    ('Method', 'Compile Time, s', 'Executable size, KiB', 'Stripped size, KiB')
  ]
  for method, method_flags in methods:
    result = results[method]
    table.append(
      (method, result.time, to_kib(result.size), to_kib(result.stripped_size)))
  print_table(table, '', '.1f', '', '')

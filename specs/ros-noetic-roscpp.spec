Name:           ros-noetic-roscpp
Version:        noetic.1.16.0
Release:        1%{?dist}
Summary:        ROS package roscpp

License:        BSD
URL:            http://www.ros.org/

Source0:        https://github.com/ros-gbp/ros_comm-release/archive/release/noetic/roscpp/1.16.0-1.tar.gz#/ros-noetic-roscpp-1.16.0-source0.tar.gz



# common BRs
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  gtest-devel
BuildRequires:  log4cxx-devel
BuildRequires:  python3-devel
BuildRequires:  python-unversioned-command

BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  log4cxx-devel
BuildRequires:  pkgconfig
BuildRequires:  ros-noetic-catkin-devel
BuildRequires:  ros-noetic-cpp_common-devel
BuildRequires:  ros-noetic-message_generation-devel
BuildRequires:  ros-noetic-rosconsole-devel
BuildRequires:  ros-noetic-roscpp_serialization-devel
BuildRequires:  ros-noetic-roscpp_traits-devel
BuildRequires:  ros-noetic-rosgraph_msgs-devel
BuildRequires:  ros-noetic-roslang-devel
BuildRequires:  ros-noetic-rostime-devel
BuildRequires:  ros-noetic-std_msgs-devel
BuildRequires:  ros-noetic-xmlrpcpp-devel

Requires:       ros-noetic-cpp_common
Requires:       ros-noetic-message_runtime
Requires:       ros-noetic-rosconsole
Requires:       ros-noetic-roscpp_serialization
Requires:       ros-noetic-roscpp_traits
Requires:       ros-noetic-rosgraph_msgs
Requires:       ros-noetic-rostime
Requires:       ros-noetic-std_msgs
Requires:       ros-noetic-xmlrpcpp

Provides:  ros-noetic-roscpp = 1.16.0-1
Obsoletes: ros-noetic-roscpp < 1.16.0-1
Obsoletes: ros-kinetic-roscpp < 1.16.0-1



%description
roscpp is a C++ implementation of ROS. It provides a

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ros-noetic-catkin-devel
Requires:       boost-devel
Requires:       console-bridge-devel
Requires:       log4cxx-devel
Requires:       pkgconfig
Requires:       ros-noetic-cpp_common-devel
Requires:       ros-noetic-message_generation-devel
Requires:       ros-noetic-rosconsole-devel
Requires:       ros-noetic-roscpp_serialization-devel
Requires:       ros-noetic-roscpp_traits-devel
Requires:       ros-noetic-rosgraph_msgs-devel
Requires:       ros-noetic-roslang-devel
Requires:       ros-noetic-rostime-devel
Requires:       ros-noetic-std_msgs-devel
Requires:       ros-noetic-xmlrpcpp-devel
Requires:       ros-noetic-message_runtime-devel

Provides: ros-noetic-roscpp-devel = 1.16.0-1
Obsoletes: ros-noetic-roscpp-devel < 1.16.0-1
Obsoletes: ros-kinetic-roscpp-devel < 1.16.0-1


%description devel
The %{name}-devel package contains libraries and header files for developing
applications that use %{name}.



%prep

%setup -c -T
tar --strip-components=1 -xf %{SOURCE0}

%build
# nothing to do here


%install

PYTHONUNBUFFERED=1 ; export PYTHONUNBUFFERED

CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS ; \
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS ; \
FFLAGS="${FFLAGS:-%optflags%{?_fmoddir: -I%_fmoddir}}" ; export FFLAGS ; \
FCFLAGS="${FCFLAGS:-%optflags%{?_fmoddir: -I%_fmoddir}}" ; export FCFLAGS ; \
%{?__global_ldflags:LDFLAGS="${LDFLAGS:-%__global_ldflags}" ; export LDFLAGS ;} \

source %{_libdir}/ros/setup.bash

# substitute shebang before install block because we run the local catkin script
%py3_shebang_fix .

DESTDIR=%{buildroot} ; export DESTDIR


catkin_make_isolated \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCATKIN_ENABLE_TESTING=OFF \
  -DPYTHON_VERSION=%{python3_version} \
  -DPYTHON_VERSION_NODOTS=%{python3_version_nodots} \
  --source . \
  --install \
  --install-space %{_libdir}/ros/ \
  --pkg roscpp




rm -rf %{buildroot}/%{_libdir}/ros/{.catkin,.rosinstall,_setup*,local_setup*,setup*,env.sh}

touch files.list
find %{buildroot}/%{_libdir}/ros/{bin,etc,lib64/python*,lib/python*/site-packages,share} \
  -mindepth 1 -maxdepth 1 | sed "s:%{buildroot}/::" > files.list
find %{buildroot}/%{_libdir}/ros/lib*/ -mindepth 1 -maxdepth 1 \
  ! -name pkgconfig ! -name "python*" \
  | sed "s:%{buildroot}/::" >> files.list

touch files_devel.list
find %{buildroot}/%{_libdir}/ros/{include,lib*/pkgconfig,share/roscpp/cmake} \
  -mindepth 1 -maxdepth 1 | sed "s:%{buildroot}/::" > files_devel.list

find . -maxdepth 1 -type f -iname "*readme*" | sed "s:^:%%doc :" >> files.list
find . -maxdepth 1 -type f -iname "*license*" | sed "s:^:%%license :" >> files.list



# replace cmake python macro in shebang
for file in $(grep -rIl '^#!.*@PYTHON_EXECUTABLE@.*$' %{buildroot}) ; do
  sed -i.orig 's:^#!\s*@PYTHON_EXECUTABLE@\s*:%{__python3}:' $file
  touch -r $file.orig $file
  rm $file.orig
done


echo "This is a package automatically generated with rosfed." >> README_FEDORA
echo "See https://pagure.io/ros for more information." >> README_FEDORA
install -m 0644 -p -D -t %{buildroot}/%{_docdir}/%{name} README_FEDORA
echo %{_docdir}/%{name} >> files.list
install -m 0644 -p -D -t %{buildroot}/%{_docdir}/%{name}-devel README_FEDORA
echo %{_docdir}/%{name}-devel >> files_devel.list

%py3_shebang_fix %{buildroot}

# Also fix .py.in files
for pyfile in $(grep -rIl '^#!.*python.*$' %{buildroot}) ; do
  %py3_shebang_fix $pyfile
done


%files -f files.list
%files devel -f files_devel.list


%changelog
* 2023-04-17 Ryan Wüest <ryan.wueest@protonmail.com> - noetic.1.16.0-1
- Initial desktop generation

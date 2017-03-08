%{?_javapackages_macros:%_javapackages_macros}

Summary:	Java Graph Visualization and Layout component
Name:		jgraph
Version:	5.13.0.0
Release:	1
License:	BSD
Group:		Development/Java
URL:		https://www.jgraph.com/
Source0:	https://www.jgraph.com/downloads/jgraph/archive/%{name}-%{version}-bsd-src.jar
Source1:	https://repo1.maven.org/maven2/jgraph/%{name}/%{version}/%{name}-%{version}.pom
BuildArch:	noarch

BuildRequires:	maven-local

%description
A component to display, edit and layout graphs (networks) with Java.

The intention of this project is to provide a freely available and fully Swing
compliant implementation of a graph component. You can display objects and
relations (networks) in any Swing UI, interact with them, automatically
position them and analysis their graph structure.

%files -f .mfiles
%doc README
%doc ChangeLog
%doc LICENSE

#----------------------------------------------------------------------------

%package javadoc
Summary:	Javadoc for %{name}
Group:		Documentation

%description javadoc
API documentation for %{name}.

%files javadoc -f .mfiles-javadoc
%doc LICENSE

#----------------------------------------------------------------------------

%prep
%setup -q -c %{name}-%{version}
# Extract source files
jar -xf %{SOURCE0}

# Delete all pre-built binaries
find . -name "*.jar" -delete
find . -name "*.class" -delete

# Remove pre-built docs
rm -rf docs/api

# Copy pom.xml file here
cp %{SOURCE1} ./pom.xml

# Add Javadoc plugin
%pom_add_plugin :maven-javadoc-plugin . "
<configuration>
	<sourcepath>src/</sourcepath>
	<footer></footer>
</configuration>
<executions>
	<execution>
		<id>attach-javadocs</id>
	<goals>
		<goal>jar</goal>
	</goals>
	</execution>
</executions>"

# Fix the sources path
%pom_xpath_inject "pom:project/pom:build" "
	<sourceDirectory>src/</sourceDirectory>" .

# Fix jar-not-indexed warning
%pom_add_plugin :maven-jar-plugin . "
<configuration>
	<archive>
		<index>true</index>
	</archive>
</configuration>"

# Fix Jar name
%mvn_file :%{name} %{name}-%{version} %{name}

%build
%mvn_build -- -Dproject.build.sourceEncoding=UTF-8 

%install
%mvn_install


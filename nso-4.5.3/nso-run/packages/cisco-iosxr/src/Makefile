
JAVA_PACKAGE = com.tailf.packages.ned.iosxr
JDIR = $(shell echo $(JAVA_PACKAGE) | sed 's/\./\//g')

NS  = namespaces

JFLAGS = --java-disable-prefix \
         --exclude-enums \
         --fail-on-warnings \
         --java-package $(JAVA_PACKAGE).$(NS) \
         --emit-java java/src/$(JDIR)/namespaces

all:	fxs javac
	cd ../netsim && $(MAKE) all

# Include standard NCS examples build definitions and rules
include $(NCS_DIR)/src/ncs/build/include.ncs.mk

FXS = ncsc-out/modules/fxs/tailf-ned-cisco-ios-xr.fxs \
	../load-dir/tailf-ned-cisco-ios-xr-id.fxs

fxs:	$(FXS)

NCSC_NED_ARGS = --ncs-device-dir ncsc-out \
	--ncs-device-type cli-ned

ifneq ($(shell $(NCSC) -h | grep ncs-ned-id),)
NCSC_NED_ARGS += --ncs-ned-id tailf-ned-cisco-ios-xr-id:cisco-ios-xr
endif

ncsc-out/modules/fxs/%.fxs:	yang/%.yang
	$(NCSC) --ncs-compile-module ./yang/$*.yang \
                --ncs-skip-statistics \
	        $(NCSC_NED_ARGS) && \
	  cp ncsc-out/modules/fxs/* ../load-dir
	$(NCSC) $(JFLAGS)/$*.java $@

../load-dir/%.fxs: yang/%.yang
	$(NCSC) -c $< -o $@
	$(NCSC) $(JFLAGS)/$*.java $@

javac:
	cd java && ant -q all

clean:
	rm -rf ncsc-out/* ../load-dir/* ncsc-out/*
	rm -f ../jar/*.jar
	rm -f java/src/$(JDIR)/$(NS)/*.java
	cd java && ant clean
	cd ../netsim && $(MAKE) clean

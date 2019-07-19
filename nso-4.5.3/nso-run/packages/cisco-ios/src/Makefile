
JAVA_PACKAGE = com.tailf.packages.ned.ios
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

FXS = ncsc-out/modules/fxs/tailf-ned-cisco-ios-stats.fxs \
	ncsc-out/modules/fxs/tailf-ned-cisco-ios.fxs \
	../load-dir/tailf-ned-cisco-ios-id.fxs

fxs:	$(FXS)

NCSC_NED_ARGS = --ncs-device-dir ncsc-out \
	--ncs-device-type cli-ned

ifneq ($(shell $(NCSC) -h | grep ncs-ned-id),)
NCSC_NED_ARGS += --ncs-ned-id tailf-ned-cisco-ios-id:cisco-ios
endif

ncsc-out/modules/fxs/tailf-ned-cisco-ios-stats.fxs:\
	yang/tailf-ned-cisco-ios-stats.yang
	$(NCSC) --ncs-compile-module $< \
	        --ncs-skip-config \
	        --ncs-skip-template \
	        $(NCSC_NED_ARGS) && \
	  cp $@ ../load-dir

ncsc-out/modules/fxs/tailf-ned-cisco-ios.fxs:\
	yang/tailf-ned-cisco-ios.yang
	$(NCSC) --ncs-compile-module $< \
	        --ncs-skip-statistics \
	        $(NCSC_NED_ARGS) && \
	  cp $@ ../load-dir

../load-dir/tailf-ned-cisco-ios-id.fxs:\
	yang/tailf-ned-cisco-ios-id.yang
	$(NCSC) -c $< -o $@

java/src/com/tailf/packages/ned/ios/namespaces/CiscoIosId.java: \
	../load-dir/tailf-ned-cisco-ios-id.fxs
	$(NCSC) $(JFLAGS)/CiscoIosId.java $<

java/src/com/tailf/packages/ned/ios/namespaces/CiscoIos.java: \
	ncsc-out/modules/fxs/tailf-ned-cisco-ios.fxs
	$(NCSC) $(JFLAGS)/CiscoIos.java $<

java/src/com/tailf/packages/ned/ios/namespaces/CiscoIosStats.java: \
	ncsc-out/modules/fxs/tailf-ned-cisco-ios-stats.fxs
	$(NCSC) $(JFLAGS)/CiscoIosStats.java $<

javac: java/src/com/tailf/packages/ned/ios/namespaces/CiscoIos.java \
	java/src/com/tailf/packages/ned/ios/namespaces/CiscoIosStats.java \
	java/src/com/tailf/packages/ned/ios/namespaces/CiscoIosId.java
	cd java && ant -q all

clean:
	rm -rf ncsc-out/* ../load-dir/*
	rm -f ../jar/*.jar
	rm -f java/src/$(JDIR)/$(NS)/*.java
	cd java && ant clean
	cd ../netsim && $(MAKE) clean

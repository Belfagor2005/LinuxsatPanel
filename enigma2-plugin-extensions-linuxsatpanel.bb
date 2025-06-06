SUMMARY = "linuxsat panel addon"
MAINTAINER = "lululla"
SECTION = "extra"
PRIORITY = "required"
LICENSE = "proprietary"

require conf/license/license-gplv2.inc

inherit gitpkgv

SRCREV = "${AUTOREV}"
PV = "1.0+git${SRCPV}"
PKGV = "1.0+git${GITPKGV}"
VER ="2.7"
PR = "r0"

SRC_URI = "git://github.com/Belfagor2005/LinuxsatPanel.git;protocol=https;branch=main"

S = "${WORKDIR}/git"

FILES_${PN} = "/usr/*"

do_install() {
    cp -af --no-preserve=ownership ${S}/usr* ${D}/
}


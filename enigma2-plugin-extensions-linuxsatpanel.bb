SUMMARY = "linuxsat panel addon"
MAINTAINER = "lululla"
SECTION = "extra"
PRIORITY = "required"
LICENSE = "CLOSED"

inherit gitpkgv allarch

SRCREV = "${AUTOREV}"
PV = "2.4+git${SRCPV}"
PKGV = "2.4+git${GITPKGV}"
PR = "r0"

SRC_URI = "git://github.com/Belfagor2005/LinuxsatPanel.git;protocol=https;branch=main"

S = "${WORKDIR}/git"

do_install() {
    install -d ${D}${libdir}/enigma2/python/Plugins/Extensions/LinuxsatPanel
    cp -r ${S}/usr/lib/enigma2/python/Plugins/Extensions/LinuxsatPanel/* \
          ${D}${libdir}/enigma2/python/Plugins/Extensions/LinuxsatPanel/
}

FILES:${PN} = "${libdir}/enigma2/python/Plugins/Extensions/LinuxsatPanel"
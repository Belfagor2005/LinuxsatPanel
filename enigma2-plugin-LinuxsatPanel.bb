SUMMARY = "linuxsat panel addon"
MAINTAINER = "www.linuxsat-support.com"
SECTION = "extra"
LICENSE = "proprietary"

inherit gitpkgv
SRCREV = "${AUTOREV}"
PV = "2.2+git${SRCPV}"
PKGV = "2.2+git${GITPKGV}"
PR = "r0"

SRC_URI = "git://github.com/Belfagor2005/LinuxsatPanel.git;branch=main"

S = "${WORKDIR}/git"
FILES_${PN} = "/usr/*"

do_install() {
    cp -rp ${S}/usr ${D}/
}

do_package_qa[noexec] = "1"

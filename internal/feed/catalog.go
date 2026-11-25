// SPDX-License-Identifier: GPL-3.0-only

package feed

import "strings"

type Package struct {
	Tag          string
	SourceURL    string
	Kind         string
	Policy       string
	AllowTLD     bool
	RequireCount bool
}

const (
	Domain    = "domain"
	IP        = "ip"
	Block     = "block"
	Allow     = "allow"
	MediumTag = "tif-medium"
)

func (p Package) Asset() string {
	if p.Tag == MediumTag {
		return "hagezi-tif.dat"
	}
	return "hagezi-" + p.Tag + ".dat"
}

func (p Package) SourceFile() string {
	return "source-" + p.Tag + ".txt"
}

func Packages() []Package {
	const source = "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/"
	const registrations = "https://raw.githubusercontent.com/hagezi/nrd/main/domains/"

	domains := []struct{ tag, file string }{
		{MediumTag, "tif.medium"},
		{"tif-full", "tif"},
		{"tif-mini", "tif.mini"},
		{"multi-light", "light"},
		{"multi-normal", "multi"},
		{"multi-pro", "pro"},
		{"multi-pro-mini", "pro.mini"},
		{"multi-pro-plus", "pro.plus"},
		{"multi-pro-plus-mini", "pro.plus.mini"},
		{"multi-ultimate", "ultimate"},
		{"multi-ultimate-mini", "ultimate.mini"},
		{"fake", "fake"},
		{"popupads", "popupads"},
		{"dyndns", "dyndns"},
		{"badware-hoster", "hoster"},
		{"spam-tlds", "spam-tlds"},
		{"spam-tlds-allow", "spam-tlds-allow"},
		{"doh", "doh"},
		{"doh-vpn-proxy-bypass", "doh-vpn-proxy-bypass"},
		{"nosafesearch", "nosafesearch"},
		{"urlshortener", "urlshortener"},
		{"anti-piracy", "anti.piracy"},
		{"gambling", "gambling"},
		{"gambling-medium", "gambling.medium"},
		{"gambling-mini", "gambling.mini"},
		{"social", "social"},
		{"nsfw", "nsfw"},
		{"referral-block", "blocklist-referral"},
		{"referral-allow", "whitelist-referral"},
		{"native-amazon", "native.amazon"},
		{"native-apple", "native.apple"},
		{"native-huawei", "native.huawei"},
		{"native-lgwebos", "native.lgwebos"},
		{"native-oppo-realme", "native.oppo-realme"},
		{"native-roku", "native.roku"},
		{"native-samsung", "native.samsung"},
		{"native-tiktok", "native.tiktok"},
		{"native-tiktok-extended", "native.tiktok.extended"},
		{"native-vivo", "native.vivo"},
		{"native-winoffice", "native.winoffice"},
		{"native-xiaomi", "native.xiaomi"},
	}

	packages := make([]Package, 0, len(domains)+11)
	for _, entry := range domains {
		p := Package{
			Tag:          entry.tag,
			SourceURL:    source + "wildcard/" + entry.file + "-onlydomains.txt",
			Kind:         Domain,
			Policy:       Block,
			RequireCount: true,
		}
		if strings.HasSuffix(p.Tag, "-allow") {
			p.Policy = Allow
		}
		if p.Tag == "spam-tlds" {
			p.AllowTLD = true
			p.RequireCount = false
		}
		if p.Tag == "spam-tlds-allow" {
			p.RequireCount = false
		}
		packages = append(packages, p)
	}
	for _, tag := range []string{"nrd7", "nrd14-8", "nrd21-15", "nrd28-22", "nrd35-29", "dga7", "dga14", "dga30"} {
		packages = append(packages, Package{
			Tag: tag, SourceURL: registrations + tag + ".txt", Kind: Domain, Policy: Block, RequireCount: true,
		})
	}
	return append(packages,
		Package{Tag: "tif-ipv4", SourceURL: source + "ips/tif.txt", Kind: IP, Policy: Block},
		Package{Tag: "doh-ipv4", SourceURL: source + "ips/doh.txt", Kind: IP, Policy: Block},
		Package{Tag: "nameserver-ip", SourceURL: source + "ips/nameserver.txt", Kind: IP, Policy: Block},
	)
}

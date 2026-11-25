// SPDX-License-Identifier: GPL-3.0-only

package geosite

import (
	"net/netip"
	"strings"

	"github.com/v2fly/v2ray-core/v5/app/router/routercommon"
	"google.golang.org/protobuf/proto"
)

func Encode(tag string, domains []string) ([]byte, error) {
	entries := make([]routercommon.Domain, len(domains))
	site := &routercommon.GeoSite{
		CountryCode: strings.ToUpper(tag),
		Domain:      make([]*routercommon.Domain, len(domains)),
	}
	for i, domain := range domains {
		entries[i].Type = routercommon.Domain_RootDomain
		entries[i].Value = domain
		site.Domain[i] = &entries[i]
	}
	return proto.Marshal(&routercommon.GeoSiteList{Entry: []*routercommon.GeoSite{site}})
}

func EncodeIPs(tag string, prefixes []string) ([]byte, error) {
	entries := make([]routercommon.CIDR, len(prefixes))
	list := &routercommon.GeoIP{
		CountryCode: strings.ToUpper(tag),
		Cidr:        make([]*routercommon.CIDR, len(prefixes)),
	}
	for i, value := range prefixes {
		prefix, err := netip.ParsePrefix(value)
		if err != nil {
			return nil, err
		}
		entries[i].Ip = prefix.Addr().AsSlice()
		entries[i].Prefix = uint32(prefix.Bits())
		list.Cidr[i] = &entries[i]
	}
	return proto.Marshal(&routercommon.GeoIPList{Entry: []*routercommon.GeoIP{list}})
}

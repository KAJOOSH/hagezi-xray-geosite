// SPDX-License-Identifier: GPL-3.0-only

package geosite

import (
	"strings"

	"github.com/v2fly/v2ray-core/v5/app/router/routercommon"
	"google.golang.org/protobuf/proto"
)

const (
	Filename = "hagezi-tif.dat"
	Category = "tif-medium"
)

func Encode(domains []string) ([]byte, error) {
	entries := make([]routercommon.Domain, len(domains))
	site := &routercommon.GeoSite{
		CountryCode: strings.ToUpper(Category),
		Domain:      make([]*routercommon.Domain, len(domains)),
	}
	for i, domain := range domains {
		entries[i].Type = routercommon.Domain_RootDomain
		entries[i].Value = domain
		site.Domain[i] = &entries[i]
	}
	return proto.Marshal(&routercommon.GeoSiteList{Entry: []*routercommon.GeoSite{site}})
}

// SPDX-License-Identifier: GPL-3.0-only

package feed

import (
	"bufio"
	"bytes"
	"context"
	"fmt"
	"io"
	"net/http"
	"net/netip"
	"slices"
	"strconv"
	"strings"
	"time"
)

const (
	SourceURL = "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/wildcard/tif.medium-onlydomains.txt"
	maxBytes  = 16 << 20
)

type Snapshot struct {
	Raw     []byte
	Version string
	Domains []string
}

func Download(ctx context.Context) (Snapshot, error) {
	request, err := http.NewRequestWithContext(ctx, http.MethodGet, SourceURL, nil)
	if err != nil {
		return Snapshot{}, err
	}
	client := &http.Client{Timeout: 45 * time.Second}
	response, err := client.Do(request)
	if err != nil {
		return Snapshot{}, fmt.Errorf("download HaGeZi feed: %w", err)
	}
	defer response.Body.Close()
	if response.StatusCode != http.StatusOK {
		return Snapshot{}, fmt.Errorf("download HaGeZi feed: HTTP %s", response.Status)
	}

	raw, err := io.ReadAll(io.LimitReader(response.Body, maxBytes+1))
	if err != nil {
		return Snapshot{}, fmt.Errorf("read HaGeZi feed: %w", err)
	}
	if len(raw) > maxBytes {
		return Snapshot{}, fmt.Errorf("HaGeZi feed exceeds %d bytes", maxBytes)
	}
	return parse(raw)
}

func parse(raw []byte) (Snapshot, error) {
	snapshot := Snapshot{Raw: raw}
	declaredCount := 0
	scanner := bufio.NewScanner(bytes.NewReader(bytes.TrimPrefix(raw, []byte("\xef\xbb\xbf"))))
	for lineNumber := 1; scanner.Scan(); lineNumber++ {
		line := strings.TrimSpace(scanner.Text())
		switch {
		case line == "":
			continue
		case strings.HasPrefix(line, "# Version:"):
			snapshot.Version = strings.TrimSpace(strings.TrimPrefix(line, "# Version:"))
		case strings.HasPrefix(line, "# Number of entries:"):
			count, err := strconv.Atoi(strings.TrimSpace(strings.TrimPrefix(line, "# Number of entries:")))
			if err != nil || count <= 0 {
				return Snapshot{}, fmt.Errorf("invalid feed entry count on line %d", lineNumber)
			}
			declaredCount = count
		case strings.HasPrefix(line, "#"):
			continue
		default:
			domain := strings.ToLower(line)
			if !validDomain(domain) {
				return Snapshot{}, fmt.Errorf("invalid domain rule on line %d", lineNumber)
			}
			snapshot.Domains = append(snapshot.Domains, domain)
		}
	}
	if err := scanner.Err(); err != nil {
		return Snapshot{}, fmt.Errorf("scan HaGeZi feed: %w", err)
	}
	if snapshot.Version == "" || declaredCount == 0 || len(snapshot.Domains) != declaredCount {
		return Snapshot{}, fmt.Errorf("incomplete HaGeZi feed: version %q, read %d of %d domains",
			snapshot.Version, len(snapshot.Domains), declaredCount)
	}

	slices.Sort(snapshot.Domains)
	snapshot.Domains = slices.Compact(snapshot.Domains)
	return snapshot, nil
}

func validDomain(domain string) bool {
	if len(domain) > 253 || !strings.Contains(domain, ".") {
		return false
	}
	if _, err := netip.ParseAddr(domain); err == nil {
		return false
	}
	for label := range strings.SplitSeq(domain, ".") {
		if len(label) == 0 || len(label) > 63 || label[0] == '-' || label[len(label)-1] == '-' {
			return false
		}
		for i := range len(label) {
			ch := label[i]
			if (ch < 'a' || ch > 'z') && (ch < '0' || ch > '9') && ch != '-' {
				return false
			}
		}
	}
	return true
}

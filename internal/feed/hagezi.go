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

const maxBytes = 128 << 20

type Snapshot struct {
	Raw     []byte
	Version string
	Entries []string
}

func Download(ctx context.Context, client *http.Client, p Package) (Snapshot, error) {
	var err error
	for attempt := 0; attempt < 3; attempt++ {
		var raw []byte
		raw, err = download(ctx, client, p.SourceURL)
		if err == nil {
			return parse(raw, p)
		}
		if attempt == 2 {
			break
		}
		select {
		case <-ctx.Done():
			return Snapshot{}, ctx.Err()
		case <-time.After(time.Duration(attempt+1) * time.Second):
		}
	}
	return Snapshot{}, err
}

func download(ctx context.Context, client *http.Client, url string) ([]byte, error) {
	request, err := http.NewRequestWithContext(ctx, http.MethodGet, url, nil)
	if err != nil {
		return nil, err
	}
	response, err := client.Do(request)
	if err != nil {
		return nil, fmt.Errorf("download HaGeZi feed: %w", err)
	}
	defer response.Body.Close()
	if response.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("download HaGeZi feed: HTTP %s", response.Status)
	}

	raw, err := io.ReadAll(io.LimitReader(response.Body, maxBytes+1))
	if err != nil {
		return nil, fmt.Errorf("read HaGeZi feed: %w", err)
	}
	if len(raw) > maxBytes {
		return nil, fmt.Errorf("HaGeZi feed exceeds %d bytes", maxBytes)
	}
	return raw, nil
}

func parse(raw []byte, p Package) (Snapshot, error) {
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
			snapshot.Entries = make([]string, 0, min(count, len(raw)/3))
		case strings.HasPrefix(line, "#"):
			continue
		default:
			entry, err := normalize(line, p)
			if err != nil {
				return Snapshot{}, fmt.Errorf("line %d: %w", lineNumber, err)
			}
			snapshot.Entries = append(snapshot.Entries, entry)
		}
	}
	if err := scanner.Err(); err != nil {
		return Snapshot{}, fmt.Errorf("scan HaGeZi feed: %w", err)
	}
	if len(snapshot.Entries) == 0 ||
		(p.RequireCount && (declaredCount == 0 || snapshot.Version == "")) ||
		(declaredCount != 0 && len(snapshot.Entries) != declaredCount) {
		return Snapshot{}, fmt.Errorf("incomplete HaGeZi feed: version %q, read %d of %d entries",
			snapshot.Version, len(snapshot.Entries), declaredCount)
	}

	slices.Sort(snapshot.Entries)
	snapshot.Entries = slices.Compact(snapshot.Entries)
	return snapshot, nil
}

func normalize(line string, p Package) (string, error) {
	if p.Kind == IP {
		if addr, err := netip.ParseAddr(line); err == nil && addr.Zone() == "" {
			return netip.PrefixFrom(addr, addr.BitLen()).String(), nil
		}
		if prefix, err := netip.ParsePrefix(line); err == nil {
			return prefix.Masked().String(), nil
		}
		return "", fmt.Errorf("invalid IP rule")
	}

	domain := strings.ToLower(strings.TrimSuffix(line, "."))
	if !validDomain(domain, p.AllowTLD) {
		return "", fmt.Errorf("invalid domain rule")
	}
	return domain, nil
}

func validDomain(domain string, allowTLD bool) bool {
	if len(domain) > 253 || (!allowTLD && !strings.Contains(domain, ".")) {
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
			if (ch < 'a' || ch > 'z') && (ch < '0' || ch > '9') && ch != '-' && ch != '_' {
				return false
			}
		}
	}
	return true
}

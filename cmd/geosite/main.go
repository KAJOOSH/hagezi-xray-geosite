// SPDX-License-Identifier: GPL-3.0-only

package main

import (
	"context"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"os"
	"os/signal"
	"path/filepath"

	"hagezi-xray-geosite/internal/feed"
	"hagezi-xray-geosite/internal/geosite"
)

const sourceFilename = "source-tif-medium.txt"

type manifest struct {
	SourceURL     string `json:"source_url"`
	SourceVersion string `json:"source_version"`
	SourceSHA256  string `json:"source_sha256"`
	License       string `json:"license"`
	Asset         string `json:"asset"`
	AssetSHA256   string `json:"asset_sha256"`
	Category      string `json:"category"`
	DomainCount   int    `json:"domain_count"`
}

func main() {
	outputDir := flag.String("out-dir", "dist", "directory for the generated files")
	flag.Parse()
	if flag.NArg() != 0 {
		log.Fatal("unexpected positional arguments")
	}

	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt)
	defer stop()
	if err := generate(ctx, *outputDir); err != nil {
		log.Fatal(err)
	}
}

func generate(ctx context.Context, outputDir string) error {
	snapshot, err := feed.Download(ctx)
	if err != nil {
		return err
	}
	asset, err := geosite.Encode(snapshot.Domains)
	if err != nil {
		return fmt.Errorf("encode GeoSite: %w", err)
	}

	assetHash := sha256.Sum256(asset)
	sourceHash := sha256.Sum256(snapshot.Raw)
	info := manifest{
		SourceURL:     feed.SourceURL,
		SourceVersion: snapshot.Version,
		SourceSHA256:  hex.EncodeToString(sourceHash[:]),
		License:       "GPL-3.0-only",
		Asset:         geosite.Filename,
		AssetSHA256:   hex.EncodeToString(assetHash[:]),
		Category:      geosite.Category,
		DomainCount:   len(snapshot.Domains),
	}
	metadata, err := json.MarshalIndent(info, "", "  ")
	if err != nil {
		return fmt.Errorf("encode manifest: %w", err)
	}

	if err := os.MkdirAll(outputDir, 0o755); err != nil {
		return err
	}
	files := []struct {
		name string
		data []byte
	}{
		{geosite.Filename, asset},
		{geosite.Filename + ".sha256", []byte(fmt.Sprintf("%s  %s\n", info.AssetSHA256, info.Asset))},
		{sourceFilename, snapshot.Raw},
		{"manifest.json", append(metadata, '\n')},
	}
	for _, file := range files {
		if err := writeFile(outputDir, file.name, file.data); err != nil {
			return fmt.Errorf("write %s: %w", file.name, err)
		}
	}
	fmt.Printf("Generated %s from HaGeZi %s with %d domains\n",
		filepath.Join(outputDir, info.Asset), info.SourceVersion, info.DomainCount)
	return nil
}

func writeFile(dir, name string, data []byte) error {
	temp, err := os.CreateTemp(dir, "."+name+"-*")
	if err != nil {
		return err
	}
	defer os.Remove(temp.Name())
	_, writeErr := temp.Write(data)
	closeErr := temp.Close()
	if writeErr != nil {
		return writeErr
	}
	if closeErr != nil {
		return closeErr
	}
	if err := os.Chmod(temp.Name(), 0o644); err != nil {
		return err
	}
	return os.Rename(temp.Name(), filepath.Join(dir, name))
}

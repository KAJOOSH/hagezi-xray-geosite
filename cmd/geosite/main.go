// SPDX-License-Identifier: GPL-3.0-only

package main

import (
	"archive/zip"
	"context"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"os/signal"
	"path/filepath"
	"strings"
	"time"

	"hagezi-xray-geosite/internal/feed"
	"hagezi-xray-geosite/internal/geosite"
)

const sourceArchive = "sources.zip"

type packageManifest struct {
	Category      string `json:"category"`
	Kind          string `json:"kind"`
	Policy        string `json:"policy"`
	Asset         string `json:"asset"`
	AssetSHA256   string `json:"asset_sha256"`
	SourceFile    string `json:"source_file"`
	SourceURL     string `json:"source_url"`
	SourceVersion string `json:"source_version,omitempty"`
	SourceSHA256  string `json:"source_sha256"`
	EntryCount    int    `json:"entry_count"`
}

type manifest struct {
	Version         string `json:"version"`
	BuiltAt         string `json:"built_at"`
	GeneratorCommit string `json:"generator_commit,omitempty"`
	License         string `json:"license"`
	DomainCount     int    `json:"domain_count"`
	packageManifest
	Packages []packageManifest `json:"packages"`
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
	if err := os.MkdirAll(outputDir, 0o755); err != nil {
		return err
	}
	stagingDir, err := os.MkdirTemp(outputDir, ".build-*")
	if err != nil {
		return err
	}
	defer os.RemoveAll(stagingDir)
	if err := build(ctx, stagingDir); err != nil {
		return err
	}

	entries, err := os.ReadDir(stagingDir)
	if err != nil {
		return err
	}
	for _, entry := range entries {
		if entry.Name() == "manifest.json" {
			continue
		}
		if err := os.Rename(filepath.Join(stagingDir, entry.Name()), filepath.Join(outputDir, entry.Name())); err != nil {
			return err
		}
	}
	return os.Rename(filepath.Join(stagingDir, "manifest.json"), filepath.Join(outputDir, "manifest.json"))
}

func build(ctx context.Context, outputDir string) error {
	tempArchive, err := os.CreateTemp(outputDir, ".sources-*.zip")
	if err != nil {
		return err
	}
	defer os.Remove(tempArchive.Name())
	defer tempArchive.Close()

	archiveHash := sha256.New()
	sources := zip.NewWriter(io.MultiWriter(tempArchive, archiveHash))
	client := &http.Client{Timeout: 3 * time.Minute}
	defer client.CloseIdleConnections()

	var info manifest
	var checksums strings.Builder
	for _, p := range feed.Packages() {
		entry, err := buildPackage(ctx, client, p, outputDir, sources)
		if err != nil {
			return fmt.Errorf("%s: %w", p.Tag, err)
		}
		fmt.Fprintf(&checksums, "%s  %s\n", entry.AssetSHA256, entry.Asset)
		info.Packages = append(info.Packages, entry)
		if p.Tag == feed.MediumTag {
			info.packageManifest = entry
			info.DomainCount = entry.EntryCount
		}
		fmt.Printf("Generated %s with %d entries\n", entry.Asset, entry.EntryCount)
	}
	if err := sources.Close(); err != nil {
		return fmt.Errorf("finish source archive: %w", err)
	}
	if err := tempArchive.Close(); err != nil {
		return err
	}
	if err := os.Chmod(tempArchive.Name(), 0o644); err != nil {
		return err
	}
	if err := os.Rename(tempArchive.Name(), filepath.Join(outputDir, sourceArchive)); err != nil {
		return err
	}
	fmt.Fprintf(&checksums, "%s  %s\n", hex.EncodeToString(archiveHash.Sum(nil)), sourceArchive)

	builtAt := time.Now().UTC()
	buildNumber := os.Getenv("GITHUB_RUN_NUMBER")
	if buildNumber == "" {
		buildNumber = builtAt.Format("150405")
	}
	info.Version = "v" + builtAt.Format("20060102") + "." + buildNumber
	info.BuiltAt = builtAt.Format(time.RFC3339)
	info.GeneratorCommit = os.Getenv("GITHUB_SHA")
	info.License = "GPL-3.0-only"
	metadata, err := json.MarshalIndent(info, "", "  ")
	if err != nil {
		return fmt.Errorf("encode manifest: %w", err)
	}
	if err := writeFile(outputDir, "checksums.sha256", []byte(checksums.String())); err != nil {
		return err
	}
	if err := writeFile(outputDir, "manifest.json", append(metadata, '\n')); err != nil {
		return err
	}
	fmt.Printf("Prepared %s with %d separate Xray packages\n", info.Version, len(info.Packages))
	return nil
}

func buildPackage(ctx context.Context, client *http.Client, p feed.Package, outputDir string, sources *zip.Writer) (packageManifest, error) {
	snapshot, err := feed.Download(ctx, client, p)
	if err != nil {
		return packageManifest{}, err
	}
	var encoded []byte
	if p.Kind == feed.IP {
		encoded, err = geosite.EncodeIPs(p.Tag, snapshot.Entries)
	} else {
		encoded, err = geosite.Encode(p.Tag, snapshot.Entries)
	}
	if err != nil {
		return packageManifest{}, fmt.Errorf("encode package: %w", err)
	}
	assetHash := sha256.Sum256(encoded)
	sourceHash := sha256.Sum256(snapshot.Raw)
	entry := packageManifest{
		Category:      p.Tag,
		Kind:          p.Kind,
		Policy:        p.Policy,
		Asset:         p.Asset(),
		AssetSHA256:   hex.EncodeToString(assetHash[:]),
		SourceFile:    p.SourceFile(),
		SourceURL:     p.SourceURL,
		SourceVersion: snapshot.Version,
		SourceSHA256:  hex.EncodeToString(sourceHash[:]),
		EntryCount:    len(snapshot.Entries),
	}

	if err := writeFile(outputDir, entry.Asset, encoded); err != nil {
		return packageManifest{}, err
	}
	member, err := sources.Create(entry.SourceFile)
	if err != nil {
		return packageManifest{}, err
	}
	if _, err := member.Write(snapshot.Raw); err != nil {
		return packageManifest{}, err
	}
	if p.Tag == feed.MediumTag {
		if err := writeFile(outputDir, "source-tif-medium.txt", snapshot.Raw); err != nil {
			return packageManifest{}, err
		}
		checksum := fmt.Sprintf("%s  %s\n", entry.AssetSHA256, entry.Asset)
		if err := writeFile(outputDir, entry.Asset+".sha256", []byte(checksum)); err != nil {
			return packageManifest{}, err
		}
	}
	return entry, nil
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

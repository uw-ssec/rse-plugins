# GAIA Data Downloader Plugin

This plugin provides tools for generating hydroclimatological data download scripts for the GAIA project.

## Components

### Agent: `data-downloader`

Invoke when the user needs to download data from GAIA sources (CONUS404, HRRR, WRF, PRISM, Stage IV, USGS, ORNL, DEM, Synoptic, IRIS). The agent uses a three-phase interaction:

1. **Parse** the user's request to identify source and parameters
2. **Propose** a configuration for scientist review (never silently assume required parameters)
3. **Generate** a Python script with CONFIG dict at top

### Skill: `download-script-dev`

Provides templates, reference documentation, and debugging guidance for developing download scripts. Use when:
- Developing a new download script manually
- Debugging an existing download script
- Looking up data source details, endpoints, or parameter schemas

The skill includes three reference files with detailed information:
- `references/DATA_SOURCES.md` — Per-source documentation
- `references/DOWNLOAD_PATTERNS.md` — Code templates and full pipeline examples
- `references/CONFIGURATION.md` — Parameter tables and validation rules

## Conventions

- All generated scripts use a CONFIG dict at the top for parameter transparency
- Scripts include `if __name__ == "__main__":` guard
- Scripts include `print()` statements for progress reporting
- No Python shebang line in generated scripts

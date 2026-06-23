# `tap-clinicaltrials`

Singer tap for [ClinicalTrials.gov](https://clinicaltrials.gov/data-about-studies/learn-about-api) study records data.

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

## Capabilities

- `catalog`
- `state`
- `discover`
- `activate-version`
- `about`
- `stream-maps`
- `schema-flattening`
- `batch`
- `structured-logging`

## Settings

| Setting | Required | Default | Description |
|:--------------------|:--------:|:-------:|:------------|
| start_date | False | None | Earliest datetime to get data from |
| condition | False | None | Conditions or disease query |
| sponsor | False | None | Sponsor query |
| stream_maps | False | None | Config object for stream maps capability. For more information check out [Stream Maps](https://sdk.meltano.com/en/latest/stream_maps.html). |
| stream_map_config | False | None | User-defined config values to be used within map expressions. |
| flattening_enabled | False | None | 'True' to enable schema flattening and automatically expand nested properties. |
| flattening_max_depth| False | None | The max depth to flatten schemas. |
| batch_config | False | None | |

A full list of supported settings and capabilities is available by running: `tap-clinicaltrials --about`

## Installation

### In a Meltano project

#### Using a direct reference

```bash
meltano add extractor tap-clinicaltrials --from-ref=https://raw.githubusercontent.com/edgarrmondragon/tap-clinicaltrials/main/plugin.yaml
```

Requires Meltano v3.1.0+.

#### From MeltanoHub

Not yet available.

### From PyPI

```bash
python3 -m pip install --upgrade tap-clinicaltrials
```

### With [pipx]

```bash
pipx install tap-clinicaltrials
```

### From source

```bash
git clone https://github.com/edgarrmondragon/tap-clinicaltrials
cd tap-clinicaltrials
python3 -m pip install .
```

## Usage

You can easily run `tap-clinicaltrials` by itself or in a pipeline using [Meltano](https://meltano.com/).

### With Meltano

1. Clone the repo and `cd` into it:

   ```bash
   git clone https://github.com/edgarrmondragon/tap-clinicaltrials.git
   cd tap-clinicaltrials
   ```

1. Make sure you have [Meltano](https://docs.meltano.com/guide/installation-guide) installed

1. Install all plugins

   ```bash
   meltano install
   ```

1. Configure the `tap-clinicaltrials` tap:

   ```bash
   meltano config tap-clinicaltrials set start_date '2020-01-01'
   meltano config tap-clinicaltrials set condition 'COVID-19'
   meltano config tap-clinicaltrials set sponsor 'Pfizer'
   ```

1. Run a test `tap-clinicaltrials` extraction

   ```bash
   meltano run tap-clinicaltrials target-duckdb
   ```

1. That's it! Check the data

   ```console
   $ duckdb output/warehouse.duckdb -c "select nctid, lastUpdateSubmitDate, protocolsection->>'$.identificationModule.briefTitle' from clinicaltrials.studies limit 5;
   ┌─────────────┬──────────────────────┬─────────────────────────────────────────────────────────────────────────────────────────────────────┐
   │    nctid    │ lastupdatesubmitdate │                      (protocolsection ->> '$.identificationModule.briefTitle')                      │
   │   varchar   │       varchar        │                                               varchar                                               │
   ├─────────────┼──────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────┤
   │ NCT06156215 │ 2023-12-06           │ PROmotion of COVID-19 BOOSTer VA(X)Ccination in the Emergency Department - PROBOOSTVAXED            │
   │ NCT05487040 │ 2023-12-06           │ A Study to Measure the Amount of Study Medicine in Blood in Adult Participants With COVID-19 and …  │
   │ NCT06163677 │ 2023-12-07           │ A Study to Look at the Health Outcomes of Patients With COVID-19 and Influenza.                     │
   │ NCT05032976 │ 2023-12-07           │ Korea Comirnaty Post-marketing Surveillance                                                         │
   │ NCT05596734 │ 2023-12-11           │ A Study to Evaluate the Safety, Tolerability, and Immunogenicity of Combined Modified RNA Vaccine…  │
   └─────────────┴──────────────────────┴─────────────────────────────────────────────────────────────────────────────────────────────────────┘
   ```

### Executing the Tap Directly

```bash
tap-clinicaltrials --version
tap-clinicaltrials --help
tap-clinicaltrials --config CONFIG --discover > ./catalog.json
```

## Developer Resources

### Initialize your Development Environment

```bash
pipx install hatch
```

### Create and Run Tests

Run integration tests:

```bash
hatch run test:integration
```

You can also test the `tap-clinicaltrials` CLI interface directly:

```bash
hatch run sync:console -- --about --format=json
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.

[pipx]: https://github.com/pypa/pipx

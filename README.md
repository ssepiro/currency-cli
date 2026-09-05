# 💱 Currency Comparison CLI

A lightweight, zero-dependency Python CLI tool to compare major world currencies with clean visual text bar graphs right in your terminal.

## 🚀 Features

- **Visual Text Bar Graphs**: High-resolution Unicode sub-block bars (`█`, `▉`, `▊`, ...) or ASCII bars (`=`).
- **Live & Offline Modes**: Fetches live rates automatically from public open exchange rate API with offline fallback.
- **Multiple Comparison Modes**:
  - `strength` (default): Compares relative purchasing power / currency worth in terms of the base currency.
  - `convert`: Shows total converted amount of the specified base sum.
- **Trading Unit Normalization (`-u`)**: Normalizes small currency denominations (e.g. 100 JPY, 1000 KRW, 10 CNY) so bars are directly comparable at a glance.
- **Customizable**: Choose base currency (`-b`), custom currency list (`-c`), custom amounts (`-a`), sort order (`-s`), and chart width (`-w`).
- **Script-Friendly**: Supports `--json`, `--ascii`, `--no-color`, and `--no-flags`.

---

## 💻 Quick Start

Run directly with Python 3:

```bash
# Compare major currencies against USD (default)
./currency_cli.py

# Compare with normalized market units (100 JPY, 1000 KRW, etc.)
./currency_cli.py -u

# Compare relative to EUR or GBP
./currency_cli.py -b EUR -u
./currency_cli.py -b GBP

# Convert $100 USD into other currencies
./currency_cli.py -m convert -a 100 -b USD

# Filter specific currencies
./currency_cli.py -b USD -c EUR,GBP,JPY,CAD,AUD,KRW,CNY -u
```

---

## ⚙️ Command-Line Options

| Option | Flag | Description | Default |
|---|---|---|---|
| `--base` | `-b` | Base currency code (e.g. `USD`, `EUR`, `JPY`, `KRW`, `GBP`) | `USD` |
| `--amount` | `-a` | Base currency amount (for conversion) | `1.0` |
| `--units` | `-u` | Normalize small unit currencies (100 JPY, 1000 KRW, 10 CNY) | `False` |
| `--currencies` | `-c` | Comma-separated list of target currency codes | Major G10 + Asian currencies |
| `--mode` | `-m` | Display mode: `strength` or `convert` | `strength` |
| `--width` | `-w` | Width of the text bar chart in characters | `32` |
| `--sort` | `-s` | Sort order: `desc`, `asc`, `name`, `none` | `desc` |
| `--ascii` | | Use plain ASCII characters (`=`) instead of Unicode blocks | `False` |
| `--no-color` | | Disable ANSI terminal colors | `False` |
| `--no-flags` | | Disable country flag emojis | `False` |
| `--offline` | | Use built-in offline snapshot without network call | `False` |
| `--json` | | Output raw JSON data for piping into scripts | `False` |

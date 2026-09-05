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


---

## 📋 Example Outputs

### 1. Default Comparison (Against USD)
```bash
./currency_cli.py
```
```text
══════════════════════════════════════════════════════════════════════════════════════════
 💱 MAJOR CURRENCIES COMPARISON  [Data: Live]
 Metric: Value of 1 Unit in USD (Relative Currency Strength)
══════════════════════════════════════════════════════════════════════════════════════════

      CODE       NAME                       Value in USD   VISUAL BAR COMPARISON
  ────────────────────────────────────────────────────────────────────────────────────────
  🇬🇧 GBP        British Pound                1.3521 USD  ████████████████████████████████
  🇨🇭 CHF        Swiss Franc                  1.2348 USD  █████████████████████████████▎  
  🇪🇺 EUR        Euro                         1.1613 USD  ███████████████████████████▌    
  🇺🇸 USD        US Dollar                    1.0000 USD  ███████████████████████▋         ◄ BASE
  🇸🇬 SGD        Singapore Dollar             0.7894 USD  ██████████████████▋             
  🇨🇦 CAD        Canadian Dollar              0.7231 USD  █████████████████▏              
  🇦🇺 AUD        Australian Dollar            0.7204 USD  █████████████████               
  🇳🇿 NZD        New Zealand Dollar           0.5881 USD  █████████████▉                  
  🇨🇳 CNY        Chinese Yuan                 0.1486 USD  ███▌                            
  🇭🇰 HKD        Hong Kong Dollar             0.1275 USD  ███                             
  🇯🇵 JPY        Japanese Yen               0.006404 USD  ▏                               
  🇰🇷 KRW        South Korean Won           0.000741 USD                                  
  ────────────────────────────────────────────────────────────────────────────────────────
  💡 Tip: Use '-u' for normalized units (100 JPY / 1000 KRW), '-b EUR' to switch base.
```

### 2. Normalized Market Units (`-u`)
Normalizes small currency denominations (100 JPY, 1000 KRW, 10 CNY, 10 HKD) for direct visual comparison:
```bash
./currency_cli.py -u
```
```text
══════════════════════════════════════════════════════════════════════════════════════════
 💱 MAJOR CURRENCIES COMPARISON  [Data: Live]
 Metric: Value of Standard Market Units in USD (Relative Currency Strength)
══════════════════════════════════════════════════════════════════════════════════════════

      CURRENCY   NAME                       Value in USD   VISUAL BAR COMPARISON
  ────────────────────────────────────────────────────────────────────────────────────────
  🇨🇳 10 CNY     Chinese Yuan                 1.4861 USD  ████████████████████████████████
  🇬🇧 GBP        British Pound                1.3521 USD  █████████████████████████████▏  
  🇭🇰 10 HKD     Hong Kong Dollar             1.2753 USD  ███████████████████████████▌    
  🇨🇭 CHF        Swiss Franc                  1.2348 USD  ██████████████████████████▋     
  🇪🇺 EUR        Euro                         1.1613 USD  █████████████████████████       
  🇺🇸 USD        US Dollar                    1.0000 USD  █████████████████████▌           ◄ BASE
  🇸🇬 SGD        Singapore Dollar             0.7894 USD  █████████████████               
  🇰🇷 1000 KRW   South Korean Won             0.7413 USD  ████████████████                
  🇨🇦 CAD        Canadian Dollar              0.7231 USD  ███████████████▋                
  🇦🇺 AUD        Australian Dollar            0.7204 USD  ███████████████▌                
  🇯🇵 100 JPY    Japanese Yen                 0.6404 USD  █████████████▊                  
  🇳🇿 NZD        New Zealand Dollar           0.5881 USD  ████████████▋                   
  ────────────────────────────────────────────────────────────────────────────────────────
  💡 Tip: Use '-u' for normalized units (100 JPY / 1000 KRW), '-b EUR' to switch base.
```

### 3. Currency Conversion Mode (`-m convert`)
Convert a specific amount into target currencies:
```bash
./currency_cli.py -m convert -a 100 -b USD
```
```text
══════════════════════════════════════════════════════════════════════════════════════════
 💱 MAJOR CURRENCIES COMPARISON  [Data: Live]
 Metric: Value of 100 USD in target currencies
══════════════════════════════════════════════════════════════════════════════════════════

      CODE       NAME                     Rate (100 USD)   VISUAL BAR COMPARISON
  ────────────────────────────────────────────────────────────────────────────────────────
  🇰🇷 KRW        South Korean Won           134,899.04 ₩  ████████████████████████████████
  🇯🇵 JPY        Japanese Yen                15,615.66 ¥  ███▊                            
  🇭🇰 HKD        Hong Kong Dollar             784.10 HK$  ▏                               
  🇨🇳 CNY        Chinese Yuan                   672.89 ¥  ▏                               
  🇳🇿 NZD        New Zealand Dollar           170.03 NZ$                                  
  🇦🇺 AUD        Australian Dollar             138.82 A$                                  
  🇨🇦 CAD        Canadian Dollar              138.29 CA$                                  
  🇸🇬 SGD        Singapore Dollar              126.68 S$                                  
  🇺🇸 USD        US Dollar                      100.00 $                                   ◄ BASE
  🇪🇺 EUR        Euro                            86.11 €                                  
  🇨🇭 CHF        Swiss Franc                    80.99 Fr                                  
  🇬🇧 GBP        British Pound                   73.96 £                                  
  ────────────────────────────────────────────────────────────────────────────────────────
  💡 Tip: Use '-u' for normalized units (100 JPY / 1000 KRW), '-b EUR' to switch base.
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

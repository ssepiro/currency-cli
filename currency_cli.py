#!/usr/bin/env python3
"""
Simple Currency Comparison CLI with Visual Text Bar Graphs.
Compares major currencies relative to a base currency with clean terminal bar graphs.
"""

import sys
import os
import json
import argparse
import urllib.request
import urllib.error
from datetime import datetime

# Fallback offline exchange rates (relative to USD)
DEFAULT_RATES_USD = {
    "USD": 1.0,
    "EUR": 0.86,
    "GBP": 0.74,
    "CHF": 0.81,
    "CAD": 1.36,
    "AUD": 1.48,
    "NZD": 1.65,
    "SGD": 1.32,
    "HKD": 7.82,
    "JPY": 154.2,
    "CNY": 7.18,
    "KRW": 1390.0,
    "INR": 86.4,
    "BRL": 5.75,
    "MXN": 19.8,
    "SEK": 10.2,
    "NOK": 10.4,
    "TRY": 34.5,
    "ZAR": 18.2,
    "AED": 3.67,
}

CURRENCY_INFO = {
    "USD": {"name": "US Dollar", "symbol": "$", "flag": "🇺🇸", "unit_mult": 1},
    "EUR": {"name": "Euro", "symbol": "€", "flag": "🇪🇺", "unit_mult": 1},
    "GBP": {"name": "British Pound", "symbol": "£", "flag": "🇬🇧", "unit_mult": 1},
    "CHF": {"name": "Swiss Franc", "symbol": "Fr", "flag": "🇨🇭", "unit_mult": 1},
    "CAD": {"name": "Canadian Dollar", "symbol": "CA$", "flag": "🇨🇦", "unit_mult": 1},
    "AUD": {"name": "Australian Dollar", "symbol": "A$", "flag": "🇦🇺", "unit_mult": 1},
    "NZD": {"name": "New Zealand Dollar", "symbol": "NZ$", "flag": "🇳🇿", "unit_mult": 1},
    "SGD": {"name": "Singapore Dollar", "symbol": "S$", "flag": "🇸🇬", "unit_mult": 1},
    "HKD": {"name": "Hong Kong Dollar", "symbol": "HK$", "flag": "🇭🇰", "unit_mult": 10},
    "JPY": {"name": "Japanese Yen", "symbol": "¥", "flag": "🇯🇵", "unit_mult": 100},
    "CNY": {"name": "Chinese Yuan", "symbol": "¥", "flag": "🇨🇳", "unit_mult": 10},
    "KRW": {"name": "South Korean Won", "symbol": "₩", "flag": "🇰🇷", "unit_mult": 1000},
    "INR": {"name": "Indian Rupee", "symbol": "₹", "flag": "🇮🇳", "unit_mult": 100},
    "BRL": {"name": "Brazilian Real", "symbol": "R$", "flag": "🇧🇷", "unit_mult": 1},
    "MXN": {"name": "Mexican Peso", "symbol": "Mex$", "flag": "🇲🇽", "unit_mult": 10},
    "SEK": {"name": "Swedish Krona", "symbol": "kr", "flag": "🇸🇪", "unit_mult": 10},
    "NOK": {"name": "Norwegian Krone", "symbol": "kr", "flag": "🇳🇴", "unit_mult": 10},
    "TRY": {"name": "Turkish Lira", "symbol": "₺", "flag": "🇹🇷", "unit_mult": 10},
    "ZAR": {"name": "South African Rand", "symbol": "R", "flag": "🇿🇦", "unit_mult": 10},
    "AED": {"name": "UAE Dirham", "symbol": "AED", "flag": "🇦🇪", "unit_mult": 1},
}

DEFAULT_MAJOR_CURRENCIES = [
    "GBP", "EUR", "CHF", "USD", "CAD", "AUD", "SGD", "NZD", "CNY", "HKD", "JPY", "KRW"
]

SUB_BLOCKS = ["", "▏", "▎", "▍", "▌", "▋", "▊", "▉", "█"]

# Terminal styling
class Style:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'

def disable_styles():
    Style.HEADER = ''
    Style.BLUE = ''
    Style.CYAN = ''
    Style.GREEN = ''
    Style.YELLOW = ''
    Style.RED = ''
    Style.BOLD = ''
    Style.DIM = ''
    Style.RESET = ''

def fetch_rates(base="USD", offline=False):
    """Fetch latest exchange rates with USD as reference from Open Exchange Rates API."""
    if offline:
        return DEFAULT_RATES_USD, "Offline Snapshot"

    url = f"https://open.er-api.com/v6/latest/{base}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "currency-cli/1.0"})
        with urllib.request.urlopen(req, timeout=4) as response:
            data = json.loads(response.read().decode())
            if data.get("result") == "success" and "rates" in data:
                time_str = data.get("time_last_update_utc", "")
                if time_str:
                    try:
                        dt = datetime.strptime(time_str[:25].strip(), "%a, %d %b %Y %H:%M:%S")
                        time_str = dt.strftime("%Y-%m-%d %H:%M UTC")
                    except Exception:
                        pass
                else:
                    time_str = datetime.now().strftime("%Y-%m-%d %H:%M")
                return data["rates"], f"Live ({time_str})"
    except Exception:
        pass

    # Convert default USD rates to requested base if needed
    if base != "USD" and base in DEFAULT_RATES_USD:
        usd_rate = DEFAULT_RATES_USD[base]
        converted = {c: r / usd_rate for c, r in DEFAULT_RATES_USD.items()}
        return converted, "Offline Snapshot (Fallback)"
    return DEFAULT_RATES_USD, "Offline Snapshot (Fallback)"

def render_bar(value, max_val, max_width=32, style_color=Style.CYAN, ascii_only=False):
    """Draw a smooth horizontal bar graph."""
    if max_val <= 0:
        return " " * max_width
    ratio = min(max(value / max_val, 0.0), 1.0)
    
    if ascii_only:
        length = int(round(ratio * max_width))
        bar = "=" * length
        remaining = max_width - length
        return f"{style_color}{bar}{Style.RESET}" + (" " * max(0, remaining))

    total_eighths = int(round(ratio * max_width * 8))
    full_blocks = total_eighths // 8
    sub_index = total_eighths % 8

    bar = "█" * full_blocks
    if full_blocks < max_width and sub_index > 0:
        bar += SUB_BLOCKS[sub_index]
        remaining = max_width - full_blocks - 1
    else:
        remaining = max_width - full_blocks

    bar_str = f"{style_color}{bar}{Style.RESET}" + (" " * max(0, remaining))
    return bar_str

def main():
    parser = argparse.ArgumentParser(
        description="A very simple, clean CLI to compare major currencies with visual text bar graphs.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  ./currency_cli.py                           # Compare major currencies against USD (default)
  ./currency_cli.py -u                        # Use trading units (e.g. 100 JPY, 1000 KRW) for balanced bars
  ./currency_cli.py -b EUR                    # Compare major currencies against EUR
  ./currency_cli.py -b USD -c EUR,GBP,JPY,CAD,KRW  # Compare specific currencies
  ./currency_cli.py -m convert -a 100 -b USD  # Compare converted total of $100 across currencies
  ./currency_cli.py --sort name               # Sort alphabetically by code
  ./currency_cli.py --json                    # Output structured JSON data
  ./currency_cli.py --ascii                   # Use simple ASCII '=' bars
        """
    )
    parser.add_argument("-b", "--base", default="USD", help="Base currency code (e.g. USD, EUR, GBP, JPY, KRW). Default: USD")
    parser.add_argument("-a", "--amount", type=float, default=1.0, help="Base currency amount (used for convert mode). Default: 1.0")
    parser.add_argument("-c", "--currencies", default=None, help="Comma-separated list of target currency codes to display")
    parser.add_argument("-m", "--mode", choices=["strength", "convert"], default="strength",
                        help="Display mode: 'strength' (value in Base), 'convert' (converted total of Amount Base). Default: strength")
    parser.add_argument("-u", "--units", action="store_true",
                        help="Scale nominal small currencies to standard market units (e.g. 100 JPY, 1000 KRW, 10 CNY) for balanced visual comparison")
    parser.add_argument("-w", "--width", type=int, default=32, help="Bar chart width in characters. Default: 32")
    parser.add_argument("-s", "--sort", choices=["desc", "asc", "name", "none"], default="desc",
                        help="Sort order: desc (highest value first), asc, name, none. Default: desc")
    parser.add_argument("--ascii", action="store_true", help="Use standard ASCII characters ('=') for bars")
    parser.add_argument("--no-color", action="store_true", help="Disable colored output")
    parser.add_argument("--no-flags", action="store_true", help="Disable flag emoji display")
    parser.add_argument("--offline", action="store_true", help="Use built-in offline rates snapshot without network request")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")

    args = parser.parse_args()

    if args.no_color or not sys.stdout.isatty():
        disable_styles()

    base_code = args.base.strip().upper()
    rates, source_info = fetch_rates(base="USD", offline=args.offline)

    if base_code not in rates and base_code not in DEFAULT_RATES_USD:
        print(f"{Style.RED}Error: Unknown base currency '{base_code}'.{Style.RESET}", file=sys.stderr)
        sys.exit(1)

    base_usd_rate = rates.get(base_code, DEFAULT_RATES_USD.get(base_code, 1.0))

    if args.currencies:
        target_codes = [c.strip().upper() for c in args.currencies.split(",") if c.strip()]
    else:
        target_codes = list(DEFAULT_MAJOR_CURRENCIES)
        if base_code not in target_codes:
            target_codes.append(base_code)

    items = []
    for code in target_codes:
        if code not in rates and code not in DEFAULT_RATES_USD:
            continue
        c_usd_rate = rates.get(code, DEFAULT_RATES_USD.get(code, 1.0))
        if c_usd_rate <= 0:
            continue

        units_per_base = c_usd_rate / base_usd_rate
        base_per_unit = 1.0 / units_per_base if units_per_base != 0 else 0

        info = CURRENCY_INFO.get(code, {"name": code, "symbol": code, "flag": "🌐", "unit_mult": 1})
        mult = info.get("unit_mult", 1) if args.units else 1
        
        display_label = f"{mult} {code}" if mult > 1 else code
        scaled_base_val = base_per_unit * mult

        items.append({
            "code": code,
            "label": display_label,
            "name": info["name"],
            "symbol": info["symbol"],
            "flag": info["flag"] if not args.no_flags else "",
            "multiplier": mult,
            "units_per_base": units_per_base,
            "base_per_unit": base_per_unit,
            "scaled_base_val": scaled_base_val,
            "converted_val": args.amount * units_per_base,
        })

    if not items:
        print(f"{Style.RED}Error: No valid currency codes found.{Style.RESET}", file=sys.stderr)
        sys.exit(1)

    # Determine metric to compare
    for item in items:
        if args.mode == "strength":
            item["comp_val"] = item["scaled_base_val"] if args.units else item["base_per_unit"]
        elif args.mode == "convert":
            item["comp_val"] = item["converted_val"]

    # Sort
    if args.sort == "desc":
        items.sort(key=lambda x: x["comp_val"], reverse=True)
    elif args.sort == "asc":
        items.sort(key=lambda x: x["comp_val"])
    elif args.sort == "name":
        items.sort(key=lambda x: x["code"])

    if args.json:
        out = {
            "base": base_code,
            "mode": args.mode,
            "amount": args.amount,
            "source": source_info,
            "currencies": items
        }
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return

    max_comp_val = max((it["comp_val"] for it in items), default=1.0)

    # Print Header
    print()
    print(f"{Style.BOLD}{Style.CYAN}══════════════════════════════════════════════════════════════════════════════════════════{Style.RESET}")
    print(f" {Style.BOLD}💱 MAJOR CURRENCIES COMPARISON{Style.RESET}  {Style.DIM}[Data: {source_info}]{Style.RESET}")
    if args.mode == "strength":
        unit_text = "Standard Market Units" if args.units else "1 Unit"
        print(f" {Style.YELLOW}Metric:{Style.RESET} Value of {Style.BOLD}{unit_text}{Style.RESET} in {Style.BOLD}{base_code}{Style.RESET} (Relative Currency Strength)")
    elif args.mode == "convert":
        print(f" {Style.YELLOW}Metric:{Style.RESET} Value of {Style.BOLD}{args.amount:g} {base_code}{Style.RESET} in target currencies")
    print(f"{Style.BOLD}{Style.CYAN}══════════════════════════════════════════════════════════════════════════════════════════{Style.RESET}")
    print()

    # Column header
    flag_header = "    " if not args.no_flags else ""
    code_hdr = "CURRENCY" if args.units else "CODE"
    if args.mode == "strength":
        val_header = f"Value in {base_code}"
    else:
        val_header = f"Rate ({args.amount:g} {base_code})"

    print(f"  {Style.DIM}{flag_header}{code_hdr:<10} {'NAME':<20} {val_header:>18}   VISUAL BAR COMPARISON{Style.RESET}")
    print(f"  {Style.DIM}{'─'*88}{Style.RESET}")

    # Render rows
    for it in items:
        is_base = (it["code"] == base_code)
        
        # Formatting elements
        lbl = it["label"] if args.units else it["code"]
        code_str = f"{Style.BOLD}{lbl:<10}{Style.RESET}" if is_base else f"{lbl:<10}"
        flag_str = f"{it['flag']} " if not args.no_flags else ""
        name_str = f"{it['name'][:20]:<20}"

        # Choose bar color
        if is_base:
            bar_color = Style.GREEN
            tag = f"{Style.GREEN}◄ BASE{Style.RESET}"
        elif it["comp_val"] >= 1.0 and args.mode == "strength":
            bar_color = Style.CYAN
            tag = ""
        else:
            bar_color = Style.BLUE
            tag = ""

        # Value display
        if args.mode == "strength":
            val = it["scaled_base_val"] if args.units else it["base_per_unit"]
            if val >= 1000000:
                num_str = f"{val:12,.1f} {base_code}"
            elif val >= 1000:
                num_str = f"{val:12,.2f} {base_code}"
            elif val >= 1:
                num_str = f"{val:12.4f} {base_code}"
            elif val >= 0.01:
                num_str = f"{val:12.4f} {base_code}"
            else:
                num_str = f"{val:12.6f} {base_code}"
            bar = render_bar(val, max_comp_val, max_width=args.width, style_color=bar_color, ascii_only=args.ascii)
        elif args.mode == "convert":
            if it["converted_val"] >= 1000000:
                num_str = f"{it['converted_val']:13,.1f} {it['symbol']}"
            elif it["converted_val"] >= 1000:
                num_str = f"{it['converted_val']:13,.2f} {it['symbol']}"
            elif it["converted_val"] >= 1:
                num_str = f"{it['converted_val']:13.2f} {it['symbol']}"
            else:
                num_str = f"{it['converted_val']:13.4f} {it['symbol']}"
            bar = render_bar(it["converted_val"], max_comp_val, max_width=args.width, style_color=bar_color, ascii_only=args.ascii)

        base_indicator = f" {tag}" if tag else ""
        print(f"  {flag_str}{code_str} {name_str} {num_str:>18}  {bar}{base_indicator}")

    print(f"  {Style.DIM}{'─'*88}{Style.RESET}")
    print(f"  {Style.DIM}💡 Tip: Use '-u' for normalized units (100 JPY / 1000 KRW), '-b EUR' to switch base.{Style.RESET}")
    print()

if __name__ == "__main__":
    main()

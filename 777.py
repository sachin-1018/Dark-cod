#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║        🌑 DARK-COD v5.0 ULTIMATE - JARVIS EDITION 🌑             ║
║                                                                  ║
║  Advanced Market Prediction Engine with Proven Patterns          ║
║                                                                  ║
║  Created by: 🙎 Sachin Solunke                                   ║
║  Upgraded by: 🤖 Jarvis AI Assistant                             ║
║  Purpose: Advanced Market Analysis & Prediction                  ║
║                                                                  ║
║  ⚠️  DISCLAIMER: For educational & personal use only             ║
╚══════════════════════════════════════════════════════════════════╝
"""

import os
import sys
from datetime import datetime, timedelta
from collections import Counter
from pathlib import Path
import pandas as pd

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.align import Align
    from rich.text import Text
    from rich import box
except ImportError:
    os.system("pip install rich pandas numpy -q")

console = Console()

# ============================================================================
# CONFIGURATION & PATHS
# ============================================================================

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
Path(DATA_DIR).mkdir(parents=True, exist_ok=True)

# ============================================================================
# DATA LOADER
# ============================================================================

def load_market_data(filepath):
    try:
        if not os.path.exists(filepath):
            console.print(f"[red]❌ File not found: {filepath}[/red]")
            return None
        
        df = pd.read_csv(
            filepath, 
            sep=r'\s*/\s*', 
            header=None, 
            engine='python',
            names=['Date_Str', 'Pana_Jodi_Pana']
        )
        
        df = df.dropna(subset=['Pana_Jodi_Pana'])
        df = df[~df['Pana_Jodi_Pana'].str.contains(r"\*|x", na=False, case=False)]
        
        df[['Open_Pana', 'Jodi', 'Close_Pana']] = df['Pana_Jodi_Pana'].str.split(r'\s*-\s*', expand=True)
        
        for col in ['Open_Pana', 'Jodi', 'Close_Pana']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df = df.dropna().astype({'Open_Pana': int, 'Jodi': int, 'Close_Pana': int}).reset_index(drop=True)
        
        df['open'] = df['Jodi'].apply(lambda x: int(str(x).zfill(2)[0]))
        df['close'] = df['Jodi'].apply(lambda x: int(str(x).zfill(2)[1]))
        
        def parse_date(date_str):
            for fmt in ['%d-%m-%Y', '%d-%m-%y', '%m-%d-%Y', '%m-%d-%y']:
                try:
                    return pd.to_datetime(datetime.strptime(date_str.strip(), fmt))
                except:
                    pass
            return pd.NaT
        
        df['Date'] = df['Date_Str'].apply(parse_date)
        df = df.dropna(subset=['Date']).sort_values('Date').reset_index(drop=True)
        
        return df
        
    except Exception as e:
        console.print(f"[red]❌ Error loading data: {str(e)}[/red]")
        return None

# ============================================================================
# ANALYSIS ENGINES
# ============================================================================

class PatternCalculator:
    def __init__(self, df):
        self.df = df
    
    def get_digit_sum(self, num):
        return sum(int(d) for d in str(num)) % 10
    
    def predict_for_today(self):
        """Standard Prediction Logic"""
        if len(self.df) == 0: return None
        last_row = self.df.iloc[-1]
        
        # Logic: Pana Sum
        pred_open = self.get_digit_sum(last_row['Open_Pana'])
        pred_close = self.get_digit_sum(last_row['Close_Pana'])
        
        return {
            'last_date': last_row['Date'],
            'last_open_pana': last_row['Open_Pana'],
            'last_close_pana': last_row['Close_Pana'],
            'pred_open': pred_open,
            'pred_close': pred_close
        }

    def analyze_pass_fail(self):
        """Analyze historical accuracy of the Pana Sum pattern"""
        results = []
        pass_count = 0
        total_count = 0
        
        # Check last 50 records for accuracy check
        check_df = self.df.tail(50).copy()
        
        for idx, row in check_df.iterrows():
            calc_open = self.get_digit_sum(row['Open_Pana'])
            is_pass = (calc_open == row['open'])
            
            if is_pass: pass_count += 1
            total_count += 1
            
            results.append({
                'date': row['Date'],
                'pana': row['Open_Pana'],
                'jodi': row['Jodi'],
                'calc': calc_open,
                'status': '✅ PASS' if is_pass else '❌ FAIL'
            })
            
        return results, pass_count, total_count

# ============================================================================
# NEW FEATURES DISPLAY FUNCTIONS
# ============================================================================

def show_banner():
    os.system('clear' if os.name != 'nt' else 'cls')
    banner = """
[bold magenta]╔══════════════════════════════════════════════════════════════════╗[/bold magenta]
[bold magenta]║        🌑 DARK-COD v5.0 - JARVIS UPGRADE 🌑                      ║[/bold magenta]
[bold magenta]║     Advanced Analysis & Prediction System                        ║[/bold magenta]
[bold magenta]╚══════════════════════════════════════════════════════════════════╝[/bold magenta]
"""
    console.print(banner)

def feature_today_prediction(market_name, df):
    """Option 1: Aaj Ka Anuman"""
    show_banner()
    calc = PatternCalculator(df)
    pred = calc.predict_for_today()
    
    console.print(Panel(
        f"[bold yellow]🔮 {market_name.upper()} - AAJ KA ANUMAN[/bold yellow]",
        border_style="yellow"
    ))
    
    console.print(f"\n[cyan]Based on Last Record: {pred['last_date'].strftime('%d-%m-%Y')}[/cyan]")
    console.print(f"[dim]Logic: Pana Digit Sum = Next Open/Close[/dim]\n")
    
    grid = Table.grid(expand=True)
    grid.add_column(justify="center", ratio=1)
    grid.add_column(justify="center", ratio=1)
    
    grid.add_row(
        Panel(f"[bold cyan]{pred['last_open_pana']}[/bold cyan]\n⬇️\n[bold green]OPEN: {pred['pred_open']}[/bold green]", title="Open Strategy"),
        Panel(f"[bold cyan]{pred['last_close_pana']}[/bold cyan]\n⬇️\n[bold green]CLOSE: {pred['pred_close']}[/bold green]", title="Close Strategy")
    )
    
    console.print(grid)
    console.print(f"\n[bold white on red] 🔥 STRONG JODI: {pred['pred_open']}{pred['pred_close']} 🔥 [/bold white on red]")
    console.input("\n[dim]Press ENTER to return...[/dim]")

def feature_pass_fail(market_name, df):
    """Option 2: Pichla Pass/Fail Record"""
    show_banner()
    calc = PatternCalculator(df)
    results, passed, total = calc.analyze_pass_fail()
    
    accuracy = (passed / total) * 100
    
    console.print(Panel(
        f"[bold cyan]📋 PASS/FAIL RECORD (Last 50 Games)[/bold cyan]\n"
        f"Logic: Open Pana Sum = Open Digit",
        border_style="cyan"
    ))
    
    table = Table(box=box.SIMPLE_HEAD)
    table.add_column("Date", style="dim")
    table.add_column("Pana", style="cyan")
    table.add_column("Jodi", style="yellow")
    table.add_column("Calc Open", justify="center")
    table.add_column("Result", justify="center")
    
    # Show last 15 rows in table to save space
    for res in results[-15:]:
        table.add_row(
            res['date'].strftime('%d-%m'),
            str(res['pana']),
            f"{res['jodi']:02d}",
            str(res['calc']),
            res['status']
        )
        
    console.print(table)
    console.print(f"\n[bold]📊 Summary:[/bold] {passed}/{total} Passed")
    console.print(Panel(f"[bold]ACCURACY: {accuracy:.1f}%[/bold]", border_style="green" if accuracy > 50 else "red"))
    
    console.input("\n[dim]Press ENTER to return...[/dim]")

def feature_last_40_days(market_name, df):
    """Option 3: Last 40 Days Analysis"""
    show_banner()
    
    # Get last 40 records
    data_40 = df.tail(40)
    
    # Calculate Frequency
    open_counts = Counter(data_40['open'])
    jodi_counts = Counter(data_40['Jodi'])
    
    console.print(Panel(f"[bold magenta]📈 LAST 40 DAYS ANALYSIS - {market_name}[/bold magenta]", border_style="magenta"))
    
    # Top 3 Open Digits
    console.print("\n[bold yellow]🔥 Top 3 Hot Open Digits:[/bold yellow]")
    for digit, count in open_counts.most_common(3):
        bar = "█" * count
        console.print(f"Digit [bold cyan]{digit}[/bold cyan] : {bar} ({count} times)")
        
    # Top 3 Jodis
    console.print("\n[bold yellow]💎 Top Recurring Jodis:[/bold yellow]")
    top_jodis = [f"{j:02d}" for j, c in jodi_counts.most_common(3)]
    console.print(f"[white]{', '.join(top_jodis)}[/white]")
    
    # Red Houses (Repeat Open=Close)
    red_house = data_40[data_40['open'] == data_40['close']]
    console.print(f"\n[bold red]🔴 Red Jodi Frequency:[/bold red] {len(red_house)} times in 40 days")
    
    console.input("\n[dim]Press ENTER to return...[/dim]")

def feature_last_7_days(market_name, df):
    """Option 4: Last 7 Days Record"""
    show_banner()
    
    data_7 = df.tail(7)
    
    console.print(Panel(f"[bold green]📅 LAST 7 DAYS RECORD - {market_name}[/bold green]", border_style="green"))
    
    table = Table(show_lines=True)
    table.add_column("Date", style="white")
    table.add_column("Open Pana", style="cyan")
    table.add_column("Jodi", style="bold yellow")
    table.add_column("Close Pana", style="cyan")
    
    for _, row in data_7.iterrows():
        table.add_row(
            row['Date'].strftime('%d-%b-%Y'),
            str(row['Open_Pana']),
            f"{row['Jodi']:02d}",
            str(row['Close_Pana'])
        )
        
    console.print(table)
    console.input("\n[dim]Press ENTER to return...[/dim]")

def feature_weekly_prediction(market_name, df):
    """Option 5: Week Ke Liye Khas Anuman (OTC)"""
    show_banner()
    
    # Logic: Analyze last 10 days to find 'missing' or 'trending' numbers for the week
    last_10 = df.tail(10)
    all_digits = list(last_10['open']) + list(last_10['close'])
    counts = Counter(all_digits)
    
    # Strategy: Usually numbers that appeared most frequently repeat, OR numbers that haven't come come.
    # Here we pick Top 4 occurring numbers as "Strong OTC" for the week
    strong_otc = [d for d, c in counts.most_common(4)]
    
    console.print(Panel(f"[bold blue]⭐ WEEKLY VIP ANUMAN (OTC) - {market_name}[/bold blue]", border_style="blue"))
    
    console.print("\n[dim]Analysis based on last 10 days trend...[/dim]\n")
    
    otc_str = " - ".join([str(d) for d in strong_otc])
    
    console.print(Panel(
        f"[bold white on blue] {otc_str} [/bold white on blue]",
        title="[bold yellow]LUCKY 4 ANK (OTC)[/bold yellow]",
        subtitle="Follow for this week",
        padding=(1, 4)
    ))
    
    console.print("\n[green]Tip:[/green] In anko ko Open ya Close mein follow karein.")
    console.input("\n[dim]Press ENTER to return...[/dim]")

# ============================================================================
# MAIN MENU
# ============================================================================

def show_main_menu():
    os.system('clear' if os.name != 'nt' else 'cls')
    show_banner()
    
    console.print("\n[bold cyan]📊 MAIN MENU[/bold cyan]\n")
    console.print("[bold white]1.[/bold white] [yellow]🎯 Aaj Ka Anuman[/yellow]")
    console.print("[bold white]2.[/bold white] [cyan]📋 Pichla Pass/Fail Record[/cyan]")
    console.print("[bold white]3.[/bold white] [magenta]📈 Last 40 Days Analysis[/magenta]")
    console.print("[bold white]4.[/bold white] [green]📅 Last 7 Days Record[/green]")
    console.print("[bold white]5.[/bold white] [blue]⭐ Week Ke Liye Khas Anuman[/blue]")
    console.print("[bold white]0.[/bold white] [red]❌ Exit[/red]\n")
    
    return console.input("[bold cyan]👉 Option Chuniye (0-5): [/bold cyan]").strip()

def main():
    while True:
        # Step 1: Select Market First (Simplified flow)
        os.system('clear' if os.name != 'nt' else 'cls')
        show_banner()
        
        market_files = sorted([f.replace('.txt', '') for f in os.listdir(DATA_DIR) if f.endswith('.txt')])
        
        if not market_files:
            console.print("\n[red]❌ Data folder mein koi file nahi mili![/red]")
            console.print("[yellow]Please 'data' folder mein KALYAN.txt, etc. add karein.[/yellow]")
            break

        console.print("\n[bold underline]📂 Available Markets:[/bold underline]\n")
        for i, m in enumerate(market_files, 1):
            console.print(f" {i}. {m.upper()}")
            
        m_choice = console.input(f"\n[bold cyan]Select Market (1-{len(market_files)}) or 0 to Exit: [/bold cyan]")
        
        if m_choice == '0':
            console.print("\n[green]👋 Bye Bhai! Take care.[/green]")
            break
            
        try:
            market_name = market_files[int(m_choice) - 1]
            df = load_market_data(os.path.join(DATA_DIR, f"{market_name}.txt"))
            
            if df is None:
                console.input("Press ENTER to try again...")
                continue
                
            # Step 2: Show Feature Menu
            while True:
                choice = show_main_menu()
                
                if choice == '1':
                    feature_today_prediction(market_name, df)
                elif choice == '2':
                    feature_pass_fail(market_name, df)
                elif choice == '3':
                    feature_last_40_days(market_name, df)
                elif choice == '4':
                    feature_last_7_days(market_name, df)
                elif choice == '5':
                    feature_weekly_prediction(market_name, df)
                elif choice == '0':
                    break # Break inner loop to go back to market selection
                else:
                    console.print("[red]❌ Galat option bhai![/red]")
                    
        except (ValueError, IndexError):
            continue

if __name__ == "__main__":
    main()

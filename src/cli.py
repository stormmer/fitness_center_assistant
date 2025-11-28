"""Command-line interface for Fitness Center Assistant."""

import sys
from typing import Dict

from src.data import plans, class_schedule, promo_codes
from src.logic.messaging import build_welcome, reminders
from src.logic.pricing import price_membership
from src.logic.attendance import add_entry, summarize
from src.logic.export import export_text


def format_currency(amount: float) -> str:
    """Format a float as currency string."""
    return f"${amount:,.2f}"


def print_pricing_breakdown(breakdown: Dict) -> None:
    """Print formatted pricing breakdown."""
    print("\n" + "="*50)
    print("MEMBERSHIP PRICING BREAKDOWN")
    print("="*50)
    print(f"Plan: {breakdown['plan']}")
    print(f"Duration: {breakdown['months']} month(s)")
    print(f"Monthly Price: {format_currency(breakdown['monthly_price'])}")
    print(f"Base Cost: {format_currency(breakdown['base_cost'])}")
    
    if breakdown['student_staff_discount'] > 0:
        print(f"Student/Staff Discount (15%): -{format_currency(breakdown['student_staff_discount'])}")
    
    if breakdown['promo_applied']:
        print(f"Promo Code ({breakdown['promo_applied']}): -{format_currency(breakdown['base_cost'] * breakdown['promo_rate'])}")
    elif breakdown.get('promo_attempted'):
        print("⚠️  Invalid promo code - not applied")
    
    print("-"*50)
    print(f"FINAL COST: {format_currency(breakdown['final_cost'])}")
    print("="*50 + "\n")


def main() -> None:
    """Main CLI application flow."""
    print("="*60)
    print("🏋️  FITNESS CENTER MEMBERSHIP ASSISTANT")
    print("="*60)
    print()
    
    # 1. Personalized greeting
    name = input("Enter your name: ").strip()
    if not name:
        name = "Guest"
    
    center = "Baun Fitness Center"
    welcome_msg = build_welcome(name, center)
    print(f"\n{welcome_msg}\n")
    
    # 2. Class reminders
    print("-"*60)
    day_input = input("Enter a day of the week for class reminders: ").strip()
    if day_input:
        day_classes = reminders(day_input, class_schedule)
        if day_classes:
            print(f"\n📅 Classes on {day_input.title()}:")
            for cls in day_classes:
                print(f"  • {cls}")
        else:
            print(f"\n📅 No classes scheduled for {day_input.title()}")
    print()
    
    # 3. Pricing calculator
    print("-"*60)
    print("MEMBERSHIP PRICING CALCULATOR")
    print("-"*60)
    
    # Plan selection
    print(f"\nAvailable plans: {', '.join(plans.keys())}")
    plan = input("Select a plan: ").strip()
    if plan not in plans:
        print(f"⚠️  Invalid plan. Using 'Basic' as default.")
        plan = "Basic"
    
    # Months
    try:
        months = int(input("Enter number of months: ").strip())
        if months <= 0:
            print("⚠️  Invalid months. Using 1 as default.")
            months = 1
    except ValueError:
        print("⚠️  Invalid input. Using 1 month as default.")
        months = 1
    
    # Student/staff
    student_staff_input = input("Are you a student or staff member? (Y/N): ").strip().upper()
    is_student_or_staff = student_staff_input in ['Y', 'YES']
    
    # Promo code
    promo = input("Enter promo code (optional, press Enter to skip): ").strip()
    promo = promo if promo else None
    
    breakdown = {}
    try:
        breakdown = price_membership(
            plan=plan,
            months=months,
            is_student_or_staff=is_student_or_staff,
            promo=promo,
            plans=plans,
            promo_codes=promo_codes
        )
        
        if promo and not breakdown['promo_applied']:
            breakdown['promo_attempted'] = True
        
        print_pricing_breakdown(breakdown)
    except ValueError as e:
        print(f"❌ Error: {e}\n")
    
    # 4. Attendance tracking
    print("-"*60)
    print("ATTENDANCE TRACKING")
    print("-"*60)
    print("Enter activity names and attendance counts.")
    print("Type 'done' when finished.\n")
    
    attendance_store: Dict[str, int] = {}
    
    while True:
        activity = input("Activity name (or 'done' to finish): ").strip()
        if activity.lower() == 'done':
            break
        
        if not activity:
            print("⚠️  Activity name cannot be empty. Skipping.")
            continue
        
        try:
            count = int(input(f"  Attendance count for '{activity}': ").strip())
            if count < 0:
                print("⚠️  Count must be non-negative. Skipping.")
                continue
            
            add_entry(attendance_store, activity, count)
            print(f"  ✓ Added {count} to {activity}\n")
        except ValueError:
            print("⚠️  Invalid count. Must be an integer. Skipping.\n")
    
    # Print attendance summary
    if attendance_store:
        summary = summarize(attendance_store)
        print("\n" + "="*50)
        print("ATTENDANCE SUMMARY")
        print("="*50)
        print(f"Total Attendance: {summary['total']}")
        print(f"Average per Activity: {summary['avg_per_activity']:.2f}")
        print("\nBy Activity:")
        for activity, count in summary['by_activity'].items():
            print(f"  • {activity}: {count}")
        print("="*50 + "\n")
    else:
        print("\nNo attendance data recorded.\n")
    
    # 5. Export summary
    print("-"*60)
    export_choice = input("Export session summary to file? (Y/N): ").strip().upper()
    
    if export_choice in ['Y', 'YES']:
        lines = [
            "="*60,
            "FITNESS CENTER SESSION SUMMARY",
            "="*60,
            f"Name: {name}",
            f"Center: {center}",
            "",
            "PRICING BREAKDOWN:",
            f"  Plan: {breakdown.get('plan', 'N/A')}",
            f"  Months: {breakdown.get('months', 'N/A')}",
            f"  Final Cost: {format_currency(breakdown.get('final_cost', 0.0))}",
            "",
            "ATTENDANCE SUMMARY:",
        ]
        
        if attendance_store:
            summary = summarize(attendance_store)
            lines.append(f"  Total Attendance: {summary['total']}")
            lines.append(f"  Average per Activity: {summary['avg_per_activity']:.2f}")
            lines.append("  By Activity:")
            for activity, count in summary['by_activity'].items():
                lines.append(f"    • {activity}: {count}")
        else:
            lines.append("  No attendance data recorded.")
        
        lines.append("")
        lines.append("="*60)
        
        export_path = "fitness_session_summary.txt"
        try:
            export_text(export_path, lines)
            print(f"\n✓ Summary exported to: {export_path}\n")
        except Exception as e:
            print(f"\n❌ Error exporting file: {e}\n")
    
    print("="*60)
    print("Thank you for using Fitness Center Assistant! 👋")
    print("="*60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


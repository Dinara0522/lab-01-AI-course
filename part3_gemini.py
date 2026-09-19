import argparse
import json
from pathlib import Path


MEASUREMENTS_FILE = Path("measurements.json")

INPUT_PRICE_PER_MTOK = 0.75
OUTPUT_PRICE_PER_MTOK = 3.75

LANGUAGES = ("en", "ru", "kk")


def load_measurements():
    with open(MEASUREMENTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def gemini_cost_usd(input_tokens, output_tokens):
    return (
        input_tokens * INPUT_PRICE_PER_MTOK
        + output_tokens * OUTPUT_PRICE_PER_MTOK
    ) / 1_000_000


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--requests-per-day",
        type=int,
        default=5000
    )
    args = parser.parse_args()

    data = load_measurements()

    billed = data["one_request_billed"]

    inputs = {
        lang: billed[lang]["input_tokens"]
        for lang in LANGUAGES
    }

    outputs = {
        lang: billed[lang]["output_tokens"] + billed[lang]["thoughts_tokens"]
        for lang in LANGUAGES
    }

    costs = {
        lang: gemini_cost_usd(inputs[lang], outputs[lang])
        for lang in LANGUAGES
    }

    requests_per_year = args.requests_per_day * 365

    yearly = {
        lang: costs[lang] * requests_per_year
        for lang in LANGUAGES
    }

    print("=" * 72)
    print("GEMINI 3.6 FLASH — COST CALCULATION")
    print("=" * 72)

    print(f"Provider: Google Gemini API")
    print(f"Model: {data['model_id']}")
    print(f"Input price: ${INPUT_PRICE_PER_MTOK:.2f} per 1M tokens")
    print(f"Output price: ${OUTPUT_PRICE_PER_MTOK:.2f} per 1M tokens")
    print(f"Requests per day: {args.requests_per_day:,}")
    print(f"Requests per year: {requests_per_year:,}")

    print("\nONE SUPPORT REQUEST")
    print("-" * 72)

    print(
        f"{'':<18}"
        f"{'EN':>12}"
        f"{'RU':>12}"
        f"{'KK':>12}"
    )

    print(
        f"{'Input tokens':<18}"
        f"{inputs['en']:>12}"
        f"{inputs['ru']:>12}"
        f"{inputs['kk']:>12}"
    )

    print(
        f"{'Output tokens':<18}"
        f"{outputs['en']:>12}"
        f"{outputs['ru']:>12}"
        f"{outputs['kk']:>12}"
    )

    print(
        f"{'Cost, USD':<18}"
        f"{costs['en']:>12.6f}"
        f"{costs['ru']:>12.6f}"
        f"{costs['kk']:>12.6f}"
    )

    print("\nANNUAL COST")
    print("-" * 72)

    print(
        f"{'':<18}"
        f"{'EN':>12}"
        f"{'RU':>12}"
        f"{'KK':>12}"
    )

    print(
        f"{'USD/year':<18}"
        f"{yearly['en']:>12,.2f}"
        f"{yearly['ru']:>12,.2f}"
        f"{yearly['kk']:>12,.2f}"
    )

    print("\nTOKEN RATIOS")
    print("-" * 72)

    print(
        f"RU / EN input tokens: "
        f"{inputs['ru'] / inputs['en']:.2f}x"
    )

    print(
        f"KK / EN input tokens: "
        f"{inputs['kk'] / inputs['en']:.2f}x"
    )

    print("\nTOTAL COST RATIOS")
    print("-" * 72)

    print(
        f"RU / EN cost: "
        f"{costs['ru'] / costs['en']:.2f}x"
    )

    print(
        f"KK / EN cost: "
        f"{costs['kk'] / costs['en']:.2f}x"
    )

    print("\nADDITIONAL ANNUAL COST VS ENGLISH")
    print("-" * 72)

    print(
        f"Russian instead of English: "
        f"${yearly['ru'] - yearly['en']:,.2f}/year more"
    )

    print(
        f"Kazakh instead of English: "
        f"${yearly['kk'] - yearly['en']:,.2f}/year more"
    )

    print("\nNOTE")
    print("-" * 72)
    print(
        "The annual figures above use published Paid Tier list prices."
    )
    print(
        "The API key used in this experiment is on the Free Tier, "
        "so these figures are a hypothetical list-price calculation, "
        "not necessarily the amount actually charged to the account."
    )


if __name__ == "__main__":
    main()
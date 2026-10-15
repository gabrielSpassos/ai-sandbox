# Jev Support Ticket Classification POC

A small, isolated example that sends a support ticket to TypeSafe's Jev API, receives a typed category decision, and routes low-confidence results to manual review.

## Requirements

- Python 3.10 or newer
- A Jev Model API key

The script uses only the Python standard library; no package installation is needed.

## Setup

Sign in to the [TypeSafe Console](https://console.typesafe.ai/login) and create or copy an API key for your account. Use a TypeSafe API key; keys from other Jev-branded services will not authenticate with this API.

From this directory, copy `.env.example` to `.env` and add your API key:

```sh
cp .env.example .env
```

Edit `.env`:

```text
JEV_API_KEY=your_api_key
```

The `.env` file is ignored by Git.

## Classify one ticket

```sh
python3 main.py "I was charged twice for my annual subscription."
```

The result includes the selected category, probabilities, confidence, and a route. Results below the default confidence threshold of `0.65` go to `manual_review`.

## Run the sample set

```sh
python3 main.py --examples examples.json
```

This sends each labeled example separately and prints exact-match accuracy. The sample set is intentionally tiny; add representative, anonymized tickets before drawing conclusions.

Change the routing threshold with `--threshold`:

```sh
python3 main.py --threshold 0.75 "I cannot sign in to my account."
```

## Scope

This POC asks one `choice` question with four fixed categories: `billing`, `technical`, `account`, and `other`. It does not update a ticketing system or take actions on behalf of a user. The application owns the confidence threshold and sends uncertain or unknown categories to manual review.

The API key is sent from this local script to `https://api.typesafe.ai/v1/systemone`. Do not use real customer data until your team's privacy and data-handling requirements have been reviewed.

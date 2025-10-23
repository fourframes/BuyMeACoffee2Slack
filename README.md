# Buy Me a Coffee to Slack Notifier Cloudflare Worker

This Cloudflare Worker listens for donation webhook events from Buy Me a Coffee and sends a notification message to a Slack channel via Slack Incoming Webhooks.

## Features

- Receives **order.created** events from Buy Me a Coffee webhooks
- Parses donor name, donation amount, and message from the webhook payload
- Sends a formatted notification message to Slack using a Slack webhook URL
- Simple and async implementation following Cloudflare Workers best practices

## Setup

### Prerequisites

- A Cloudflare account with Workers enabled
- Buy Me a Coffee account with webhook URL configured to this Worker
- Slack workspace with an Incoming Webhook URL created for your desired channel

### Environment Variables

Set the following secrets in your Cloudflare Worker environment:

- `SECRET_SLACK_WEBHOOK_URL` — The Slack Incoming Webhook URL

You can set secrets via the Cloudflare CLI or dashboard, for example:

`wrangler secret put SECRET_SLACK_WEBHOOK_URL`


### Deploy

Use the Cloudflare Wrangler CLI or UI to deploy the Worker.

Example CLI deploy:

`wrangler publish`

## Usage

Configure your Buy Me a Coffee account webhook to send events to your Worker URL. The Worker will listen for **order.created** events and send a message to Slack like:

`New donation from DonorName: $Amount`
`Message: Donor's message`

## Development

- `entry.py` contains the worker logic
- Uses Cloudflare Workers Python runtime style with async fetch calls
- Logs incoming requests and errors for easier troubleshooting

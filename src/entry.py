import json
from workers import Response, WorkerEntrypoint
from js import console, fetch, Object, Headers

class Default(WorkerEntrypoint):
    async def fetch(self, request, env):
        if request.method != "POST":
            return Response("Method Not Allowed", status=405)

        try:
            payload = await request.json()
            console.log("Received webhook payload:", payload)
        except Exception as e:
            console.error("Failed to parse JSON payload:", str(e))
            return Response("Bad Request", status=400)

        event_type = payload.get("type", "")
        data = payload.get("data", {})

        # Compose Slack message based on event type
        slack_message = None

        if event_type == "donation.created":
            name = data.get("supporter_name", "Someone")
            amount = data.get("amount", 0)
            currency = data.get("currency", "USD")
            message = data.get("message", "")
            support_note = data.get("support_note", "")
            slack_message = (
                f"🎉 Neue Spende von *{name}*!\n"
                f"Betrag: {currency} {amount}\n"
                f"Nachricht: {support_note}"
            )

        elif event_type == "recurring_donation.started":
            name = data.get("supporter_name", "Someone")
            amount = data.get("amount", 0)
            currency = data.get("currency", "USD")
            duration = data.get("duration_type", "unknown period")
            support_note = data.get("support_note", "")
            slack_message = (
                f"🔄 Wiederkehrende Spende gestartet von﻿ *{name}*!\n"
                f"Betrag: {currency} {amount} per {duration}\n"
                f"Nachricht: {support_note}"
            )

        elif event_type == "membership.started":
            name = data.get("supporter_name", "Someone")
            membership_level = data.get("membership_level_name", "Unknown")
            amount = data.get("amount", 0)
            currency = data.get("currency", "USD")
            duration = data.get("duration_type", "unknown period")
            support_note = data.get("support_note", "")
            slack_message = (
                f"👥 Mitgliedschaft gestartet von *{name}*!\n"
                f"Level: {membership_level}\n"
                f"Betrag: {currency} {amount} per {duration}\n"
                f"Nachricht: {support_note}"
            )

        else:
            console.log(f"Ignored event type: {event_type}")
            return Response("Ignored event type", status=200)

        # Post message to Slack
        slack_webhook_url = self.env.SECRET_SLACK_WEBHOOK_URL
        headers = Headers.new()
        headers.set("Content-Type", "application/json")
        body = json.dumps({"text": slack_message})

        options = Object.fromEntries([
            ["method", "POST"],
            ["headers", headers],
            ["body", body]
        ])

        slack_response = await fetch(slack_webhook_url, options)

        if slack_response.status != 200:
            error_text = await slack_response.text()
            console.error(f"Slack webhook error: {error_text}")
            return Response("Slack webhook error", status=500)

        return Response("Notification sent", status=200)
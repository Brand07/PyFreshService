import requests
import base64
import os
import json
import threading

from dotenv import load_dotenv

# Init .env file
load_dotenv()

API_KEY = os.getenv("API_KEY")
TICKET_API_URL = os.getenv("API_URL")
REQUESTERS_API_URL = os.getenv("REQUESTER_URL")


class FreshServiceAPI:
    def __init__(self, ticket_api_url, requesters_api_url, api_key):
        self.ticket_api_url = ticket_api_url
        self.requesters_api_url = requesters_api_url
        self.api_key = API_KEY
        self.encoded_api_key = base64.b64encode(f"{api_key}:x".encode()).decode()
        self.headers = {
            "Authorization": f"Basic {self.encoded_api_key}",
            "Content-Type": "application/json",
        }

    def _build_url(self, endpoint):
        """
        Helper to build the full API url from the base URL
        """

        return f"{self.ticket_api_url}/{endpoint.lstrip('/')}"

    def create_ticket(
        self,
        subject,
        description,
        email=None,
        category=None,
        priority=None,
        status=None,
        type=None,
        requester_id=None,
        responder_id=None,
        group_id=None,
        location=None,
    ):
        url = self._build_url("tickets")
        response = requests.post(
            url,
            headers=self.headers,
            json={
                "subject": subject,
                "description": description,
                "email": email,
                "priority": priority,  # 1: Low, 2: Med, 3: High, 4: Urgent
                "status": status,  # 2:Open, 3:Pending, 4:Resolve, 5:Closed,
                "type": type,  # Service Request or Incident
                "requester_id": requester_id,
                "group_id": group_id,  # Group where the ticket should be assigned.
                "responder_id": responder_id,  # Who the ticket should be assigned
                "custom_fields": {
                    "please_select_the_service": category,
                    "location": f"{os.getenv("LOCATION")}",
                    "site": "Garrison GSN"
                },
            },
        )

        # Check if the ticket response was good
        if response.status_code == 201:
            print(f"{type} ticket created successfully for {email}")
            return response.json()
        elif response.status_code == 400:
            print("Failed to create ticket: Bad Request (400)")
            print("Response:", response.json())
            return None
        else:
            print(f"Failed to create ticket: {response.status_code}")
            return None

    def get_requesters(
        self, output_file="requesters.json", per_page=100, max_pages=200, progress_callback=None
    ):
        """
        Gets all the non-agent requesters from FreshService and formats it
        in a JSON file.
        """
        all_requesters = []
        page = 1
        while page <= max_pages:
            url = self._build_url("requesters") + f"?page={page}&per_page={per_page}"
            print(f"[DEBUG] Fetching: {url}")

            # Update progress if callback is provided
            if progress_callback:
                progress_text = f"Fetching page {page} of requesters..."
                progress_callback(progress_text)

            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                requesters = data.get("requesters", [])
                if not requesters:
                    print(f"[DEBUG] No more requesters found on page {page}.")
                    break
                all_requesters.extend(requesters)
                print(
                    f"[DEBUG] Page {page}: {len(requesters)} requesters fetched. Total so far: {len(all_requesters)}."
                )
                page += 1
            else:
                print(
                    f"Failed to fetch requesters on page {page}: {response.status_code}"
                )
                try:
                    print("Response", response.json())
                except Exception:
                    print("Response content:", response.text)
                    break

        # Update progress for saving file
        if progress_callback:
            progress_callback("Saving requesters to file...")

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump({"requesters": all_requesters}, f, indent=4)
        print(f"Total requesters fetched: {len(all_requesters)}")
        print(f"Data saved to {output_file}")

        # Final progress update
        if progress_callback:
            progress_callback("Complete!")

        return {"requesters": all_requesters}

    def update_requester_file(self, progress_callback=None, completion_callback=None):
        """
        Updates the requesters.json file with the latest data from FreshService.
        Can be called with progress and completion callbacks for UI integration.
        """
        def worker():
            print("Updating requesters.json file...")
            try:
                result = self.get_requesters(progress_callback=progress_callback)
                if completion_callback:
                    completion_callback(True, "Requesters file updated successfully!")
                return result
            except Exception as e:
                error_msg = f"Failed to update requesters file: {str(e)}"
                print(error_msg)
                if completion_callback:
                    completion_callback(False, error_msg)
                return None

        # Run in a separate thread if callbacks are provided (UI context)
        if progress_callback or completion_callback:
            thread = threading.Thread(target=worker)
            thread.daemon = True
            thread.start()
        else:
            return worker()

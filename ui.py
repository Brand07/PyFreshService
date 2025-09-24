import customtkinter
import requests
from CTkMessagebox import CTkMessagebox
from fresh import FreshServiceAPI
from dotenv import load_dotenv
import json
import os

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("dark-blue")

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")
TICKET_API_URL = os.getenv("API_URL")
REQUESTERS_API_URL = os.getenv("REQUESTER_URL")
# Ensure API_KEY and URLs are set
if not API_KEY or not TICKET_API_URL or not REQUESTERS_API_URL:
	raise ValueError(
		"API_KEY, TICKET_API_URL, and REQUESTERS_API_URL must be set in the environment variables."
	)

# Init API class
api = FreshServiceAPI(TICKET_API_URL, REQUESTERS_API_URL, API_KEY)

# Verify that the requesters.json file exists
if not os.path.exists("requesters.json"):
	api.get_requesters()
	print(
		"Requesters file not found. Fetching requesters from API and creating requesters.json."
	)
else:
	print("Requesters file found. Using existing data.")

request_type_values = [
	"",
	"Incident",
	"Service Request",
]

# Map display names to Freshservice API values
service_field_map = {
	"Password Reset": "Active Directory",
	"Account Lockout": "Active Directory",
	"Software Installation": "Software",
	"Laptop Issue": "Laptop",
	"Desktop Issue": "Desktop",
	"Network Connectivity": "Network",
	"Wi-Fi": "Wi-Fi",
	"WorkDay": "WorkDay",
	"Printer Issue": "Printer",
	"Hardware Request": "Hardware Refresh",
	"Other": "Other",
	"WorldShip": "WorldShip",
	"RF Gun": "RF Guns",
	"Apex": "Apex",
	"": "Other",  # fallback for blank
}

ticket_categories = [
	"",
	"Apex",
	"Password Reset",
	"Account Lockout",
	"Software Installation",
	"Laptop Issue",
	"Desktop Issue",
	"Network Connectivity",
	"Printer Issue",
	"Hardware Request",
	"Other",
	"WorldShip",
	"WorkDay",
	"Wi-Fi",
	"RF Gun",
]

ticket_priorities = [
	"Low",
	"Medium",
	"High",
]


class App(customtkinter.CTk):
	HEIGHT = 600
	WIDTH = 900

	def __init__(self):
		super().__init__()
		self.title("Easy Ticket v0.1")
		self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
		self.resizable(False, False)

		self.left_frame = customtkinter.CTkFrame(self, height = 580)
		self.left_frame.place(x = 10, y = 10)

		self.about_label = customtkinter.CTkLabel(
			self,
			bg_color = ["gray86", "gray17"],
			font = customtkinter.CTkFont("Roboto", size = 13, underline = 1),
			width = 140,
			text = "Built in GSN",
		)
		self.about_label.place(x = 40, y = 550)

		self.main_frame = customtkinter.CTkFrame(self, width = 660,
												 height = 580)
		self.main_frame.place(x = 225, y = 10)

		self.top_label = customtkinter.CTkLabel(
			self.main_frame,
			font = customtkinter.CTkFont("Roboto", size = 20, weight = "bold",
										 underline = 1),
			width = 330,
			text = "Report an Incident or Make a Request",
		)
		self.top_label.place(x = 165, y = 20)

		self.ticket_type_selector = customtkinter.CTkOptionMenu(
			self.main_frame, values = request_type_values, width = 160
		)
		self.ticket_type_selector.place(x = 250, y = 50)

		self.first_name_entry = customtkinter.CTkEntry(self.main_frame,
													   width = 180)
		self.first_name_entry.place(x = 240, y = 110)

		self.first_name_label = customtkinter.CTkLabel(
			self.main_frame,
			font = customtkinter.CTkFont("Roboto", size = 16, weight = "bold"),
			width = 180,
			text = "First Name",
		)
		self.first_name_label.place(x = 240, y = 80)

		self.last_name_label = customtkinter.CTkLabel(
			self.main_frame,
			font = customtkinter.CTkFont("Roboto", size = 16, weight = "bold"),
			width = 180,
			text = "Last Name",
		)
		self.last_name_label.place(x = 240, y = 140)

		self.last_name_entry = customtkinter.CTkEntry(self.main_frame,
													  width = 180)
		self.last_name_entry.place(x = 240, y = 170)

		self.category_label = customtkinter.CTkLabel(
			self.main_frame,
			font = customtkinter.CTkFont("Roboto", size = 16, weight = "bold",
										 underline = 1),
			width = 260,
			text = "Select the category for your ticket",
		)
		self.category_label.place(x = 200, y = 230)

		self.category_selector = customtkinter.CTkOptionMenu(
			self.main_frame, values = ticket_categories, width = 160
		)
		self.category_selector.place(x = 250, y = 260)

		self.priority_label = customtkinter.CTkLabel(
			self.main_frame,
			font = customtkinter.CTkFont("Roboto", size = 16, weight = "bold",
										 underline = 1),
			width = 200,
			text = "Priority Level",
		)
		self.priority_label.place(x = 230, y = 290)

		self.priority_selector = customtkinter.CTkOptionMenu(
			self.main_frame, values = ticket_priorities, width = 160
		)
		self.priority_selector.place(x = 250, y = 320)

		self.info_label = customtkinter.CTkLabel(
			self.main_frame,
			font = customtkinter.CTkFont("Roboto", size = 16, weight = "bold",
										 underline = 1),
			width = 160,
			text = "Describe your issue",
		)
		self.info_label.place(x = 250, y = 390)

		self.description_box = customtkinter.CTkTextbox(
			self.main_frame, width = 600, height = 100
		)
		self.description_box.place(x = 30, y = 420)
		self.description_box.insert(1.0, "")

		self.submit_button = customtkinter.CTkButton(
			self.main_frame,
			width = 600,
			font = customtkinter.CTkFont("Roboto", size = 16, weight = "bold",
										 underline = 1),
			text = "Submit Ticket",
			fg_color = "#009f00",
			command = lambda: self.create_ticket(),
		)
		self.submit_button.place(x = 30, y = 535)

	def clear_entries(self):
		"""
		Clears all input fields in the UI.
		"""
		self.first_name_entry.delete(0, "end")
		self.last_name_entry.delete(0, "end")
		self.description_box.delete("1.0", "end")
		self.category_selector.set("")
		self.priority_selector.set("")
		self.ticket_type_selector.set("")
		print("All entries cleared.")

	def show_error(self, message):
		"""
		Displays an error message in a message box.
		"""
		CTkMessagebox(title = "Error", message = message,
					  icon = "cancel").show()
		print(f"Error: {message}")

	def show_success(self, message):
		CTkMessagebox(title = "Success", message = message, icon = "check")
		print(f"Success: {message}")

	def send_to_teams(
			self, message, ticket_url = None, requester = None, subject = None,
			category = None, description = None, priority = None
			):
		"""
		Sends a formatted message to Microsoft Teams using a webhook with an attachment (Adaptive Card).
		"""
		webhook_url = os.getenv("WEBHOOK")
		# Build a nicely formatted message using Markdown
		card_body = [
			{"type": "TextBlock", "text": "**New ticket created:**",
			 "wrap": True},
		]
		if requester:
			card_body.append(
				{"type": "TextBlock", "text": f"**Requester:** {requester}",
				 "wrap": True})
		if subject:
			card_body.append(
				{"type": "TextBlock", "text": f"**Subject:** {subject}",
				 "wrap": True})
		if category:
			card_body.append(
				{"type": "TextBlock", "text": f"**Category:** {category}",
				 "wrap": True})
		if priority:
			card_body.append(
				{"type": "TextBlock", "text": f"**Priority:** {priority}",
				 "wrap": True})
		if description:
			card_body.append(
				{"type": "TextBlock", "text": f"**Description:** {description}",
				 "wrap": True})
		if ticket_url:
			card_body.append(
				{"type": "TextBlock", "text": f"[Ticket URL]({ticket_url})",
				 "wrap": True})
		payload = {
			"attachments": [
				{
					"contentType": "application/vnd.microsoft.card.adaptive",
					"contentUrl": None,
					"content": {
						"$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
						"type": "AdaptiveCard",
						"version": "1.0",
						"body": card_body
					}
				}
			]
		}
		response = requests.post(webhook_url, json = payload)
		if response.status_code == 200:
			print("Message sent to Teams successfully.")
			return True
		else:
			print(f"Failed to send message to Teams: {response.status_code}")
			print(f"Response: {response.text}")
			return False

	def create_ticket(self):
		"""
		Creates a ticket using the Freshservice API with the provided details.
		"""
		requester_name = f"{self.first_name_entry.get()} {self.last_name_entry.get()}"
		subject = "Issue Reported by " + requester_name.title()
		description = self.description_box.get("1.0", "end-1c")
		category = self.category_selector.get()
		email = f"{self.first_name_entry.get().lower()}.{self.last_name_entry.get().lower()}{os.getenv('EMAIL_DOMAIN')}"
		requester_id = self.get_requester_id(email)

		if not category or not description:
			self.show_error("All fields are required.")
			return

		# Build ticket data
		# Map priority string to integer as required by API
		priority_map = {"Low": 1, "Medium": 2, "High": 3, "Urgent": 4}
		priority_value = priority_map.get(self.priority_selector.get(), 1)
		ticket_data = {
			"subject": f"{subject} - {category}",
			"description": description,
			"type": self.ticket_type_selector.get(),
			"email": email,
			"priority": priority_value,
			"status": 2,
			"requester_id": requester_id,
			"responder_id": None,
			"group_id": None,
			# int(os.getenv("GROUP_ID")),  # Load your group ID in the .env file as int
			"custom_fields": {
				"please_select_the_service": service_field_map.get(category,
																   "Other")
			},
		}

		result = api.create_ticket(
			subject = ticket_data["subject"],
			description = ticket_data["description"],
			email = ticket_data["email"],
			priority = ticket_data["priority"],
			status = ticket_data["status"],
			type = ticket_data["type"],
			requester_id = ticket_data["requester_id"],
			responder_id = ticket_data["responder_id"],
			group_id = ticket_data["group_id"],
			category = ticket_data["custom_fields"][
				"please_select_the_service"],
		)
		print("Clearing entries after ticket creation.")
		# Try to get the ticket ID from the API response
		ticket_id = None
		if isinstance(result, dict):
			if "id" in result:
				ticket_id = result["id"]
			elif "ticket" in result and "id" in result["ticket"]:
				ticket_id = result["ticket"]["id"]
		if ticket_id:
			ticket_url = f"https://{os.getenv('DOMAIN')}.freshservice.com/helpdesk/tickets/{ticket_id}"  # Replace 'domain' with your Freshservice domain
			print(f"Ticket created successfully: {ticket_url}")
			self.send_to_teams(
				message = None,
				ticket_url = ticket_url,
				requester = requester_name.title(),
				subject = f"Issue Reported by {requester_name.title()} - {category}",
				category = category,
				description = description,
				priority = self.priority_selector.get()
			)
			self.show_success("Ticket created successfully!")
		else:
			self.show_error(
				"Ticket creation failed or ticket ID not found. No URL available."
			)
		self.clear_entries()

	# Get the requester ID based on the email from requesters.json
	def get_requester_id(self, email):
		"""
		Fetches the requester ID based on the provided email.
		"""
		with open("requesters.json", "r") as file:
			data = json.load(file)
			for requester in data["requesters"]:
				if requester.get("email") == email:
					return requester.get("id")
		return None

	def clear_entries(self):  # noqa: F811
		"""
		Clears all input fields in the UI.
		"""
		self.first_name_entry.delete(0, "end")
		self.last_name_entry.delete(0, "end")
		self.description_box.delete("1.0", "end")
		self.category_selector.set("")
		self.priority_selector.set("")
		self.ticket_type_selector.set("")
		print("All entries cleared.")

	def show_error(self, message):  # noqa: F811
		CTkMessagebox(title = "Error", message = message, icon = "cancel")

	def show_success(self, message):
		CTkMessagebox(title = "Success", message = message, icon = "check")
		print(f"Success: {message}")


if __name__ == "__main__":
	app = App()
	app.mainloop()

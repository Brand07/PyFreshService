# PyFreshService

A Python application for interacting with the FreshService API, featuring both a programmatic interface and a GUI for creating tickets and managing requesters.

<img width="897" height="626" alt="image" src="https://github.com/user-attachments/assets/00730a5d-dc00-4bf4-b575-7c326a738eca" />


## Features

- **FreshService API Integration**: Complete Python wrapper for FreshService ticket management
- **GUI Application**: User-friendly interface built with CustomTkinter for creating tickets
- **Requester Management**: Fetch and manage FreshService requesters
- **Ticket Creation**: Create incidents and service requests with customizable fields
- **Environment Configuration**: Secure API key management using environment variables

## Installation

### Prerequisites

- Python 3.13 or higher
- FreshService API access with valid API key

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Brand07/PyFreshService.git
cd PyFreshService
```

2. Install dependencies using uv (recommended) or pip:
```bash
# Using uv
uv sync

# Or using pip
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your FreshService credentials:
```env
API_KEY=your_freshservice_api_key
API_URL=https://your-domain.freshservice.com/api/v2
REQUESTER_URL=https://your-domain.freshservice.com/api/v2/requesters
REQUESTER_ID=your_default_requester_id
RESPONDER_ID=your_default_responder_id
GROUP_ID=your_default_group_id
```

## Usage

### GUI Application

Launch the graphical interface for easy ticket creation:

```bash
python ui.py
```

The GUI provides:
- Dropdown menus for ticket types, priorities, and services
- Email/requester selection
- Rich text description input
- One-click ticket creation

### Programmatic Usage

#### Basic API Usage

```python
from fresh import FreshServiceAPI
import os

# Initialize the API client
api = FreshServiceAPI(
    ticket_api_url=os.getenv("API_URL"),
    requesters_api_url=os.getenv("REQUESTER_URL"),
    api_key=os.getenv("API_KEY")
)

# Create a ticket
ticket = api.create_ticket(
    subject="Network connectivity issue",
    description="User cannot access shared drives",
    email="user@company.com",
    priority=3,  # High priority
    type="Incident",
    category="Network"
)
```

#### Fetch Requesters

```python
# Get all requesters and save to JSON
requesters = api.get_requesters(output_file="requesters.json")
```


## Project Structure

```
PyFreshService/
├── fresh.py              # Core FreshService API wrapper
├── ui.py                 # GUI application using CustomTkinter
├── requesters.json       # Cached requester data
├── pyproject.toml        # Project dependencies and metadata
├── .env                  # Environment variables (create this)
├── UI_Files/             # GUI configuration files
│   ├── window.json
│   ├── v2.json
│   └── updated_window.json
└── README.md            # This file
```

## Dependencies

- **requests**: HTTP library for API calls
- **customtkinter**: Modern GUI framework
- **ctkmessagebox**: Message boxes for the GUI
- **python-dotenv**: Environment variable management
- **pillow**: Image processing support
- **tomli**: TOML file parsing

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `API_KEY` | Your FreshService API key | Yes |
| `API_URL` | FreshService API base URL | Yes |
| `REQUESTER_URL` | FreshService requesters endpoint | Yes |
| `REQUESTER_ID` | Default requester ID for bulk operations | No |
| `RESPONDER_ID` | Default responder ID | No |
| `GROUP_ID` | Default group ID for ticket assignment | No |

### Ticket Priorities

- `1`: Low
- `2`: Medium  
- `3`: High
- `4`: Urgent

### Ticket Statuses

- `2`: Open
- `3`: Pending
- `4`: Resolved
- `5`: Closed

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Support

For support or questions, please open an issue on the GitHub repository.

## Changelog

### v0.1.0
- Initial release
- Core FreshService API integration
- GUI application for ticket creation
- Requester management features
